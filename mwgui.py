import sys

from PyQt5.QtWidgets import QToolButton, QMainWindow, QApplication, QPushButton, QWidget, QSizePolicy, \
    QAction, QTabWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QStackedLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSlot



class MainGui(QMainWindow):
    """This is the main window."""
    def __init__(self):
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        super(MainGui, self).__init__()
        self.font = QFont('Sans Serif', 12)
        app.setFont(self.font)
        self.title = 'AWG control'
        self.left = 200
        self.top = 50
        self.width = 300
        self.height = 300
        self.initUI()
        sys.exit(app.exec_())



    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setCentralWidget(AWGbtns())
        self.show()


class AWGbtns(QWidget):
    def __init__(self):
        super(AWGbtns, self).__init__()
        self.left = 12.5
        self.top = 12.5
        self.width = 275
        self.height = 475
        self.initdropdown()
        grid = QGridLayout()
        grid.addWidget(self.initdropdown(), 0, 0)
        self.setLayout(grid)
        self.rabigui = Rabigui()
        self.ramseygui = Ramseygui()
        self.cpmggui = CPMGgui()
        self.xy8gui = XY8gui()


    def initdropdown(self):
        self.setGeometry(self.left, self.top, self.width, self.height)

        Rabibtn = QPushButton('Rabi', self)
        Rabibtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        Rabibtn.clicked.connect(self.on_click_Rabi)

        Ramseybtn = QPushButton('Ramsey', self)
        Ramseybtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        Ramseybtn.clicked.connect(self.on_click_Ramsey)

        CPMGbtn = QPushButton('CPMG', self)
        CPMGbtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        CPMGbtn.clicked.connect(self.on_click_CPMG)

        XY8btn = QPushButton('XY8', self)
        XY8btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        XY8btn.clicked.connect(self.on_click_XY8)

        spectbox = QGroupBox()
        spectvbox = QVBoxLayout()
        vbox1 = QVBoxLayout()
        spectvbox.addWidget(Rabibtn)
        spectvbox.addWidget(Ramseybtn)
        spectvbox.addWidget(CPMGbtn)
        spectvbox.addWidget(XY8btn)
        spectvbox.addLayout(vbox1)
        spectbox.setLayout(spectvbox)

        return spectbox


    @pyqtSlot()
    def on_click_Rabi(self):
        self.rabigui.show()

    def on_click_Ramsey(self):
        self.ramseygui.show()

    def on_click_CPMG(self):
        self.cpmggui.show()
    #
    def on_click_XY8(self):
        self.xy8gui.show()

class Rabigui(QMainWindow):
    def __init__(self):
        # app = QApplication(sys.argv)
        # app.setStyle('Fusion')
        super(Rabigui, self).__init__()
        self.title = 'Rabi settings'
        self.left = 50
        self.top = 50
        
        rabiLayout = self.create_Rabi_seq()
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(rabiLayout)
        self.setCentralWidget(self.centralWidget)

    def create_Rabi_seq(self):
        Rabilayout = QGridLayout()

        RabiStart = QLabel('MW duration initial (ns)')
        self.RabiStartbutton = QLineEdit('5')

        RabiSteps = QLabel('N steps')
        self.RabiStepsbutton = QLineEdit('512')

        RabiResolution = QLabel('step length (ns)')
        self.RabiResolutionbutton = QLineEdit('3')

        self.RabiLoadbutton = QPushButton('Load')
        #RabiLoadbutton.clicked.connect(self.on_click_savetext)

        Rabilayout.addWidget(RabiStart, 0,0)
        Rabilayout.addWidget(self.RabiStartbutton,0,1)
        Rabilayout.addWidget(RabiSteps, 1,0)
        Rabilayout.addWidget(self.RabiStepsbutton,1,1)
        Rabilayout.addWidget(RabiResolution, 2,0)
        Rabilayout.addWidget(self.RabiResolutionbutton,2,1)
        Rabilayout.addWidget(self.RabiLoadbutton, 3,0)

        self.Rabi_widget = QWidget()
        self.Rabi_widget.setLayout(Rabilayout)

        return Rabilayout


class Ramseygui(QMainWindow):
    def __init__(self):
        # app = QApplication(sys.argv)
        # app.setStyle('Fusion')
        super(Ramseygui, self).__init__()
        self.title = 'Ramsey settings'
        self.left = 50
        self.top = 50
        
        ramseyLayout = self.create_Ramsey_seq()
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(ramseyLayout)
        self.setCentralWidget(self.centralWidget)

    def create_Ramsey_seq(self):
        Ramseylayout = QGridLayout()

        T90label = QLabel('T90 (ns)')
        self.T90button = QLineEdit('50')

        RamseyStart = QLabel('tau duration initial (ns)')
        self.RamseyStartbutton = QLineEdit('5')

        RamseySteps = QLabel('N steps')
        self.RamseyStepsbutton = QLineEdit('512')

        RamseyResolution = QLabel('tau step length (ns)')
        self.RamseyResolutionbutton = QLineEdit('3')

        self.RamseyLoadbutton = QPushButton('Load')
        #RamseyLoadbutton.clicked.connect(self.on_click_savetext)

        
        Ramseylayout.addWidget(T90label, 0,0)
        Ramseylayout.addWidget(self.T90button,0,1)
        Ramseylayout.addWidget(RamseyStart, 1,0)
        Ramseylayout.addWidget(self.RamseyStartbutton,1,1)
        Ramseylayout.addWidget(RamseySteps, 2,0)
        Ramseylayout.addWidget(self.RamseyStepsbutton,2,1)
        Ramseylayout.addWidget(RamseyResolution, 3,0)
        Ramseylayout.addWidget(self.RamseyResolutionbutton,3,1)
        Ramseylayout.addWidget(self.RamseyLoadbutton, 4,0)
    

        self.Ramsey_widget = QWidget()
        self.Ramsey_widget.setLayout(Ramseylayout)

        return Ramseylayout


