from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import skimage
from skimage import io, filter, data
from skimage.morphology import disk
import numpy as np

class Form(QWidget):
    def __init__(self):
        super(Form, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle("qt make contour")

        self.mainLayout = QGridLayout()

        #load image
        self.image = QImage()
        self.image.load('test image/I0000535.JPG')
        self.imageName = 'I0000535.JPG'

        #create a Qlabel for image display
        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(QPixmap(self.image))

        #create a Qlabel for click position
        self.positionLabel = QLabel()
        self.positionLabel.setText('position')

        #create a Qlabel for click position
        self.messageLabel = QLabel()
        self.messageLabel.setText('message')

        #QPushButton, open file
        self.openFileButton = QPushButton()
        self.openFileButton.setText("open file")
        self.openFileButton.clicked.connect(self.openFileButtonClick)

        #QPushButton, print all contour point in terminal
        self.listContourButton = QPushButton()
        self.listContourButton.setText("list contour")
        self.listContourButton.clicked.connect(self.listContourButtonClick)

        #QPushButton, draw line form contour[0] ~ contour[n]
        self.drawContourButton = QPushButton()
        self.drawContourButton.setText("draw contour")
        self.drawContourButton.clicked.connect(self.drawContourButtonClick)

        #QPushButton, draw line from counout[n] to contour[0]
        self.closeContourButton = QPushButton()
        self.closeContourButton.setText("close contour")
        self.closeContourButton.clicked.connect(self.closeContourButtonClick)

        #QPushButton, clear contour
        self.clearContourButton = QPushButton()
        self.clearContourButton.setText("clear contour")
        self.clearContourButton.clicked.connect(self.clearContourButtonClick)

        #QPushButton, clear contour
        self.saveContourButton = QPushButton()
        self.saveContourButton.setText("save contour")
        self.saveContourButton.clicked.connect(self.saveContourButtonClick)

        #QPushButton, save image
        self.saveImageButton = QPushButton()
        self.saveImageButton.setText('save image')
        self.saveImageButton.clicked.connect(self.saveImageButtonClick)

        #QGroupBox, Heaviside function type selection
        self.heavisideTypeGroup = QGroupBox()

        #QRadioButton, Heaviside function type selection
        self.heavisideBoolButton = QRadioButton('010')
        self.heavisideNormButton = QRadioButton('-101')
        self.heavisideBoolButton.setChecked(True)

        #QHBoxLayout, Heaviside function type selection
        self.heavisideLayout = QHBoxLayout()
        self.heavisideLayout.addWidget(self.heavisideBoolButton)
        self.heavisideLayout.addWidget(self.heavisideNormButton)

        self.heavisideTypeGroup.setLayout(self.heavisideLayout)

        #QPushButton, save Heaviside function
        self.savePhiButton = QPushButton()
        self.savePhiButton.setText('save phi')
        self.savePhiButton.clicked.connect(self.savePhiButtonClick)

        self.vLayout = QVBoxLayout()
        self.vGroupBox = QGroupBox()

        #add widget into layout
        self.mainLayout.addWidget(self.imageLabel, 0, 0)
        self.mainLayout.addWidget(self.positionLabel, 1, 0)
        self.mainLayout.addWidget(self.messageLabel, 2,0)

        #add button to vBoxLayout 
        self.vLayout.addWidget(self.openFileButton)
        self.vLayout.addWidget(self.listContourButton)
        self.vLayout.addWidget(self.drawContourButton)
        self.vLayout.addWidget(self.closeContourButton)
        self.vLayout.addWidget(self.clearContourButton)
        self.vLayout.addWidget(self.saveContourButton)
        self.vLayout.addWidget(self.saveImageButton)
        self.vLayout.addWidget(self.heavisideTypeGroup)
        self.vLayout.addWidget(self.savePhiButton)

        self.vGroupBox.setLayout(self.vLayout)
        self.mainLayout.addWidget(self.vGroupBox, 0, 1)

        self.setLayout(self.mainLayout)

        self.initData()

        self.show()

    def initData(self):
        self.contour = []
        self.originImage = QImage(self.image)
        self.imageNumber = 'I0000535'
        self.imageName = 'I0000535.JPG'

    def mousePressEvent(self, event):
        point = event.pos() - self.imageLabel.pos()
        self.positionLabel.setText(str(point.x()) + " " + str(point.y()) )

        temp = QImage(self.imageLabel.pixmap().toImage())
        painter = QPainter(temp)
        pen = QPen(Qt.red)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawPoint(point)
        self.imageLabel.setPixmap(QPixmap(temp))
        del painter

        self.contour.append(point)

    def listContourButtonClick(self):
        for p in self.contour:
            print(str(p.x()) + " " + str(p.y()))

    def drawContourButtonClick(self):
        if len(self.contour) < 2:
            return
        
        temp = QImage(self.originImage)
        painter = QPainter(temp)
        pen = QPen(Qt.red)
        pen.setWidth(2)
        painter.setPen(pen)

        for idx in range(len(self.contour) - 1):
            painter.drawLine(self.contour[idx], self.contour[idx + 1])

        self.imageLabel.setPixmap(QPixmap(temp))
        del painter

    def closeContourButtonClick(self):
        if len(self.contour) < 2:
            return
        
        temp = QImage(self.imageLabel.pixmap())
        painter = QPainter(temp)
        pen = QPen(Qt.red)
        pen.setWidth(2)
        painter.setPen(pen)

        painter.drawLine(self.contour[0], self.contour[-1])

        self.imageLabel.setPixmap(QPixmap(temp))
        del painter

    def clearContourButtonClick(self):
        self.imageLabel.setPixmap(QPixmap(self.originImage))
        self.contour = []

    def saveContourButtonClick(self):

        f = open(self.imageNumber + '_contour.txt', 'w')

        image = QImage(self.imageLabel.pixmap())
        sImage = io.imread(self.imageName, as_grey=True)
        median = filter.rank.median(sImage, disk(3))
        gradent = filter.rank.gradient(sImage, disk(3))

        for h in range(image.height()):
            for w in range(image.width()):
                rgb = image.pixel(w, h)
                if qRed(rgb) != qBlue(rgb):
                    f.write(str(w) + " " + str(h) + " " + str(median[h][w]) + " " + str(gradent[h][w]) + "\n")
        f.close()
        print("contour saved!")

    def openFileButtonClick(self):
        fname = QFileDialog.getOpenFileName(self, 'open file', '.', 'Images (*.jpg *.bmp)')
        print(fname[0])
        self.image.load(fname[0]) 
        self.imageLabel.setPixmap(QPixmap(self.image))
        self.originImage.load(fname[0])

        imageNumber = fname[0].split('.')[0]

        self.imageName = fname[0]

    def saveImageButtonClick(self):
        image = QImage(self.imageLabel.pixmap())
        image.save('contour_' + self.imageName, format='JPG')

    def savePhiButtonClick(self):

        f = open(self.imageNumber + '_heaviside.txt', 'w')

        if self.heavisideBoolButton.isChecked() == True:
            print('010')
            image = QImage(self.imageLabel.pixmap())
            for h in range(image.height()):
                for w in range(image.width()):
                    rgb = image.pixel(w, h)
                    if qRed(rgb) != qBlue(rgb):
                        f.write(str(1) + ' ')
                    else:
                        f.write(str(0) + ' ')
                f.write('\n')

        if self.heavisideNormButton.isChecked() == True:
            print('-101')
            image = QImage(self.imageLabel.pixmap())

            contourList = []
            contourListNext = []
            tempList = []
            heavisideMap = np.zeros((image.width(), image.height()), dtype='int8') 
            regionMap = np.zeros((image.width(), image.height()), dtype='int8') 

            for h in range(image.height()):
                for w in range(image.width()):
                    rgb = image.pixel(w, h)
                    if qRed(rgb) != qBlue(rgb):
                        contourList.append(QPoint(w, h))
                        regionMap[w][h] = -1 

            tempList.append(QPoint(0,0))

            while tempList:
                point = tempList.pop()
                print(len(tempList))

                if point.x() < 0 or point.x() >= image.width() or point.y() < 0 or point.y() >= image.height():
                    continue

                if regionMap[point.x()][point.y()] == 0: 
                    regionMap[point.x()][point.y()] = 1
                    tempList.append(QPoint(point.x() + 1, point.y()))
                    tempList.append(QPoint(point.x(), point.y() + 1))
                    tempList.append(QPoint(point.x() - 1, point.y()))
                    tempList.append(QPoint(point.x(), point.y() - 1))


            print('finish region grow')
                    
            for p in contourList:
                regionMap[p.x()][p.y()] = 1

            for h in range(image.height()):
                for w in range(image.width()):
                    if regionMap[w][h] == 0:
                        regionMap[w][h] = -1

            for p in contourList:
                regionMap[p.x()][p.y()] = 0

            for h in range(image.height()):
                for w in range(image.width()):
                    f.write(str(regionMap[w][h]) + ' ')
                f.write('\n')

        f.close()                    
        print('Heaviside function saved')


def main():
    app = QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

