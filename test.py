from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout
import sys

from PyQt5.QtGui import QPixmap, QImage, QColor
from method.Grey import Grey


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
        imagePath = 'TestData/test.jpeg'
        self.image = QImage(imagePath)
        pixmap = QPixmap(imagePath)
        self.label1.setPixmap(QPixmap(pixmap))

    def convert(self):
        colors_matrix = []
        img = self.image
        output = QImage(img.width(), img.height(), img.format())

        for w in range(img.width()):
            temp = []
            for h in range(img.height()):
                value = img.pixel(w, h)
                colors = QColor(value).getRgb()
                temp.append(colors)
            colors_matrix.append(temp)

        # run method here
        result_matrix = Grey(colors_matrix)

        for w in range(output.width()):
            for h in range(output.height()):
                color = result_matrix[w][h]
                output.setPixelColor(w, h, color)

        result_pixmap = QPixmap().fromImage(output)
        self.label2.setPixmap(result_pixmap)


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())