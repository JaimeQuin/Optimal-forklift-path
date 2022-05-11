# importing modules
from cmath import sqrt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from matplotlib import scale
import numpy as np
import math

array = np.array([[200, 500], [200, 450], [140, 450], [140, 150], [400, 150]])

SCALE = 10000  # 1 : 10.000

# creating class for window
class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        title = "Paint and save Application"

        top = 400
        left = 400
        width = 800
        height = 600

        # setting title of window
        self.setWindowTitle(title)

        # setting geometry
        self.setGeometry(top, left, width, height)

        # creating canvas
        self.image = QImage(self.size(), QImage.Format_RGB32)

        # setting canvas color to white
        self.image.fill(Qt.white)

        # creating menu bar
        mainMenu = self.menuBar()

        # adding file menu in it
        fileMenu = mainMenu.addMenu("File")

        # creating save action
        saveAction = QAction("Save", self)

        # setting save action shortcut
        saveAction.setShortcut("Ctrl + S")

        # adding save action to filemenu
        fileMenu.addAction(saveAction)

        # setting triggered method
        saveAction.triggered.connect(self.save)

        # calling draw_something method
        self.draw_something()

    # paintEvent for creating blank canvas
    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    # this method will draw a line
    def draw_something(self):

        painter = QPainter(self.image)

        painter.setPen(QPen(Qt.green, 5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

        # drawing a line
        _drawCustomLine(painter, _returnListOfPoints())

        # updating it to canvas
        self.update()

    # save method
    def save(self):

        # selecting file path
        filePath, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) "
        )

        # if file path is blank return back
        if filePath == "":
            return

        # saving canvas at desired path
        self.image.save(filePath)


def _returnListOfPoints():
    listOfPoints = list()
    for i in range(len(array)):
        point = QPoint(array[i][0], array[i][1])
        listOfPoints.append(point)
    return listOfPoints


def _drawCustomLine(painter: QPainter, listOfPoints: list):
    for i in range(len(listOfPoints) - 1):
        currentPoint = listOfPoints[i]
        nextPoint = listOfPoints[i + 1]
        painter.drawLine(currentPoint, nextPoint)


def _changePointScale(point: QPoint) -> QPoint:
    point.setX(point.x() * SCALE)
    point.setY(point.y() * SCALE)
    return point


def _calculateDistance(listOfPoints: list):
    for i in range(len(listOfPoints) - 1):
        currentPoint = _changePointScale(listOfPoints[i])
        nextPoint = _changePointScale(listOfPoints[i + 1])
        distance = math.sqrt(
            (nextPoint.x() - currentPoint.x()) ** 2
            + (nextPoint.y() - currentPoint.y()) ** 2
        )

        return distance


def _calculateDistanceInRealScale(listOfPoints: list):
    for i in range(len(listOfPoints) - 1):
        currentPoint = listOfPoints[i]
        nextPoint = listOfPoints[i + 1]
        distance = math.sqrt(
            (nextPoint.x() - currentPoint.x()) ** 2
            + (nextPoint.y() - currentPoint.y()) ** 2
        )

        return distance


# main method
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()

    print("Real distance: " + str(_calculateDistance(_returnListOfPoints())) + " m")

    # looping for window
    sys.exit(app.exec())
