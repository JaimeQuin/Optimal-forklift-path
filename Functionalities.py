import numpy as np
from PyQt5 import QtCore

import math
import Constants
from PointBean import Point

def returnListOfQPoints(array: np.ndarray):
    listOfQPoints = list()
    for i in range(len(array)):
        qPoint = QtCore.QPoint(int(array[i][0]), int(array[i][1]))

        listOfQPoints.append(qPoint)

    return listOfQPoints

def returnListOfPoints(array: np.ndarray):

    listOfPoints = list()
    for i in range(len(array)):

        point = Point(array[i][0], array[i][1])

        listOfPoints.append(point)
    return listOfPoints

def _changePointToRealScale(point: Point) -> Point:
    newPoint = Point(
        point.x * Constants.SCALE * Constants.PIXEL_TO_MM_CONVERSOR * Constants.RATIO / Constants.CONVERSOR_MM_M, point.y * Constants.SCALE * Constants.PIXEL_TO_MM_CONVERSOR * Constants.RATIO/ Constants.CONVERSOR_MM_M
    )

    return newPoint

def calculateDistanceInRealScale(listOfPoints: list):
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

def _convertToMeterPerSecond(velocityKmH):
    return velocityKmH / 3.6


def _returnTimeSpent(velocityKmH, spaceMeters):
    if velocityKmH is 0:
        return 0
    else:
        return round(spaceMeters / _convertToMeterPerSecond(velocityKmH), 2)

def printPathInfo(FORKLIFT_VELOCITY, distance):
    print("PATH:\n")
    print("Real distance: " + str(distance) + " m")
    print("Velocity: " + str(FORKLIFT_VELOCITY) + " km/h")
    print("Time spent: " + str(_returnTimeSpent(FORKLIFT_VELOCITY, distance)) + " s")

