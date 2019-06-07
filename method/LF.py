from cmath import sqrt
from typing import List
from PyQt5.QtGui import QColor, QImage
from math import floor


D_cut_off = 20
n = 1


def LF(img: QImage) -> List[List[float]]:
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

    # get low filter
    h = len(grey_matrix)
    w = len(grey_matrix[0])

    for x in range(h):
        for y in range(w):
            # set to middle
            u = x - h / 2
            v = y - w / 2

            filter = 1 / 1 + pow(sqrt(u * u + v * v) / D_cut_off, 2 * n)
            grey_matrix[x][y] *= filter
            grey_matrix[x][y] = grey_matrix[x][y]

    return grey_matrix
