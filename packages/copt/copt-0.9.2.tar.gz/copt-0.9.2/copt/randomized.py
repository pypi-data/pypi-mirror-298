"""Module that contains randomized (also known as stochastic) algorithms."""
from collections import defaultdict
import numpy as np
from scipy import sparse, optimize

from copt import utils
from copt.frank_wolfe import update_active_set


@utils.njit(nogil=True)
def _support_matrix(A_indices, A_indptr, reverse_blocks_indices, n_blocks):
    """Compute the support matrix, used by variance-reduced algorithms.

  Args:
    A_indices, A_indptr: arrays-like
        Arrays representing the data matrix in CSR format.

    reverse_blocks_indices: array-like

    n_blocks: integer
        Number of unique blocks in array blocks.


  Notes
  -----
  BS stands for Block Support

  Returns:
    Parameters of a CSR matrix representing the extended support. The returned
    vectors represent a sparse matrix of shape (n_samples, n_blocks),
    element (i, j) is one if j is in the extended support of f_i, zero
    otherwise.
  """
    BS_indices = np.zeros(A_indices.size, dtype=np.int64)
    BS_indptr = np.zeros(A_indptr.size, dtype=np.int64)
    seen_blocks = np.zeros(n_blocks, dtype=np.int64)
    BS_indptr[0] = 0
    counter_indptr = 0
    for i in range(A_indptr.size - 1):
        low = A_indptr[i]
        high = A_indptr[i + 1]
        for j in range(low, high):
            g_idx = reverse_blocks_indices[A_indices[j]]
            if seen_blocks[g_idx] == 0:
                # if first time we encouter this block,
                # add to the index and mark as seen
                BS_indices[counter_indptr] = g_idx
                seen_blocks[g_idx] = 1
                counter_indptr += 1
        BS_indptr[i + 1] = counter_indptr
        # cleanup
        for j in range(BS_indptr[i], counter_indptr):
            seen_blocks[BS_indices[j]] = 0
    BS_data = np.ones(counter_indptr)
    return BS_data, BS_indices[:counter_indptr], BS_indptr


