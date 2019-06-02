from PyQt5.QtGui import QPixmap, QImage, QColor
from constant import method_shortcut
from method.Grey import Grey


function_dict = {
method_shortcut[0][0]: None,
}


def run_method(method_name: str, img: QImage) -> QPixmap:
    colors_matrix = []
    output = QImage(img.width(), img.height(), img.format())

    for r in range(img.width()):
        temp = []
        for c in range(img.height()):
            value = img.pixel(r, c)
            colors = QColor(value).getRgb()
            temp.append(colors)
        colors_matrix.append(temp)

    # run method here
    result_matrix = Grey(colors_matrix)

    for r in range(output.width()):
        for c in range(output.height()):
            color = result_matrix[r][c]
            output.setPixelColor(r, c, color)

    result_pixmap = QPixmap().fromImage(output)
    return result_pixmap

