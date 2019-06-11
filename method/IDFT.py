from cmath import exp, pi, sqrt
from typing import List


def IDFT(complex_mat: List[List[complex]], D_cut, n) -> List[List[complex]]:
    F = complex_mat
    M = len(F)
    N = len(F[0])
    f = []

    for x in range(M):
        temp = []
        for y in range(N):
            f_x_y = InverseDicreteFourierTransform(F, y, x)
            temp.append(f_x_y)
        f.append(temp)

    return f


def InverseDicreteFourierTransform(F: List[List[complex]], x, y) -> complex:
    M = len(F)
    N = len(F[0])
    f_x_y = 0

    for u in range(M):
        for v in range(N):
            w = exp(2j * pi * ((u * x) / M + (v * y) / N))
            f_x_y += F[u][v] * w

    f_x_y /= sqrt(M * N)

    return f_x_y
