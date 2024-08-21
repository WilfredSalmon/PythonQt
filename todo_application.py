from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt
from typing import List

tick = QtGui.QImage("tick.png")

class Main_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Todo list")
        
        self.setup_widgets()
        
        self.model = Todo_Model()
        self.todo_view.setModel(self.model)

    def setup_widgets(self):
        self.todo_view = QtWidgets.QListView()

        self.delete_button = QtWidgets.QPushButton("Delete")
        self.complete_button = QtWidgets.QPushButton("Complete")
        
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.complete_button)
        
        self.todo_edit = QtWidgets.QLineEdit()
        self.add_button = QtWidgets.QPushButton("Add Todo")

        self.add_button.pressed.connect(self.add_todo)
        self.delete_button.pressed.connect(self.delete_todo)
        self.complete_button.pressed.connect(self.complete_todo)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.todo_view)
        layout.addLayout(button_layout)
        layout.addWidget(self.todo_edit)
        layout.addWidget(self.add_button)
        
        container = QtWidgets.QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def add_todo(self):
        text = self.todo_edit.text()

        if text:
            self.model.todos.append(Todo(False, text))
            self.model.layoutChanged.emit()
            self.todo_edit.setText("")

    def delete_todo(self):
        indices = self.todo_view.selectedIndexes()

        for index in indices:
            del self.model.todos[index.row()]
        
        self.model.layoutChanged.emit()
        self.todo_view.clearSelection()

    def complete_todo(self):
        indices = self.todo_view.selectedIndexes()

        for index in indices:
            self.model.todos[index.row()].completed = True
            self.model.dataChanged.emit(index, index)
        
        self.todo_view.clearSelection()

class Todo():
    def __init__(self, completed : bool, task : str):
        self.completed = completed
        self.task = task

class Todo_Model(QtCore.QAbstractListModel):
    def __init__(self, todos : List[Todo] = []):
        super().__init__()
        self.todos = todos

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            todo = self.todos[index.row()]
            return todo.task
        
        if role == Qt.ItemDataRole.DecorationRole:
            todo = self.todos[index.row()]
            if todo.completed:
                return tick
        
    def rowCount(self, _):
        return len(self.todos)

app = QtWidgets.QApplication([])
window = Main_Window()
window.show()
app.exec()