import sys
import numpy as np
from PyQt5.QtWidgets import QToolButton, QFileDialog, QLabel,  QLineEdit, QComboBox, QSizePolicy, QTableWidget, QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon, QFont
import csv
import datetime
from PyQt5.QtCore import pyqtSlot
from functionpool import savedPara
now = datetime.datetime.now()


class MainGui(QMainWindow):
    """This is the main window."""
    def __init__(self):
        super(MainGui, self).__init__()
        self.font = QFont('Sans Serif', 12)
        app.setFont(self.font)
        self.title = 'ODMR Control'
        self.left = 200
        self.top = 50
        self.width = 1000
        self.height = 300
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        buttons = PulseInputButtons()
        self.setCentralWidget(buttons)

        self.show()

class PulseInputButtons(QWidget):
    def __init__(self):
        super(PulseInputButtons, self).__init__()

        self.initpulsebuttons()

    def initpulsebuttons(self):
        grid = QGridLayout()
        MW = self.MWbuttons()
        Laser = self.Laserbuttons()
        DAQ = self.DAQbuttons()
        Save = self.SaveLoadButtons()
        Sequence = self.sequence()

        grid.addWidget(MW,0,0)
        grid.addWidget(Laser, 1,0)
        grid.addWidget(DAQ, 2,0)
        grid.addWidget(Save, 3, 0)
        # grid.addWidget(Sequence, 0,1, 8,8)
        buttonbox = QGroupBox()
        buttonbox.setLayout(grid)
        buttonbox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        Sequence.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QHBoxLayout()
        layout.addWidget(buttonbox)
        layout.addWidget(Sequence)
        self.setLayout(layout)

    def MWbuttons(self):
        MWgroupbox = QGroupBox()
        MWlayout = QGridLayout()
        MWgroupbox.setTitle('MW')
        MWgroupbox.setLayout(MWlayout)

        self.MWPWlabel = QLabel('PW (dbm)')
        self.MWPWbutton = QLineEdit('4.0')

        self.Triggerlabel = QLabel('Trigger Mode')
        self.Triggermode = QComboBox()
        self.Triggermode.addItem('trig')
        self.Triggermode.addItem('cont')
        self.Triggermode.addItem('gate')
        self.Triggermode.activated[str].connect(lambda x: self.setmode(x))

        self.Samplinglabel = QLabel('Sampling Mode')
        self.Samplingmode = QComboBox()
        self.Samplingmode.addItem('RF')
        self.Samplingmode.addItem('NRZ')
        self.Samplingmode.addItem('NRTZ')
        self.Samplingmode.addItem('RTZ')
        self.Samplingmode.activated[str].connect(lambda x: self.setmode(x))

        # self.Routelabel = QLabel('Sampling Route')
        # self.Samplingroute = QLineEdit()

        MWlayout.addWidget(self.MWPWlabel,0,0)
        MWlayout.addWidget(self.MWPWbutton,0,1)

        MWlayout.addWidget(self.Triggerlabel,1,0)
        MWlayout.addWidget(self.Triggermode,1,1)

        MWlayout.addWidget(self.Samplinglabel,2,0)
        MWlayout.addWidget(self.Samplingmode,2,1)

        # MWlayout.addWidget(Routelabel,3,0)
        # MWlayout.addWidget(Samplingroute,3,1)

        return MWgroupbox

    def Laserbuttons(self):
        Laserbox = QGroupBox()
        Laserlayout = QGridLayout()
        Laserbox.setTitle('Laser')
        Laserbox.setLayout(Laserlayout)

        Laserlabel = QLabel('Laser Power (mW)')
        self.Laserbutton = QLineEdit('300')

        Laserlayout.addWidget(Laserlabel, 0,0)
        Laserlayout.addWidget(self.Laserbutton,0,1)
        return Laserbox

    def DAQbuttons(self):
        DAQbox = QGroupBox()
        DAQlayout = QGridLayout()
        DAQbox.setTitle('DAQ')
        DAQbox.setLayout(DAQlayout)

        Samplelabel = QLabel('N Sample')
        self.Samplebutton = QLineEdit('20000')

        Timeoutlabel = QLabel('Timeout (s)')
        self.Timeoutbutton = QLineEdit('60')

        DAQlayout.addWidget(Samplelabel,0,0)
        DAQlayout.addWidget(self.Samplebutton,0,1)
        DAQlayout.addWidget(Timeoutlabel,1,0)
        DAQlayout.addWidget(self.Timeoutbutton,1,1)

        return DAQbox

    def sequence(self):
        self.columns = 3
        self.rows = 5

        sequencelayout = QGridLayout()
        sequencebox = QGroupBox()
        sequencebox.setLayout(sequencelayout)
        table_widget = QTableWidget(self.rows,self.columns)
        sequencelayout.addWidget(table_widget,0,0)

        i=0
        j=0
        while i < self.rows:

            while j < self.columns:
                self.sequence_options_i_j = QComboBox()
                self.sequence_options_i_j.addItem('Option a')
                self.sequence_options_i_j.addItem('Option b')
                table_widget.setCellWidget(i,j,self.sequence_options_i_j)
                j=j+1
                # print(j, 'added column')
            j=0
            i =i+1
            # print(i, 'added row')
        return sequencebox

    def SaveLoadButtons(self):
        SaveLoadbox = QGroupBox()
        SaveLoadlayout = QHBoxLayout()
        SaveLoadbox.setLayout(SaveLoadlayout)

        Savebutton = QPushButton('Save')
        ## by clicking save button, it will also load all the parameters to the device, waiting for execute
        Savebutton.clicked.connect(self.on_click_savetext)
        Savebutton.clicked.connect(self.on_click_loadparameters)
        Loadbutton = QPushButton('Load')
        Loadbutton.clicked.connect(self.on_click_loadtext)

        SaveLoadlayout.addWidget(Savebutton)
        SaveLoadlayout.addWidget(Loadbutton)
        return SaveLoadbox

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        return fileName

    def loadtext(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        fileName = str(fileName)
        print(fileName)
        if not fileName: return
        self.text1, self.text = np.loadtxt(fileName, usecols=(0,1), skiprows=2, unpack=True)
        return self.text1, self.text


    @pyqtSlot()
    def on_click_savetext(self):
        #here we get instrument info for the file saving header

        #this is where we start to format the save files
        datafilename = self.saveFileDialog() #using the file name selected in the file dialog
        file = open(datafilename, 'w', newline='') #begin the writing
        tsv_writer = csv.writer(file, delimiter='\t') #defining the filetype as tab-separated
        tsv_writer.writerow([now.strftime("%Y-%m-%d %H:%M")]) #includes date and time
        tsv_writer.writerow([]) #blank row
        # #writes camera type and grating info
        # # if caps.ulCameraType == 14:
        # #     tsv_writer.writerow(['Camera Type:', 'InGaAs'])
        # # else:
        # #     tsv_writer.writerow(['Camera Type:', 'unknown'])
        # # tsv_writer.writerow(['Camera Serial Number:', iSerialNumber])
        tsv_writer.writerow([])
        tsv_writer.writerow(['MWPW:', float(self.MWPWbutton.text())])
        tsv_writer.writerow(['Trigger mode:', self.Triggermode.currentText()])
        tsv_writer.writerow(['Sampling Mode:', self.Samplingmode.currentText()])
        # tsv_writer.writerow([])
        tsv_writer.writerow(['Laser:', float(self.Laserbutton.text())])
        tsv_writer.writerow([])
        tsv_writer.writerow(['DAQ N sample:', float(self.Samplebutton.text())])
        tsv_writer.writerow(['DAQ Timeout:', float(self.Timeoutbutton.text())])
        tsv_writer.writerow([])
        # TODO: Figure out how to read out table values
        tsv_writer.writerow(['Pulse Sequence', ]) #writes the data
        # datalist = list(self.data)
        # for i in range(len(datalist)):
        #     tsv_writer.writerow([i, self.wavelength[i], datalist[i]])
        file.close()

    def on_click_loadtext(self):
        self.text1, self.text = self.loadtext()

        print('Loaded')

    def on_click_loadparameters(self):
        MW_pw = float(QLineEdit.text(self.MWPWbutton)) ## in dbm
        MW_trig = str(self.Triggermode.currentText())
        MW_samplingmode = str(self.Samplingmode.currentText())
        Laser_pw = float(QLineEdit.text(self.Laserbutton)) ## in mW
        DAQ_Nsample = int(QLineEdit.text(self.Samplebutton))
        DAQ_timeout = float(QLineEdit.text(self.Timeoutbutton)) ## in sec
        loaded = savedPara(MW_pw, MW_trig, MW_samplingmode, Laser_pw, \
                                        DAQ_Nsample, DAQ_timeout)
        loaded.loadParameters()
        loaded.export()
        

    def setmode(self, text):
        if text == 'a':
            self.colormap = self.heat
        if text == 'b':
            self.colormap = self.gray
        if text == 'c':
            self.colormap = self.rainbow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = MainGui()
    sys.exit(app.exec_())


#TODO: add functionality to all buttons
#TODO: make sure we have the layout correct (ask Zeppelin what buttons are missing or are formatted wrong, etc.)
#TODO: set up read/write functionality for all boxes
#TODO: set up save/load for all boxes
#TODO: figure out how to make pulse sequence widget responsive to add/remove column/row

#Button on click function added
#TODO: test in real system
