from cmath import exp, pi, sqrt
from typing import List


def DFT(complex_mat: List[List[complex]], D_cut, n) -> List[List[complex]]:
    f = complex_mat
    M = len(f)
    N = len(f[0])
    F = []

    for v in range(M):
        temp = []
        for u in range(N):
            F_u_v = DicreteFourierTransform(f, u, v)
            temp.append(F_u_v)
        F.append(temp)

    return F


def DicreteFourierTransform(f: List[List[complex]], u, v) -> complex:
    M = len(f)
    N = len(f[0])
    F_u_v = 0

    for x in range(M):
        for y in range(N):
            w = exp(-2j * pi * ((u * x) / M + (v * y) / N))
            F_u_v += f[x][y] * w

    F_u_v /= sqrt(M * N)

    return F_u_v
