from PyQt5.QtGui import QPixmap, QImage, QColor
from constant import method_shortcut
from method.Grey import Grey
from method.DFT import DFT
from method.IDFT import IDFT
from method.FFT import FFT
from method.IFFT import IFFT
from method.HF import HF
from method.LF import LF

function_dict = {
method_shortcut[0][0]: FFT,
method_shortcut[1][0]: IFFT,
method_shortcut[2][0]: LF,
method_shortcut[3][0]: HF,
method_shortcut[4][0]: DFT,
method_shortcut[5][0]: IDFT,
}


def run_method(method_name: str, img: QImage) -> QPixmap:
    output = QImage(img.width(), img.height(), img.format())

    # run method here
    result_matrix = function_dict[method_name](img)

    # means function are not done yet
    if result_matrix is None:
        return

    # return the answer
    for h in range(output.height()):
        for w in range(output.width()):
            if result_matrix[w][h] > 255:
                result_matrix[w][h] = 255
            elif result_matrix[w][h] < 0:
                result_matrix[w][h] = 0
            grey = result_matrix[w][h]
            output.setPixelColor(w, h, QColor(grey, grey, grey, 255))

    result_pixmap = QPixmap().fromImage(output)
    return result_pixmap