def minimize_saga(
    f_deriv,
    A,
    b,
    x0,
    step_size,
    prox=None,
    alpha=0,
    max_iter=500,
    tol=1e-6,
    verbose=1,
    callback=None,
):
    r"""Stochastic average gradient augmented (SAGA) algorithm.

    This algorithm can solve linearly-parametrized loss functions of the form

        minimize_x \sum_{i}^n_samples f(A_i^T x, b_i) + alpha ||x||_2^2 + g(x)

    where g is a function for which we have access to its proximal operator.

    .. warning::
        This function is experimental, API is likely to change.


    Args:
      f
          loss functions.

      x0: np.ndarray or None, optional
          Starting point for optimization.

      step_size: float or None, optional
          Step size for the optimization. If None is given, this will be
          estimated from the function f.

      max_iter: int
          Maximum number of passes through the data in the optimization.

      tol: float
          Tolerance criterion. The algorithm will stop whenever the norm of the
          gradient mapping (generalization of the gradient for nonsmooth
          optimization) is below tol.

      verbose: bool
          Verbosity level. True might print some messages.

      trace: bool
          Whether to trace convergence of the function, useful for plotting
          and/or debugging. If ye, the result will have extra members trace_func,
          trace_time.


    Returns:
      opt: OptimizeResult
          The optimization result represented as a
          ``scipy.optimize.OptimizeResult`` object. Important attributes are:
          ``x`` the solution array, ``success`` a Boolean flag indicating if
          the optimizer exited successfully and ``message`` which describes
          the cause of the termination. See `scipy.optimize.OptimizeResult`
          for a description of other attributes.


    References:
      This variant of the SAGA algorithm is described in:

      `"Breaking the Nonsmooth Barrier: A Scalable Parallel Method for Composite
      Optimization."
      <https://arxiv.org/pdf/1707.06468.pdf>`_, Fabian Pedregosa, Remi Leblond,
      and Simon Lacoste-Julien. Advances in Neural Information Processing Systems
      (NIPS) 2017.
    """
    # convert any input to CSR sparse matrix representation. In the future we
    # might want to implement also a version for dense data (numpy arrays) to
    # better exploit data locality
    x = np.ascontiguousarray(x0).copy()
    n_samples, n_features = A.shape
    A = sparse.csr_matrix(A)

    if step_size is None:
        # then need to use line search
        raise ValueError

    if hasattr(prox, "__len__") and len(prox) == 2:
        blocks = prox[1]
        prox = prox[0]
    else:
        blocks = sparse.eye(n_features, n_features, format="csr")

    if prox is None:

        @utils.njit
        def prox(x, i, indices, indptr, d, step_size):
            pass

    A_data = A.data
    A_indices = A.indices
    A_indptr = A.indptr
    n_samples, n_features = A.shape

    rblocks_indices = blocks.T.tocsr().indices
    blocks_indptr = blocks.indptr
    bs_data, bs_indices, bs_indptr = _support_matrix(
        A_indices, A_indptr, rblocks_indices, blocks.shape[0]
    )
    csr_blocks_1 = sparse.csr_matrix((bs_data, bs_indices, bs_indptr))

    # .. diagonal reweighting ..
    d = np.array(csr_blocks_1.sum(0), dtype=float).ravel()
    idx = d != 0
    d[idx] = n_samples / d[idx]
    d[~idx] = 1

    @utils.njit(nogil=True)
    def _saga_epoch(x, idx, memory_gradient, gradient_average, grad_tmp, step_size):
        # .. inner iteration of the SAGA algorithm..
        for i in idx:

            # .. gradient estimate ..
            p = 0.0
            for j in range(A_indptr[i], A_indptr[i + 1]):
                j_idx = A_indices[j]
                p += x[j_idx] * A_data[j]
            grad_i = f_deriv(np.array([p]), np.array([b[i]]))[0]
            for j in range(A_indptr[i], A_indptr[i + 1]):
                j_idx = A_indices[j]
                grad_tmp[j_idx] = (grad_i - memory_gradient[i]) * A_data[j]

            # .. update coefficients ..
            # .. first iterate on blocks ..
            for h_j in range(bs_indptr[i], bs_indptr[i + 1]):
                h = bs_indices[h_j]
                # .. then iterate on features inside block ..
                for b_j in range(blocks_indptr[h], blocks_indptr[h + 1]):
                    bias_term = d[h] * (gradient_average[b_j] + alpha * x[b_j])
                    x[b_j] -= step_size * (grad_tmp[b_j] + bias_term)
            prox(x, i, bs_indices, bs_indptr, d, step_size)

            # .. update memory terms ..
            for j in range(A_indptr[i], A_indptr[i + 1]):
                j_idx = A_indices[j]
                tmp = (grad_i - memory_gradient[i]) * A_data[j]
                tmp /= n_samples
                gradient_average[j_idx] += tmp
                grad_tmp[j_idx] = 0
            memory_gradient[i] = grad_i

    # .. initialize memory terms ..
    memory_gradient = np.zeros(n_samples)
    gradient_average = np.zeros(n_features)
    grad_tmp = np.zeros(n_features)
    idx = np.arange(n_samples)
    success = False
    if callback is not None:
        callback(locals())
    for it in range(max_iter):
        x_old = x.copy()
        np.random.shuffle(idx)
        _saga_epoch(x, idx, memory_gradient, gradient_average, grad_tmp, step_size)
        if callback is not None:
            callback(locals())

        diff_norm = np.abs(x - x_old).sum()
        if diff_norm < tol:
            success = True
            break
    return optimize.OptimizeResult(x=x, success=success, nit=it)


