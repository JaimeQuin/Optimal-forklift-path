import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QPropertyAnimation, QPoint, QEasingCurve
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import path

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 600)
        self.child = QWidget(self)
        self.child.setStyleSheet("background-color:red;border-radius:15px;")
        self.child.resize(100, 100)
        self.anim = QPropertyAnimation(self.child, b"pos")
        self.anim.setEasingCurve(QEasingCurve.InOutCubic)
        for i in range(len(path.ARRAY) -1) :
            currentPoint = QPoint(path.ARRAY[i][0], path.ARRAY[i][1])
            nextPoint = QPoint(path.ARRAY[i + 1][0], path.ARRAY[i + 1][1])
            self.anim.setStartValue(currentPoint)
            self.anim.setEndValue(nextPoint)
            self.anim.setDuration(1500)
            self.anim.start()
app = QApplication(sys.argv)
window = Window()
window.show()

# looping for window
sys.exit(app.exec())