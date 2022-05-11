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

# array = np.array([[200, 500], [200, 501]])
# array = np.array([[200, 500], [200, 501], [200, 502]])
SCALE = 3  # 1 : SCALE m
FORKLIFT_VELOCITY = 10  # km/h
PIXEL_TO_CM_CONVERSOR = 0.0264583333


# creating class for window
class Window(QMainWindow):
    def __init__(self, listOfQPoints):
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
        self.draw_something(array)

    # paintEvent for creating blank canvas
    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    # this method will draw a line
    def draw_something(self, array: np.ndarray):

        painter = QPainter(self.image)

        painter.setPen(QPen(Qt.green, 5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

        # drawing a line
        _drawCustomLine(painter, listOfQPoints)

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


def _returnListOfPoints(array: np.ndarray):
    listOfQPoints = list()
    listOfPoints = list()
    for i in range(len(array)):
        qPoint = QPoint(array[i][0], array[i][1])
        point = Point(array[i][0], array[i][1])
        listOfQPoints.append(qPoint)
        listOfPoints.append(point)
    return listOfPoints, listOfQPoints


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def _drawCustomLine(painter: QPainter, listOfQPoints: list):
    for i in range(len(listOfQPoints) - 1):
        currentPoint = listOfQPoints[i]
        nextPoint = listOfQPoints[i + 1]
        painter.drawLine(currentPoint, nextPoint)


def _changePointToRealScale(point: Point) -> Point:
    newPoint = Point(
        point.x * SCALE * PIXEL_TO_CM_CONVERSOR, point.y * SCALE * PIXEL_TO_CM_CONVERSOR
    )

    return newPoint


def _calculateDistanceInRealScale(listOfPoints: list):
    distance = 0
    for i in range(len(listOfPoints) - 1):
        currentPoint = _changePointToRealScale(listOfPoints[i])
        nextPoint = _changePointToRealScale(listOfPoints[i + 1])
        if (
            (nextPoint.x - currentPoint.x) ** 2 + (nextPoint.y - currentPoint.y) ** 2
        ) > 0:
            distance = distance + math.sqrt(
                (nextPoint.x - currentPoint.x) ** 2
                + (nextPoint.y - currentPoint.y) ** 2
            )

    return round(distance, 2)


def _calculateDistance(listOfPoints: list):
    distance = 0
    for i in range(len(listOfPoints) - 1):
        currentPoint = listOfPoints[i]
        nextPoint = listOfPoints[i + 1]
        distance = distance + math.sqrt(
            (nextPoint.x() - currentPoint.x()) ** 2
            + (nextPoint.y() - currentPoint.y()) ** 2
        )
    return round(distance, 2)


def _convertToMeterPerSecond(velocityKmH):
    return velocityKmH / 3.6


def _returnTimeSpent(velocityKmH, spaceMeters):
    if velocityKmH is 0:
        return 0
    else:
        return round(spaceMeters / _convertToMeterPerSecond(velocityKmH), 2)


# main method
if __name__ == "__main__":
    listOfPoints, listOfQPoints = _returnListOfPoints(array)

    app = QApplication(sys.argv)
    window = Window(listOfQPoints)
    window.show()

    distance = _calculateDistanceInRealScale(listOfPoints)

    print("Real distance: " + str(distance) + " m")
    print("Velocity: " + str(FORKLIFT_VELOCITY) + " km/h")
    print("Time spent: " + str(_returnTimeSpent(FORKLIFT_VELOCITY, distance)) + " s")

    # looping for window
    sys.exit(app.exec())