def minimize_svrg(
    f_deriv,
    A,
    b,
    x0,
    step_size,
    alpha=0,
    prox=None,
    max_iter=500,
    tol=1e-6,
    verbose=False,
    callback=None,
):
    r"""Stochastic average gradient augmented (SAGA) algorithm.

    The SAGA algorithm can solve optimization problems of the form

        argmin_{x \in R^p} \sum_{i}^n_samples f(A_i^T x, b_i) + alpha *
        ||x||_2^2 +
                                            + beta * ||x||_1

    Args:
      f_deriv
          derivative of f

      x0: np.ndarray or None, optional
          Starting point for optimization.

      step_size: float or None, optional
          Step size for the optimization. If None is given, this will be
          estimated from the function f.

      n_jobs: int
          Number of threads to use in the optimization. A number higher than 1
          will use the Asynchronous SAGA optimization method described in
          [Pedregosa et al., 2017]

      max_iter: int
          Maximum number of passes through the data in the optimization.

      tol: float
          Tolerance criterion. The algorithm will stop whenever the norm of the
          gradient mapping (generalization of the gradient for nonsmooth
          optimization)
          is below tol.

      verbose: bool
          Verbosity level. True might print some messages.

      trace: bool
          Whether to trace convergence of the function, useful for plotting
          and/or debugging. If ye, the result will have extra members
          trace_func, trace_time.


    Returns:
      opt: OptimizeResult
          The optimization result represented as a
          ``scipy.optimize.OptimizeResult`` object. Important attributes are:
          ``x`` the solution array, ``success`` a Boolean flag indicating if
          the optimizer exited successfully and ``message`` which describes
          the cause of the termination. See `scipy.optimize.OptimizeResult`
          for a description of other attributes.


    References:
      The SAGA algorithm was originally described in

      Aaron Defazio, Francis Bach, and Simon Lacoste-Julien. `SAGA: A fast
      incremental gradient method with support for non-strongly convex composite
      objectives. <https://arxiv.org/abs/1407.0202>`_ Advances in Neural
      Information Processing Systems. 2014.

      The implemented has some improvements with respect to the original,
      like support for sparse datasets and is described in

      Fabian Pedregosa, Remi Leblond, and Simon Lacoste-Julien.
      "Breaking the Nonsmooth Barrier: A Scalable Parallel Method
      for Composite Optimization." Advances in Neural Information
      Processing Systems (NIPS) 2017.
    """
    x = np.ascontiguousarray(x0).copy()
    n_samples, n_features = A.shape
    A = sparse.csr_matrix(A)

    if step_size is None:
        # then need to use line search
        raise ValueError

    if hasattr(prox, "__len__") and len(prox) == 2:
        blocks = prox[1]
        prox = prox[0]
    else:
        blocks = sparse.eye(n_features, n_features, format="csr")

    if prox is None:

        @utils.njit
        def prox(x, i, indices, indptr, d, step_size):
            pass

    A_data = A.data
    A_indices = A.indices
    A_indptr = A.indptr
    n_samples, n_features = A.shape

    rblocks_indices = blocks.T.tocsr().indices
    blocks_indptr = blocks.indptr
    bs_data, bs_indices, bs_indptr = _support_matrix(
        A_indices, A_indptr, rblocks_indices, blocks.shape[0]
    )
    csr_blocks_1 = sparse.csr_matrix((bs_data, bs_indices, bs_indptr))

    # .. diagonal reweighting ..
    d = np.array(csr_blocks_1.sum(0), dtype=float).ravel()
    idx = d != 0
    d[idx] = n_samples / d[idx]
    d[~idx] = 1

    @utils.njit
    def full_grad(x):
        grad = np.zeros(x.size)
        for i in range(n_samples):
            p = 0.0
            for j in range(A_indptr[i], A_indptr[i + 1]):
                j_idx = A_indices[j]
                p += x[j_idx] * A_data[j]
            grad_i = f_deriv(np.array([p]), np.array([b[i]]))[0]
            # .. gradient estimate (XXX difference) ..
            for j in range(A_indptr[i], A_indptr[i + 1]):
                j_idx = A_indices[j]
                grad[j_idx] += grad_i * A_data[j] / n_samples
        return grad

    @utils.njit(nogil=True)
    def _svrg_epoch(x, x_snapshot, idx, gradient_average, grad_tmp, step_size):

        # .. inner iteration ..
        for i in idx:
            p = 0.0
            p_old = 0.0
            for j in range(A_indptr[i], A_indptr[i + 1]):
                j_idx = A_indices[j]
                p += x[j_idx] * A_data[j]
                p_old += x_snapshot[j_idx] * A_data[j]

            grad_i = f_deriv(np.array([p]), np.array([b[i]]))[0]
            old_grad_i = f_deriv(np.array([p_old]), np.array([b[i]]))[0]
            for j in range(A_indptr[i], A_indptr[i + 1]):
                j_idx = A_indices[j]
                grad_tmp[j_idx] = (grad_i - old_grad_i) * A_data[j]

            # .. update coefficients ..
            # .. first iterate on blocks ..
            for h_j in range(bs_indptr[i], bs_indptr[i + 1]):
                h = bs_indices[h_j]
                # .. then iterate on features inside block ..
                for b_j in range(blocks_indptr[h], blocks_indptr[h + 1]):
                    bias_term = d[h] * (gradient_average[b_j] + alpha * x[b_j])
                    x[b_j] -= step_size * (grad_tmp[b_j] + bias_term)
            prox(x, i, bs_indices, bs_indptr, d, step_size)

    idx = np.arange(n_samples)
    grad_tmp = np.zeros(n_features)
    success = False
    if callback is not None:
        callback(locals())
    for it in range(max_iter):
        x_snapshot = x.copy()
        gradient_average = full_grad(x_snapshot)
        np.random.shuffle(idx)
        _svrg_epoch(x, x_snapshot, idx, gradient_average, grad_tmp, step_size)
        if callback is not None:
            callback(locals())

        if np.abs(x - x_snapshot).sum() < tol:
            success = True
            break
    message = ""
    return optimize.OptimizeResult(x=x, success=success, nit=it, message=message)


