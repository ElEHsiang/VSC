from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import skimage
import copy
import numpy as np
from skimage import io, filter, data
from skimage.morphology import disk
from gaussian_model import *

class Form(QWidget):
    def __init__(self):
        super(Form, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 1440, 960)
        self.setWindowTitle("qt spine segmentation")

        self.mainLayout = QGridLayout()

        #load image
        self.image = QImage()
        self.image.load('test image/I0000535.JPG')
        self.sImage = io.imread('test image/I0000535.JPG')

        #create a Qlabel for image display
        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(QPixmap(self.image))

        #QLabel, temp display
        self.label_tempImage = QLabel()
        self.label_tempImage.setPixmap(QPixmap(self.image))

        #QLineEdit, input image name
        self.imageNameLine = QLineEdit()
        self.imageNameLine.setFixedWidth(100)

        #QPushButton, read image by filename
        self.button_loadData = QPushButton()
        self.button_loadData.setText('load data')
        self.button_loadData.setFixedWidth(100)
        self.button_loadData.clicked.connect(self.button_loadDataClick)

        #QPushButton, load contour
        self.button_loadContour = QPushButton()
        self.button_loadContour.setText('load contour')
        self.button_loadContour.clicked.connect(self.button_loadContourClick)

        #QPushButton, level set step
        self.button_levelSetStep = QPushButton()
        self.button_levelSetStep.setText('LS step')
        self.button_levelSetStep.clicked.connect(self.button_levelSetStepClick)

        #QPushButton, level set
        self.button_levelSet = QPushButton()
        self.button_levelSet.setText('LS')
        self.button_levelSet.clicked.connect(self.button_levelSetClick)

        #QPushButton, show intensity classify
        self.button_showIntensitySegment = QPushButton()
        self.button_showIntensitySegment.setText('show intensity classify')
        self.button_showIntensitySegment.clicked.connect(self.button_showIntensitySegmentClick)

        #QPushButton, show gradient classify
        self.button_showGradientSegment = QPushButton()
        self.button_showGradientSegment.setText('show gradient classify')
        self.button_showGradientSegment.clicked.connect(self.button_showGradientSegmentClick)

        self.hLayout = QHBoxLayout()
        self.hGroupBox = QGroupBox()

        #add widget into layout
        self.mainLayout.addWidget(self.imageLabel, 0, 0)
        self.mainLayout.addWidget(self.label_tempImage,0, 1)

        #add button to vBoxLayout
        self.hLayout.addWidget(self.imageNameLine)
        self.hLayout.addWidget(self.button_loadData)
        self.hLayout.addWidget(self.button_loadContour)
        self.hLayout.addWidget(self.button_levelSet)
        self.hLayout.addWidget(self.button_levelSetStep)
        self.hLayout.addWidget(self.button_showIntensitySegment)
        self.hLayout.addWidget(self.button_showGradientSegment)

        self.hGroupBox.setLayout(self.hLayout)
        self.mainLayout.addWidget(self.hGroupBox, 1, 0)

        self.setLayout(self.mainLayout)

        self.initData()

        self.show()

    def initData(self):
        self.contour = []
        self.LSmap = []
        self.originImage = QImage(self.image)

    def mousePressEvent(self, event):
        pass

    def button_loadDataClick(self):
        fileName = self.imageNameLine.text()
        try:
            image = QImage('test image/' + fileName + '.JPG')
            sImage = io.imread('test image/' + fileName + '.JPG')
            fb = open('model/' + fileName + '_bone_model.txt', 'r')
            fnb = open('model/' + fileName + '_non-bone_model.txt', 'r')
        except IOError as e:
            print(e)
            return 0

        self.imageNumber = fileName

        self.image = image
        self.sImage = sImage
        self.originImage = image
        self.imageLabel.setPixmap(QPixmap(image))

        biMean , biStd = fb.readline()[:-1].split(' ')
        bgMean , bgStd = fb.readline()[:-1].split(' ')

        biMean = float(biMean)
        bgMean = float(bgMean)
        biStd = float(biStd)
        bgStd = float(bgStd)

        fb.close()

        nbiMean, nbiStd = fnb.readline()[:-1].split(' ')
        nbgMean, nbgStd = fnb.readline()[:-1].split(' ')

        nbiMean = float(nbiMean)
        nbgMean = float(nbgMean)
        nbiStd = float(nbiStd)
        nbgStd = float(nbgStd)

        fnb.close()

        #intensity model, bone & non-bone
        self.biModel = Gaussian_model(biMean, biStd, 0, 256)
        self.nbiModel = Gaussian_model(nbiMean, nbiStd, 0, 256)

        #gradient model, bone & non-bone
        self.bgModel = Gaussian_model(bgMean, bgStd, 0, 300)
        self.nbgModel = Gaussian_model(nbgMean, nbgStd, 0, 300)

        tempImage = QImage(self.image)

        for h in range(image.height()):
            for w in range(image.width()):
                rgb = image.pixel(w, h)
                val = qGray(rgb)
                pb = self.biModel.getProb(val)
                pnb = self.nbiModel.getProb(val)

                if pb > pnb:
                    tempImage.setPixel(w, h ,qRgb(255, 255, 255))
                else:
                    tempImage.setPixel(w, h ,qRgb(0, 0, 0))

        self.label_tempImage.setPixmap(QPixmap(tempImage))


        print('model load finish!')

    def button_showIntensitySegmentClick(self):

        if not self.imageNumber:
            print('please load file first')
            return

        tempImage = QImage(self.image)
        image = self.image

        for h in range(image.height()):
            for w in range(image.width()):
                rgb = image.pixel(w, h)
                val = qGray(rgb)
                pb = self.biModel.getProb(val)
                pnb = self.nbiModel.getProb(val)

                if pb > pnb:
                    tempImage.setPixel(w, h ,qRgb(255, 255, 255))
                else:
                    tempImage.setPixel(w, h ,qRgb(0, 0, 0))

        self.label_tempImage.setPixmap(QPixmap(tempImage))

    def button_showGradientSegmentClick(self):

        if not self.imageNumber:
            print('please load file first')
            return

        tempImage = QImage(self.image)
        gradient = filter.rank.gradient(self.sImage, disk(3))
        image = self.image

        for h in range(image.height()):
            for w in range(image.width()):
                val = gradient[w][h]
                pb = self.bgModel.getProb(val)
                pnb = self.nbgModel.getProb(val)

                if pb > pnb:
                    tempImage.setPixel(w, h ,qRgb(255, 255, 255))
                else:
                    tempImage.setPixel(w, h ,qRgb(0, 0, 0))

        self.label_tempImage.setPixmap(QPixmap(tempImage))

    def button_loadContourClick(self):
        print('load Contour')

        self.LSmap = []

        contourFileName = QFileDialog.getOpenFileName(self, 'load contour', '.', 'Txt (*.txt)')
        contour = open(contourFileName[0], 'r')

        for line in contour:
            self.LSmap.append(line[:-1].split(' ')[:-1])

        contour.close()

        self.LSmap = [list(map(int, x)) for x in self.LSmap]

        image = QImage(self.imageLabel.pixmap())
        painter = QPainter(image)
        pen = QPen(Qt.red)
        pen.setWidth(1)
        painter.setPen(pen)

        for y in range(len(self.LSmap)):
            for x in range(len(self.LSmap[0])):
                if self.LSmap[y][x] == 0:
                    self.contour.append((x, y))
                    painter.drawPoint(x, y)
        del painter

        self.label_tempImage.setPixmap(QPixmap(image))

    def button_levelSetStepClick(self):
        #print('LS step')
        currentMap =  [ list(i) for i in self.LSmap]

        image = self.image

        tempImage = QImage(self.image)

        for y in range( 1, image.height() - 1):
            for x in range( 1, image.width() - 1):
                intensity = qGray(image.pixel(x, y))
                pbi = self.biModel.getProb(intensity)
                pnbi = self.nbiModel.getProb(intensity)
                #print(str(pbi) + ' ' + str(pnbi))
                if pbi > pnbi:
                    #print('bone')
                    if self.LSmap[y + 1][x] == 0 or self.LSmap[y - 1][x] == 0 or self.LSmap[y][x + 1] == 0 or self.LSmap[y][x - 1] == 0:
                        if currentMap[y][x] > 0:
                            currentMap[y][x] -= 1
                    #tempImage.setPixel(x, y, qRgb(0, 0, 0))
                else:
                    pass
                    #print('non-bone')
                    #tempImage.setPixel(x, y, qRgb(255, 255, 255))

        for y in range(image.height()):
            for x in range(image.width()):
                if currentMap[y][x] == 0:
                    tempImage.setPixel(x, y, qRgb(255, 0, 0))
        self.LSmap = currentMap
        #self.label_tempImage.setPixmap(QPixmap(tempImage))

        self.fillHole()


    def button_levelSetClick(self):
        print('level set')

        step = 0
        lastContour = list(self.contour)

        while True:
            self.button_levelSetStepClick()
            QEventLoop().processEvents()
            step += 1

            #print(lastContour)
            #print(self.contour)

            if lastContour == self.contour:
                lastContour = list(self.contour)
                break

            lastContour = list(self.contour)

    def fillHole(self):
        image = QImage(self.image)

        self.contour = []

        holeMap = np.array([row[:] for row in self.LSmap])

        for y, l in enumerate(holeMap):
            for x, val in enumerate(l):
                if val == 0:
                    if holeMap[y - 1][x] == 1 or holeMap[y + 1][x] == 1 or holeMap[y][x - 1] == 1 or holeMap[y][x + 1] == 1:
                        self.contour.append((x, y))
                        image.setPixel(x, y, qRgb(255, 0, 0))
                        pass
                    else:
                        holeMap[y][x] = -1

        for p in self.contour:
            pass

        self.label_tempImage.setPixmap(QPixmap(image))
        self.LSmap = holeMap


def main():
    app = QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

