from cmath import exp, pi, sqrt
from typing import List
from PyQt5.QtGui import QImage, QColor


def DFT(img: QImage) -> List[List[float]]:
    grey_matrix = []

    # get the grey value
    for h in range(img.height()):
        temp = []
        for w in range(img.width()):
            value = QColor(img.pixel(w, h))
            grey = value.red() * 0.299 + value.green() * 0.587 + value.blue() * 0.144
            grey = grey * pow(-1, w + h)  # move to middle
            temp.append(grey)
        grey_matrix.append(temp)

    f = grey_matrix
    M = len(f)
    N = len(f[0])
    F = []

    for u in range(M):
        temp = []
        for v in range(N):
            F_u_v = DicreteFourierTransform(f, u, v)
            temp.append(abs(F_u_v))
        F.append(temp)

    return F


def DicreteFourierTransform(f: List[List[float]], u, v) -> complex:
    M = len(f)
    N = len(f[0])
    F_u_v = 0

    for x in range(M):
        for y in range(N):
            w = exp(-2j * pi * ((u * x) / M + (v * y) / N))
            F_u_v += f[x][y] * w

    F_u_v /= sqrt(M * N)

    return F_u_v