def minimize_vrtos(
    f_deriv,
    A,
    b,
    x0,
    step_size,
    prox_1=None,
    prox_2=None,
    alpha=0,
    max_iter=500,
    tol=1e-6,
    callback=None,
    verbose=0,
):
    r"""Variance-reduced three operator splitting (VRTOS) algorithm.

    The VRTOS algorithm can solve optimization problems of the form

        argmin_{x \in R^p} \sum_{i}^n_samples f(A_i^T x, b_i) + alpha *
        ||x||_2^2 +
                                            + pen1(x) + pen2(x)

    Parameters
    ----------
    f_deriv
        derivative of f

    x0: np.ndarray or None, optional
        Starting point for optimization.

    step_size: float or None, optional
        Step size for the optimization. If None is given, this will be
        estimated from the function f.

    n_jobs: int
        Number of threads to use in the optimization. A number higher than 1
        will use the Asynchronous SAGA optimization method described in
        [Pedregosa et al., 2017]

    max_iter: int
        Maximum number of passes through the data in the optimization.

    tol: float
        Tolerance criterion. The algorithm will stop whenever the norm of the
        gradient mapping (generalization of the gradient for nonsmooth
        optimization)
        is below tol.

    verbose: bool
        Verbosity level. True might print some messages.

    trace: bool
        Whether to trace convergence of the function, useful for plotting and/or
        debugging. If ye, the result will have extra members trace_func,
        trace_time.

    Returns
    -------
    opt: OptimizeResult
        The optimization result represented as a
        ``scipy.optimize.OptimizeResult`` object. Important attributes are:
        ``x`` the solution array, ``success`` a Boolean flag indicating if
        the optimizer exited successfully and ``message`` which describes
        the cause of the termination. See `scipy.optimize.OptimizeResult`
        for a description of other attributes.

    References
    ----------
    Pedregosa, Fabian, Kilian Fatras, and Mattia Casotto. "Variance Reduced
    Three Operator Splitting." arXiv preprint arXiv:1806.07294 (2018).
    """

    n_samples, n_features = A.shape
    success = False

    # FIXME: just a workaround for now
    # FIXME: check if prox_1 is a tuple
    if hasattr(prox_1, "__len__") and len(prox_1) == 2:
        blocks_1 = prox_1[1]
        prox_1 = prox_1[0]
    else:
        blocks_1 = sparse.eye(n_features, n_features, format="csr")
    if hasattr(prox_2, "__len__") and len(prox_2) == 2:
        blocks_2 = prox_2[1]
        prox_2 = prox_2[0]
    else:
        blocks_2 = sparse.eye(n_features, n_features, format="csr")

    Y = np.zeros((2, x0.size))
    z = x0.copy()

    assert A.shape[0] == b.size

    if step_size < 0:
        raise ValueError

    if prox_1 is None:

        @utils.njit
        def prox_1(x, i, indices, indptr, d, step_size):
            pass

    if prox_2 is None:

        @utils.njit
        def prox_2(x, i, indices, indptr, d, step_size):
            pass

    A = sparse.csr_matrix(A)
    epoch_iteration = _factory_sparse_vrtos(
        f_deriv, prox_1, prox_2, blocks_1, blocks_2, A, b, alpha, step_size
    )

    # .. memory terms ..
    memory_gradient = np.zeros(n_samples)
    gradient_average = np.zeros(n_features)
    x1 = x0.copy()
    grad_tmp = np.zeros(n_features)

    # warm up for the JIT
    epoch_iteration(
        Y,
        x0,
        x1,
        z,
        memory_gradient,
        gradient_average,
        np.array([0]),
        grad_tmp,
        step_size,
    )

    # .. iterate on epochs ..
    if callback is not None:
        callback(locals())
    for it in range(max_iter):
        epoch_iteration(
            Y,
            x0,
            x1,
            z,
            memory_gradient,
            gradient_average,
            np.random.permutation(n_samples),
            grad_tmp,
            step_size,
        )

        certificate = np.linalg.norm(x0 - z) + np.linalg.norm(x1 - z)
        if callback is not None:
            callback(locals())

    return optimize.OptimizeResult(
        x=z, success=success, nit=it, certificate=certificate
    )


