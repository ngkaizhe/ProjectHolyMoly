from cmath import exp, pi, sqrt
from typing import List
from PyQt5.QtGui import QImage, QColor


def IDFT(img: QImage) -> List[List[float]]:
    grey_matrix = []

    # get the grey value
    for h in range(img.height()):
        temp = []
        for w in range(img.width()):
            value = QColor(img.pixel(w, h))
            grey = value.red() * 0.299 + value.green() * 0.587 + value.blue() * 0.144
            # grey = grey * pow(-1, w + h)  # move to middle
            temp.append(grey)
        grey_matrix.append(temp)

    F = grey_matrix
    M = len(F)
    N = len(F[0])
    f = []

    for x in range(M):
        temp = []
        for y in range(N):
            f_x_y = InverseDicreteFourierTransform(F, x, y)
            temp.append(abs(f_x_y))
        f.append(temp)

    return f


def InverseDicreteFourierTransform(F: List[List[float]], x, y) -> complex:
    M = len(F)
    N = len(F[0])
    f_x_y = 0

    for u in range(M):
        for v in range(N):
            w = exp(2j * pi * ((u * x) / M + (v * y) / N))
            f_x_y += F[u][v] * w

    f_x_y /= sqrt(M * N)

    return f_x_y
