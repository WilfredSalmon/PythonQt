from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QMenu
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Repeat after me")
        self.setMinimumSize(QSize(1000, 400))

        self.label = QLabel()
        self.mouse_label = QLabel()

        self.input = QLineEdit()
        self.input.textChanged.connect(self.label.setText)

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)
        layout.addWidget(self.mouse_label)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def mouseMoveEvent(self, e):
        self.mouse_label.setText("Mouse Moved!")

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            print("left button")
        elif e.button() == Qt.MouseButton.RightButton:
            print("right button")
        elif e.button() == Qt.MouseButton.MiddleButton:
            print("middle button")

        self.mouse_label.setText("Mouse pressed!")
    
    def mouseReleaseEvent(self, e):
        self.mouse_label.setText("Mouse released!")
    
    def mouseDoubleClickEvent(self, e):
        self.mouse_label.setText("Mouse double-clicked!")

    def contextMenuEvent(self, e):
        context = QMenu(self)
        context.addAction(MenuLogger("option 1", self))
        context.addAction(MenuLogger("option 2", self))
        context.addAction(MenuLogger("option 3", self))
        context.exec(e.globalPos())

class MenuLogger(QAction):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.name = name
        self.triggered.connect(self.log_name)

    def log_name(self):
        print(self.name)

app = QApplication([])

window = MainWindow()
window.show()

app.exec()