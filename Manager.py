from PyQt5.QtGui import QPixmap, QImage, QColor
from constant import method_shortcut
from method.Grey import Grey
from method.DFT import DFT
from method.IDFT import IDFT
from method.FFT import FFT
from method.IFFT import IFFT
from method.HF import HF
from method.LF import LF
from typing import List


function_dict = {
method_shortcut[0][0]: FFT,
method_shortcut[1][0]: IFFT,
method_shortcut[2][0]: LF,
method_shortcut[3][0]: HF,
method_shortcut[4][0]: DFT,
method_shortcut[5][0]: IDFT,
}
# def run_method(method_name: str, img: QImage) -> QPixmap:
#     output = QImage(img.width(), img.height(), img.format())
#
#     # run method here
#     result_matrix = function_dict[method_name](img)
#
#     # means function are not done yet
#     if result_matrix is None:
#         return
#
#     # return the answer
#     for h in range(output.height()):
#         for w in range(output.width()):
#             if result_matrix[w][h] > 255:
#                 result_matrix[w][h] = 255
#             elif result_matrix[w][h] < 0:
#                 result_matrix[w][h] = 0
#             grey = result_matrix[w][h]
#             output.setPixelColor(w, h, QColor(grey, grey, grey, 255))
#
#     result_pixmap = QPixmap().fromImage(output)
#     return result_pixmap


class Manager(object):
    def __init__(self):
        self.source_complex_mat: List[List[complex]] = None
        self.result_complex_mat: List[List[complex]] = None
        self.source_img_format = None

    def set_source_img(self, img: QImage):
        self.source_img_format = img.format()
        self.source_complex_mat = []

        # get the grey value
        a = 0
        for w in range(img.width()):
            temp = []
            for h in range(img.height()):
                value = QColor(img.pixel(w, h))
                grey = value.red() * 0.299 + value.green() * 0.587 + value.blue() * 0.144
                grey *= pow(-1, w + h)  # move to middle
                temp.append(int(grey))
            self.source_complex_mat.append(temp)

    def get_result_img(self) -> QPixmap:
        source = self.source_complex_mat
        output = QImage(len(source[0]), len(source), self.source_img_format)
        result_mat = self.result_complex_mat

        # return the answer
        for h in range(output.height()):
            for w in range(output.width()):
                grey = 0
                if abs(result_mat[w][h]) > 255:
                    grey = 255
                elif abs(result_mat[w][h]) < 0:
                    grey = 0
                else:
                    grey = abs(result_mat[w][h])
                output.setPixelColor(w, h, QColor(grey, grey, grey, 255))

        result_pixmap = QPixmap().fromImage(output)
        return result_pixmap

    def result_to_source(self):
        # set source mat as result mat
        self.source_complex_mat = self.result_complex_mat
        # clear result complex mat
        self.result_complex_mat = None

    def run_method(self, method_name: str):
        self.result_complex_mat = function_dict[method_name](self.source_complex_mat)