class CPMGgui(QMainWindow):
    def __init__(self):
        # app = QApplication(sys.argv)
        # app.setStyle('Fusion')
        super(CPMGgui, self).__init__()
        self.title = 'CPMG settings'
        self.left = 50
        self.top = 50
        
        CPMGLayout = self.create_CPMG_seq()
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(CPMGLayout)
        self.setCentralWidget(self.centralWidget)

    def create_CPMG_seq(self):
        CPMGlayout = QGridLayout()

        T90label = QLabel('T90 (ns)')
        self.T90button = QLineEdit('50')

        seqNumlabel = QLabel('N pi pulse')
        self.seqNumbutton = QLineEdit('1')

        CPMGStart = QLabel('tau duration initial (ns)')
        self.CPMGStartbutton = QLineEdit('75')

        CPMGSteps = QLabel('N steps')
        self.CPMGStepsbutton = QLineEdit('512')

        CPMGResolution = QLabel('tau step length (ns)')
        self.CPMGResolutionbutton = QLineEdit('3')

        self.CPMGLoadbutton = QPushButton('Load')
        #CPMGLoadbutton.clicked.connect(self.on_click_savetext)

        
        CPMGlayout.addWidget(T90label, 0,0)
        CPMGlayout.addWidget(self.T90button,0,1)
        CPMGlayout.addWidget(seqNumlabel, 1,0)
        CPMGlayout.addWidget(self.seqNumbutton, 1,1)
        CPMGlayout.addWidget(self.T90button,2,1)
        CPMGlayout.addWidget(CPMGStart, 2,0)
        CPMGlayout.addWidget(self.CPMGStartbutton,2,1)
        CPMGlayout.addWidget(CPMGSteps, 3,0)
        CPMGlayout.addWidget(self.CPMGStepsbutton,3,1)
        CPMGlayout.addWidget(CPMGResolution, 4,0)
        CPMGlayout.addWidget(self.CPMGResolutionbutton,4,1)
        CPMGlayout.addWidget(self.CPMGLoadbutton, 5,0)
    

        self.CPMG_widget = QWidget()
        self.CPMG_widget.setLayout(CPMGlayout)

        return CPMGlayout


class XY8gui(QMainWindow):
    def __init__(self):
        # app = QApplication(sys.argv)
        # app.setStyle('Fusion')
        super(XY8gui, self).__init__()
        self.title = 'XY8 settings'
        self.left = 50
        self.top = 50
        
        XY8Layout = self.create_XY8_seq()
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(XY8Layout)
        self.setCentralWidget(self.centralWidget)

    def create_XY8_seq(self):
        XY8layout = QGridLayout()

        T90label = QLabel('T90 (ns)')
        self.T90button = QLineEdit('50')

        seqNumlabel = QLabel('N Repeats')
        self.seqNumbutton = QLineEdit('1')

        XY8Start = QLabel('tau duration initial (ns)')
        self.XY8Startbutton = QLineEdit('75')

        XY8Steps = QLabel('N steps')
        self.XY8Stepsbutton = QLineEdit('512')

        XY8Resolution = QLabel('tau step length (ns)')
        self.XY8Resolutionbutton = QLineEdit('3')

        self.XY8Loadbutton = QPushButton('Load')
        #XY8Loadbutton.clicked.connect(self.on_click_savetext)

        
        XY8layout.addWidget(T90label, 0,0)
        XY8layout.addWidget(self.T90button,0,1)
        XY8layout.addWidget(seqNumlabel, 1,0)
        XY8layout.addWidget(self.seqNumbutton, 1,1)
        XY8layout.addWidget(self.T90button,2,1)
        XY8layout.addWidget(XY8Start, 2,0)
        XY8layout.addWidget(self.XY8Startbutton,2,1)
        XY8layout.addWidget(XY8Steps, 3,0)
        XY8layout.addWidget(self.XY8Stepsbutton,3,1)
        XY8layout.addWidget(XY8Resolution, 4,0)
        XY8layout.addWidget(self.XY8Resolutionbutton,4,1)
        XY8layout.addWidget(self.XY8Loadbutton, 5,0)
    

        self.XY8_widget = QWidget()
        self.XY8_widget.setLayout(XY8layout)

        return XY8layout
    


MainGui()