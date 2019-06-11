from PyQt5.QtWidgets import (QMainWindow, QWidget,
                             QLabel, QApplication, QAction,
                             QSizePolicy, QGraphicsView, QGraphicsScene,
                             QGraphicsPixmapItem, QGridLayout, QFileDialog,
                             QLayoutItem, QLineEdit, QHBoxLayout)
from PyQt5.QtGui import QPixmap
import sys
from constant import (method_shortcut, window_width as width,
                      window_height as height, window_x_pos, window_y_pos,
                      source_image_background_color,
                      result_image_background_color,
                      image_file_type)
import os
from Manager import Manager
from helper_function import getLargestNumberOfLog2


class UI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.menubar = self.menuBar()
        self.statusBar()

        self.layout = QGridLayout()

        self.open_file_location: str = os.path.dirname(os.path.abspath(__file__)) + '\\testData\\'
        self.save_file_location: str = os.path.dirname(os.path.abspath(__file__)) + '\\testData\\'

        self.source_image_pixmap: QPixmap = None
        self.result_image_pixmap: QPixmap = None

        self.manager: Manager = Manager()

        self.current_method: str = None
        self.D_cut: int = 10
        self.n: int = 1

        self.linebox_D_cut: QLineEdit = None
        self.linebox_n: QLineEdit = None

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
        self.set_graphic_view(QPixmap(''), source_image_background_color, 1, 0)

        # result image
        result_image_tag = QLabel('Result Image')
        result_image_tag.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # D-cut
        D_cut_tag = QLabel('D-cut: ')
        D_cut_tag.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.linebox_D_cut = QLineEdit('10')
        self.linebox_D_cut.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # n
        n_tag = QLabel('n: ')
        n_tag.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.linebox_n = QLineEdit('1')
        self.linebox_n.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        hbox = QHBoxLayout()
        hbox.addWidget(result_image_tag)
        hbox.addWidget(D_cut_tag)
        hbox.addWidget(self.linebox_D_cut)
        hbox.addWidget(n_tag)
        hbox.addWidget(self.linebox_n)

        self.layout.addLayout(hbox, 0, 1)
        self.set_graphic_view(QPixmap(''), result_image_background_color, 1, 1)

        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def set_graphic_view(self, image_pixmap: QPixmap, background_color: str, r: int, c: int):
        # rescaled original image to the proper size, to prevent FFT or IFFT throw exception (log2)
        max_length = max(image_pixmap.width(), image_pixmap.height())
        max_log2 = getLargestNumberOfLog2(max_length)
        image_pixmap = image_pixmap.scaled(max_log2, max_log2)

        # save image pixmap
        if image_pixmap:
            if (r, c) == (1, 0):
                self.source_image_pixmap = image_pixmap
            elif (r, c) == (1, 1):
                self.result_image_pixmap = image_pixmap

        # not to change the original image_pixmap
        # rescaled_pixmap just used as showing in ui purpose
        rescaled_pixmap = image_pixmap

        # get the graphicsView widget for in future using purpose
        temp_widget: QLayoutItem = self.layout.itemAtPosition(r, c)

        if temp_widget:
            # check whether the size was larger than the size of graphicsView
            # if yes, rescale it
            if rescaled_pixmap.width() > temp_widget.widget().width() or \
                    rescaled_pixmap.height() > temp_widget.widget().height():
                min_length = min(temp_widget.widget().width(), temp_widget.widget().height())
                max_log2 = getLargestNumberOfLog2(min_length)
                rescaled_pixmap = rescaled_pixmap.scaled(max_log2, max_log2)

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
        if temp_widget:
            temp_widget.widget().setParent(None)
        self.layout.addWidget(graphicsView, r, c)

    def call_method(self, method_name: str):
        self.current_method = method_name
        # run method
        D_cut = float(self.linebox_D_cut.text())
        n = float(self.linebox_n.text())

        self.manager.run_method(self.current_method, D_cut, n)
        # get image pixmap
        result_pixmap = self.manager.get_result_img()

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
            # set source for Manager
            self.manager.set_source_img(self.source_image_pixmap.toImage())

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
            self.manager.result_to_source()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UI()
    sys.exit(app.exec_())