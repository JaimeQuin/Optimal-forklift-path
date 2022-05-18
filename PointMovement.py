from PyQt5 import QtCore, QtGui, QtWidgets


class Widget(QtWidgets.QWidget):
    pointChanged = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._point = QtCore.QPoint(0, 0)

        self._animation = QtCore.QPropertyAnimation(
            self,
            duration=1000,
            propertyName=b"point",
            targetObject=self,
            startValue=QtCore.QPoint(0, 0),
            endValue=QtCore.QPoint(0, 0),
            finished=self.calculate_next_point,
        )

        points = (
            QtCore.QPoint(10, 100),
            QtCore.QPoint(400, 300),
            QtCore.QPoint(210, 500),
            QtCore.QPoint(500, 210),
            QtCore.QPoint(500, 200),
            QtCore.QPoint(150, 0),
            QtCore.QPoint(150, 100),
            QtCore.QPoint(50, 300),
            QtCore.QPoint(0, 500),
            QtCore.QPoint(110, 350),
        )
        self._points_iter = iter(points)
        self.calculate_next_point()

    def _update_end_point(self, p):
        s = self._animation.endValue()
        self._animation.setStartValue(s)
        self._animation.setEndValue(p)
        self._animation.start()

    def calculate_next_point(self):
        try:
            p = next(self._points_iter)
        except StopIteration:
            print("finished")
        else:
            self._update_end_point(p)

    @QtCore.pyqtProperty(QtCore.QPoint, notify=pointChanged)
    def point(self):
        return self._point

    @point.setter
    def point(self, p):
        self._point = p
        self.pointChanged.emit(p)
        self.update()

    def paintEvent(self, event):
        radius = 10

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        rect = QtCore.QRect(0, 0, 2 * radius, 2 * radius)
        rect.moveCenter(self.point)

        painter.setBrush(QtGui.QBrush(QtGui.QColor("salmon")))
        painter.drawEllipse(rect)


def main():
    import sys

    app = QtWidgets.QApplication(sys.argv)

    w = Widget()
    w.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
    