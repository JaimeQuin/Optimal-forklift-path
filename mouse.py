import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import numpy as np

position = 0


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.label = QLabel()
        canvas = QPixmap(400, 300)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)

        self.last_x, self.last_y = None, None

    def mouseMoveEvent(self, e):
        if self.last_x is None:  # First event.
            self.last_x = e.x()
            self.last_y = e.y()

            return  # Ignore the first time.

        painter = QPainter(self.label.pixmap())
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
        painter.end()
        self.update()

        # Update the origin for next time.
        self.last_x = e.x()
        self.last_y = e.y()
        qPoint = QPoint(self.last_x, self.last_y)
        lista.append(qPoint)

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None


"""
class MouseTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)

    def initUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle("Mouse Tracker")
        self.label = QLabel(self)
        self.label.resize(200, 40)
        self.show()

    def mouseMoveEvent(self, event):
        self.label.setText("Mouse coords: ( %d : %d )" % (event.x(), event.y()))
"""

app = QApplication(sys.argv)
window = MainWindow()
window.show()
lista = list()

# ex = MouseTracker()

app.exec_()

print(lista)
