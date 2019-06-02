from typing import List
from PyQt5.QtGui import QColor


def Grey(colors_matrix: List[List[QColor]]) -> List[List[QColor]]:

    result_matrix = []
    for r in range(len(colors_matrix)):
        temp = []
        for c in range(len(colors_matrix[r])):
            colors = colors_matrix[r][c]
            grey = colors[0] * 0.299 + colors[1] * 0.587 + colors[2] * 0.144
            temp.append(QColor(grey, grey, grey, 255))
        result_matrix.append(temp)
    return result_matrix
