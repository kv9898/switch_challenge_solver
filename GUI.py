import sys
#import os
from PySide6.QtWidgets import (QApplication, QWidget, QMainWindow, QLineEdit, QLabel,
     QHBoxLayout, QVBoxLayout, QGridLayout, QFrame)
from PySide6.QtCore import Qt, QPoint, QMimeData, QEvent
from PySide6.QtGui import QDrag, QPainter, QColor, QIcon

def compute(formula):
    fml, outcome = formula.split("=")
    fml = fml.split("+")

    def IsColor(input_string):
        r = "r" in input_string
        g = "g" in input_string
        b = "b" in input_string
        y = "y" in input_string
        return (r or g or b or y)

    def get_outcome(input_sequence, output_sequence):
        map = {i:n for n,i in enumerate(input_sequence)}
        outcome = [map[o]+1 for o in output_sequence]
        return("".join(str(x) for x in outcome))

    # if outcome and the first element of fml contains any of "y", "b", "g", "red",
    # then we need to execute get_outcome()
    if IsColor(outcome) and IsColor(fml[0]):
        outcome = get_outcome(fml[0], outcome)
        fml = fml[1:]

    #answers = ["".join([str(x) for x in list(a)]) for a in permutations([1, 2, 3, 4])]
    answers = ['1234', '1243', '1324', '1342', '1423', '1432', '2134', '2143', '2314', '2341', 
               '2413', '2431', '3124', '3142', '3214', '3241', '3412', '3421', '4123', '4132', 
               '4213', '4231', '4312', '4321']

    def switch(a, b):
        a = {o:i for o,i in enumerate(a)}
        new = [a[int(n)-1] for n in b]
        return("".join(str(x) for x in new))

    for a in answers:
        # replace x in fmlwith a
        fml_temp = list(map(lambda x: x.replace('x', a), fml))
        out = "1234"
        for i in range(len(fml_temp)):
            out = switch(out, fml_temp[i])
        if out == outcome:
            break
    return(a)

# Base class for draggable shapes
class DraggableShape(QLabel):
    def __init__(self, color, shape, shape_container):
        super().__init__()
        self.color = color
        self.shape = shape
        self.initUI()
        self.shape_container = shape_container

    def initUI(self):
        self.setFixedSize(100, 100)
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.setAlignment(Qt.AlignCenter)
        self.setAcceptDrops(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(self.color))
        painter.setPen(Qt.NoPen)
        self.drawShape(painter)

    def drawShape(self, painter):
        pass  # To be implemented in subclasses

    def mousePressEvent(self, event):
        self.drag_start_position = event.position()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.shape)
            drag.setMimeData(mime_data)

            pixmap = self.grab()
            drag.setPixmap(pixmap)

            drag.exec(Qt.MoveAction)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            # If the mouse is released and the mouse hasn't moved much, 
            # it's likely a single click event
            if abs(event.position().x() - self.drag_start_position.x()) < 5 and \
            abs(event.position().y() - self.drag_start_position.y()) < 5:
                self.singleClickEvent()
        super().mouseReleaseEvent(event)

    def singleClickEvent(self):
        # Handle single click event here
        self.shape_container.moveToLast(self)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()

    def dropEvent(self, event):
        source = event.source()
        if source and isinstance(source, DraggableShape) and source.shape_container==self.shape_container:
            self.swapAttributes(source)
            self.update()  # Update this widget
            source.update()  # Update the source widget as well
            update_sequence()

    def swapAttributes(self, other):
        self.color, other.color = other.color, self.color
        self.shape, other.shape = other.shape, self.shape
        # Reassign the class after the swap so the new shape is drawn
        self.__class__, other.__class__ = other.__class__, self.__class__

# Specific shape implementations
class CrossShape(DraggableShape):
    def __init__(self, color, shape, shape_container):
        super().__init__(color, shape, shape_container)
    def drawShape(self, painter):
        painter.drawRect(30, 10, 40, 80)
        painter.drawRect(10, 30, 80, 40)

