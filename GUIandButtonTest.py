import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 button'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        layout = QGridLayout()
        self.setLayout(layout)
        
        label = QLabel('number')
        self.Wbutton = QLineEdit('0')
        layout.addWidget(label, 0,0)
        layout.addWidget(self.Wbutton,0,1)

        
        button = QPushButton('* 2', self)
        button.setToolTip('This is an example button')
        button.clicked.connect(self.on_click)
        layout.addWidget(button,1,0)


        
        
        self.show()

    def on_click(self):
        raw_input = QLineEdit.text(self.Wbutton)
        print(type(raw_input))
        value = 2*float(raw_input)
        print(value)
        return value

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
