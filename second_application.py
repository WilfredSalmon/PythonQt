from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

class Main_Window(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("A different window!")
        
        self.button = QPushButton("Press Me!")
        self.button.setCheckable(True)
        self.button.clicked.connect(self.button_pressed)
        self.button.clicked.connect(self.print_button_state)
        self.button.released.connect(self.button_released)

        self.setCentralWidget(self.button)

    def button_released(self):
        print("button released, now", "pressed" if self.button.isChecked() else "not pressed")

    def button_pressed(self):
        print("button pressed!")
        self.button.setEnabled(False)
        self.button.setText("Pressed!")
        self.setWindowTitle("Now this app is boring")

    def print_button_state(self, checked):
        print("Button is:", "pressed" if checked else "not pressed")

app = QApplication([])

window = Main_Window()
window.show()
app.exec()