# -*- coding: utf-8 -*-

#   Copyright (C) 2008-2013 Samuele Carcagno <sam.carcagno@gmail.com>
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

from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, unicode_literals
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QLocale
import os
from .utils_process_results import*
matplotlib_available = True
pandas_available = True
try:
    import matplotlib
except:
    matplotlib_available = False

try:
    import pandas
except:
    pandas_available = False
    
if matplotlib_available and pandas_available:
    from .win_categorical_plot import*

class processResultsDialog(QtGui.QDialog):
    def __init__(self, parent, paradigm, resformat):
        QtGui.QDialog.__init__(self, parent)
        self.paradigm = paradigm
        self.resformat = resformat
        if paradigm == "adaptive":
            paradigmName = self.tr("Adaptive")
        elif paradigm == "adaptive_interleaved":
            paradigmName = self.tr("Adaptive Interleaved")
        elif paradigm == "constant1Interval2Alternatives":
            paradigmName = self.tr("Constant 1-Interval 2-Alternatives")
        elif paradigm == "multipleConstants1Interval2Alternatives":
            paradigmName = self.tr("Multiple Constants 1-Interval 2-Alternatives")
        elif paradigm == "constantMIntervalsNAlternatives":
            paradigmName = self.tr("Constant m-Intervals n-Alternatives")
        elif paradigm == "multipleConstantsMIntervalsNAlternatives":
            paradigmName = self.tr("Multiple Constants m-Intervals n-Alternatives")
        elif paradigm == "constant1PairSD":
            paradigmName = self.tr("Constant 1-Pair Same/Different")
      
        self.currLocale = self.parent().prm['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.OmitGroupSeparator | self.currLocale.RejectGroupSeparator)
        self.prm = self.parent().prm
        
        self.soundPrefWidget = QtGui.QWidget()
        self.vBoxSizer = QtGui.QVBoxLayout()
        self.hCsvSeparator =  QtGui.QHBoxLayout()
        self.plotBox =  QtGui.QHBoxLayout()
        self.pdfPlotBox =  QtGui.QHBoxLayout()
        self.hBox1 =  QtGui.QHBoxLayout()
        self.hBox1_1 =  QtGui.QHBoxLayout()
        self.hBox2 =  QtGui.QHBoxLayout()
        self.hBox3 =  QtGui.QHBoxLayout()
        self.hBox4 =  QtGui.QHBoxLayout()
        self.hBox5 =  QtGui.QHBoxLayout()
        self.hBox6 =  QtGui.QHBoxLayout()
        self.hBox7a =  QtGui.QHBoxLayout()
        self.hBox7 =  QtGui.QHBoxLayout()
        self.hBox8 =  QtGui.QHBoxLayout()
        self.hBox9 =  QtGui.QHBoxLayout()
    
        n = 0
        self.fileChooseLabel = QtGui.QLabel(self.tr('Input File(s): '))
        self.hBox1.addWidget(self.fileChooseLabel)
        self.fileTF = QtGui.QLineEdit("")
        self.hBox1.addWidget(self.fileTF)
        self.chooseFileButton = QtGui.QPushButton(self.tr("Choose File"), self)
        QtCore.QObject.connect(self.chooseFileButton,
                               QtCore.SIGNAL('clicked()'), self.onClickChooseFileButton)
        self.hBox1.addWidget(self.chooseFileButton)

        n = n +1
        self.outfileChooseLabel = QtGui.QLabel(self.tr('Output File: '))
        self.hBox1_1.addWidget(self.outfileChooseLabel)
        self.outfileTF = QtGui.QLineEdit("")
        self.hBox1_1.addWidget(self.outfileTF)
        self.chooseOutFileButton = QtGui.QPushButton(self.tr("Choose File"), self)
        QtCore.QObject.connect(self.chooseOutFileButton,
                               QtCore.SIGNAL('clicked()'), self.onClickChooseOutFileButton)
        self.hBox1_1.addWidget(self.chooseOutFileButton)

        if self.resformat == 'table':
            self.csvSeparatorLabel = QtGui.QLabel(self.tr('csv separator:'))
            self.csvSeparatorTF = QtGui.QLineEdit(parent.prm['pref']["general"]["csvSeparator"])
            self.hCsvSeparator.addWidget(self.csvSeparatorLabel)
            self.hCsvSeparator.addWidget(self.csvSeparatorTF)
            if self.parent().prm['appData']['plotting_available'] == True:
                self.plotCheckBox = QtGui.QCheckBox(self.tr('Plot'))
                #self.plotCheckBox.setChecked(True)
                self.plotBox.addWidget(self.plotCheckBox)
                self.pdfPlotCheckBox = QtGui.QCheckBox(self.tr('PDF Plot'))
                #self.plotCheckBox.setChecked(True)
                self.pdfPlotBox.addWidget(self.pdfPlotCheckBox)

        n = n+1
        self.label1 = QtGui.QLabel(self.tr('For each condition process: '))
        self.hBox2.addWidget(self.label1)

        n = n+1
        self.processAllBlocksCheckBox = QtGui.QCheckBox(self.tr('All Blocks'))
        self.processAllBlocksCheckBox.setChecked(True)
        self.hBox3.addWidget(self.processAllBlocksCheckBox)

        n = n+1
        self.label2 = QtGui.QLabel(self.tr('Last: '))
        self.hBox4.addWidget(self.label2)
        self.lastNBlocksTF = QtGui.QLineEdit("")
        self.lastNBlocksTF.setValidator(QtGui.QIntValidator(self))
        self.hBox4.addWidget(self.lastNBlocksTF)
        self.processLastNBlocksCheckBox = QtGui.QCheckBox(self.tr('Blocks'))
        self.processLastNBlocksCheckBox.setChecked(False)
        self.hBox4.addWidget(self.processLastNBlocksCheckBox)

        n = n+1
        self.processBlocksInRangeCheckBox = QtGui.QCheckBox(self.tr('Blocks in the following range'))
        self.processBlocksInRangeCheckBox.setChecked(False)
        self.hBox5.addWidget(self.processBlocksInRangeCheckBox)
        n = n+1
        self.label3 = QtGui.QLabel(self.tr('From: '))
        self.hBox6.addWidget(self.label3)
        self.label4 = QtGui.QLabel(self.tr('To: '))
        self.fromTF = QtGui.QLineEdit("")
        self.fromTF.setValidator(QtGui.QIntValidator(self))
        self.hBox6.addWidget(self.fromTF)
        self.hBox6.addWidget(self.label4)
        self.toTF = QtGui.QLineEdit("")
        self.toTF.setValidator(QtGui.QIntValidator(self))
        self.hBox6.addWidget(self.toTF)

        self.connect(self.processAllBlocksCheckBox, QtCore.SIGNAL("clicked()"), self.onCheckProcessAllBlocks)
        self.connect(self.processLastNBlocksCheckBox, QtCore.SIGNAL("clicked()"), self.onCheckProcessLastNBlocks)
        self.connect(self.processBlocksInRangeCheckBox, QtCore.SIGNAL("clicked()"), self.onCheckProcessBlocksInRange)

        if self.paradigm in ["constant1Interval2Alternatives", "multipleConstants1Interval2Alternatives", "constant1PairSD"]:
            self.dpCorrCheckBox = QtGui.QCheckBox(self.tr('d-prime correction'))
            self.dpCorrCheckBox.setChecked(self.prm['pref']['general']['dprimeCorrection'])
            self.hBox7a.addWidget(self.dpCorrCheckBox)
        n = n+1
        self.openResultsFile = QtGui.QCheckBox(self.tr('When Finished, Open Results File'))
        self.openResultsFile.setChecked(False)
        self.hBox7.addWidget(self.openResultsFile)

        n = n+1
        self.openResultsFolder = QtGui.QCheckBox(self.tr('When Finished, Open Results Folder'))
        self.openResultsFolder.setChecked(False)
        self.hBox8.addWidget(self.openResultsFolder)

        n = n+1
        self.runButton = QtGui.QPushButton(self.tr("Run!"), self)
        QtCore.QObject.connect(self.runButton,
                               QtCore.SIGNAL('clicked()'), self.onClickRunButton)
        self.runButton.setIcon(QtGui.QIcon.fromTheme("system-run", QtGui.QIcon(":/system-run")))
        self.hBox9.addWidget(self.runButton)

        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                           QtGui.QDialogButtonBox.Cancel)
        
        self.connect(buttonBox, QtCore.SIGNAL("accepted()"),
                     self, QtCore.SLOT("accept()"))
        self.connect(buttonBox, QtCore.SIGNAL("rejected()"),
                     self, QtCore.SLOT("reject()"))
        
       
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
        self.setWindowTitle(self.tr("Process Results ") + paradigmName)
        self.show()

    def onClickRunButton(self):
        fList = self.fileTF.text().split(';')
        if len(fList) == 0:
            QtGui.QMessageBox.warning(self, self.tr("Error"), self.tr("You must select one or more files to process."))
            return
        for fItem in fList:
            if os.path.exists(fItem) == False:
                QtGui.QMessageBox.warning(self, self.tr("Error"), self.tr("Selected file does not exist: ")+fItem)
                return

        if self.outfileTF.text() == '': #no output file has been chosen
            if len(fList) == 1: #there is only one file to process, choose name automatically
                if self.resformat == 'linear':
                    self.foutName = fList[0].split('.txt')[0]+'_res.txt'
                elif self.resformat == 'table':
                    self.foutName = fList[0].split('.csv')[0]+'_processed.csv'
            else: #there is more than one file to be processed, ask user the output file name
                self.onClickChooseOutFileButton()
            #self.outfileTF.setText(self.foutName)
            if len(self.foutName) < 1:
                print('No file was selected for saving the results. Skipping')
                return
        else: #file name has been choser
            self.foutName = self.outfileTF.text()
                
        if self.processAllBlocksCheckBox.isChecked() == True:
            last = None; block_range = None
        elif self.processLastNBlocksCheckBox.isChecked() == True:
            if int(self.lastNBlocksTF.text()) < 1:
                QtGui.QMessageBox.warning(self, self.tr("Error"), self.tr("Invalid number of blocks specified."))
                return
            else:   
                last = int(self.lastNBlocksTF.text()); block_range = None
        else:
            if len(self.fromTF.text()) == 0 or len(self.toTF.text()) == 0 or int(self.fromTF.text()) < 1 or int(self.fromTF.text()) > int(self.toTF.text()):
                QtGui.QMessageBox.warning(self, self.tr("Error"), self.tr("Invalid number of blocks specified."))
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
                processResultsTableAdaptive(fList, self.foutName, self.separator, last=last, block_range=block_range)
            elif self.paradigm == "adaptive_interleaved":
                processResultsTableAdaptiveInterleaved(fList, self.foutName, self.separator, last=last, block_range=block_range)
            elif self.paradigm == "constantMIntervalsNAlternatives":
                processResultsTableConstantMIntNAlt(fList, self.foutName, self.separator, last=last, block_range=block_range)
            elif self.paradigm == "multipleConstantsMIntervalsNAlternatives":
                processResultsTableMultipleConstantsMIntNAlt(fList, self.foutName, self.separator, last=last, block_range=block_range)
            elif self.paradigm == "constant1Interval2Alternatives":
                processResultsTableConstant1Int2Alt(fList, self.foutName, self.separator, last=last, block_range=block_range, dprimeCorrection=self.dpCorrCheckBox.isChecked())
            elif self.paradigm == "multipleConstants1Interval2Alternatives":
                processResultsTableMultipleConstants1Int2Alt(fList, self.foutName, self.separator, last=last, block_range=block_range, dprimeCorrection=self.dpCorrCheckBox.isChecked())
            elif self.paradigm == "constant1PairSD":
                processResultsTableConstant1PairSameDifferent(fList, self.foutName, self.separator, last=last, block_range=block_range, dprimeCorrection=self.dpCorrCheckBox.isChecked())

            if self.parent().prm['appData']['plotting_available'] == True and (self.plotCheckBox.isChecked() == True or self.pdfPlotCheckBox.isChecked() == True):
                self.plotResults(self.plotCheckBox.isChecked(), self.pdfPlotCheckBox.isChecked())
          
        if self.openResultsFile.isChecked() == True:
            if self.resformat == 'linear':
                QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(self.foutName))
            elif self.resformat == 'table':
                QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(self.foutName))
        if self.openResultsFolder.isChecked() == True:
            QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(os.path.dirname(self.foutName)))
        
    def onClickChooseFileButton(self):
        self.fName = QtGui.QFileDialog.getOpenFileNames(self, self.tr("Choose results file to load"), '', self.tr("All Files (*)"))
        self.fileTF.setText(';'.join(self.fName))
        self.outfileTF.setText('') #clear the out file name
    def onClickChooseOutFileButton(self):
        if self.resformat == 'linear':
            self.foutName = QtGui.QFileDialog.getSaveFileName(self, self.tr('Choose file to write results'), "res.txt", self.tr('All Files (*)'))
        elif self.resformat == 'table':
            self.foutName = QtGui.QFileDialog.getSaveFileName(self, self.tr('Choose file to write results'), "res.csv", self.tr('All Files (*)'))
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
         
                