def _factory_sparse_vrtos(
    f_deriv, prox_1, prox_2, blocks_1, blocks_2, A, b, alpha, gamma
):

    A_data = A.data
    A_indices = A.indices
    A_indptr = A.indptr
    n_samples, n_features = A.shape

    blocks_1_indptr = blocks_1.indptr
    blocks_2_indptr = blocks_2.indptr

    rblocks_1_indices = blocks_1.T.tocsr().indices
    bs_1_data, bs_1_indices, bs_1_indptr = _support_matrix(
        A_indices, A_indptr, rblocks_1_indices, blocks_1.shape[0]
    )
    csr_blocks_1 = sparse.csr_matrix((bs_1_data, bs_1_indices, bs_1_indptr))

    rblocks_2_indices = blocks_2.T.tocsr().indices
    bs_2_data, bs_2_indices, bs_2_indptr = _support_matrix(
        A_indices, A_indptr, rblocks_2_indices, blocks_2.shape[0]
    )
    csr_blocks_2 = sparse.csr_matrix((bs_2_data, bs_2_indices, bs_2_indptr))

    # .. diagonal reweighting ..
    d1 = np.array(csr_blocks_1.sum(0), dtype=float).ravel()
    idx = d1 != 0
    d1[idx] = n_samples / d1[idx]
    d1[~idx] = 1

    d2 = np.array(csr_blocks_2.sum(0), dtype=float).ravel()
    idx = d2 != 0
    d2[idx] = n_samples / d2[idx]
    d2[~idx] = 1

    @utils.njit(nogil=True)
    def epoch_iteration_template(
        Y,
        x1,
        x2,
        z,
        memory_gradient,
        gradient_average,
        sample_indices,
        grad_tmp,
        step_size,
    ):

        # .. iterate on samples ..
        for i in sample_indices:
            p = 0.0
            for j in range(A_indptr[i], A_indptr[i + 1]):
                j_idx = A_indices[j]
                p += z[j_idx] * A_data[j]

            # .. gradient estimate ..
            grad_i = f_deriv(np.array([p]), np.array([b[i]]))[0]
            for j in range(A_indptr[i], A_indptr[i + 1]):
                j_idx = A_indices[j]
                grad_tmp[j_idx] = (grad_i - memory_gradient[i]) * A_data[j]

            # .. x update ..
            for h_j in range(bs_1_indptr[i], bs_1_indptr[i + 1]):
                h = bs_1_indices[h_j]

                # .. iterate on features inside block ..
                for b_j in range(blocks_1_indptr[h], blocks_1_indptr[h + 1]):
                    bias_term = d1[h] * (gradient_average[b_j] + alpha * z[b_j])
                    x1[b_j] = (
                        2 * z[b_j]
                        - Y[0, b_j]
                        - step_size * 0.5 * (grad_tmp[b_j] + bias_term)
                    )

            prox_1(x1, i, bs_1_indices, bs_1_indptr, d1, step_size)

            # .. update y ..
            for h_j in range(bs_1_indptr[i], bs_1_indptr[i + 1]):
                h = bs_1_indices[h_j]
                for b_j in range(blocks_1_indptr[h], blocks_1_indptr[h + 1]):
                    Y[0, b_j] += x1[b_j] - z[b_j]

            for h_j in range(bs_2_indptr[i], bs_2_indptr[i + 1]):
                h = bs_2_indices[h_j]

                # .. iterate on features inside block ..
                for b_j in range(blocks_2_indptr[h], blocks_2_indptr[h + 1]):
                    bias_term = d2[h] * (gradient_average[b_j] + alpha * z[b_j])
                    x2[b_j] = (
                        2 * z[b_j]
                        - Y[1, b_j]
                        - step_size * 0.5 * (grad_tmp[b_j] + bias_term)
                    )

            prox_2(x2, i, bs_2_indices, bs_2_indptr, d2, step_size)

            # .. update y ..
            for h_j in range(bs_2_indptr[i], bs_2_indptr[i + 1]):
                h = bs_2_indices[h_j]
                for b_j in range(blocks_2_indptr[h], blocks_2_indptr[h + 1]):
                    Y[1, b_j] += x2[b_j] - z[b_j]

            # .. update z ..
            for h_j in range(bs_1_indptr[i], bs_1_indptr[i + 1]):
                h = bs_1_indices[h_j]

                # .. iterate on features inside block ..
                for b_j in range(blocks_1_indptr[h], blocks_1_indptr[h + 1]):
                    da = 1.0 / d1[rblocks_1_indices[b_j]]
                    db = 1.0 / d2[rblocks_2_indices[b_j]]
                    z[b_j] = (da * Y[0, b_j] + db * Y[1, b_j]) / (da + db)

            for h_j in range(bs_2_indptr[i], bs_2_indptr[i + 1]):
                h = bs_2_indices[h_j]

                # .. iterate on features inside block ..
                for b_j in range(blocks_2_indptr[h], blocks_2_indptr[h + 1]):
                    da = 1.0 / d1[rblocks_1_indices[b_j]]
                    db = 1.0 / d2[rblocks_2_indices[b_j]]
                    z[b_j] = (da * Y[0, b_j] + db * Y[1, b_j]) / (da + db)

            # .. update memory terms ..
            for j in range(A_indptr[i], A_indptr[i + 1]):
                j_idx = A_indices[j]
                tmp = (grad_i - memory_gradient[i]) * A_data[j] / n_samples
                gradient_average[j_idx] += tmp
                grad_tmp[j_idx] = 0
            memory_gradient[i] = grad_i

    return epoch_iteration_template


