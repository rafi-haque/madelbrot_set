import numpy as np


def mandelbrot_set(xmin, xmax, ymin, ymax, xn, yn, maxiter, horizon=2.0):
    X = np.linspace(xmin, xmax, xn, dtype=np.float32)
    Y = np.linspace(ymin, ymax, yn, dtype=np.float32)
    C = X + Y[:, None]*1j
    N = np.zeros(C.shape, dtype=int)
    Z = np.zeros(C.shape, np.complex64)
    for n in range(maxiter):
        I = np.less(abs(Z), horizon)
        N[I] = n
        Z[I] = Z[I]**2 + C[I]
    N[N == maxiter-1] = 0
    return Z, N


if __name__ == '__main__':
    import time
    import matplotlib
    from matplotlib import colors
    import matplotlib.pyplot as plt

    xmin, xmax, xn = -2.25, +0.75, 6000/2
    ymin, ymax, yn = -1.25, +1.25, 5000/2
    maxiter = 200
    horizon = 2.0 ** 40
    log_horizon = np.log(np.log(horizon))/np.log(2)
    Z, N = mandelbrot_set(xmin, xmax, ymin, ymax, xn, yn, maxiter, horizon)

    with np.errstate(invalid='ignore'):
        M = np.nan_to_num(N + 1 -
                          np.log(np.log(abs(Z)))/np.log(2) +
                          log_horizon)

    dpi = 96
    width = 10
    height = 10*yn/xn

    for i in range(350, 360):
        fig = plt.figure(figsize=(width, height), dpi=dpi*2)
        ax = fig.add_axes([0.0, 0.0, 1.0, 1.0], frameon=False, aspect=1)

        # Shaded rendering
        light = colors.LightSource(azdeg=i, altdeg=20)
        temp_M = light.shade(M, cmap=plt.cm.hot, vert_exag=10,
                             norm=colors.PowerNorm(5), blend_mode='hsv')
        plt.imshow(temp_M, extent=[xmin, xmax, ymin,
                                   ymax], interpolation="bicubic")
        ax.set_xticks([])
        ax.set_yticks([])

        # plt.show()
        name = str(i)+".png"
        print(name)
        plt.savefig(name, bbox_inches='tight')
