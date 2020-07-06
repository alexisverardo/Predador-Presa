import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
# Parámetros
a = 0.1
b = 0.02
c = 0.3
d = 0.01
# Condiciones para integración
tf = 200
N = 800

def getSolucion(x0, y0):
    conds_iniciales = np.array([x0, y0])

    t = np.linspace(0, tf, N)
    solucion = odeint(df_dt, conds_iniciales, t, args=(a, b, c, d))

    return {'solucion': solucion, 't': t}

def df_dt(x, t, a, b, c, d):
    dx = a * x[0] - b * x[0] * x[1]
    dy = - c * x[1] + d * x[0] * x[1]
    return np.array([dx, dy])
def getDiagramaDeComportamiento(x0, y0, name):
    datos_solucion = getSolucion(x0, y0)
    solucion = datos_solucion['solucion']
    t = datos_solucion['t']
    plt.plot(t, solucion[:, 0], label='presa')
    plt.plot(t, solucion[:, 1], label='depredador')
    plt.savefig(name + '_comportamiento.png')
    plt.close()
def getDiagramaDeFases(x0, y0, name):
    datos_solucion = getSolucion(x0, y0)
    solucion = datos_solucion['solucion']

    x_max = np.max(solucion[:, 0]) * 1.05
    y_max = np.max(solucion[:, 1]) * 1.05
    x = np.linspace(0, x_max, 25)
    y = np.linspace(0, y_max, 25)
    xx, yy = np.meshgrid(x, y)
    uu, vv = df_dt((xx, yy), 0, a, b, c, d)
    norm = np.sqrt(uu ** 2 + vv ** 2)
    uu = uu / norm
    vv = vv / norm
    plt.quiver(xx, yy, uu, vv, norm, cmap=plt.cm.gray)
    plt.plot(solucion[:, 0], solucion[:, 1])
    plt.savefig(name + '_fases.png')
    plt.close()

def getPuntoDeEquilibrio(x0, y0, name):
    datos_solucion = getSolucion(x0, y0)
    solucion = datos_solucion['solucion']
    t = datos_solucion['t']
    def C(x, y, a, b, c, d):
        return a * np.log(y) - b * y + c * np.log(x) - d * x
    fig, ax = plt.subplots(1,2)
    ax[0].plot(solucion[:, 0], solucion[:, 1], lw=2, alpha=0.8)
    ax[0].scatter(c/d, a/b)
    levels = (0.5, 0.6, 0.7, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77, 0.775, 0.78, 0.781)
    x_max = np.max(solucion[:, 0]) * 1.05
    y_max = np.max(solucion[:, 1]) * 1.05
    x = np.linspace(0, x_max, 25)
    y = np.linspace(0, y_max, 25)
    xx, yy = np.meshgrid(x, y)
    constant = C(xx, yy, a, b, c, d)
    ax[0].contour(xx, yy, constant, levels, colors='blue', alpha=0.3)
    ax[1].plot(t, solucion[:, 0], label='presa')
    ax[1].plot(t, solucion[:, 1], label='depredador')
    plt.savefig(name + '_equilibrio.png')
    plt.close()

#condiciones iniciales para 3 ejemplos
params = {
    'initial1': {'x0': 10,'y0': 500},
    'initial2': {'x0': 200,'y0': 10},
    'initial3': {'x0': 50,'y0': 50}
}
#iteramos los datos y la salidas son 3 imagenes en la raiz del mismo proyecto
for i, condition in params.items():
    getDiagramaDeComportamiento(condition['x0'], condition['y0'], i)
    getDiagramaDeFases(condition['x0'], condition['y0'], i)
    getPuntoDeEquilibrio(condition['x0'], condition['y0'], i)