def step_size_sfw(variant):
    if variant in {'SAG', 'SAGA'}:
        def step_sizes_SAG_A(kwargs):
            step_size_x = 2. / (kwargs['step']+2)
            return step_size_x, None
        return step_sizes_SAG_A

    if variant == 'MHK':
        def step_sizes_MHK(kwargs):
            step_size_x = 2. / (kwargs['step'] + 8)
            step_size_agg = step_size_x ** (2/3)
            return step_size_x, step_size_agg
        return step_sizes_MHK

    if variant == 'LF':
        def step_sizes_LF(kwargs):
            m = kwargs['n_samples'] / kwargs['batch_size']
            t = kwargs['step']
            step_x = 2 * (2 * m + t) / ((t+1) * (4 * m + t))
            step_agg = 2 * m / (2 * m + t + 1)
            return step_x, step_agg
        return step_sizes_LF


def step_size_DR(kwargs):
    norm_update_direction = (kwargs['update_direction'] ** 2).sum()
    lipschitz = kwargs['lipschitz']
    return min(kwargs['certificate'] / (norm_update_direction * lipschitz),
               kwargs['max_step_size']), None



SFW_VARIANTS = {'SAG', 'SAGA', 'MHK', 'LF'}
LMO_VARIANTS = {'vanilla', 'pairwise'}


