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
from scipy.ndimage.filters import sobel
from functools import reduce

from utils.MyQLabel import MyQLabel
from levelset.levelset import LevelSetSolver

__author__ = 'Yun Hsiang'
__email__ = 'hsiang023167@gmail.com'

class Form(QMainWindow):
    """UI main class
    
    Attributes:
        label_image: QLabel for display image.
        _image: QImage for original image.
        _data: numpy.ndarray for image, gray scale.
        _init_point: level set init point.
        _solver: LevelSetSolver

    Slot:
        _pushButton_snake_click: Start snake process.
        _update_pos: Connected with MyQLabel. Record level set init point.
    """
    def __init__(self):
        super().__init__()
        pyqtRemoveInputHook()
        self.init_UI()
        self.init_data()

    def init_data(self):
        self._image = []
        self._data = []
        self._init_point = ()
        self._solver = []

    def init_UI(self):
        self.setGeometry(300, 300, 1440, 960)
        self.setWindowTitle('morph snake')

        open_action = QAction('Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('open an image')
        open_action.triggered.connect(self._open_image)

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
        #input layout
        formLayout_input = QFormLayout()
        input_ = self.init_input_widgit()
        for t, el in input_:
            formLayout_input.addRow(t, el)

        #morph layout
        groupBox_morph = QGroupBox()
        vLayout_morph = QVBoxLayout()
        vLayout_morph.addLayout(formLayout_input)

        button = self.init_morph_button()
        for b in button:
            vLayout_morph.addWidget(b)
        vLayout_morph.addStretch(1)

        groupBox_morph.setLayout(vLayout_morph)

        #main layout
        gridLayout_main = QGridLayout()
        gridLayout_main.setColumnStretch(0, 2)
        gridLayout_main.setColumnStretch(1, 1)
        central_widget = QWidget()
        central_widget.setLayout(gridLayout_main)
        self.setCentralWidget(central_widget)

        self.init_label()

        gridLayout_main.addWidget(self.label_image, 0, 0)
        #gridLayout_main.addLayout(vLayout_morph, 0, 1)
        gridLayout_main.addWidget(groupBox_morph, 0, 1)

    def init_label(self):
        self.label_image = MyQLabel()
        self.label_image.setAlignment(Qt.AlignTop)
        self.label_image.click_pos.connect(self._update_pos)
        pass

    def init_general_button(self):
        pass

    def init_input_widgit(self):
        list_ = []
        label_text = QLabel('radius') 
        self.lineEdit_radius = QLineEdit()
        self.lineEdit_radius.setInputMask('99')
        list_.append((label_text, self.lineEdit_radius))

        label_text = QLabel('iterations')
        self.lineEdit_iter = QLineEdit()
        self.lineEdit_iter.setInputMask('999')
        list_.append((label_text, self.lineEdit_iter))

        return list_

    def init_morph_button(self):
        list_ = []

        pushButton_snake = QPushButton()
        pushButton_snake.setText('morph snake')
        pushButton_snake.clicked.connect(self._pushButton_snake_click)
        list_.append(pushButton_snake)
        return list_

    def _open_image(self):
        file_name, file_filter = QFileDialog.getOpenFileName(self, 'Open Image', '.', 'Images (*.jpg *.bmp)')
        if not file_name:
            return
        print(file_name)
        self._image = QImage(file_name)
        self._data = imread(file_name)[...,0]

        self.label_image.setPixmap(QPixmap(self._image))

    @pyqtSlot(int, int)
    def _update_pos(self, x, y):
        if not self._image:
            return
        x = x if x < self._image.width() else -1
        y = y if y < self._image.height() else -1

        if x is not -1 and y is not -1:
            self._init_point = (x, y)
            print("Click position:{} {}".format(x, y))

    #TODO: Modify if...else... to exception?
    @pyqtSlot()
    def _pushButton_snake_click(self):
        print('morph snake')
        if not self._image:
            print('Please image first')
            return
        if not self._init_point:
            print('Please click init point')
            return

        radius = int(self.lineEdit_radius.text())
        if not radius:
            print('Please input radius')
            return

        iter = self.lineEdit_iter.text()
        if not iter or iter == 0:
            print('Please input iteration times')
            return

        self._solver = LevelSetSolver(self._data, smooth=1, threshold=0.5, balloon=1)
        levelset = LevelSetSolver.circle_levelset(self._data.shape, self._init_point, radius)
        self._solver.set_levelset(levelset)
        print('init point: ' + str(self._init_point))
        print('radius: ' + str(radius))

        u = []
        for i in range(int(iter)):
            u = self._solver.step()
        """
        e = sobel(u)

        edge = np.zeros_like(u)
        edge[e != 0] = 1
        edge[u != 0] = 1
        """
        edge_points = list(reduce(zip, np.where(u == 1)))
        
        pixmap = QPixmap(self._image)
        painter = QPainter(pixmap)
        painter.setPen(Qt.red)

        for y, x in edge_points:
            painter.drawPoint(x, y)

        self.label_image.setPixmap(pixmap)

        del painter

def main():
    app = QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

