# -*- coding: utf-8 -*-

#   Copyright (C) 2008-2023 Samuele Carcagno <sam.carcagno@gmail.com>
#   This file is part of pychoacoustics

#    pychoacoustics is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    pychoacoustics is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with pychoacoustics.  If not, see <http://www.gnu.org/licenses/>.

from .pyqtver import*

if pyqtversion == 5:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtCore import QLocale
    from PyQt5.QtWidgets import QCheckBox, QDialog, QDialogButtonBox, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QVBoxLayout, QWidget
    from PyQt5.QtGui import QDesktopServices, QIcon, QIntValidator
    matplotlib_available = True
    try:
        import matplotlib
    except:
        matplotlib_available = False
    try:
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
        matplotlib_available = True
    except:
        matplotlib_available = False
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtCore import QLocale
    from PyQt6.QtWidgets import QCheckBox, QDialog, QDialogButtonBox, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QVBoxLayout, QWidget
    from PyQt6.QtGui import QDesktopServices, QIcon, QIntValidator
    matplotlib_available = True
    try:
        import matplotlib
    except:
        matplotlib_available = False
    try:
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
        matplotlib_available = True
    except:
        matplotlib_available = False

    
import os
from .utils_process_results import*

pandas_available = True
try:
    import pandas
except:
    pandas_available = False
    
if matplotlib_available and pandas_available:
    from .win_categorical_plot import*

