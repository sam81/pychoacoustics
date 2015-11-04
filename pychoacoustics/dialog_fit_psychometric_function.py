# -*- coding: utf-8 -*-

#   Copyright (C) 2008-2015 Samuele Carcagno <sam.carcagno@gmail.com>
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
from .pyqtver import*
if pyqtversion == 4:
    from PyQt4 import QtGui, QtCore
    from PyQt4.QtCore import QLocale
    from PyQt4.QtGui import QCheckBox, QComboBox, QDialog, QDesktopServices, QDialogButtonBox, QDoubleValidator, QFileDialog, QGridLayout, QHBoxLayout, QIcon, QIntValidator, QLabel, QLineEdit, QMessageBox, QPushButton, QVBoxLayout, QWidget
    QFileDialog.getOpenFileName = QFileDialog.getOpenFileNameAndFilter
    QFileDialog.getOpenFileNames = QFileDialog.getOpenFileNamesAndFilter
    QFileDialog.getSaveFileName = QFileDialog.getSaveFileNameAndFilter
    matplotlib_available = True
    try:
        import matplotlib
    except:
        matplotlib_available = False
elif pyqtversion == -4:
    from PySide import QtGui, QtCore
    from PySide.QtCore import QLocale
    from PySide.QtGui import QCheckBox, QComboBox, QDialog, QDesktopServices, QDialogButtonBox, QDoubleValidator, QFileDialog, QGridLayout, QHBoxLayout, QIcon, QIntValidator, QLabel, QLineEdit, QMessageBox, QPushButton, QVBoxLayout, QWidget
    matplotlib_available = True
    try:
        import matplotlib
    except:
        matplotlib_available = False
elif pyqtversion == 5:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtCore import QLocale
    from PyQt5.QtWidgets import QCheckBox, QComboBox, QDialog, QDialogButtonBox, QFileDialog, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QVBoxLayout, QWidget
    from PyQt5.QtGui import QDesktopServices, QDoubleValidator, QIcon, QIntValidator
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

    
import os, pystan
import numpy as np
from .stats_utils import*

pandas_available = True
try:
    import pandas as pd
except:
    pandas_available = False
    
# if matplotlib_available and pandas_available:
#     from .win_categorical_plot import*

