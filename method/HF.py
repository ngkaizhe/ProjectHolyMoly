from cmath import sqrt
from typing import List
from copy import deepcopy


def HF(complex_mat: List[List[complex]], D_cut_off, n) -> List[List[complex]]:
    grey_matrix = deepcopy(complex_mat)

    # get high filter
    h = len(grey_matrix)
    w = len(grey_matrix[0])

    for x in range(h):
        for y in range(w):
            # set to middle
            u = x - h / 2
            v = y - w / 2

            filter = 1 - 1 / (1 + pow(sqrt(u * u + v * v) / D_cut_off, 2 * n))
            grey_matrix[x][y] *= filter
            grey_matrix[x][y] = grey_matrix[x][y]

    return grey_matrix
