from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt6.QtCore import QSize

window_titles = [
    "Ouch",
    "Oi",
    "That hurt",
    "Stop poking me!",
    "Are you even listening to me?!",
    "That's very rude you know!",
    "I'm warning you",
    "I will break those buttons...",
    "Final chance",
    "No more buttons for you"
]

class Main_Window(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Hello there!")
        self.setMinimumSize(QSize(1000,400))
        
        self.button = QPushButton("Poke")
        self.button_2 = QPushButton("Prod")

        self.presses = 0
        self.button.clicked.connect(self.button_pressed)
        self.button_2.clicked.connect(self.button_pressed)
        self.windowTitleChanged.connect(self.window_title_changed)
        
        self.setCentralWidget(self.button)
        self.setMenuWidget(self.button_2)

    def button_pressed(self):
        self.setWindowTitle(window_titles[self.presses])
        self.presses += 1

    def window_title_changed(self):
        if self.presses == len(window_titles) - 1:
            self.button.setDisabled(True)
            self.button_2.setDisabled(True)
            self.button.setText("Broken")
            self.button_2.setText("Smashed")

app = QApplication([])

window = Main_Window()
window.show()
app.exec()