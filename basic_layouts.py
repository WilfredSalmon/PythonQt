from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QStackedLayout, QTabWidget
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPalette, QColor

colours = [
    "red",
    "orange",
    "yellow",
    "green",
    "blue",
    "indigo",
    "violet"
]

class Colour_Block(QWidget):
    def __init__(self, colour):
        super().__init__()
        
        self.setAutoFillBackground(True)
        
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(colour))
        self.setPalette(palette)

class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Basic Layouts")
        self.setMinimumSize(QSize(1000, 600))

        num_colours = len(colours)

        vbox_layouts = [QVBoxLayout() for _ in range(num_colours)]

        cycle_layout = QHBoxLayout()
        cycle_widget = QWidget()
        cycle_widget.setLayout(cycle_layout)
        
        for layout in vbox_layouts:
            cycle_layout.addLayout(layout)

        for i in range(num_colours):
            for j in range(num_colours):
                vbox_layouts[i].addWidget(Colour_Block(colours[(i + j) % num_colours]))
                vbox_layouts[i].setSpacing(10)
                vbox_layouts[i].setContentsMargins(15, 10, 25, 0)

        grid_layout = QGridLayout()
        grid_widget = QWidget()
        grid_widget.setLayout(grid_layout)

        for i in range(num_colours):
            grid_layout.addWidget(Colour_Block(colours[i]), i, i)

        self.outer_layout = QStackedLayout()
        self.layout_index = 0
        self.outer_layout.addWidget(cycle_widget)
        self.outer_layout.addWidget(grid_widget)
        
        container = QWidget()
        container.setLayout(self.outer_layout)
        
        self.setCentralWidget(container)

    def mouseReleaseEvent(self, _):
        self.layout_index ^= 1
        self.outer_layout.setCurrentIndex(self.layout_index)

app = QApplication([])
window = Main_Window()
window.show()
app.exec()