class processResultsDialog(QDialog):
    def __init__(self, parent, fName, resformat, paradigm, sep):
        QDialog.__init__(self, parent)
        self.fName = fName
        self.resformat = resformat
      
        self.currLocale = self.parent().prm['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.NumberOption.OmitGroupSeparator | self.currLocale.NumberOption.RejectGroupSeparator)
        self.prm = self.parent().prm

        if paradigm in [self.tr("Transformed Up-Down"), self.tr("Transformed Up-Down Limited"),
                        self.tr("Weighted Up-Down"), self.tr("PEST"), self.tr("Weighted Up-Down Limited")]:
            self.paradigm = "adaptive"
        elif paradigm in [self.tr("Transformed Up-Down Interleaved"), self.tr("Weighted Up-Down Interleaved")]:
            self.paradigm = "adaptive_interleaved"
        elif paradigm == self.tr("Constant 1-Interval 2-Alternatives"):
            self.paradigm = "constant1Interval2Alternatives" 
        elif paradigm == self.tr("Multiple Constants 1-Interval 2-Alternatives"):
            self.paradigm = "multipleConstants1Interval2Alternatives" 
        elif paradigm == self.tr("Constant m-Intervals n-Alternatives"):
            self.paradigm = "constantMIntervalsNAlternatives"
        elif paradigm == self.tr("Multiple Constants m-Intervals n-Alternatives"):
            self.paradigm = "multipleConstantsMIntervalsNAlternatives"
        elif paradigm == self.tr("Constant 1-Pair Same/Different"):
            self.paradigm = "constant1PairSD"
        elif paradigm == self.tr("Multiple Constants 1-Pair Same/Different"):
            self.paradigm = "multipleConstants1PairSD"
        elif paradigm == self.tr("Multiple Constants ABX") and self.resformat == "table": #currently supports only tabular
            self.paradigm = "multipleConstantsABX"
        elif paradigm == self.tr("Multiple Constants Odd One Out") and self.resformat == "table": #currently supports only tabular
            self.paradigm = "multipleConstantsOddOneOut"

        else:
            QMessageBox.warning(self, self.tr("Error"), self.tr("File type or paradigm not supported."))
            return
        
        self.soundPrefWidget = QWidget()
        self.vBoxSizer = QVBoxLayout()
        self.hCsvSeparator =  QHBoxLayout()
        self.plotBox =  QHBoxLayout()
        self.pdfPlotBox =  QHBoxLayout()
        self.hBox1 =  QHBoxLayout()
        self.hBox1_1 =  QHBoxLayout()
        self.hBox2 =  QHBoxLayout()
        self.hBox3 =  QHBoxLayout()
        self.hBox4 =  QHBoxLayout()
        self.hBox5 =  QHBoxLayout()
        self.hBox6 =  QHBoxLayout()
        self.hBox7a =  QHBoxLayout()
        self.hBox7 =  QHBoxLayout()
        self.hBox8 =  QHBoxLayout()
        self.hBox9 =  QHBoxLayout()
    
        n = 0
        self.fileChooseLabel = QLabel(self.tr('Input File(s): '))
        self.hBox1.addWidget(self.fileChooseLabel)
        self.fileTF = QLineEdit(';'.join(self.fName))
        self.hBox1.addWidget(self.fileTF)
        self.chooseFileButton = QPushButton(self.tr("Change File"), self)
        self.chooseFileButton.clicked.connect(self.onClickChooseFileButton)
        self.hBox1.addWidget(self.chooseFileButton)

        n = n +1
        self.outfileChooseLabel = QLabel(self.tr('Output File: '))
        self.hBox1_1.addWidget(self.outfileChooseLabel)
        self.outfileTF = QLineEdit("")
        self.hBox1_1.addWidget(self.outfileTF)
        self.chooseOutFileButton = QPushButton(self.tr("Change File"), self)
        self.chooseOutFileButton.clicked.connect(self.onClickChooseOutFileButton)
        self.hBox1_1.addWidget(self.chooseOutFileButton)

        if self.resformat == 'table':
            self.csvSeparatorLabel = QLabel(self.tr('csv separator:'))
            self.csvSeparatorTF = QLineEdit(sep)#parent.prm['pref']["general"]["csvSeparator"])
            self.hCsvSeparator.addWidget(self.csvSeparatorLabel)
            self.hCsvSeparator.addWidget(self.csvSeparatorTF)
            if self.parent().prm['appData']['plotting_available'] == True:
                self.plotCheckBox = QCheckBox(self.tr('Plot'))
                #self.plotCheckBox.setChecked(True)
                self.plotBox.addWidget(self.plotCheckBox)
                self.pdfPlotCheckBox = QCheckBox(self.tr('PDF Plot'))
                #self.plotCheckBox.setChecked(True)
                self.pdfPlotBox.addWidget(self.pdfPlotCheckBox)

        n = n+1
        self.label1 = QLabel(self.tr('For each condition process: '))
        self.hBox2.addWidget(self.label1)

        n = n+1
        self.processAllBlocksCheckBox = QCheckBox(self.tr('All Blocks'))
        self.processAllBlocksCheckBox.setChecked(True)
        self.hBox3.addWidget(self.processAllBlocksCheckBox)

        n = n+1
        self.label2 = QLabel(self.tr('Last: '))
        self.hBox4.addWidget(self.label2)
        self.lastNBlocksTF = QLineEdit("")
        self.lastNBlocksTF.setValidator(QIntValidator(self))
        self.hBox4.addWidget(self.lastNBlocksTF)
        self.processLastNBlocksCheckBox = QCheckBox(self.tr('Blocks'))
        self.processLastNBlocksCheckBox.setChecked(False)
        self.hBox4.addWidget(self.processLastNBlocksCheckBox)

        n = n+1
        self.processBlocksInRangeCheckBox = QCheckBox(self.tr('Blocks in the following range'))
        self.processBlocksInRangeCheckBox.setChecked(False)
        self.hBox5.addWidget(self.processBlocksInRangeCheckBox)
        n = n+1
        self.label3 = QLabel(self.tr('From: '))
        self.hBox6.addWidget(self.label3)
        self.label4 = QLabel(self.tr('To: '))
        self.fromTF = QLineEdit("")
        self.fromTF.setValidator(QIntValidator(self))
        self.hBox6.addWidget(self.fromTF)
        self.hBox6.addWidget(self.label4)
        self.toTF = QLineEdit("")
        self.toTF.setValidator(QIntValidator(self))
        self.hBox6.addWidget(self.toTF)

        self.processAllBlocksCheckBox.clicked.connect(self.onCheckProcessAllBlocks)
        self.processLastNBlocksCheckBox.clicked.connect(self.onCheckProcessLastNBlocks)
        self.processBlocksInRangeCheckBox.clicked.connect(self.onCheckProcessBlocksInRange)

        if self.paradigm in ["constant1Interval2Alternatives", "multipleConstants1Interval2Alternatives",
                             "constant1PairSD", "multipleConstants1PairSD", "constantABX", "multipleConstantsABX"]:
            self.dpCorrCheckBox = QCheckBox(self.tr('d-prime correction'))
            self.dpCorrCheckBox.setChecked(self.prm['pref']['general']['dprimeCorrection'])
            self.hBox7a.addWidget(self.dpCorrCheckBox)
        n = n+1
        self.openResultsFile = QCheckBox(self.tr('When Finished, Open Results File'))
        self.openResultsFile.setChecked(False)
        self.hBox7.addWidget(self.openResultsFile)

        n = n+1
        self.openResultsFolder = QCheckBox(self.tr('When Finished, Open Results Folder'))
        self.openResultsFolder.setChecked(False)
        self.hBox8.addWidget(self.openResultsFolder)

        n = n+1
        self.runButton = QPushButton(self.tr("Run!"), self)
        self.runButton.clicked.connect(self.onClickRunButton)
        self.runButton.setIcon(QIcon.fromTheme("system-run", QIcon(":/system-run")))
        self.hBox9.addWidget(self.runButton)

        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttonBox.rejected.connect(self.reject)
       
        self.vBoxSizer.addLayout(self.hBox1)
        self.vBoxSizer.addLayout(self.hBox1_1)
        if self.resformat == 'table':
            self.vBoxSizer.addLayout(self.hCsvSeparator)
            if self.parent().prm['appData']['plotting_available'] == True:
                self.vBoxSizer.addLayout(self.plotBox)
                self.vBoxSizer.addLayout(self.pdfPlotBox)
        self.vBoxSizer.addLayout(self.hBox2)
        self.vBoxSizer.addLayout(self.hBox3)
        self.vBoxSizer.addLayout(self.hBox4)
        self.vBoxSizer.addLayout(self.hBox5)
        self.vBoxSizer.addLayout(self.hBox6)
        self.vBoxSizer.addLayout(self.hBox7a)
        self.vBoxSizer.addLayout(self.hBox7)
        self.vBoxSizer.addLayout(self.hBox8)
        self.vBoxSizer.addLayout(self.hBox9)
        self.vBoxSizer.addWidget(buttonBox)
        self.setLayout(self.vBoxSizer)
        self.setWindowTitle(self.tr("Process Results "))
        self.show()

    def onClickRunButton(self):
        fList = self.fileTF.text().split(';')
        if len(fList) == 0:
            QMessageBox.warning(self, self.tr("Error"), self.tr("You must select one or more files to process."))
            return
        for fItem in fList:
            if os.path.exists(fItem) == False:
                QMessageBox.warning(self, self.tr("Error"), self.tr("Selected file does not exist: ")+fItem)
                return

        if self.outfileTF.text() == '': #no output file has been chosen
            if len(fList) == 1: #there is only one file to process, choose name automatically
                if self.resformat == 'linear':
                    self.foutName = fList[0].split('.txt')[0] + self.prm['pref']["general"]["sessSummResFileSuffix"] + ".txt"
                elif self.resformat == 'table':
                    self.foutName = fList[0].split('.csv')[0] + self.prm['pref']["general"]["sessSummResFileSuffix"] + '.csv'
            else: #there is more than one file to be processed, ask user the output file name
                self.onClickChooseOutFileButton()
            #self.outfileTF.setText(self.foutName)
            if len(self.foutName) < 1:
                print('No file was selected for saving the results. Skipping')
                return
        else: #file name has been chosen
            self.foutName = self.outfileTF.text()
                
        if self.processAllBlocksCheckBox.isChecked() == True:
            last = None; block_range = None
        elif self.processLastNBlocksCheckBox.isChecked() == True:
            if int(self.lastNBlocksTF.text()) < 1:
                QMessageBox.warning(self, self.tr("Error"), self.tr("Invalid number of blocks specified."))
                return
            else:   
                last = int(self.lastNBlocksTF.text()); block_range = None
        else:
            if len(self.fromTF.text()) == 0 or len(self.toTF.text()) == 0 or int(self.fromTF.text()) < 1 or int(self.fromTF.text()) > int(self.toTF.text()):
                QMessageBox.warning(self, self.tr("Error"), self.tr("Invalid number of blocks specified."))
                return
            else:
                    last = None; block_range=(int(self.fromTF.text()), int(self.toTF.text()))

        
        if self.resformat == 'linear':
            if self.paradigm == "adaptive":
                processResultsAdaptive(fList, self.foutName, last=last, block_range=block_range)
            elif self.paradigm == "adaptive_interleaved":
                processResultsAdaptiveInterleaved(fList, self.foutName, last=last, block_range=block_range)
            elif self.paradigm == "constantMIntervalsNAlternatives":
                processResultsConstantMIntervalsNAlternatives(fList, self.foutName, last=last, block_range=block_range)
            elif self.paradigm == "multipleConstantsMIntervalsNAlternatives":
                processResultsMultipleConstantsMIntervalsNAlternatives(fList, self.foutName, last=last, block_range=block_range)
            elif self.paradigm == "constant1Interval2Alternatives":
                processResultsConstant1Interval2Alternatives(fList, self.foutName, last=last, block_range=block_range, dprimeCorrection=self.dpCorrCheckBox.isChecked())
            elif self.paradigm == "multipleConstants1Interval2Alternatives":
                processResultsMultipleConstants1Interval2Alternatives(fList, self.foutName, last=last, block_range=block_range, dprimeCorrection=self.dpCorrCheckBox.isChecked())
            elif self.paradigm == "constant1PairSD":
                processResultsConstant1PairSameDifferent(fList, self.foutName, last=last, block_range=block_range, dprimeCorrection=self.dpCorrCheckBox.isChecked())

        elif self.resformat == 'table':
            self.separator = self.csvSeparatorTF.text()
            if self.paradigm == "adaptive":
                procResTableAdaptive(fList, self.foutName, self.separator, last=last, block_range=block_range)
            elif self.paradigm == "adaptive_interleaved":
                procResTableAdaptiveInterleaved(fList, self.foutName, self.separator, last=last, block_range=block_range)
            elif self.paradigm == "constantMIntervalsNAlternatives":
                procResTableConstantMIntNAlt(fList, self.foutName, self.separator, last=last, block_range=block_range)
            elif self.paradigm == "multipleConstantsMIntervalsNAlternatives":
                procResTableMultipleConstantsMIntNAlt(fList, self.foutName, self.separator, last=last, block_range=block_range)
            elif self.paradigm == "constant1Interval2Alternatives":
                procResTableConstant1Int2Alt(fList, self.foutName, self.separator, last=last, block_range=block_range, dprimeCorrection=self.dpCorrCheckBox.isChecked())
            elif self.paradigm == "multipleConstants1Interval2Alternatives":
                procResTableMultipleConstants1Int2Alt(fList, self.foutName, self.separator, last=last, block_range=block_range, dprimeCorrection=self.dpCorrCheckBox.isChecked())
            elif self.paradigm == "constant1PairSD":
                procResTableConstant1PairSameDifferent(fList, self.foutName, self.separator, last=last, block_range=block_range, dprimeCorrection=self.dpCorrCheckBox.isChecked())
            elif self.paradigm == "multipleConstants1PairSD":
                procResTableMultipleConstants1PairSameDifferent(fList, self.foutName, self.separator, last=last, block_range=block_range, dprimeCorrection=self.dpCorrCheckBox.isChecked())
            elif self.paradigm == "multipleConstantsABX":
                procResTableMultipleConstantsABX(fList, self.foutName, self.separator, last=last, block_range=block_range, dprimeCorrection=self.dpCorrCheckBox.isChecked())
            elif self.paradigm == "multipleConstantsOddOneOut":
                procResTableMultipleConstantsOddOneOut(fList, self.foutName, self.separator, last=last, block_range=block_range)


            if self.parent().prm['appData']['plotting_available'] == True and (self.plotCheckBox.isChecked() == True or self.pdfPlotCheckBox.isChecked() == True):
                self.plotResults(self.plotCheckBox.isChecked(), self.pdfPlotCheckBox.isChecked())
          
        if self.openResultsFile.isChecked() == True:
            if self.resformat == 'linear':
                QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(self.foutName))
            elif self.resformat == 'table':
                QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(self.foutName))
        if self.openResultsFolder.isChecked() == True:
            QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(os.path.dirname(self.foutName)))
        
    def onClickChooseFileButton(self):
        self.fName = QFileDialog.getOpenFileNames(self, self.tr("Choose results file to load"), '', self.tr("All Files (*)"))[0]
        self.fileTF.setText(';'.join(self.fName))
        self.outfileTF.setText('') #clear the out file name
        
    def onClickChooseOutFileButton(self):
        if self.resformat == 'linear':
            self.foutName = QFileDialog.getSaveFileName(self, self.tr('Choose file to write results'), "res.txt", self.tr('All Files (*)'))[0]
        elif self.resformat == 'table':
            self.foutName = QFileDialog.getSaveFileName(self, self.tr('Choose file to write results'), "res.csv", self.tr('All Files (*)'))[0]
        self.outfileTF.setText(self.foutName)
        
    def onCheckProcessAllBlocks(self):
        self.processLastNBlocksCheckBox.setChecked(False)
        self.processBlocksInRangeCheckBox.setChecked(False)
        
    def onCheckProcessLastNBlocks(self):
        self.processAllBlocksCheckBox.setChecked(False)
        self.processBlocksInRangeCheckBox.setChecked(False)
        
    def onCheckProcessBlocksInRange(self):
        self.processAllBlocksCheckBox.setChecked(False)
        self.processLastNBlocksCheckBox.setChecked(False)
  
    def plotResults(self, winPlot, pdfPlot):
        if self.prm['appData']['plotting_available']:
            categoricalPlot(self, 'average', self.foutName, winPlot, pdfPlot, self.paradigm, self.separator, None, self.prm)
         
                
