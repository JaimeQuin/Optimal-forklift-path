# importing modules
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import numpy as np
import math
import path

#ARRAY = np.array([[340, 780], [340, 660], [190, 660], [190, 350], [380, 350]])
ARRAY = path.ARRAY
CALIBRATION_VELOCITY = 10  # km/h

RATIO = 1
WIDTH = 1246*RATIO  # Pixels
HEIGTH = 884*RATIO # Pixels

X_AXIS_REAL_DISTANCE = 144.5  # m CHECK
X_AXIS = np.array([[0, HEIGTH/2], [WIDTH, HEIGTH/2]])  # X Axis
X_AXIS_REAL_TIME_10_KMH = X_AXIS_REAL_DISTANCE / (CALIBRATION_VELOCITY / 3.6)  # s


Y_AXIS_REAL_DISTANCE = 99.875  # m CHECK
Y_AXIS = np.array([[WIDTH/2, 0], [WIDTH/2, HEIGTH]])  # Y Axis
Y_AXIS_REAL_TIME_10_KMH = Y_AXIS_REAL_DISTANCE / (CALIBRATION_VELOCITY / 3.6)  # s CHECK

SCALE = 427  # 1 : SCALE mm
CONVERSOR_MM_M = 1000
FORKLIFT_VELOCITY = 10  # km/h
#PIXEL_TO_MM_CONVERSOR = 0.264583333
PIXEL_TO_MM_CONVERSOR = 0.27


# creating class for window
class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        title = "Paint and save Application"

        # setting title of window
        self.setWindowTitle(title)

        # setting geometry
        self.setFixedSize(int(WIDTH), int(HEIGTH))
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
        pixmap = QPixmap("layout vacío.png")
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
        qPoint = QPoint(int(array[i][0]), int(array[i][1]))

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
        point.x * SCALE * PIXEL_TO_MM_CONVERSOR * RATIO / CONVERSOR_MM_M, point.y * SCALE * PIXEL_TO_MM_CONVERSOR * RATIO/ CONVERSOR_MM_M
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
def _printCalibrationInfo(
    CALIBRATION_VELOCITY,
    X_AXIS_REAL_DISTANCE,
    X_AXIS_REAL_TIME_10_KMH,
    Y_AXIS_REAL_DISTANCE,
    Y_AXIS_REAL_TIME_10_KMH,
    _returnTimeSpent,
    xCalibrationDistance,
    yCalibrationDistance,
):
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


def _printPathInfo(FORKLIFT_VELOCITY, _returnTimeSpent, distance):
    print("PATH:\n")
    print("Real distance: " + str(distance) + " m")
    print("Velocity: " + str(FORKLIFT_VELOCITY) + " km/h")
    print("Time spent: " + str(_returnTimeSpent(FORKLIFT_VELOCITY, distance)) + " s")


if __name__ == "__main__":
    # Axis calculation
    xAxisQPoints = _returnListOfQPoints(X_AXIS)
    xAxisPoints = _returnListOfPoints(X_AXIS)
    yAxisQPoints = _returnListOfQPoints(Y_AXIS)
    yAxisPoints = _returnListOfPoints(Y_AXIS)

    # Path calculation
    listOfPoints = _returnListOfPoints(ARRAY)
    listOfQPoints = _returnListOfQPoints(ARRAY)

    # App
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    # Real distances of axis to calibrate
    xCalibrationDistance = _calculateDistanceInRealScale(xAxisPoints)
    yCalibrationDistance = _calculateDistanceInRealScale(yAxisPoints)

    # Path distance
    distance = _calculateDistanceInRealScale(listOfPoints)

    # Printing in terminal calibration data
    '''_printCalibrationInfo(
        CALIBRATION_VELOCITY,
        X_AXIS_REAL_DISTANCE,
        X_AXIS_REAL_TIME_10_KMH,
        Y_AXIS_REAL_DISTANCE,
        Y_AXIS_REAL_TIME_10_KMH,
        _returnTimeSpent,
        xCalibrationDistance,
        yCalibrationDistance,
    )'''

    # Printing in terminal path data
    _printPathInfo(FORKLIFT_VELOCITY, _returnTimeSpent, distance)

    # looping for window
    sys.exit(app.exec())
