"""Morph snake UI
Author: Yun Hsiang
Email: hsiang023167@gmail.com
Last modified: 2014/12/14
"""
import sys

import numpy as np

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from scipy.misc import imread

__author__ = 'Yun Hsiang'
__email__ = 'hsiang023167@gmail.com'

class Form(QMainWindow):
    """UI main class
    
    Attributes:
        label_image: QLabel for display image.
        _image: QImage for original image.
        _data: numpy.ndarray for image, gray scale.

    """
    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        self.setGeometry(300, 300, 1440, 960)
        self.setWindowTitle('morph snake')

        open_action = QAction('Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('open an image')
        open_action.triggered.connect(self.open_image_)

        close_action = QAction('Close', self)
        close_action.setShortcut('Ctrl+Q')
        close_action.setStatusTip('Close program')
        close_action.triggered.connect(self.close)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(open_action)
        file_menu.addAction(close_action)

        self.init_layout()

        self.show()

    def init_layout(self):
        #morph layout
        groupBox_morph = QGroupBox()
        vLayout_morph = QHBoxLayout()

        button = self.init_morph_buttion()
        for b in button:
            vLayout_morph.addWidget(b)

        groupBox_morph.setLayout(vLayout_morph)

        #main layout
        gridLayout_main = QGridLayout()
        central_widget = QWidget()
        central_widget.setLayout(gridLayout_main)
        self.setCentralWidget(central_widget)

        self.init_label()

        gridLayout_main.addWidget(self.label_image, 0, 0)
        gridLayout_main.addWidget(groupBox_morph, 0, 1)

    def init_label(self):
        self.label_image = QLabel()
        pass

    def init_general_button(self):
        pass

    def init_morph_buttion(self):
        pushButton_snake = QPushButton()
        pushButton_snake.setText('morph snake')
        return [pushButton_snake]

    def open_image_(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open Image', '.', 'Images (*.jpg, *.bmp)')
        if not file_name:
            return

        pass
        
        



def main():
    app = QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

