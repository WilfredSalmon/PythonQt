from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import Qt

class Canvas(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        canvas = QtGui.QPixmap(1000, 600)
        canvas.fill(Qt.GlobalColor.lightGray)
        self.setPixmap(canvas)

        self.last_point = None
        self.pen_colour = QtGui.QColor("black")
        self.pen_size = 5
    
    def set_pen_colour(self, colour):
        self.pen_colour = colour

    def set_pen_size(self, size):
        self.pen_size = size

    def mouseMoveEvent(self, e):
        if self.last_point is None:
            self.last_point = e.position()
            return

        canvas = self.pixmap()
        painter = QtGui.QPainter(canvas)

        pen = painter.pen()
        pen.setColor(self.pen_colour)
        pen.setWidth(self.pen_size)
        painter.setPen(pen)

        painter.drawLine(self.last_point, e.position())
        painter.end()
        
        self.setPixmap(canvas)
        self.last_point = e.position()
    
    def mouseReleaseEvent(self, _):
        self.last_point = None

class Colour_Selector(QtWidgets.QToolButton):
    def __init__(self, colour):
        super().__init__()
        self.setFixedSize(QtCore.QSize(24,24))
        self.colour = QtGui.QColor(colour)
        self.setStyleSheet(f'''
            QToolButton {{
                background-color: {colour};
                border: none
            }}
            QToolButton:checked {{
                border: 3px solid white;
            }}
        ''')
        self.setCheckable(True)

colours = ["black", "red", "green", "blue", "yellow", "orange", "pink", "purple"]

class Main_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Basic Paint!")

        self.canvas = Canvas()
        menu_layout = QtWidgets.QHBoxLayout()

        for colour in colours:
            selector = Colour_Selector(colour)
            menu_layout.addWidget(selector)
            selector.pressed.connect(lambda sel = selector : self.new_colour_selected(sel))

            if colour == "black":
                self.currently_selected = selector
                selector.toggle()

        slider = QtWidgets.QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(1)
        slider.setMaximum(20)
        slider.setSingleStep(1)
        slider.setValue(self.canvas.pen_size)
        slider.valueChanged.connect(self.pen_size_changed)
        slider.setFixedSize(QtCore.QSize(300, 24))

        menu_layout.addWidget(slider)

        vertical_layout = QtWidgets.QVBoxLayout()

        vertical_layout.addWidget(self.canvas)
        vertical_layout.addLayout(menu_layout)
        vertical_layout.setSpacing(10)
        vertical_layout.setContentsMargins(5, 5, 5, 10)

        vertical_container = QtWidgets.QWidget()
        vertical_container.setLayout(vertical_layout)
        
        self.setCentralWidget(vertical_container)

    def new_colour_selected(self, selector):
        self.canvas.set_pen_colour(selector.colour)
        self.currently_selected.toggle()
        self.currently_selected = selector
    
    def pen_size_changed(self, size):
        self.canvas.set_pen_size(size)

app = QtWidgets.QApplication([])
window = Main_Window()
window.show()
app.exec()