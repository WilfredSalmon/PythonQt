from PyQt6.QtWidgets import QApplication, QWidget

app = QApplication([])

window = QWidget()
window.show()

app.exec() # Starts the event loop