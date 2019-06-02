from PyQt5.QtWidgets import (QMainWindow, QWidget,
                             QLabel, QApplication, QAction,
                             QSizePolicy, QGraphicsView, QGraphicsScene,
                             QGraphicsPixmapItem, QGridLayout, QFileDialog)
from PyQt5.QtGui import QPixmap
import sys
from constant import (method_shortcut, window_width as width,
                      window_height as height, window_x_pos, window_y_pos,
                      source_image_background_color,
                      result_image_background_color, image_need_rescale,
                      image_file_type)
import os
from Manager import run_method


class UI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.menubar = self.menuBar()
        self.statusBar()

        self.layout = QGridLayout()

        self.open_file_location: str = os.path.dirname(os.path.abspath(__file__))
        self.save_file_location: str = os.path.dirname(os.path.abspath(__file__))

        self.source_image_pixmap: QPixmap = None
        self.result_image_pixmap: QPixmap = None

        self.initUI()

    def initUI(self):

        # set bar
        self.set_menu_bar()
        self.set_method_bar()

        # set source image box and result image box
        self.set_image_box()

        self.setGeometry(window_x_pos, window_y_pos, width, height)
        self.setMinimumSize(width, height)
        self.setWindowTitle('Project3-Fourier Transform')

        self.show()

    def set_menu_bar(self):
        # open image action
        open_image_action = QAction('&Open', self)
        open_image_action.setShortcut('Ctrl+O')
        open_image_action.setStatusTip('Open Image')
        open_image_action.triggered.connect(self.open_image_dialog)

        # save image action
        save_image_action = QAction('&Save', self)
        save_image_action.setShortcut('Ctrl+S')
        save_image_action.setStatusTip('Save Image')
        save_image_action.triggered.connect(self.save_image_dialog)

        # set result image as source image action
        RIASI = QAction('&set result image as source image', self)
        RIASI.setShortcut('Ctrl+R')
        RIASI.setStatusTip('Set result image as source image')
        RIASI.triggered.connect(self.set_result_image_as_source_image)

        fileMenu = self.menubar.addMenu('&File')
        fileMenu.addAction(open_image_action)
        fileMenu.addAction(save_image_action)
        fileMenu.addAction(RIASI)

    def set_method_bar(self):
        methodMenu = self.menubar.addMenu('&Method')
        # create action for FFT, IFFT, LF, HF, DFT, IDFT
        for i in method_shortcut:
            methodMenu.addAction(self.create_action(i[0], i[1]))

    def create_action(self, action_name: str, action_shortcut: str) -> QAction:
        action = QAction(action_name, self)
        action.setShortcut(action_shortcut)
        action.setStatusTip(action_name)
        action.triggered.connect(lambda: self.call_method(action_name))
        return action

    def set_image_box(self):
        # source image
        source_image_tag = QLabel('Source Image')
        source_image_tag.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.layout.addWidget(source_image_tag, 0, 0)
        self.set_graphic_view(QPixmap('testData/test1.bmp'), source_image_background_color, 1, 0)

        # result image
        result_image_tag = QLabel('Result Image')
        result_image_tag.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.layout.addWidget(result_image_tag, 0, 1)
        self.set_graphic_view(QPixmap(''), result_image_background_color, 1, 1)

        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def set_graphic_view(self, image_pixmap: QPixmap, background_color: str, r: int, c: int):
        # save image pixmap
        if image_pixmap:
            if (r, c) == (1, 0):
                self.source_image_pixmap = image_pixmap
            elif (r, c) == (1, 1):
                self.result_image_pixmap = image_pixmap

        # not to change the original image_pixmap
        rescaled_pixmap = image_pixmap

        if image_need_rescale:
            # if image has the larger width then the scene, resize the image
            other_space_value = 50
            if rescaled_pixmap.width() > (width / 2 - other_space_value):
                image_new_height = rescaled_pixmap.height() * ((width / 2 - other_space_value) / rescaled_pixmap.width())
                rescaled_pixmap = rescaled_pixmap.scaledToHeight(image_new_height)
                rescaled_pixmap = rescaled_pixmap.scaledToWidth((width / 2 - other_space_value))

            # same things go to height
            if rescaled_pixmap.height() > (height / 2 - other_space_value):
                image_new_width = rescaled_pixmap.width() * ((height / 2 - other_space_value) / rescaled_pixmap.height())
                rescaled_pixmap = rescaled_pixmap.scaledToWidth(image_new_width)
                rescaled_pixmap = rescaled_pixmap.scaledToHeight(height / 2 - other_space_value)

        # add graphics view
        graphicsView = QGraphicsView()

        # set scene
        scene = QGraphicsScene()
        graphicsView.setScene(scene)
        graphicsView.setStyleSheet("background-color: %s" % background_color)

        # add pixmap
        image_pixmap_item = QGraphicsPixmapItem(rescaled_pixmap)
        scene.addItem(image_pixmap_item)

        # delete the previous position widget
        temp_widget = self.layout.itemAtPosition(r, c)
        if temp_widget:
            temp_widget.widget().setParent(None)
        self.layout.addWidget(graphicsView, r, c)

    def call_method(self, method_name: str):
        # print('Current Method: %s' % method_name)
        result_pixmap = run_method(method_name, self.source_image_pixmap.toImage())

        # set graphic view in result image box
        if result_pixmap:
            self.set_graphic_view(result_pixmap, result_image_background_color, 1, 1)

    def open_image_dialog(self):
        # print('Opening image')
        # self.set_graphic_view('testData/test.jpeg', source_image_background_color, 1, 0)
        filename, _ = QFileDialog.getOpenFileName(None, "Open file", self.open_file_location,
                                                  "Image files %s" % image_file_type)
        temp_pos = filename.rfind('/')
        if temp_pos:
            self.open_file_location = filename[: temp_pos + 1]

        if filename:
            # print('Image found!')
            self.set_graphic_view(QPixmap(filename), source_image_background_color, 1, 0)

    def save_image_dialog(self):
        # print('Saving image')
        # self.set_graphic_view('testData/testPng.png', result_image_background_color, 1, 0)
        filename, _ = QFileDialog.getSaveFileName(None, "Save File", self.save_file_location,
                                                  "Image Files %s" % image_file_type)
        temp_pos = filename.rfind('/')
        self.save_file_location = filename[: temp_pos + 1]

        if filename:
            self.result_image_pixmap.save(filename)

    def set_result_image_as_source_image(self):
        # print('Set result image as source image')
        if self.result_image_pixmap:
            source_pixmap = self.result_image_pixmap
            self.set_graphic_view(source_pixmap, source_image_background_color, 1, 0)
            self.set_graphic_view(QPixmap(''), result_image_background_color, 1, 1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UI()
    sys.exit(app.exec_())