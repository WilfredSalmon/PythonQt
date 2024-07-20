from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

class Main_Window(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("A different window!")
        
        button = QPushButton("Press Me!")
        button.setCheckable(True)
        button.clicked.connect(self.button_pressed)
        button.clicked.connect(self.print_button_state)

        self.setCentralWidget(button)

    def button_pressed(self):
        print("button pressed!")

    def print_button_state(self, checked):
        print("Button is:", "pressed" if checked else "not pressed")

app = QApplication([])

window = Main_Window()
window.show()
app.exec()