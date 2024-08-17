from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from enum import Enum

class Animation_Type(Enum):
    SEQUENTIAL = "Sequential"
    PARALLEL = "Parallel"

class Animated_Toggle(QtWidgets.QCheckBox):
    _transparent_pen = QtGui.QPen(Qt.GlobalColor.transparent)
    _light_grey_pen = QtGui.QPen(Qt.GlobalColor.lightGray)
    
    def __init__ (
            self,
            bar_color = Qt.GlobalColor.gray,
            checked_color = QtGui.QColor("#00B0FF"),
            handle_color = Qt.GlobalColor.white,
            pulse_unchecked_color = QtGui.QColor("#44999999"),
            pulse_checked_color = QtGui.QColor("#4400B0EE"),
            handle_animation_curve = QtCore.QEasingCurve.Type.InOutCubic,
            pulse_animation_curve = QtCore.QEasingCurve.Type.OutCubic,
            animation_type : Animation_Type = Animation_Type.SEQUENTIAL
        ):
        super().__init__()

        self._bar_brush = QtGui.QBrush(bar_color)
        self._bar_checked_brush = QtGui.QBrush(QtGui.QColor(checked_color).lighter())
        self._handle_brush = QtGui.QBrush(handle_color)
        self._handle_checked_brush = QtGui.QBrush(checked_color)
        self._pulse_unchecked_brush = QtGui.QBrush(pulse_unchecked_color)
        self._pulse_checked_brush = QtGui.QBrush(pulse_checked_color)

        self.setContentsMargins(8, 0, 8, 0)
        self._handle_position = 0
        self._pulse_radius = 0

        self.handle_animation = QtCore.QPropertyAnimation(self, b"handle_position", self)
        self.handle_animation.setEasingCurve(handle_animation_curve)
        self.handle_animation.setDuration(200)

        self.pulse_animation = QtCore.QPropertyAnimation(self, b"pulse_radius")
        self.pulse_animation.setEasingCurve(pulse_animation_curve)
        self.pulse_animation.setDuration(350)
        self.pulse_animation.setStartValue(0)
        self.pulse_animation.setEndValue(20)
        
        match animation_type:
            case Animation_Type.SEQUENTIAL:
                self.animation_group = QtCore.QSequentialAnimationGroup()
            case Animation_Type.PARALLEL:
                self.animation_group = QtCore.QParallelAnimationGroup()

        self.animation_group = QtCore.QParallelAnimationGroup()
        self.animation_group.addAnimation(self.handle_animation)
        self.animation_group.addAnimation(self.pulse_animation)

        self.stateChanged.connect(self.setup_animation)
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)

    @QtCore.pyqtSlot(int)
    def setup_animation(self, value : int):
        self.animation_group.stop()
        
        if value:
            self.handle_animation.setEndValue(1)
        else:
            self.handle_animation.setEndValue(0)
        
        self.animation_group.start()

    def sizeHint(self):
        return QtCore.QSize(75, 50)

    def hitButton(self, position : QtCore.QPoint):
        return self.contentsRect().contains(position)
    
    @QtCore.pyqtProperty(float)
    def handle_position(self):
        return self._handle_position
    
    @handle_position.setter
    def handle_position(self, position : float):
        self._handle_position = position
        self.update()

    @QtCore.pyqtProperty(float)
    def pulse_radius(self):
        return self._pulse_radius
    
    @pulse_radius.setter
    def pulse_radius(self, radius : float):
        self._pulse_radius = radius
        self.update()

    def paintEvent(self, e : QtGui.QPaintEvent):

        content_rectangle = self.contentsRect()
        handle_radius = round(0.25 * content_rectangle.height())

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        # Don't want shapes to have a border
        painter.setPen(self._transparent_pen)
        bar_rectangle = QtCore.QRectF(
            0, 0,
            content_rectangle.width() - handle_radius,
            0.4 * content_rectangle.height()
        )

        bar_rectangle.moveCenter(content_rectangle.center().toPointF())
        rounding = bar_rectangle.height()/2

        handle_run_length = content_rectangle.width() - 2 * handle_radius
        # First term is a constant shift
        handle_x_position = content_rectangle.x() + handle_radius + handle_run_length * self._handle_position

        if self.pulse_animation.state() == QtCore.QPropertyAnimation.State.Running:
            painter.setBrush(
                self._pulse_checked_brush if self.isChecked()
                else self._pulse_unchecked_brush
            )
            painter.drawEllipse(QtCore.QPointF(handle_x_position, bar_rectangle.center().y()), self._pulse_radius, self._pulse_radius)

        if self.isChecked():
            painter.setBrush(self._bar_checked_brush)
            painter.drawRoundedRect(bar_rectangle, rounding, rounding)
            painter.setBrush(self._handle_checked_brush)
        else:
            painter.setBrush(self._bar_brush)
            painter.drawRoundedRect(bar_rectangle, rounding, rounding)
            painter.setBrush(self._handle_brush)

        painter.drawEllipse(QtCore.QPointF(handle_x_position, bar_rectangle.center().y()), handle_radius, handle_radius)
        painter.end()

class Labelled_Animated_Toggle(QtWidgets.QWidget):
    def __init__ (
            self, 
            handle_animation_curve,
            handle_string : str,
            pulse_animation_curve,
            pulse_string : str,
            animation_type : Animation_Type
        ):
        super().__init__()
        
        animated_toggle = Animated_Toggle(handle_animation_curve = handle_animation_curve, pulse_animation_curve = pulse_animation_curve, animation_type = animation_type)
        
        label_text = f'Handle: {handle_string}\nPulse:    {pulse_string}\nStyle:     {animation_type.value}'
        label = QtWidgets.QLabel(label_text)
        label.setStyleSheet("color : black")

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout.addWidget(animated_toggle)
        layout.addWidget(label)

        self.setLayout(layout)

animation_curves_to_test = {
    "InOutCubic" : QtCore.QEasingCurve.Type.InOutCubic,
    "OutCubic" : QtCore.QEasingCurve.Type.OutCubic,
    "InOutQuad" : QtCore.QEasingCurve.Type.InOutQuad,
}

class Main_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(1000, 600)
        self.setWindowTitle("Custom slider")

        NO_COLS = 7
        row = 0
        col = 0

        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(30, 30, 30, 30)

        for handle_string, handle_animtation in animation_curves_to_test.items():
            for pulse_string, pulse_animation in animation_curves_to_test.items():
                for animation_type in Animation_Type:
                    toggle = Labelled_Animated_Toggle(handle_animtation, handle_string, pulse_animation, pulse_string, animation_type)
                    layout.addWidget(toggle, row, col)

                    col += 1

                    if col == NO_COLS:
                        row += 1
                        col = 0

        container = QtWidgets.QWidget()
        container.setLayout(layout)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(container)

        self.setCentralWidget(scroll)
        self.setStyleSheet("background-color:#D3D3D3")

app = QtWidgets.QApplication([])
window = Main_Window()
window.show()
app.exec()