from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt

class _Bar(QtWidgets.QWidget):
    clicked_value = QtCore.pyqtSignal(int)

    def __init__(self, min_value : int, max_value: int, initial_value : int, max_boxes : int, padding : int = 5):
        super().__init__()

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding
        )

        self.min_value = min_value
        self.max_value = max_value
        self.current_value = initial_value
        self.max_boxes = max_boxes
        self.padding = padding
    
    def paintEvent(self, _):
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor("blue"))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        rectangle = QtCore.QRect(0, 0, self.width(), self.height())
        painter.fillRect(rectangle, brush)
        
        fraction_filled = (self.current_value - self.min_value)/(self.max_value - self.min_value)
        number_boxes = round(fraction_filled * self.max_boxes)

        rect_height = int((self.height() - (self.max_boxes + 1) * self.padding)/self.max_boxes)
        rect_width = self.width() - 2 * self.padding

        brush.setColor(QtGui.QColor("purple"))

        for i in range(number_boxes):
            top = self.padding + (self.max_boxes - i - 1)*(self.padding + rect_height)
            rectangle = QtCore.QRect(self.padding, top, rect_width, rect_height)
            frac = i/(self.max_boxes - 1)
            brush.setColor(QtGui.QColor(int(255 * (1-frac)), int(255 * frac) ,0))
            painter.fillRect(rectangle, brush)


    def update_value(self, new_value : int):
        self.current_value = new_value
        
        self.update()

    def _calculate_clicked_value(self, e):
        distance = e.position().y() - self.padding
        max_distance = self.height() - 2*self.padding
        fraction = 1 - distance/max_distance

        fraction = max(min(fraction, 1), 0)
        value = round(fraction * (self.max_value - self.min_value) + self.min_value)
        
        self.clicked_value.emit(value)

    def mousePressEvent(self, e):
        self._calculate_clicked_value(e)
    
    def mouseMoveEvent(self, e):
        self._calculate_clicked_value(e)


class Power_Bar(QtWidgets.QWidget):
    def __init__(self, steps = 5):
        super().__init__()

        self._dial = QtWidgets.QDial()
        self._bar = _Bar(self._dial.minimum(), self._dial.maximum(), self._dial.value(), steps)
        
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._bar)
        layout.addWidget(self._dial)
        self.setLayout(layout)

        self._dial.valueChanged.connect(self._bar.update_value)
        self._bar.clicked_value.connect(self._dial.setValue)

        self.setMinimumSize(QtCore.QSize(200,600))

    def __getattr__(self, name):
        if name in self.__dict__:
            return self[name]
        
        try:
            return self._dial.__getattribute__(name)
        except AttributeError:
            raise AttributeError(
                f'{self.__class__.__name__} has no attribute {name}'
            )

app = QtWidgets.QApplication([])
bar = Power_Bar(steps = 10)
bar.setNotchesVisible(True)
bar.show()
app.exec()