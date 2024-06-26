from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt6.QtCore import QSize

class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Example Application")
        
        button = QPushButton("Press Here.")
        self.setCentralWidget(button)

        self.setMaximumSize(QSize(1000,400))
        self.setMinimumSize(QSize(400,200))

app = QApplication([])

window = Main_Window()
window.show()

app.exec() # Starts the event loop