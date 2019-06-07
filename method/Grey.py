from typing import List
from PyQt5.QtGui import QColor


#unused method
def Grey(colors_matrix: List[List[float]]) -> List[List[float]]:

    result_matrix = []
    for w in range(len(colors_matrix)):
        temp = []
        for h in range(len(colors_matrix[w])):
            colors = colors_matrix[w][h]
            grey = colors[0] * 0.299 + colors[1] * 0.587 + colors[2] * 0.144
            temp.append(QColor(grey, grey, grey, 255))
        result_matrix.append(temp)
    return result_matrix
