from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout
import sys

from PyQt5.QtGui import QPixmap, QImage, QColor
from method.Grey import Grey
from method.FFT import FFT
from method.DFT import DFT
from method.IDFT import IDFT


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.title = "PyQt5 Open File"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 300

        self.image = QImage()

        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        layout = QGridLayout()

        self.btn1 = QPushButton("Set")
        self.btn1.clicked.connect(self.getImage)

        self.btn2 = QPushButton("Convert")
        self.btn2.clicked.connect(self.convert)

        layout.addWidget(self.btn1, 0, 0)
        layout.addWidget(self.btn2, 0, 1)

        self.label1 = QLabel("First Image")
        layout.addWidget(self.label1, 1, 0)

        self.label2 = QLabel("Second Image")
        layout.addWidget(self.label2, 1, 1)

        self.setLayout(layout)

        self.show()

    def getImage(self):
        imagePath = 'TestData/test1.bmp'
        self.image = QImage(imagePath)
        pixmap = QPixmap(imagePath)
        self.label1.setPixmap(QPixmap(pixmap))

    def convert(self):
        colors_matrix = []
        img = self.image
        output = QImage(img.width(), img.height(), img.format())

        # get the grey value
        for w in range(img.width()):
            temp = []
            for h in range(img.height()):
                value = QColor(img.pixel(w, h))
                grey = value.red() * 0.299 + value.green() * 0.587 + value.blue() * 0.144
                grey = grey * pow(-1, w + h)
                temp.append(grey)
            colors_matrix.append(temp)

        # run method here
        result_matrix = DFT(colors_matrix)

        # return the answer
        for w in range(output.width()):
            for h in range(output.height()):
                grey = result_matrix[w][h] if result_matrix[w][h] <= 255 else 255
                output.setPixelColor(w, h, QColor(grey, grey, grey, 255))

        result_pixmap = QPixmap().fromImage(output)
        self.label2.setPixmap(result_pixmap)


if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())