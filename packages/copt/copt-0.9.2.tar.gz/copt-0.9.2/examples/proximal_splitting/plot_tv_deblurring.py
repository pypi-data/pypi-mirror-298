# python3
"""
Total variation regularization
==============================

Comparison of solvers with total variation regularization.
"""
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy import misc
from scipy import sparse

import copt as cp

np.random.seed(0)

img = misc.face(gray=True).astype(float)
# resize
img = np.array(Image.fromarray(img).resize((153, 115)))
img = img.astype(float) / img.max()

n_rows, n_cols = img.shape
n_features = n_rows * n_cols
n_samples = n_features
max_iter = 2000

# .. compute blurred and noisy image ..
A = sparse.load_npz("data/blur_matrix.npz")
b = A.dot(img.ravel())

np.random.seed(0)

# .. compute the step-size ..
f = cp.loss.SquareLoss(A, b)
step_size = 1.0 / f.lipschitz


def loss(x, pen):
    x_mat = x.reshape((n_rows, n_cols))
    tmp1 = np.abs(np.diff(x_mat, axis=0))
    tmp2 = np.abs(np.diff(x_mat, axis=1))
    return f(x) + pen * (tmp1.sum() + tmp2.sum())


# .. run the solver for different values ..
# .. of the regularization parameter beta ..
all_betas = [0, 1e-7, 1e-6]
all_trace_ls, all_trace_nols, all_trace_pdhg, out_img = [], [], [], []
all_trace_ls_time, all_trace_nols_time, all_trace_pdhg_time = [], [], []
for i, beta in enumerate(all_betas):
    print("Iteration %s, beta %s" % (i, beta))

    def g_prox(x, gamma, pen=beta):
        return cp.tv_prox.prox_tv1d_cols(gamma * pen, x, n_rows, n_cols)

    def h_prox(x, gamma, pen=beta):
        return cp.tv_prox.prox_tv1d_rows(gamma * pen, x, n_rows, n_cols)

    cb_adatos = cp.utils.Trace()
    adatos = cp.minimize_three_split(
        f.f_grad,
        np.zeros(n_features),
        g_prox,
        h_prox,
        step_size=step_size,
        max_iter=max_iter,
        tol=0,
        callback=cb_adatos,
        h_Lipschitz=beta,
    )
    trace_ls = [loss(x, beta) for x in cb_adatos.trace_x]
    all_trace_ls.append(trace_ls)
    all_trace_ls_time.append(cb_adatos.trace_time)
    out_img.append(adatos.x.reshape(img.shape))

    cb_tos = cp.utils.Trace()
    cp.minimize_three_split(
        f.f_grad,
        np.zeros(n_features),
        g_prox,
        h_prox,
        step_size=step_size,
        max_iter=max_iter,
        tol=0,
        callback=cb_tos,
        line_search=False,
    )
    trace_nols = [loss(x, beta) for x in cb_tos.trace_x]
    all_trace_nols.append(trace_nols)
    all_trace_nols_time.append(cb_tos.trace_time)

    cb_pdhg = cp.utils.Trace()
    cp.minimize_primal_dual(
        f.f_grad,
        np.zeros(n_features),
        g_prox,
        h_prox,
        callback=cb_pdhg,
        max_iter=max_iter,
        step_size=step_size,
        step_size2=(1. / step_size) / 2,
        line_search=False,
    )
    trace_pdhg = np.array([loss(x, beta) for x in cb_pdhg.trace_x])
    all_trace_pdhg.append(trace_pdhg)
    all_trace_pdhg_time.append(cb_pdhg.trace_time)

# .. plot the results ..
f, ax = plt.subplots(2, 3, sharey=False)
xlim = [0.02, 0.02, 0.1]
for i, beta in enumerate(all_betas):
    ax[0, i].set_title(r"$\lambda=%s$" % beta)
    ax[0, i].imshow(out_img[i], interpolation="nearest", cmap=plt.cm.gray)
    ax[0, i].set_xticks(())
    ax[0, i].set_yticks(())

    fmin = min(np.min(all_trace_ls[i]), np.min(all_trace_pdhg[i]))
    scale = all_trace_ls[i][0] - fmin
    plot_tos, = ax[1, i].plot(
        (all_trace_ls[i] - fmin) / scale,
        "--",
        lw=2,
        marker="o",
        markevery=400,
        markersize=7,
    )

    plot_tos_nols, = ax[1, i].plot(
        (all_trace_nols[i] - fmin) / scale,
        lw=2,
        marker="<",
        markevery=400,
        markersize=7,
    )

    plot_pdhg, = ax[1, i].plot(
        (all_trace_pdhg[i] - fmin) / scale,
        "--",
        lw=2,
        marker="^",
        markevery=400,
        markersize=7,
    )

    ax[1, i].set_xlabel("Iterations")
    ax[1, i].set_yscale("log")
    ax[1, i].set_ylim((1e-14, None))
    ax[1, i].set_xlim((0, 1500))
    ax[1, i].grid(True)


plt.gcf().subplots_adjust(bottom=0.25)
plt.figlegend(
    (plot_tos, plot_tos_nols, plot_pdhg),
    (
        "Adaptive three operator splitting",
        "Three operator splitting",
        "Primal-dual hybrid gradient",
    ),
    "lower center",
    ncol=2,
    scatterpoints=1,
    frameon=False,
)

ax[1, 0].set_ylabel("Objective minus optimum")
plt.show()