class TriangleShape(DraggableShape):
    def __init__(self, color, shape, shape_container):
        super().__init__(color, shape, shape_container)
    def drawShape(self, painter):
        points = [
            QPoint(self.width() // 2, 20),
            QPoint(20, self.height() - 20),
            QPoint(self.width() - 20, self.height() - 20)
        ]
        painter.drawPolygon(points)  # Correctly pass the list of points

class CircleShape(DraggableShape):
    def __init__(self, color, shape, shape_container):
        super().__init__(color, shape, shape_container)
    def drawShape(self, painter):
        painter.drawEllipse(10, 10, 80, 80)

class SquareShape(DraggableShape):
    def __init__(self, color, shape, shape_container):
        super().__init__(color, shape, shape_container)
    def drawShape(self, painter):
        painter.drawRect(10, 10, 80, 80)

# Main widget containing the draggable shapes
class ShapeContainer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.layout = QGridLayout(self)
        shapes = [
            CrossShape("blue", "cross", self),
            TriangleShape("yellow", "triangle", self),
            CircleShape("green", "circle", self),
            SquareShape("red", "square", self)
        ]
        for i, shape in enumerate(shapes):
            self.layout.addWidget(shape, 0, i)
        self.setFixedSize(450, 150)

    def moveToLast(self, shape_widget):
        self.layout.removeWidget(shape_widget)
        self.layout.addWidget(shape_widget, 0, self.layout.columnCount())
        update_sequence()
    def moveToBeginning(self, shape_widget):
        self.layout.removeWidget(shape_widget)
        column_count = self.layout.columnCount()
        widgets = [self.layout.itemAtPosition(0, i).widget() for i in range(column_count) if self.layout.itemAtPosition(0, i) is not None]
        for widget in widgets:
            self.layout.removeWidget(widget)
        for i, widget in enumerate(widgets):
            self.layout.addWidget(widget, 0, i + 1)
        self.layout.addWidget(shape_widget, 0, 0)
        update_sequence()

def update_sequence():
    global input_sequence
    input_sequence = ''
    for i in range(window.input_shapes.layout.columnCount()+1):
        item = window.input_shapes.layout.itemAtPosition(0, i)
        if item is not None:
            widget = item.widget()
            #if isinstance(widget, ShapeContainer):  # assuming ShapeContainer has a color property
            input_sequence += widget.color[0].lower()  # get the first letter of the color
    global output_sequence
    output_sequence = ''
    for i in range(window.output_shapes.layout.columnCount()+1):
        item = window.output_shapes.layout.itemAtPosition(0, i)
        if item is not None:
            widget = item.widget()
            #if isinstance(widget, ShapeContainer):  # assuming ShapeContainer has a color property
            output_sequence += widget.color[0].lower()  # get the first letter of the color  

def clear_lineedits():
    window.line_edit.clear()
    window.result.clear()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Switch Challenge Solver')

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.input_shapes = ShapeContainer()  # assume ShapeContainer is a valid class
        self.layout.addWidget(self.input_shapes)

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText('Enter formula here...')

        self.result = QLabel()
        self.result.setMargin(10)

        hlayout = QHBoxLayout()
        #hlayout.addStretch()
        hlayout.addSpacing(100)
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.line_edit)
        vlayout.addWidget(self.result)
        hlayout.addLayout(vlayout)
        #hlayout.addStretch()
        hlayout.addSpacing(100)

        self.layout.addLayout(hlayout)

        self.output_shapes = ShapeContainer()
        self.layout.addWidget(self.output_shapes)

        #icon_path = os.path.join(os.path.dirname(__file__) , 'favicon.ico') # comment this out if you don't have an icon
        #icon = QIcon(icon_path) # comment this out if you don't have an icon
        #self.setWindowIcon(icon) # comment this out if you don't have an icon

    def keyPressEvent(self, event):
        # clear line edits if c is pressed
        if event.key() == Qt.Key_Tab:
           clear_lineedits()
        elif event.key() == Qt.Key_Return:
            # if the first line edit includes x then execute computation straight away
            if '=' in self.line_edit.text() and not self.line_edit.text().endswith("="):
                self.result.setText(compute(self.line_edit.text()))
            elif self.line_edit.text()=='':
                formula = input_sequence + '+x=' + output_sequence
                self.result.setText(compute(formula))
            else:
                if self.line_edit.text().endswith("="):
                    formula = input_sequence + '+' + self.line_edit.text() + output_sequence
                else:
                    formula = input_sequence + '+' + self.line_edit.text()+ '=' + output_sequence
                self.result.setText(compute(formula))
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    update_sequence()
    sys.exit(app.exec())

#build using pyinstaller --windowed --icon=favicon.ico --add-data="favicon.ico;." GUI.py --onefile
