from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QCheckBox, QWidget, QVBoxLayout, QComboBox, QListWidget, QLineEdit
from PyQt6.QtGui import QPixmap

class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Widget experimentation")
        self.setMinimumSize(QSize(1000, 400))
    
    def mousePressEvent(self, e):
        layout = QVBoxLayout()
       
        layout.addWidget(self.get_label())
        layout.addWidget(self.get_checkbox())
        layout.addWidget(self.get_dropdown())
        layout.addWidget(self.get_scroll_dropdown())
        layout.addWidget(self.get_line_edit())

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def get_label(self):
        # label = QLabel("Initial Label")
        # font = label.font()
        # font.setPointSize(30)
        # label.setFont(font)

        label = QLabel()
        label.setPixmap(QPixmap("gigachad.jpg"))
        label.setScaledContents(True)

        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        return label

    def get_checkbox(self):
        checkbox = QCheckBox("Checkbox")
        checkbox.setCheckState(Qt.CheckState.PartiallyChecked)
        return checkbox
    
    def get_dropdown(self):
        combo_box = QComboBox()

        combo_box.addItems(["option 1", "option 2", "option 3"])
        combo_box.currentIndexChanged.connect(self.index_changed)
        combo_box.currentTextChanged.connect(self.option_changed)

        combo_box.setEditable(True)
        combo_box.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        combo_box.setMaxCount(5)

        return combo_box
    
    def get_scroll_dropdown(self):
        scroll_dropdown = QListWidget()

        scroll_dropdown.addItems(["A", "B", "C"])

        scroll_dropdown.currentItemChanged.connect(self.scroll_item_changed)
        scroll_dropdown.currentTextChanged.connect(self.text_changed)

        return scroll_dropdown
    
    def get_line_edit(self):
        line_edit = QLineEdit()

        line_edit.setMaxLength(6)
        line_edit.setPlaceholderText("Write in me!")

        line_edit.returnPressed.connect(lambda : print("Pressed enter!"))
        line_edit.selectionChanged.connect(lambda : print("selection changed"))
        line_edit.textChanged.connect(lambda x : print(f'text changed to {x}'))
        line_edit.textEdited.connect(lambda x : print(f'Text edited to {x}'))

        line_edit.setInputMask("Aa90")

        return line_edit

    def scroll_item_changed(self, item):
        print(f'via item: {item.text()}')

    def text_changed(self, text):
        print(f'via text: {text}')

    def index_changed(self, index):
        print(f'new index is {index}')
    
    def option_changed(self, text):
        print(f'new option is {text}')
    
app = QApplication([])
window = Main_Window()
window.show()
app.exec()