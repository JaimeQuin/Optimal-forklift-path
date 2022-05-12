# importing modules
from cmath import sqrt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from matplotlib import scale
import numpy as np
import math

ARRAY = np.array([[340, 780], [340, 660], [190, 660], [190, 350], [380, 350]])

CALIBRATION_VELOCITY = 10  # km/h

X_AXIS_REAL_DISTANCE = 101.6  # m CHECK
X_AXIS = np.array([[0, 480], [1280, 480]])  # X Axis
X_AXIS_REAL_TIME_10_KMH = X_AXIS_REAL_DISTANCE / (CALIBRATION_VELOCITY / 3.6)  # s


Y_AXIS_REAL_DISTANCE = 76.2  # m CHECK
Y_AXIS = np.array([[640, 0], [640, 960]])  # Y Axis
Y_AXIS_REAL_TIME_10_KMH = Y_AXIS_REAL_DISTANCE / (CALIBRATION_VELOCITY / 3.6)  # s CHECK

# array = np.array([[200, 500], [200, 501]])
# array = np.array([[200, 500], [200, 501], [200, 502]])
SCALE = 3  # 1 : SCALE m
FORKLIFT_VELOCITY = 10  # km/h
PIXEL_TO_CM_CONVERSOR = 0.0264583333
WIDTH = 1280
HEIGTH = 960


# creating class for window
class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        title = "Paint and save Application"

        # setting title of window
        self.setWindowTitle(title)

        # setting geometry
        self.setFixedSize(WIDTH, HEIGTH)
        # self.showMaximized()
        # self.showFullScreen()

        # creating canvas
        self.image = QImage(self.size(), QImage.Format_RGB32)

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

    # paintEvent for creating blank canvas
    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        pixmap = QPixmap("snapshot3.png")
        canvasPainter.drawPixmap(self.rect(), pixmap)

        # drawing axis
        canvasPainter.setPen(QPen(Qt.red, 2, Qt.DashDotLine, Qt.RoundCap, Qt.RoundJoin))
        _drawCustomLine(canvasPainter, xAxisQPoints)
        _drawCustomLine(canvasPainter, yAxisQPoints)

        # drawing real path
        canvasPainter.setPen(QPen(Qt.green, 5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        _drawCustomLine(canvasPainter, listOfQPoints)

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


def _returnListOfQPoints(array: np.ndarray):
    listOfQPoints = list()
    for i in range(len(array)):
        qPoint = QPoint(array[i][0], array[i][1])

        listOfQPoints.append(qPoint)

    return listOfQPoints


def _returnListOfPoints(array: np.ndarray):

    listOfPoints = list()
    for i in range(len(array)):

        point = Point(array[i][0], array[i][1])

        listOfPoints.append(point)
    return listOfPoints


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
    xAxisQPoints = _returnListOfQPoints(X_AXIS)
    xAxisPoints = _returnListOfPoints(X_AXIS)
    yAxisQPoints = _returnListOfQPoints(Y_AXIS)
    yAxisPoints = _returnListOfPoints(Y_AXIS)

    listOfPoints = _returnListOfPoints(ARRAY)
    listOfQPoints = _returnListOfQPoints(ARRAY)

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    # Real distances of axis to calibrate
    xCalibrationDistance = _calculateDistanceInRealScale(xAxisPoints)
    yCalibrationDistance = _calculateDistanceInRealScale(yAxisPoints)

    # Path distance
    distance = _calculateDistanceInRealScale(listOfPoints)

    # Printing in terminal calibration data
    print("##########################################################")
    print("CALIBRATION:\n")
    print("X-Axis real distance is: " + str(X_AXIS_REAL_DISTANCE) + " m")
    print("X-Axis calculated distance is: " + str(xCalibrationDistance) + " m\n")
    print("X-Axis real time is: " + str(round(X_AXIS_REAL_TIME_10_KMH, 2)) + " s")
    print(
        "X-Axis calculated time is: "
        + str(_returnTimeSpent(CALIBRATION_VELOCITY, xCalibrationDistance))
        + " s\n"
    )

    print("Y-Axis real distance is: " + str(Y_AXIS_REAL_DISTANCE) + " m")
    print("Y-Axis calculated distance is: " + str(yCalibrationDistance) + " m\n")
    print("Y-Axis real time is: " + str(round(Y_AXIS_REAL_TIME_10_KMH, 2)) + " s")
    print(
        "Y-Axis calculated time is: "
        + str(_returnTimeSpent(CALIBRATION_VELOCITY, yCalibrationDistance))
        + " s\n"
    )
    print("##########################################################")

    # Printing in terminal path data
    print("PATH:\n")
    print("Real distance: " + str(distance) + " m")
    print("Velocity: " + str(FORKLIFT_VELOCITY) + " km/h")
    print("Time spent: " + str(_returnTimeSpent(FORKLIFT_VELOCITY, distance)) + " s")

    # looping for window
    sys.exit(app.exec())
