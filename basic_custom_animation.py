from PyQt6 import QtWidgets, QtCore

class Negative_Number(QtCore.QObject):
    
    value_changed = QtCore.pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self._value = 0

    @QtCore.pyqtProperty(int)
    def value(self):
        return -self._value
    
    @value.setter
    def value(self, value):
        if value != self._value:
            self.value_changed.emit(value)
        
        self._value = value

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.resize(QtCore.QSize(600, 600))

        self.square = QtWidgets.QWidget(self)
        self.square.setStyleSheet("background-color:red; border-radius:15px;")
        self.square.resize(QtCore.QSize(100, 100))

        self.animation = QtCore.QPropertyAnimation(self.square, b'pos')
        self.animation.setStartValue(QtCore.QPoint(450, 50))
        self.animation.setEndValue(QtCore.QPoint(50, 450))
        self.animation.setDuration(1500)
        self.animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        self.animation_2 = QtCore.QPropertyAnimation(self.square, b'size')
        self.animation_2.setEndValue(QtCore.QSize(300, 100))
        self.animation_2.setDuration(1500)
        self.animation_2.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)

        self.animation_group = QtCore.QSequentialAnimationGroup()
        self.animation_group.addAnimation(self.animation)
        self.animation_group.addAnimation(self.animation_2)
        self.animation_group.start()

neg_num = Negative_Number()
neg_num.value = 1
print(neg_num.value)

app = QtWidgets.QApplication([])
window = Window()
window.show()
app.exec()