class fitPsychometricFunctionDialog(QDialog):
    def __init__(self, parent, fList):
        QDialog.__init__(self, parent)
        self.fList = fList
      
        self.currLocale = self.parent().prm['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.OmitGroupSeparator | self.currLocale.RejectGroupSeparator)
        self.prm = self.parent().prm
        
        self.vBoxSizer = QVBoxLayout()
        #self.hCsvSeparator =  QHBoxLayout()
        self.plotBox =  QHBoxLayout()
        self.pdfPlotBox =  QHBoxLayout()
        self.hBox1 =  QHBoxLayout()
        self.hBox1_1 =  QHBoxLayout()
        self.hBox9 =  QHBoxLayout()
        self.gridBox = QGridLayout()
    
        n = 0
        self.fileChooseLabel = QLabel(self.tr('Input File(s): '))
        self.hBox1.addWidget(self.fileChooseLabel)
        self.fileTF = QLineEdit(';'.join(self.fList))
        self.hBox1.addWidget(self.fileTF)
        self.chooseFileButton = QPushButton(self.tr("Change File"), self)
        self.chooseFileButton.clicked.connect(self.onClickChooseFileButton)
        self.hBox1.addWidget(self.chooseFileButton)

        n = n +1
        # self.outfileChooseLabel = QLabel(self.tr('Output File: '))
        # self.hBox1_1.addWidget(self.outfileChooseLabel)
        # self.outfileTF = QLineEdit("")
        # self.hBox1_1.addWidget(self.outfileTF)
        # self.chooseOutFileButton = QPushButton(self.tr("Change File"), self)
        # self.chooseOutFileButton.clicked.connect(self.onClickChooseOutFileButton)
        # self.hBox1_1.addWidget(self.chooseOutFileButton)

        self.csvSeparatorLabel = QLabel(self.tr('csv separator:'))
        self.csvSeparatorTF = QLineEdit(self.prm['pref']["general"]["csvSeparator"])
        self.gridBox.addWidget(self.csvSeparatorLabel, n, 0)
        self.gridBox.addWidget(self.csvSeparatorTF, n, 1)
        n = n+1
        self.functionShapeLabel = QLabel("Shape: ")
        self.functionShape = QComboBox()
        self.functionShape.addItems([self.tr("Logistic")])
        self.gridBox.addWidget(self.functionShapeLabel, n, 0)
        self.gridBox.addWidget(self.functionShape, n, 1)

        self.functionScalingLabel = QLabel("Scale: ")
        self.functionScaling = QComboBox()
        self.functionScaling.addItems([self.tr("Linear"), self.tr("Logarithmic")])
        self.gridBox.addWidget(self.functionScalingLabel, n, 2)
        self.gridBox.addWidget(self.functionScaling, n, 3)

        n = n+1
        self.midpointPriorLabel = QLabel("Midpoint Prior: ")
        self.midpointPrior = QComboBox()
        self.midpointPrior.addItems([self.tr("Normal")])
        self.gridBox.addWidget(self.midpointPriorLabel, n, 0)
        self.gridBox.addWidget(self.midpointPrior, n, 1)

        #n = n+1
        self.midpointPriorMuLabel = QLabel(self.tr("Midpoint Prior mu"), self)
        self.gridBox.addWidget(self.midpointPriorMuLabel, n, 2)
        self.midpointPriorMu = QLineEdit()
        self.midpointPriorMu.setText('')
        self.midpointPriorMu.setValidator(QDoubleValidator(self))
        self.gridBox.addWidget(self.midpointPriorMu, n, 3)
        # midpoint SD prior
        #n = n+1
        self.midpointPriorSTDLabel = QLabel(self.tr("Midpoint Prior STD"), self)
        self.gridBox.addWidget(self.midpointPriorSTDLabel, n, 4)
        self.midpointPriorSTD = QLineEdit()
        self.midpointPriorSTD.setText('')
        self.midpointPriorSTD.setValidator(QDoubleValidator(self))
        self.gridBox.addWidget(self.midpointPriorSTD, n, 5)
        n = n+1

        n = n+1
        self.slopePriorLabel = QLabel(self.tr("Slope Prior: "), self)
        self.slopePrior = QComboBox()
        self.slopePrior.addItems([self.tr("Gamma")])
        self.gridBox.addWidget(self.slopePriorLabel, n, 0)
        self.gridBox.addWidget(self.slopePrior, n, 1)

        #n = n+1
        self.slopePriorModeLabel = QLabel(self.tr("Slope Prior Mode"), self)
        self.gridBox.addWidget(self.slopePriorModeLabel, n, 2)
        self.slopePriorMode = QLineEdit()
        self.slopePriorMode.setText('2')
        self.slopePriorMode.setValidator(QDoubleValidator(self))
        self.gridBox.addWidget(self.slopePriorMode, n, 3)
        # slope SD prior
        #n = n+1
        self.slopePriorSTDLabel = QLabel(self.tr("Slope Prior STD"), self)
        self.gridBox.addWidget(self.slopePriorSTDLabel, n, 4)
        self.slopePriorSTD = QLineEdit()
        self.slopePriorSTD.setText('3')
        self.slopePriorSTD.setValidator(QDoubleValidator(self))
        self.gridBox.addWidget(self.slopePriorSTD, n, 5)
        n = n+1

        self.lapsePriorLabel = QLabel(self.tr("Lapse Prior: "), self)
        self.lapsePrior = QComboBox()
        self.lapsePrior.addItems([self.tr("Gamma")])
        self.gridBox.addWidget(self.lapsePriorLabel, n, 0)
        self.gridBox.addWidget(self.lapsePrior, n, 1)
        #n = n+1
        self.lapsePriorModeLabel = QLabel(self.tr("Lapse Prior Mode"), self)
        self.gridBox.addWidget(self.lapsePriorModeLabel, n, 2)
        self.lapsePriorMode = QLineEdit()
        self.lapsePriorMode.setText('0.05')
        self.lapsePriorMode.setValidator(QDoubleValidator(self))
        self.gridBox.addWidget(self.lapsePriorMode, n, 3)
        # lapse SD prior
        #n = n+1
        self.lapsePriorSTDLabel = QLabel(self.tr("Lapse Prior STD"), self)
        self.gridBox.addWidget(self.lapsePriorSTDLabel, n, 4)
        self.lapsePriorSTD = QLineEdit()
        self.lapsePriorSTD.setText('0.05')
        self.lapsePriorSTD.setValidator(QDoubleValidator(self))
        self.gridBox.addWidget(self.lapsePriorSTD, n, 5)
        n = n+1

        n = n+1
        self.guessLabel = QLabel(self.tr("Guess Rate: "), self)
        self.guessTF = QLineEdit('0.5')
        self.guessTF.setValidator(QDoubleValidator(self))
        self.gridBox.addWidget(self.guessLabel, n, 0)
        self.gridBox.addWidget(self.guessTF, n, 1)
        n = n+1

        self.iterationsLabel = QLabel(self.tr("No. Iterations"), self)
        self.iterationsTF = QLineEdit("10000")
        self.iterationsTF.setValidator(QIntValidator(self))
        self.gridBox.addWidget(self.iterationsLabel, n, 0)
        self.gridBox.addWidget(self.iterationsTF, n, 1)

        self.warmupLabel = QLabel(self.tr("No. Warmup"), self)
        self.warmupTF = QLineEdit("500")
        self.warmupTF.setValidator(QIntValidator(self))
        self.gridBox.addWidget(self.warmupLabel, n, 2)
        self.gridBox.addWidget(self.warmupTF, n, 3)

        self.thinLabel = QLabel(self.tr("Thin"), self)
        self.thinTF = QLineEdit("1")
        self.thinTF.setValidator(QIntValidator(self))
        self.gridBox.addWidget(self.thinLabel, n, 4)
        self.gridBox.addWidget(self.thinTF, n, 5)

        self.chainsLabel = QLabel(self.tr("No. Chains"), self)
        self.chainsTF = QLineEdit("4")
        self.chainsTF.setValidator(QIntValidator(self))
        self.gridBox.addWidget(self.chainsLabel, n, 6)
        self.gridBox.addWidget(self.chainsTF, n, 7)


        if self.parent().prm['appData']['plotting_available'] == True:
            self.plotCheckBox = QCheckBox(self.tr('Plot'))
            self.plotBox.addWidget(self.plotCheckBox)
            self.pdfPlotCheckBox = QCheckBox(self.tr('PDF Plot'))
            self.pdfPlotBox.addWidget(self.pdfPlotCheckBox)


        n = n+1
        self.runButton = QPushButton(self.tr("Run!"), self)
        self.runButton.clicked.connect(self.onClickRunButton)
        self.runButton.setIcon(QIcon.fromTheme("system-run", QIcon(":/system-run")))
        self.hBox9.addWidget(self.runButton)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Close)
        buttonBox.rejected.connect(self.reject)
       
        self.vBoxSizer.addLayout(self.hBox1)
        self.vBoxSizer.addLayout(self.hBox1_1)
        self.vBoxSizer.addLayout(self.gridBox)

        #self.vBoxSizer.addLayout(self.hCsvSeparator)
        if self.parent().prm['appData']['plotting_available'] == True:
            self.vBoxSizer.addLayout(self.plotBox)
            self.vBoxSizer.addLayout(self.pdfPlotBox)

        self.vBoxSizer.addLayout(self.hBox9)
        self.vBoxSizer.addWidget(buttonBox)
        self.setLayout(self.vBoxSizer)
        self.setWindowTitle(self.tr("Fit Psychometric Function"))
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
        self.csvSeparator = self.csvSeparatorTF.text()
        for i in range(len(fList)):
            if i == 0:
                self.dats = pd.read_csv(self.fList[i], sep=self.csvSeparator)
            else:
                self.dats = self.dats.append(pd.read_csv(self.fList[i], sep=self.csvSeparator))

        cnds = np.unique(self.dats['condition'])
        for c in range(len(cnds)):
            thisCnd = cnds[c]
            thisDats = self.dats[self.dats['condition'] == thisCnd]
            x = thisDats['adaptive_difference']
            y = thisDats['response']
            xScale = self.functionScaling.currentText()
            midpointPrior = self.midpointPrior.currentText()
            if self.midpointPriorMu.text() == "":
                midpointMu = np.nan
            else:
                midpointMu = self.currLocale.toDouble(self.midpointPriorMu.text())[0]
            if self.midpointPriorSTD.text() == "":
                midpointSTD = np.nan
            else:
                midpointSTD = self.currLocale.toDouble(self.midpointPriorSTD.text())[0]
            slopePrior = self.slopePrior.currentText()
            slopeMode = self.currLocale.toDouble(self.slopePriorMode.text())[0]
            slopeSTD = self.currLocale.toDouble(self.slopePriorSTD.text())[0]
            lapsePrior = self.lapsePrior.currentText()
            lapseMode = self.currLocale.toDouble(self.lapsePriorMode.text())[0]
            lapseSTD = self.currLocale.toDouble(self.lapsePriorSTD.text())[0]
            guess = self.currLocale.toDouble(self.guessTF.text())[0]
            iterations = self.currLocale.toInt(self.iterationsTF.text())[0]
            warmup = self.currLocale.toInt(self.warmupTF.text())[0]
            thin = self.currLocale.toInt(self.thinTF.text())[0]
            chains = self.currLocale.toInt(self.chainsTF.text())[0]
            self.pystanFitLogisticPsy(x=x, y=y, iterations=iterations, warmup=warmup, thin=thin, chains=chains, xScale=xScale,
                                      midpointPrior=midpointPrior, midpointMu=midpointMu, midpointSTD=midpointSTD,
                                      slopePrior=slopePrior, slopeMode=slopeMode, slopeSTD=slopeSTD,
                                      lapsePrior=lapsePrior, lapseMode=lapseMode, lapseSTD=lapseSTD,
                                      guess=guess)

        # if self.outfileTF.text() == '': #no output file has been chosen
        #     self.onClickChooseOutFileButton()
        #     if len(self.foutName) < 1:
        #         print('No file was selected for saving the results. Skipping')
        #         return
        # else: #file name has been chosen
        #     self.foutName = self.outfileTF.text()


        #     if self.parent().prm['appData']['plotting_available'] == True and (self.plotCheckBox.isChecked() == True or self.pdfPlotCheckBox.isChecked() == True):
        #         self.plotResults(self.plotCheckBox.isChecked(), self.pdfPlotCheckBox.isChecked())
        
        
    def onClickChooseFileButton(self):
        self.fName = QFileDialog.getOpenFileNames(self, self.tr("Choose results file to load"), '', self.tr("All Files (*)"))[0]
        self.fileTF.setText(';'.join(self.fName))
        #self.outfileTF.setText('') #clear the out file name
        
    # def onClickChooseOutFileButton(self):
    #     if self.resformat == 'linear':
    #         self.foutName = QFileDialog.getSaveFileName(self, self.tr('Choose file to write results'), "res.txt", self.tr('All Files (*)'))[0]
    #     elif self.resformat == 'table':
    #         self.foutName = QFileDialog.getSaveFileName(self, self.tr('Choose file to write results'), "res.csv", self.tr('All Files (*)'))[0]
    #     self.outfileTF.setText(self.foutName)
        
  
    def plotResults(self, winPlot, pdfPlot):
        if self.prm['appData']['plotting_available']:
            categoricalPlot(self, 'average', self.foutName, winPlot, pdfPlot, self.paradigm, self.separator, None, self.prm)
         
                
    def pystanFitLogisticPsy(self, x, y, iterations=10000, warmup=500, thin=1, chains=4, xScale="Linear",
                             midpointPrior="Normal", midpointMu=np.nan, midpointSTD=np.nan,
                             slopePrior="Gamma", slopeMode=2, slopeSTD=2,
                             lapsePrior="Gamma", lapseMode=0.5, lapseSTD=0.5,
                             guess=0.5):
        modelString = """
        data {
            int<lower=0> nTrials; #number of trials
            real<lower=0,upper=1> g;
            int<lower=0,upper=1> y[nTrials]; #the vecotor of response 0, or 1
            real x[nTrials]; #the vector of stimulus values
            real meanX;
            real slopeGammaShape;
            real slopeGammaRate;
            real lapseGammaShape;
            real lapseGammaRate;
            }
           parameters {
            real<lower=0,upper=1> lmbd; #lapse rate
            real slp; #the slope
            real mdpnt;
            }

           model {
            lmbd ~ gamma(lapseGammaShape, lapseGammaRate);
            mdpnt ~ normal(meanX, 10^2);
            slp ~ gamma(slopeGammaShape, slopeGammaRate);

            for (i in 1:nTrials) {
              y[i] ~ bernoulli(g+(1-g-lmbd)*1/(1+exp(slp*(mdpnt-x[i]))));

            }

          }
          """ # close quote for modelString

        
        nTrials = len(x)
        dataList = {}
        dataList['nTrials'] = nTrials
        if xScale == "Linear":
            dataList['x'] = x
        elif xScale == "Logarithmic":
            dataList['x'] = np.log(x)
        dataList['y'] =  y
        if np.isnan(midpointMu) == True:
            dataList['meanX'] = np.mean(dataList['x'])
        else:
            dataList['meanX'] = midpointMu
        if np.isnan(midpointSTD) == True:
            dataList['STDX'] = np.std(dataList['x'])*10
        else:
            dataList['STDX'] = midpointSTD
            
        dataList['slopeGammaShape'], dataList['slopeGammaRate'] = gammaShRaFromModeSD(slopeMode, slopeSTD)
        dataList['lapseGammaShape'], dataList['lapseGammaRate'] = gammaShRaFromModeSD(lapseMode, lapseSTD)
        dataList['g'] = guess


        fit = pystan.stan(model_code=modelString, data=dataList,
                          iter=iterations, warmup=warmup, chains=chains, thin=thin)

        print(fit)
