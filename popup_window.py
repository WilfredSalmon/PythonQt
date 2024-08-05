from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QDialogButtonBox, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QMessageBox
from PyQt6.QtCore import QSize

class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Testing Pop-Ups")
        self.setMinimumSize(QSize(1000,600))

        layout = QHBoxLayout()

        button = QPushButton("Press for pop-up")
        button.clicked.connect(self.button_pressed)

        other_button = QPushButton("Press for message")
        other_button.clicked.connect(self.other_button_pressed)

        third_button = QPushButton("Third Button")
        third_button.clicked.connect(self.third_button_pressed)

        layout.addWidget(button)
        layout.addWidget(other_button)
        layout.addWidget(third_button)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def button_pressed(self, _):
        print("Clicked")

        dialog = Example_Dialog(self)
        
        if dialog.exec():
            print("Accepted")
        else:
            print("Rejected")
    
    def other_button_pressed(self, _):
        print("Other button clicked!")

        message = QMessageBox(self)
        message.setWindowTitle("Different Example Pop Up")
        message.setText("Are you sure you want to proceed?")
        message.setIcon(QMessageBox.Icon.Critical)
        message.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        button = message.exec()

        if button == QMessageBox.StandardButton.Ok:
            print("OK pressed!")

    def third_button_pressed(self):
        QMessageBox.about(self, "About", "The message")
        QMessageBox.question(self, "Question", "Wherefore art thou Romeo?")
        QMessageBox.critical(self, "Critical", "Computer says no")



class Example_Dialog(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.setWindowTitle("Example Pop Up")

        button_setup = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        button_box = QDialogButtonBox(button_setup)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        label = QLabel("An event happened")

        layout.addWidget(label)
        layout.addWidget(button_box)
        self.setLayout(layout)



app = QApplication([])
window = Main_Window()
window.show()
app.exec()