def minimize_sfw(
        f_deriv,
        A,
        b,
        x0,
        lmo,
        x0_rep=None,
        batch_size=1,
        step_size="sublinear",
        lipschitz=None,
        max_iter=500,
        tol=1e-6,
        verbose=False,
        callback=None,
        variant='SAGA',
        lmo_variant='vanilla'
):
    r"""Stochastic Frank-Wolfe (SFW) algorithm.

    This implementation of SFW algorithms can solve optimization problems of the form

        argmin_{x \in constraint} (1/n)\sum_{i}^n_samples f(A_i^T x, b_i)

    Args:
      f_deriv
          derivative of f

      x0: np.ndarray
          Starting point for optimization.

      step_size: Step size for the optimization. should be one of
          - callable: should return a tuple of floats.
          - 'sublinear': sets the step size as the default for `variant`.
          - 'DR': uses the Demyanov-Rubinov step size scheme, using the Lipschitz estimate given in
        the lipschitz parameter.

      lipschitz: None or float, optional
        Estimate for the Lipschitz constant of the gradient. Required when step_size="DR".

      lmo: function
          returns the update direction

      batch_size: int
          Size of the random subset (without replacement) to compute the stochastic gradient estimator.

      max_iter: int
          Maximum number of passes on the dataset (epochs).

      tol: float
          Tolerance criterion. The algorithm will stop whenever the
          difference between two successive iterates is below tol.

      verbose: bool
          Verbosity level. True might print some messages.

      callback: function or None
          If not None, callback will be called at each iteration.

      variant: str in {'SAG', 'MHK', 'LF'}
          Controls which variant of SFW to use.
          'SAG' is described in [NDTELP2020],
          'SAGA' is yet to be described.
          'MHK' is described in [MHK2020],
          'LF' is described in [LF2020].

      lmo_variant: str in {'vanilla', 'pairwise'}
        Controls which variant of the LMO we're using.
        Using 'pairwise' will create and update an active set of vertices.

    Returns:
      opt: OptimizeResult
          The optimization result represented as a
          ``scipy.optimize.OptimizeResult`` object. Important attributes are:
          ``x`` the solution array, ``success`` a Boolean flag indicating if
          the optimizer exited successfully and ``message`` which describes
          the cause of the termination. See `scipy.optimize.OptimizeResult`
          for a description of other attributes.

    References:

    .. [NDTELP2020] Negiar, Geoffrey, Dresdner, Gideon, Tsai Alicia, El Ghaoui, Laurent, Locatello, Francesco, and Pedregosa, Fabian.
    `"Stochastic Frank-Wolfe for Constrained Finite-Sum Minimization" <https://arxiv.org/abs/2002.11860v2>` arxiv:2002.11860v2 (2020).

    .. [MHK2018] Mokhtari, Aryan, Hassani, Hamed, and Karbassi, Amin `"Stochastic Conditional Gradient Methods:
From Convex Minimization to Submodular Maximization" <https://arxiv.org/abs/1804.09554>`_, arxiv:1804.09554 (2018)

    .. [LF2020] Lu, Haihao, and Freund, Robert `"Generalized Stochastic Frank-Wolfe Algorithm with Stochastic 'Substitute' Gradient for Structured Convex Optimization"
    <https://arxiv.org/pdf/1806.05123.pdf>`_, Mathematical Programming (2020).
    """

    if variant not in SFW_VARIANTS:
        raise ValueError(f"This variant is not implemented. "
                         f"Please use one from {SFW_VARIANTS}.")
    if lmo_variant not in LMO_VARIANTS:
        raise ValueError(f"This LMO variant is not implemented. "
                         f"Please use one from {LMO_VARIANTS}.")

    n_samples, n_features = A.shape
    x = np.reshape(x0, n_features).astype(float)
    x = np.ascontiguousarray(x)

    assert x.shape == (n_features,)

    A = sparse.csr_matrix(A)
    A_data = A.data
    A_indptr = A.indptr
    A_indices = A.indices

    dual_var = np.zeros(n_samples)  # alpha_t in [NDTELP2020]
    grad_agg = np.zeros(n_features)  # r_t in [NDTELP2020]

    if variant == 'LF':
        agg = utils.safe_sparse_dot(A, x)  # sigma_t in [LF2020]

    success = False

    if callback is not None:
        callback(locals())

    if step_size == 'sublinear':
        # then use sublinear step size according to variant
        step_size_fun = step_size_sfw(variant)
    elif step_size == 'DR':
        if lipschitz is None:
            raise ValueError('lipschitz needs to be specified with step_size="DR"')
        step_size_fun = step_size_DR


    if lmo_variant == 'vanilla':
        active_set = None

    elif lmo_variant == 'pairwise':
        active_set = defaultdict(float)
        active_set[x0_rep] = 1.

    step = 0

    # Perform an epoch
    for it in range(max_iter):

        if batch_size == 1:
            idx = np.random.randint(n_samples, size=n_samples)
        else:
            # Sample without replacement batch wise
            idx = utils.sample_batches(n_samples, n_samples // batch_size, batch_size)

        i = 0
        while i < len(idx):
            batch_idx = idx[i: min(i + batch_size, n_samples)]

            x_prev = x.copy()
            if step_size != 'DR':
                step_size_x, step_size_agg = step_size_fun(locals())
            dual_var_prev = dual_var[batch_idx].copy()

            if variant in {'SAG', 'SAGA'}:
                p = utils.fast_csr_mv(A_data, A_indptr, A_indices, x, batch_idx)
                dual_var[batch_idx] = (1 / n_samples) * f_deriv(p, b[batch_idx])

            elif variant == 'MHK':
                p = utils.fast_csr_mv(A_data, A_indptr, A_indices, x, batch_idx)
                dual_var[batch_idx] += step_size_agg * (f_deriv(p, b[batch_idx]) - dual_var[batch_idx])

            elif variant == 'LF':
                update_direction, fw_vertex_rep, away_vertex_rep, max_step_size = lmo(-grad_agg, x, active_set)
                extr_point = update_direction + x
                agg[batch_idx] += step_size_agg * (utils.fast_csr_mv(A_data, A_indptr, A_indices, extr_point,
                                                                     batch_idx)
                                                   - agg[batch_idx])
                dual_var[batch_idx] = (1 / n_samples) * f_deriv(agg[batch_idx], b[batch_idx])

            # For all variants, update the aggregate gradient
            grad_agg_update = utils.fast_csr_vm(dual_var[batch_idx] - dual_var_prev,
                                                A_data, A_indptr, A_indices, n_features, batch_idx)
            grad_agg += grad_agg_update

            if variant in {'SAG', 'MHK'}:
                update_direction, fw_vertex_rep, away_vertex_rep, max_step_size = lmo(-grad_agg, x, active_set)

            elif variant == 'SAGA':
                grad_est = utils.safe_sparse_add(grad_agg, (n_samples - 1) * utils.fast_csr_vm(dual_var[batch_idx] - dual_var_prev,
                                                                                               A_data, A_indptr, A_indices,
                                                                                               n_features, batch_idx))
                update_direction, fw_vertex_rep, away_vertex_rep, max_step_size = lmo(-grad_est, x, active_set)

            if step_size == 'DR':
                certificate = utils.safe_sparse_dot(-grad_agg, update_direction)
                step_size_x, _ = step_size_fun(locals())

            x += step_size_x * update_direction

            if lmo_variant == 'pairwise':
                update_active_set(active_set, fw_vertex_rep, away_vertex_rep,
                                  step_size_x)

            if callback is not None:
                callback(locals())

            if np.abs(x - x_prev).sum() < tol:
                success = True
                break
            i += batch_size
            step += 1

    message = ""
    return optimize.OptimizeResult(x=x, success=success, nit=it, message=message)
