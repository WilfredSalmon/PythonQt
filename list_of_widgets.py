from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
)

widgets = [
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QWidget
]

class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("A bunch of applications")
        self.setMinimumSize(QSize(1000, 400))

        layout = QVBoxLayout()

        for widget in widgets:
            layout.addWidget(widget())

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

app = QApplication([])
window = Main_Window()
window.show()
app.exec()