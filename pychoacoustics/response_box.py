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
from .pyqtver import*
if pyqtversion == 4:
    from PyQt4 import QtGui, QtCore
    from PyQt4.QtCore import Qt, QEvent, QThread, QDate, QTime, QDateTime
    from PyQt4.QtGui import QAction, QApplication, QComboBox, QFileDialog, QFrame, QGridLayout, QInputDialog, QLabel, QLineEdit, QMainWindow, QMessageBox, QPainter, QProgressBar, QPushButton, QScrollArea, QShortcut, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget, QWidgetItem
    QFileDialog.getOpenFileName = QFileDialog.getOpenFileNameAndFilter
    QFileDialog.getOpenFileNames = QFileDialog.getOpenFileNamesAndFilter
    QFileDialog.getSaveFileName = QFileDialog.getSaveFileNameAndFilter
    try:
        import matplotlib
        matplotlib_available = True
    except:
        matplotlib_available = False
elif pyqtversion == -4:
    from PySide import QtGui, QtCore
    from PySide.QtCore import Qt, QEvent, QThread, QDate, QTime, QDateTime
    from PySide.QtGui import QAction, QApplication, QComboBox, QFileDialog, QFrame, QGridLayout, QInputDialog, QLabel, QLineEdit, QMainWindow, QMessageBox, QPainter, QProgressBar, QPushButton, QScrollArea, QShortcut, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget, QWidgetItem
    try:
        import matplotlib
        matplotlib_available = True
    except:
        matplotlib_available = False
elif pyqtversion == 5:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtCore import Qt, QEvent, QThread, QDate, QTime, QDateTime
    from PyQt5.QtWidgets import QAction, QApplication, QComboBox, QFileDialog, QFrame, QGridLayout, QInputDialog, QLabel, QLineEdit, QMainWindow, QMessageBox, QProgressBar, QPushButton, QScrollArea, QShortcut, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget, QWidgetItem
    from PyQt5.QtGui import QPainter
    matplotlib_available = False
    
from numpy.fft import rfft, irfft, fft, ifft
import base64, fnmatch, copy, numpy, os, platform, random, string, smtplib, sys, time     
from numpy import array, concatenate, log10, nan, mean, repeat, std
from .utils_general import*
from .stats_utils import*
from .pysdt import*
from scipy.stats.distributions import norm

from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders

from .audio_manager import*
from .stats_utils import*
from .sndlib import*
from .utils_general import*
from .utils_process_results import*




try:
    import pandas
    pandas_available = True
except:
    pandas_available = False
    
if matplotlib_available and pandas_available:
    from .win_categorical_plot import*


from . import default_experiments

homeExperimentsPath = os.path.normpath(os.path.expanduser("~") +'/pychoacoustics_exp/')
if os.path.exists(os.path.normpath(homeExperimentsPath + '/labexp/__init__.py')) == True:
    sys.path.append(homeExperimentsPath)

try:
    import labexp
    from labexp import*
    labexp_exists = True
except:
    labexp_exists = False

class responseBox(QMainWindow):
    def __init__(self, parent):
        QMainWindow.__init__(self, parent)
        self.emailThread = emailSender(self)
        self.executerThread = commandExecuter(self)
        self.playThread = threadedPlayer(self)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowMaximizeButtonHint)
        self.setWindowModality(Qt.NonModal)
        self.prm = parent.prm
        self.audioManager = audioManager(self)
        self.currLocale = self.parent().prm['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.OmitGroupSeparator | self.currLocale.RejectGroupSeparator)
        self.setWindowTitle(self.tr('Response Box'))
        self.setStyleSheet("QPushButton[responseBoxButton='true'] {font-weight:bold; font-size: %spx;} " % self.prm['pref']['interface']['responseButtonSize'])
        self.menubar = self.menuBar()
        #FILE MENU
        self.fileMenu = self.menubar.addMenu(self.tr('-'))
       
        self.toggleControlWin = QAction(self.tr('Show/Hide Control Window'), self)
        self.toggleControlWin.setShortcut('Ctrl+C')
        self.toggleControlWin.setCheckable(True)
        #self.toggleControlWin.setStatusTip(self.tr('Toggle Control Window'))
        self.toggleControlWin.triggered.connect(self.onToggleControlWin)
        if self.prm['hideWins'] == True:
            self.toggleControlWin.setChecked(False)
        else:
            self.toggleControlWin.setChecked(True)
        
        self.toggleGauge = QAction(self.tr('Show/Hide Progress Bar'), self)
        self.toggleGauge.setShortcut('Ctrl+P')
        self.toggleGauge.setCheckable(True)
        self.toggleGauge.triggered.connect(self.onToggleGauge)

        self.toggleBlockGauge = QAction(self.tr('Show/Hide Block Progress Bar'), self)
        self.toggleBlockGauge.setShortcut('Ctrl+B')
        self.toggleBlockGauge.setCheckable(True)
        self.toggleBlockGauge.triggered.connect(self.onToggleBlockGauge)

        #self.statusBar()
        self.fileMenu.addAction(self.toggleControlWin)
        self.fileMenu.addAction(self.toggleGauge)
        self.fileMenu.addAction(self.toggleBlockGauge)
        
        self.rb = QFrame()
        self.rb.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
        self.rb_sizer = QVBoxLayout()
        self.intervalSizer = QGridLayout()
        self.responseButtonSizer = QGridLayout()
       
        self.statusButton = QPushButton(self.prm['rbTrans'].translate('rb', "Wait"), self)
        self.statusButton.clicked.connect(self.onClickStatusButton)
        self.statusButton.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.statusButton.setProperty("responseBoxButton", True)
        self.statBtnShortcut = QShortcut("Ctrl+R", self, activated = self.onClickStatusButton)
        self.statusButton.setToolTip(self.tr("Press Ctrl+R to activate"))
        
        self.responseLight = responseLight(self)

        self.gauge = QProgressBar(self)
        self.gauge.setRange(0, 100)
        self.blockGauge = QProgressBar(self)
        
        self.rb_sizer.addWidget(self.statusButton)
        self.rb_sizer.addSpacing(20)
        self.rb_sizer.addWidget(self.responseLight)
        self.rb_sizer.addSpacing(20)
        self.intervalLight = []
        self.responseButton = []
        self.setupLights()
        self.rb_sizer.addLayout(self.intervalSizer)
        self.rb_sizer.addSpacing(5)
        self.rb_sizer.addLayout(self.responseButtonSizer)
        self.rb_sizer.addSpacing(20)
        self.rb_sizer.addWidget(self.gauge)
        self.rb_sizer.addWidget(self.blockGauge)
        if self.prm['progbar'] == True:
            self.toggleGauge.setChecked(True)
            self.onToggleGauge()
        else:
            self.toggleGauge.setChecked(False)
            self.onToggleGauge()
        if self.prm['blockProgbar'] == True:
            self.toggleBlockGauge.setChecked(True)
            self.onToggleBlockGauge()
        else:
            self.toggleBlockGauge.setChecked(False)
            self.onToggleBlockGauge()
        self.rb.setLayout(self.rb_sizer)
        self.setCentralWidget(self.rb)
        self.show()
        self.prm['listener'] = self.parent().listenerTF.text()
        self.prm['sessionLabel'] = self.parent().sessionLabelTF.text()
        if self.prm['hideWins'] == True:
            self.parent().hide()
        
    def clearLayout(self, layout):
        #http://stackoverflow.com/questions/9374063/pyqt4-remove-widgets-and-layout-as-well
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            layout.removeItem(item)
            if isinstance(item, QWidgetItem):
                #item.widget().close()
                # or
                item.widget().setParent(None)
            elif isinstance(item, QSpacerItem):
                pass
                # no need to do extra stuff
            else:
                self.clearLayout(item.layout())

            # remove the item from layout
             
    def setupLights(self):
        nIntervals = self.prm['nIntervals']
        nResponseIntervals = nIntervals
        #remove previous lights and buttons
    
        self.clearLayout(self.intervalSizer)
        self.intervalLight = []
     
        self.clearLayout(self.responseButtonSizer)
        self.responseButton = []

        n = 0
        if self.prm["warningInterval"] == True:
            self.intervalLight.append(intervalLight(self))
            self.intervalSizer.addWidget(self.intervalLight[n], 0, n)
            n = n+1
                
        if self.prm[self.parent().currExp]["hasAlternativesChooser"] == True:
            nAlternatives = self.currLocale.toInt(self.parent().nAlternativesChooser.currentText())[0]
        else:
            nAlternatives = nIntervals
        
        if self.parent().currParadigm in ["Adaptive", "Weighted Up/Down", "Constant m-Intervals n-Alternatives",
                                 "Adaptive Interleaved", "Weighted Up/Down Interleaved", "Multiple Constants m-Intervals n-Alternatives"]:

            if self.prm["preTrialInterval"] == True:
                self.intervalLight.append(intervalLight(self))
                self.intervalSizer.addWidget(self.intervalLight[n], 0, n)
                n = n+1
            
            for i in range(nIntervals):
                if self.prm["precursorInterval"] == True:
                    self.intervalLight.append(intervalLight(self))
                    self.intervalSizer.addWidget(self.intervalLight[n], 0, n)
                    n = n+1
                 
                self.intervalLight.append(intervalLight(self))
                self.intervalSizer.addWidget(self.intervalLight[n], 0, n)
                n = n+1
            
                if self.prm["postcursorInterval"] == True:
                    self.intervalLight.append(intervalLight(self))
                    self.intervalSizer.addWidget(self.intervalLight[n], 0, n)
                    n = n+1

            r = 0
            if self.prm["warningInterval"] == True:
                self.responseButtonSizer.addItem(QSpacerItem(-1, -1, QSizePolicy.Expanding), 0, r)
                r = r+1
            if self.prm["preTrialInterval"] == True:
                self.responseButtonSizer.addItem(QSpacerItem(-1, -1, QSizePolicy.Expanding), 0, r)
                r = r+1
            if nAlternatives == nIntervals:
                for i in range(nAlternatives):
                    if self.prm["precursorInterval"] == True:
                        self.responseButtonSizer.addItem(QSpacerItem(-1, -1, QSizePolicy.Expanding), 0, r)
                        r = r+1
                    self.responseButton.append(QPushButton(str(i+1), self))
                    self.responseButtonSizer.addWidget(self.responseButton[i], 1, r)
                    self.responseButton[i].setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
                    self.responseButton[i].setProperty("responseBoxButton", True)
                    r = r+1
                    if self.prm[self.parent().currExp]["hasPostcursorInterval"] == True:
                        self.responseButtonSizer.addItem(QSpacerItem(-1, -1, QSizePolicy.Expanding), 0, r)
                        r = r+1
                    self.responseButton[i].clicked.connect(self.sortResponseButton)
                    self.responseButton[i].setFocusPolicy(Qt.NoFocus)

            elif nAlternatives == nIntervals-1:
                for i in range(nAlternatives):
                    if self.prm[self.parent().currExp]["hasPrecursorInterval"] == True:
                        self.responseButtonSizer.addItem(QSpacerItem(-1, -1, QSizePolicy.Expanding), 0, r)
                        r = r+1
                    if i == 0:
                        self.responseButtonSizer.addItem(QSpacerItem(-1, -1, QSizePolicy.Expanding), 0, r)
                        r = r+1
                  
                    self.responseButton.append(QPushButton(str(i+1), self))
                    self.responseButtonSizer.addWidget(self.responseButton[i], 1, r)
                    self.responseButton[i].setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
                    self.responseButton[i].setProperty("responseBoxButton", True)
                    r = r+1
                    self.responseButton[i].clicked.connect(self.sortResponseButton)
                    self.responseButton[i].setFocusPolicy(Qt.NoFocus)
                    if self.prm[self.parent().currExp]["hasPostcursorInterval"] == True:
                        self.responseButtonSizer.addItem(QSpacerItem(-1, -1, QSizePolicy.Expanding), 0, r)
                        r = r+1
                  
        elif self.parent().currParadigm in ["Constant 1-Interval 2-Alternatives", "Multiple Constants 1-Interval 2-Alternatives",
                                   "Constant 1-Pair Same/Different"]:
            for i in range(nIntervals):
                self.intervalLight.append(intervalLight(self))
                self.intervalSizer.addWidget(self.intervalLight[n], 0, n)
                n = n+1
                
            for i in range(self.prm['nAlternatives']):
                self.responseButton.append(QPushButton(self.prm[self.tr(self.parent().experimentChooser.currentText())]['buttonLabels'][i], self))
            
                self.responseButtonSizer.addWidget(self.responseButton[i], 1, i)
                self.responseButton[i].setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
                self.responseButton[i].setProperty("responseBoxButton", True)
                self.responseButton[i].clicked.connect(self.sortResponseButton)
                self.responseButton[i].setFocusPolicy(Qt.NoFocus)
        self.showHideIntervalLights(self.prm['intervalLights'])

    def showHideIntervalLights(self, status):
        if status == self.tr("Yes"):
            for light in self.intervalLight:
                light.show()
        else:
            for light in self.intervalLight:
                light.hide()

    def onToggleControlWin(self):
        if self.toggleControlWin.isChecked() == True:
            self.parent().show()
        elif self.toggleControlWin.isChecked() == False:
            self.parent().hide()
            if self.prm['storedBlocks'] > 0:
                if self.parent().listenerTF.text() == "" and self.prm['pref']['general']['listenerNameWarn'] == True:
                    msg = self.prm['rbTrans'].translate('rb', "Please, enter the listener's name:") 
                    text, ok = QInputDialog.getText(self, self.prm['rbTrans'].translate('rb', "Input Dialog:") , msg)
                    if ok:
                        self.parent().listenerTF.setText(text)
                        self.prm['listener'] = text
                if self.parent().sessionLabelTF.text() == "" and self.prm['pref']['general']['sessionLabelWarn'] == True:
                    msg = self.prm['rbTrans'].translate('rb', "Please, enter the session label:") 
                    text, ok = QInputDialog.getText(self, self.prm['rbTrans'].translate('rb', "Input Dialog:") , msg)
                    if ok:
                        self.parent().sessionLabelTF.setText(text)
                        self.prm['sessionLabel'] = text
                if 'resultsFile' not in self.prm:
                    self.onAskSaveResultsButton()

    def onAskSaveResultsButton(self):
        ftow = QFileDialog.getSaveFileName(self, self.tr('Choose file to write results'), "", self.tr('All Files (*)'), QFileDialog.DontConfirmOverwrite)[0]
        if os.path.exists(ftow) == False and len(ftow) > 0:
                fName = open(ftow, 'w')
                fName.write('')
                fName.close()
        if len(ftow) > 0:
            if fnmatch.fnmatch(ftow, '*.txt') == False:
                ftow = ftow + '.txt'
            self.prm['resultsFile'] = ftow
            self.parent().statusBar().showMessage(self.tr('Saving results to file: ') + self.prm["resultsFile"])
           
    def onToggleGauge(self):
        if self.toggleGauge.isChecked() == True:
            self.gauge.show()
        elif self.toggleGauge.isChecked() == False:
            self.gauge.hide()

    def onToggleBlockGauge(self):
        if self.toggleBlockGauge.isChecked() == True:
            self.blockGauge.show()
        elif self.toggleBlockGauge.isChecked() == False:
            self.blockGauge.hide()

    def onClickStatusButton(self):
        self.parent().compareGuiStoredParameters()
        if self.prm['storedBlocks'] == 0 or self.statusButton.text() == self.prm['rbTrans'].translate("rb", "Running") or self.statusButton.text() == self.prm['rbTrans'].translate("rb", "Finished"):
            return

        if self.prm['currentBlock'] > self.prm['storedBlocks']: #the user did not choose to store the unsaved block, move to first block
            self.parent().moveToBlockPosition(1)    
       
        if self.parent().listenerTF.text() == "" and self.prm['pref']['general']['listenerNameWarn'] == True:
            msg = self.prm['rbTrans'].translate('rb', "Please, enter the listener's name:") 
            text, ok = QInputDialog.getText(self, self.prm['rbTrans'].translate('rb', "Input Dialog:") , msg)
            if ok:
                self.parent().listenerTF.setText(text)
                self.prm['listener'] = text

            return
        if self.parent().sessionLabelTF.text() == "" and self.prm['pref']['general']['sessionLabelWarn'] == True:
            msg = self.prm['rbTrans'].translate('rb', "Please, enter the session label:") 
            text, ok = QInputDialog.getText(self, self.prm['rbTrans'].translate('rb', "Input Dialog:") , msg)
            if ok:
                self.parent().sessionLabelTF.setText(text)
                self.prm['sessionLabel'] = text
            return
        
        if int(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition']) == 1 and self.prm['allBlocks']['shuffleMode'] == self.tr("Ask") and self.prm["shuffled"] == False and self.prm['storedBlocks'] > 1 :
            reply = QMessageBox.question(self, self.prm['rbTrans'].translate('rb', "Message"),
                                               self.prm['rbTrans'].translate('rb', "Do you want to shuffle the blocks?"), QMessageBox.Yes | 
                                               QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.parent().onClickShuffleBlocksButton()
                self.prm["shuffled"] = True
        elif int(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition']) == 1 and self.prm["shuffled"] == False and self.prm['allBlocks']['shuffleMode'] == self.tr("Auto") and self.prm['storedBlocks'] > 1 :
         
            self.parent().onClickShuffleBlocksButton()
            self.prm["shuffled"] = True

        self.prm['startOfBlock'] = True
        self.statusButton.setText(self.prm['rbTrans'].translate("rb", "Running"))
        self.prm['trialRunning'] = True
        QApplication.processEvents()

        if self.prm['allBlocks']['sendTriggers'] == True:
            thisSnd = pureTone(440, 0, -200, 980, 10, "Both", self.prm['allBlocks']['sampRate'], 100)
            playCmd = self.prm['pref']['sound']['playCommand']
            self.audioManager.playSoundWithTrigger(thisSnd, self.prm['allBlocks']['sampRate'], self.prm['allBlocks']['nBits'], playCmd, False, 'ONTrigger.wav', self.prm["pref"]["general"]["ONTrigger"])
            print("SENDING START TRIGGER", self.prm["pref"]["general"]["ONTrigger"])
        if self.prm['currentBlock'] > self.prm['storedBlocks']:
            self.parent().onClickNextBlockPositionButton()
        
        self.doTrial()

    def playRandomisedIntervals(self, stimulusCorrect, stimulusIncorrect, preTrialStim=None, precursorStim=None, postCursorStim=None):
        # this randint function comes from numpy and has different behaviour than in the python 'random' module
        # Return random integers x such that low <= x < high
        currBlock = 'b'+ str(self.prm['currentBlock'])
        nAlternatives = self.prm[currBlock]['nAlternatives']
        nIntervals = self.prm[currBlock]['nIntervals']
        cmd = self.prm['pref']['sound']['playCommand']
        if nAlternatives == nIntervals:
            self.correctInterval = numpy.random.randint(0, nIntervals)
            self.correctButton = self.correctInterval + 1
        elif nAlternatives == nIntervals-1:
            self.correctInterval = numpy.random.randint(1, nIntervals)
            self.correctButton = self.correctInterval 
        soundList = []
        for i in range(nIntervals):
            if i == self.correctInterval:
                soundList.append(stimulusCorrect)
            else:
                foo = stimulusIncorrect.pop()
                soundList.append(foo)

        nLight = 0
        if self.prm["warningInterval"] == True:
            self.intervalLight[nLight].setStatus('on')
            time.sleep(self.prm[currBlock]['warningIntervalDur']/1000)
            self.intervalLight[nLight].setStatus('off')
            nLight = nLight+1
            time.sleep(self.prm[currBlock]['warningIntervalISI']/1000)
        if self.prm["preTrialInterval"] == True:
            self.intervalLight[nLight].setStatus('on')
            self.audioManager.playSound(preTrialStim, self.prm['allBlocks']['sampRate'], self.prm['allBlocks']['nBits'], cmd, self.prm['pref']['sound']['writewav'], 'pre-trial_interval' +'.wav')
            self.intervalLight[nLight].setStatus('off')
            nLight = nLight+1
            time.sleep(self.prm[currBlock]['preTrialIntervalISI']/1000)
        for i in range(nIntervals):
            if self.prm["precursorInterval"] == True:
                self.intervalLight[nLight].setStatus('on')
                self.audioManager.playSound(precursorStim, self.prm['allBlocks']['sampRate'], self.prm['allBlocks']['nBits'], cmd, self.prm['pref']['sound']['writewav'], 'precursor_interval'+str(i+1) +'.wav')
                self.intervalLight[nLight].setStatus('off')
                nLight = nLight+1
                time.sleep(self.prm[currBlock]['precursorIntervalISI']/1000)
            self.intervalLight[nLight].setStatus('on')
            self.audioManager.playSound(soundList[i], self.prm['allBlocks']['sampRate'], self.prm['allBlocks']['nBits'], cmd, self.prm['pref']['sound']['writewav'], 'interval'+str(i+1) +'.wav')
            self.intervalLight[nLight].setStatus('off')
            nLight = nLight+1
            if self.prm["postcursorInterval"] == True:
                self.intervalLight[nLight].setStatus('on')
                self.audioManager.playSound(postcursorStim, self.prm['allBlocks']['sampRate'], self.prm['allBlocks']['nBits'], cmd, self.prm['pref']['sound']['writewav'], 'postcursor_interval'+str(i+1) +'.wav')
                self.intervalLight[nLight].setStatus('off')
                nLight = nLight+1
                time.sleep(self.prm[currBlock]['postcursorIntervalISI']/1000)
            if i < nIntervals-1:
                time.sleep(self.prm['isi']/1000.)

    def playSequentialIntervals(self, sndList, ISIList=[], trigNum=None):
        currBlock = 'b'+ str(self.prm['currentBlock'])
        cmd = self.prm['pref']['sound']['playCommand']
        for i in range(len(sndList)):
            if self.prm['pref']['sound']['writeSndSeqSegments'] == True:
                self.audioManager.scipy_wavwrite("sndSeq%i.wav"%(i+1), self.prm['allBlocks']['sampRate'], self.prm['allBlocks']['nBits'], sndList[i])
        nLight = 0
        if self.prm["warningInterval"] == True:
            self.intervalLight[nLight].setStatus('on')
            time.sleep(self.prm[currBlock]['warningIntervalDur']/1000)
            self.intervalLight[nLight].setStatus('off')
            nLight = nLight+1
            time.sleep(self.prm[currBlock]['warningIntervalISI']/1000)
        for i in range(len(sndList)):
            self.intervalLight[nLight].setStatus('on')
            if trigNum != None:
                self.audioManager.playSoundWithTrigger(sndList[i], self.prm['allBlocks']['sampRate'], self.prm['allBlocks']['nBits'], cmd, self.prm['pref']['sound']['writewav'], 'soundSequence.wav', trigNum)
            else:
                self.audioManager.playSound(sndList[i], self.prm['allBlocks']['sampRate'], self.prm['allBlocks']['nBits'], cmd, self.prm['pref']['sound']['writewav'], 'soundSequence.wav')
            self.intervalLight[nLight].setStatus('off')
            nLight = nLight+1

            if i < (len(sndList) - 1):
                time.sleep(ISIList[i]/1000)

    def doTrial(self):
        self.prm['trialRunning'] = True
        self.prm['sortingResponse'] = False
        currBlock = 'b'+ str(self.prm['currentBlock'])
        #for compatibility otherwise need to change in all experiments
        self.prm['maxLevel'] = self.prm['allBlocks']['maxLevel']
        self.prm['sampRate'] = self.prm['allBlocks']['sampRate']
        self.prm['nBits'] = self.prm['allBlocks']['nBits']
   
        self.prm['paradigm'] = self.prm[currBlock]['paradigm']
        if self.prm[self.parent().currExp]["hasISIBox"] == True:
            self.prm['isi'] = self.prm[currBlock]['ISIVal']
        if self.prm[self.parent().currExp]["hasAlternativesChooser"] == True:
            self.prm['nAlternatives'] = self.prm[currBlock]['nAlternatives']
        self.prm["responseLight"] = self.prm[currBlock]['responseLight']

        if self.prm['startOfBlock'] == True:
            self.getStartTime()

            if self.prm['paradigm'] in [self.tr("Adaptive Interleaved"), self.tr("Weighted Up/Down Interleaved")]:
                self.prm['nDifferences'] = int(self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("No. Tracks:"))])
                if self.prm['nDifferences'] == 1:
                    self.prm['maxConsecutiveTrials'] = self.tr('unlimited')
                else:
                    self.prm['maxConsecutiveTrials'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Max. Consecutive Trials x Track:"))]
           

            if self.prm['paradigm'] == self.tr("Adaptive"):
                self.prm['numberCorrectNeeded'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Rule Down"))])
                self.prm['numberIncorrectNeeded'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Rule Up"))])
                self.prm['initialTurnpoints'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Initial Turnpoints"))])
                self.prm['totalTurnpoints'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Total Turnpoints"))])
                self.prm['adaptiveStepSize1'] = self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Step Size 1"))]
                self.prm['adaptiveStepSize2'] = self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Step Size 2"))]
                self.prm['adaptiveType'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Procedure:"))]
                self.prm['trackDir'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Initial Track Direction:"))]
            elif self.prm['paradigm'] == self.tr("Adaptive Interleaved"):
                self.prm['adaptiveType'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Procedure:"))]
                self.prm['turnpointsToAverage'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Turnpoints to average:"))]
                
                self.prm['numberCorrectNeeded'] = []
                self.prm['numberIncorrectNeeded'] = []
                self.prm['initialTurnpoints'] = []
                self.prm['totalTurnpoints'] = []
                self.prm['adaptiveStepSize1'] = []
                self.prm['adaptiveStepSize2'] = []
                self.prm['consecutiveTrialsCounter'] = []
                self.prm['trackDir'] = []
                for i in range(self.prm['nDifferences']):
                    self.prm['numberCorrectNeeded'].append(int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Rule Down Track " + str(i+1)))]))
                    self.prm['numberIncorrectNeeded'].append(int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Rule Up Track " + str(i+1)))]))
                    self.prm['initialTurnpoints'].append(int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Initial Turnpoints Track " + str(i+1)))]))
                    self.prm['totalTurnpoints'].append(int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Total Turnpoints Track " + str(i+1)))]))
                    self.prm['adaptiveStepSize1'].append(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Step Size 1 Track " + str(i+1)))])
                    self.prm['adaptiveStepSize2'].append(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Step Size 2 Track " + str(i+1)))])
                    self.prm['consecutiveTrialsCounter'].append(0)
                    self.prm['trackDir'].append(self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Initial Track {0} Direction:".format(str(i+1))))])
            elif self.prm['paradigm'] == self.tr("Weighted Up/Down"):
                self.prm['percentCorrectTracked'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Percent Correct Tracked"))])

                self.prm['initialTurnpoints'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Initial Turnpoints"))])
                self.prm['totalTurnpoints'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Total Turnpoints"))])
                self.prm['adaptiveStepSize1'] = self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Step Size 1"))]
                self.prm['adaptiveStepSize2'] = self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Step Size 2"))]
                self.prm['adaptiveType'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Procedure:"))]
                self.prm['trackDir'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Initial Track Direction:"))]
                self.prm['numberCorrectNeeded'] = 1
                self.prm['numberIncorrectNeeded'] = 1

            elif self.prm['paradigm'] == self.tr("Weighted Up/Down Interleaved"):
                self.prm['adaptiveType'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Procedure:"))]
                self.prm['turnpointsToAverage'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Turnpoints to average:"))]
                self.prm['percentCorrectTracked'] = []
                self.prm['numberCorrectNeeded'] = []
                self.prm['numberIncorrectNeeded'] = []
                self.prm['initialTurnpoints'] = []
                self.prm['totalTurnpoints'] = []
                self.prm['adaptiveStepSize1'] = []
                self.prm['adaptiveStepSize2'] = []
                self.prm['consecutiveTrialsCounter'] = []
                self.prm['trackDir'] = []
                for i in range(self.prm['nDifferences']):
                    self.prm['numberCorrectNeeded'].append(1)
                    self.prm['numberIncorrectNeeded'].append(1)
                    self.prm['percentCorrectTracked'].append(float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Percent Correct Tracked Track " + str(i+1)))]))
                    self.prm['initialTurnpoints'].append(int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Initial Turnpoints Track " + str(i+1)))]))
                    self.prm['totalTurnpoints'].append(int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Total Turnpoints Track " + str(i+1)))]))
                    self.prm['adaptiveStepSize1'].append(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Step Size 1 Track " + str(i+1)))])
                    self.prm['adaptiveStepSize2'].append(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Step Size 2 Track " + str(i+1)))])
                    self.prm['consecutiveTrialsCounter'].append(0)
                    self.prm['trackDir'].append(self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Initial Track {0} Direction:".format(str(i+1))))])
            elif self.prm['paradigm'] in [self.tr("Constant m-Intervals n-Alternatives"), self.tr("Constant 1-Interval 2-Alternatives"), self.tr("Constant 1-Pair Same/Different")]:
                self.prm['nTrials'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("No. Trials"))])
                self.prm['nPracticeTrials'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("No. Practice Trials"))])
            elif self.prm['paradigm'] in [self.tr("Multiple Constants 1-Interval 2-Alternatives"), self.tr("Multiple Constants m-Intervals n-Alternatives")]:
                self.prm['nTrials'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("No. Trials"))])
                self.prm['nPracticeTrials'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("No. Practice Trials"))])
                self.prm['nDifferences'] = int(self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("No. Differences:"))])
                if self.prm['startOfBlock'] == True:
                    self.prm['currentDifference'] = numpy.random.randint(self.prm['nDifferences'])
        
        if self.prm['startOfBlock'] == True and 'resultsFile' not in self.prm:
            if self.prm['pref']['general']['resFileFormat'] == 'fixed':
                self.prm['resultsFile'] = self.prm['pref']['general']['resFileFixedString']
                resFileToOpen = copy.copy(self.prm['pref']['general']['resFileFixedString'])

                fName = open(resFileToOpen, 'w')
                fName.write('')
                fName.close()
            elif self.prm['pref']['general']['resFileFormat'] == 'variable':
                self.prm['resultsFile'] = self.prm['listener'] + '_' + time.strftime("%y-%m-%d_%H-%M-%S", time.localtime())

        if self.prm['paradigm'] in [self.tr("Adaptive Interleaved"), self.tr("Weighted Up/Down Interleaved")]:
            if self.prm['maxConsecutiveTrials'] == self.tr('unlimited'):
                self.prm['currentDifference'] = numpy.random.randint(self.prm['nDifferences'])
            elif  max(self.prm['consecutiveTrialsCounter']) < int(self.prm['maxConsecutiveTrials']):
                self.prm['currentDifference'] = numpy.random.randint(self.prm['nDifferences'])
            else:
                choices = list(range(self.prm['nDifferences']))
                choices.pop(self.prm['consecutiveTrialsCounter'].index(max(self.prm['consecutiveTrialsCounter'])))
                self.prm['currentDifference'] = random.choice(choices)
            for i in range(self.prm['nDifferences']):
                if i == self.prm['currentDifference']:
                    self.prm['consecutiveTrialsCounter'][self.prm['currentDifference']] = self.prm['consecutiveTrialsCounter'][self.prm['currentDifference']] + 1
                else:
                    self.prm['consecutiveTrialsCounter'][i] = 0
     

        currExp = self.tr(self.prm[currBlock]['experiment'])
        self.pychovariables =           ["[resDir]",
                                         "[resFile]",
                                         "[resFileFull]",
                                         "[resFileRes]",
                                         "[resTable]",
                                         "[listener]",
                                         "[experimenter]",
                                         "[resTableProcessed]",
                                         "[pdfPlot]"]
        self.pychovariablesSubstitute = [os.path.dirname(self.prm['resultsFile']),
                                         self.prm['resultsFile'],
                                         self.prm['resultsFile'].split('.txt')[0]+'_full.txt',
                                         self.prm['resultsFile'].split('.txt')[0]+'_res.txt',
                                         self.prm['resultsFile'].split('.txt')[0]+'_table.csv',
                                         self.prm['listener'], self.prm['experimenter'],
                                         self.prm['resultsFile'].split('.txt')[0]+'_table_processed.csv',
                                         self.prm['resultsFile'].split('.txt')[0]+'_table_processed.pdf']
      

        
        time.sleep(self.prm[currBlock]['preTrialSilence']/1000)
        execString = self.prm[currExp]['execString']
      
        try:
            methodToCall1 = getattr(default_experiments, execString)
        except:
            pass
        try:
            methodToCall1 = getattr(labexp, execString)
        except:
            pass
        
        methodToCall2 = getattr(methodToCall1, 'doTrial_'+ execString)
        result = methodToCall2(self)
        QApplication.processEvents()
        self.prm['trialRunning'] = False
        if self.prm['allBlocks']['responseMode'] == self.tr("Automatic"):
            if numpy.random.uniform(0, 1, 1)[0] < self.prm['allBlocks']['autoPCCorr']:
                self.sortResponse(self.correctButton)
            else:
                self.sortResponse(random.choice(numpy.delete(numpy.arange(self.prm['nAlternatives'])+1, self.correctButton-1)))
       #==================================================================
       
    def sortResponseButton(self):
        buttonClicked = self.responseButton.index(self.sender())+1
        self.sortResponse(buttonClicked)
        
    def keyPressEvent(self, event):
        if (event.type() == QEvent.KeyPress): 
            if event.key()==Qt.Key_0:
                buttonClicked = 0
            elif event.key()==Qt.Key_1:
                buttonClicked = 1
            elif event.key()==Qt.Key_2:
                buttonClicked = 2
            elif event.key()==Qt.Key_3:
                buttonClicked = 3
            elif event.key()==Qt.Key_4:
                buttonClicked = 4
            elif event.key()==Qt.Key_5:
                buttonClicked = 5
            elif event.key()==Qt.Key_6:
                buttonClicked = 6
            elif event.key()==Qt.Key_7:
                buttonClicked = 7
            elif event.key()==Qt.Key_8:
                buttonClicked = 8
            elif event.key()==Qt.Key_9:
                buttonClicked = 9
            else:
                buttonClicked = 0
            self.sortResponse(buttonClicked)
        return 
       
    def sortResponse(self, buttonClicked):
        
        currBlock = 'b'+ str(self.prm['currentBlock'])
        if buttonClicked == 0: #0 is not a response option
            return
        if buttonClicked > self.prm['nAlternatives'] or self.statusButton.text() != self.prm['rbTrans'].translate("rb", "Running"): #self.tr("Running"): #1) do not accept responses outside the possible alternatives and 2) if the block is not running (like wait or finished)
            return
        if buttonClicked < (self.prm['nAlternatives']+1) and self.prm['trialRunning'] == True: #1) can't remember why I put the first condition 2) do not accept responses while the trial is running
            return
        if self.prm['sortingResponse'] == True: #Do not accept other responses while processing the current one
            return
        self.prm['sortingResponse'] = True

        if self.prm['paradigm'] == self.tr("Adaptive"):
            self.sortResponseAdaptive(buttonClicked, 'transformedUpDown')
        elif self.prm['paradigm'] == self.tr("Adaptive Interleaved"):
            self.sortResponseAdaptiveInterleaved(buttonClicked, 'transformedUpDown')
        elif self.prm['paradigm'] == self.tr("Weighted Up/Down"):
            self.sortResponseAdaptive(buttonClicked, 'weightedUpDown')
        elif self.prm['paradigm'] == self.tr("Weighted Up/Down Interleaved"):
            self.sortResponseAdaptiveInterleaved(buttonClicked, 'weightedUpDown')
        elif self.prm['paradigm'] == self.tr("Constant 1-Interval 2-Alternatives"):
            self.sortResponseConstant1Interval2Alternatives(buttonClicked)
        elif self.prm['paradigm'] == self.tr("Multiple Constants 1-Interval 2-Alternatives"):
            self.sortResponseMultipleConstants1Interval2Alternatives(buttonClicked)
        elif self.prm['paradigm'] == self.tr("Constant m-Intervals n-Alternatives"):
            self.sortResponseConstantMIntervalsNAlternatives(buttonClicked)
        elif self.prm['paradigm'] == self.tr("Multiple Constants m-Intervals n-Alternatives"):
            self.sortResponseMultipleConstantsMIntervalsNAlternatives(buttonClicked)
        elif self.prm['paradigm'] == self.tr("Constant 1-Pair Same/Different"):
            self.sortResponseConstant1PairSameDifferent(buttonClicked)
        elif self.prm['paradigm'] == self.tr("Same Different 4"):
            self.sortResponseSameDifferent4(buttonClicked)
            self.prm['sortingResponse'] = False
            
    def sortResponseAdaptive(self, buttonClicked, method):
        if self.prm['startOfBlock'] == True:
            self.prm['correctCount'] = 0
            self.prm['incorrectCount'] = 0
            self.prm['nTurnpoints'] = 0
            self.prm['startOfBlock'] = False
            self.prm['turnpointVal'] = []
            self.fullFileLines = []
            self.prm['buttonCounter'] = [0 for i in range(self.prm['nAlternatives'])]
        self.prm['buttonCounter'][buttonClicked-1] = self.prm['buttonCounter'][buttonClicked-1] + 1

        if method == 'transformedUpDown':
            if self.prm['nTurnpoints'] < self.prm['initialTurnpoints']:
                stepSizeDown = self.prm['adaptiveStepSize1']
                stepSizeUp   = self.prm['adaptiveStepSize1']
            else:
                stepSizeDown = self.prm['adaptiveStepSize2']
                stepSizeUp   = self.prm['adaptiveStepSize2']
        elif method == 'weightedUpDown':
            if self.prm['nTurnpoints'] < self.prm['initialTurnpoints']:
                stepSizeDown = self.prm['adaptiveStepSize1']
                if self.prm['adaptiveType'] == self.tr("Arithmetic"):
                    stepSizeUp = self.prm['adaptiveStepSize1'] * (self.prm['percentCorrectTracked'] / (100-self.prm['percentCorrectTracked']))
                elif self.prm['adaptiveType'] == self.tr("Geometric"):
                    stepSizeUp = self.prm['adaptiveStepSize1'] ** (self.prm['percentCorrectTracked'] / (100-self.prm['percentCorrectTracked']))
            else:
                stepSizeDown = self.prm['adaptiveStepSize2']
                if self.prm['adaptiveType'] == self.tr("Arithmetic"):
                    stepSizeUp = self.prm['adaptiveStepSize2'] * (self.prm['percentCorrectTracked'] / (100-self.prm['percentCorrectTracked']))
                elif self.prm['adaptiveType'] == self.tr("Geometric"):
                    stepSizeUp = self.prm['adaptiveStepSize2'] ** (self.prm['percentCorrectTracked'] / (100-self.prm['percentCorrectTracked']))
            
        if buttonClicked == self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback("correct")
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback("neutral")
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback("off")
            
            self.fullFileLog.write(str(self.prm['adaptiveDifference']) + '; ')
            self.fullFileLines.append(str(self.prm['adaptiveDifference']) + '; ')
            self.fullFileLog.write('1; ')
            self.fullFileLines.append('1; ')
            if 'additional_parameters_to_write' in self.prm:
                for p in range(len(self.prm['additional_parameters_to_write'])):
                    self.fullFileLog.write(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileLines.append(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileLog.write(' ;')
                    self.fullFileLines.append(' ;')
            self.fullFileLog.write('\n')
            self.fullFileLines.append('\n')
            self.prm['correctCount'] = self.prm['correctCount'] + 1
            self.prm['incorrectCount'] = 0

            if self.prm['correctCount'] == self.prm['numberCorrectNeeded']:
                self.prm['correctCount'] = 0
                if self.prm['trackDir'] == self.tr('Up'):
                    self.prm['turnpointVal'].append(self.prm['adaptiveDifference'])
                    self.prm['nTurnpoints'] = self.prm['nTurnpoints'] +1
                    self.prm['trackDir'] = self.tr('Down')
                        
                if self.prm['adaptiveType'] == self.tr("Arithmetic"):
                    self.prm['adaptiveDifference'] = self.prm['adaptiveDifference'] - stepSizeDown
                elif self.prm['adaptiveType'] == self.tr("Geometric"):
                    self.prm['adaptiveDifference'] = self.prm['adaptiveDifference'] / stepSizeDown
                
        elif buttonClicked != self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback("incorrect")
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback("neutral")
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback("off")
                
            self.fullFileLog.write(str(self.prm['adaptiveDifference']) + '; ')
            self.fullFileLines.append(str(self.prm['adaptiveDifference']) + '; ')
            self.fullFileLog.write('0; ')
            self.fullFileLines.append('0; ')
            if 'additional_parameters_to_write' in self.prm:
                for p in range(len(self.prm['additional_parameters_to_write'])):
                    self.fullFileLog.write(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileLines.append(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileLog.write('; ')
                    self.fullFileLines.append('; ')
            self.fullFileLog.write('\n')
            self.fullFileLines.append('\n')
            
            self.prm['incorrectCount'] = self.prm['incorrectCount'] + 1
            self.prm['correctCount'] = 0

            if self.prm['incorrectCount'] == self.prm['numberIncorrectNeeded']:
                self.prm['incorrectCount'] = 0
                if self.prm['trackDir'] == self.tr('Down'):
                    self.prm['turnpointVal'].append(self.prm['adaptiveDifference'])
                    self.prm['nTurnpoints'] = self.prm['nTurnpoints'] +1
                    self.prm['trackDir'] = self.tr('Up')
                    
                if self.prm['adaptiveType'] == self.tr("Arithmetic"):
                    self.prm['adaptiveDifference'] = self.prm['adaptiveDifference'] + stepSizeUp
                elif self.prm['adaptiveType'] == self.tr("Geometric"):
                    self.prm['adaptiveDifference'] = self.prm['adaptiveDifference'] * stepSizeUp

        self.fullFileLog.flush()
        pcDone = (self.prm['nTurnpoints'] / self.prm['totalTurnpoints']) * 100
        bp = int(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'])
        pcThisRep = (bp-1) / self.prm['storedBlocks']*100 + 1 / self.prm['storedBlocks']*pcDone
        pcTot = (self.prm['currentRepetition'] - 1) / self.prm['allBlocks']['repetitions']*100 + 1 / self.prm['allBlocks']['repetitions']*pcThisRep
        self.gauge.setValue(pcTot)
        if self.prm['nTurnpoints'] == self.prm['totalTurnpoints']:
            self.writeResultsHeader('standard')
            #process results
            self.fullFileLog.write('\n')
            self.fullFileLines.append('\n')
            for i in range(len(self.fullFileLines)):
                self.fullFile.write(self.fullFileLines[i])
            for i in range(len(self.prm['turnpointVal'])):
                if i == self.prm['initialTurnpoints']:
                    self.resFile.write('| ')
                self.resFile.write('%5.2f ' %self.prm['turnpointVal'][i])
                self.resFileLog.write('%5.2f ' %self.prm['turnpointVal'][i])
                if i == self.prm['totalTurnpoints']-1:
                    self.resFile.write('| ')
            if self.prm['adaptiveType'] == self.tr("Arithmetic"):
                turnpointMean = mean(self.prm['turnpointVal'][self.prm['initialTurnpoints'] : self.prm['totalTurnpoints']])
                turnpointSd = std(self.prm['turnpointVal'][self.prm['initialTurnpoints'] : self.prm['totalTurnpoints']], ddof=1)
                self.resFile.write('\n\n')
                self.resFile.write('turnpointMean = %5.2f, s.d. = %5.2f \n' %(turnpointMean,turnpointSd))
                self.resFileLog.write('\n\n')
                self.resFileLog.write('turnpointMean = %5.2f, s.d. = %5.2f \n' %(turnpointMean,turnpointSd))
            elif self.prm['adaptiveType'] == self.tr("Geometric"):
                turnpointMean = geoMean(self.prm['turnpointVal'][self.prm['initialTurnpoints'] : self.prm['totalTurnpoints']])
                turnpointSd = geoSd(self.prm['turnpointVal'][self.prm['initialTurnpoints'] : self.prm['totalTurnpoints']])
                self.resFile.write('\n\n')
                self.resFile.write('geometric turnpointMean = %5.2f, s.d. = %5.2f \n' %(turnpointMean,turnpointSd))
                self.resFileLog.write('\n\n')
                self.resFileLog.write('geometric turnpointMean = %5.2f, s.d. = %5.2f \n' %(turnpointMean,turnpointSd))

            for i in range(self.prm['nAlternatives']):
                self.resFile.write("B{0} = {1}".format(i+1, self.prm['buttonCounter'][i]))
                self.resFileLog.write("B{0} = {1}".format(i+1, self.prm['buttonCounter'][i]))
                if i != self.prm['nAlternatives']-1:
                    self.resFile.write(', ')
                    self.resFileLog.write(', ')
            self.resFile.write('\n\n')
            self.resFile.flush()
            self.resFileLog.write('\n\n')
            self.resFileLog.flush()
            self.getEndTime()

            currBlock = 'b' + str(self.prm['currentBlock'])
            durString = '{0:5.3f}'.format(self.prm['blockEndTime'] - self.prm['blockStartTime'])
            resLineToWrite = '{0:5.3f}'.format(turnpointMean) + self.prm['pref']["general"]["csvSeparator"] + \
                             '{0:5.3f}'.format(turnpointSd) + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm[currBlock]['conditionLabel'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm['listener'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm['sessionLabel'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm['allBlocks']['experimentLabel'] + self.prm['pref']["general"]["csvSeparator"] +\
                             self.prm['blockEndDateString'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm['blockEndTimeString'] + self.prm['pref']["general"]["csvSeparator"] + \
                             durString + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm[currBlock]['blockPosition'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm[currBlock]['experiment'] + self.prm['pref']["general"]["csvSeparator"] +\
                             self.prm[currBlock]['paradigm'] + self.prm['pref']["general"]["csvSeparator"]
            resLineToWrite = self.getCommonTabFields(resLineToWrite)
            resLineToWrite = resLineToWrite + '\n'
            
            if method == 'transformedUpDown':
                self.writeResultsSummaryLine('Adaptive', resLineToWrite)
            elif method == 'weightedUpDown':
                self.writeResultsSummaryLine('Weighted Up/Down', resLineToWrite)

            self.atBlockEnd()
            
        else:
            self.doTrial()


    def sortResponseAdaptiveInterleaved(self, buttonClicked, method):
        if self.prm['startOfBlock'] == True:
            self.prm['correctCount'] = [0 for number in range(self.prm['nDifferences'])]
            self.prm['incorrectCount'] = [0 for number in range(self.prm['nDifferences'])]
            self.prm['nTurnpoints'] = [0 for number in range(self.prm['nDifferences'])]
            self.prm['startOfBlock'] = False
            self.prm['turnpointVal'] = [[] for number in range(self.prm['nDifferences'])]
            self.fullFileLines = []
            self.prm['buttonCounter'] = [[0 for a in range(self.prm['nAlternatives'])] for i in range(self.prm['nDifferences'])]
           
        trackNumber = self.prm['currentDifference']
        self.prm['buttonCounter'][trackNumber][buttonClicked-1] = self.prm['buttonCounter'][trackNumber][buttonClicked-1] + 1
            
        if method == 'weightedUpDown':
            if self.prm['nTurnpoints'][trackNumber] < self.prm['initialTurnpoints'][trackNumber]:
                stepSizeDown = self.prm['adaptiveStepSize1'][trackNumber]
                if self.prm['adaptiveType'] == self.tr("Arithmetic"):
                    stepSizeUp   = self.prm['adaptiveStepSize1'][trackNumber] * (self.prm['percentCorrectTracked'][trackNumber] / (100-self.prm['percentCorrectTracked'][trackNumber]))
                elif self.prm['adaptiveType'] == self.tr("Geometric"):
                    stepSizeUp   = self.prm['adaptiveStepSize1'][trackNumber] ** (self.prm['percentCorrectTracked'][trackNumber] / (100-self.prm['percentCorrectTracked'][trackNumber]))
            else:
                stepSizeDown = self.prm['adaptiveStepSize2'][trackNumber]
                if self.prm['adaptiveType'] == self.tr("Arithmetic"):
                    stepSizeUp   = self.prm['adaptiveStepSize2'][trackNumber] * (self.prm['percentCorrectTracked'][trackNumber] / (100-self.prm['percentCorrectTracked'][trackNumber]))
                elif self.prm['adaptiveType'] == self.tr("Geometric"):
                    stepSizeUp   = self.prm['adaptiveStepSize2'][trackNumber] ** (self.prm['percentCorrectTracked'][trackNumber] / (100-self.prm['percentCorrectTracked'][trackNumber]))
        elif method == 'transformedUpDown':
            if self.prm['nTurnpoints'][trackNumber] < self.prm['initialTurnpoints'][trackNumber]:
                stepSizeDown = self.prm['adaptiveStepSize1'][trackNumber]
                stepSizeUp   = self.prm['adaptiveStepSize1'][trackNumber]
            else:
                stepSizeDown = self.prm['adaptiveStepSize2'][trackNumber]
                stepSizeUp   = self.prm['adaptiveStepSize2'][trackNumber]
            
        if buttonClicked == self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback('correct')
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback('neutral')
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback('off')
            
            self.fullFileLog.write(str(self.prm['adaptiveDifference'][trackNumber]) + '; ')
            self.fullFileLines.append(str(self.prm['adaptiveDifference'][trackNumber]) + '; ')
            self.fullFileLog.write('TRACK %d; 1; ' %(trackNumber+1))
            self.fullFileLines.append('TRACK %d; 1; ' %(trackNumber+1))
            if 'additional_parameters_to_write' in self.prm:
                for p in range(len(self.prm['additional_parameters_to_write'])):
                    self.fullFileLog.write(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileLines.append(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileLog.write('; ')
                    self.fullFileLines.append('; ')
            self.fullFileLog.write('\n')
            self.fullFileLines.append('\n')
            self.prm['correctCount'][trackNumber] = self.prm['correctCount'][trackNumber] + 1
            self.prm['incorrectCount'][trackNumber] = 0

            if self.prm['correctCount'][trackNumber] == self.prm['numberCorrectNeeded'][trackNumber]:
                self.prm['correctCount'][trackNumber] = 0
                if self.prm['trackDir'][trackNumber] == self.tr('Up'):
                    self.prm['turnpointVal'][trackNumber].append(self.prm['adaptiveDifference'][trackNumber])
                    self.prm['nTurnpoints'][trackNumber] = self.prm['nTurnpoints'][trackNumber] +1
                    self.prm['trackDir'][trackNumber] = self.tr('Down')
                        
                if self.prm['adaptiveType'] == self.tr("Arithmetic"):
                    self.prm['adaptiveDifference'][trackNumber] = self.prm['adaptiveDifference'][trackNumber] - stepSizeDown
                elif self.prm['adaptiveType'] == self.tr("Geometric"):
                    self.prm['adaptiveDifference'][trackNumber] = self.prm['adaptiveDifference'][trackNumber] / stepSizeDown
                
        elif buttonClicked != self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback('incorrect')
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback('neutral')
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback('off')
                
            self.fullFileLog.write(str(self.prm['adaptiveDifference'][trackNumber]) + '; ')
            self.fullFileLines.append(str(self.prm['adaptiveDifference'][trackNumber]) + '; ')
            self.fullFileLog.write('TRACK %d; 0; ' %(trackNumber+1))
            self.fullFileLines.append('TRACK %d; 0; ' %(trackNumber+1))
            if 'additional_parameters_to_write' in self.prm:
                for p in range(len(self.prm['additional_parameters_to_write'])):
                    self.fullFileLog.write(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileLines.append(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileLog.write('; ')
                    self.fullFileLines.append('; ')
            self.fullFileLog.write('\n')
            self.fullFileLines.append('\n')
            
            self.prm['incorrectCount'][trackNumber] = self.prm['incorrectCount'][trackNumber] + 1
            self.prm['correctCount'][trackNumber] = 0

            if self.prm['incorrectCount'][trackNumber] == self.prm['numberIncorrectNeeded'][trackNumber]:
                self.prm['incorrectCount'][trackNumber] = 0
                if self.prm['trackDir'][trackNumber] == self.tr('Down'):
                    self.prm['turnpointVal'][trackNumber].append(self.prm['adaptiveDifference'][trackNumber])
                    self.prm['nTurnpoints'][trackNumber] = self.prm['nTurnpoints'][trackNumber] +1
                    self.prm['trackDir'][trackNumber] = self.tr('Up')
                    
                if self.prm['adaptiveType'] == self.tr("Arithmetic"):
                    self.prm['adaptiveDifference'][trackNumber] = self.prm['adaptiveDifference'][trackNumber] + stepSizeUp
                elif self.prm['adaptiveType'] == self.tr("Geometric"):
                    self.prm['adaptiveDifference'][trackNumber] = self.prm['adaptiveDifference'][trackNumber] * stepSizeUp
      
        self.fullFileLog.flush()
        currNTurnpoints = 0
        currTotTurnpoints = 0
        for i in range(self.prm['nDifferences']):
            currNTurnpoints = currNTurnpoints + min(self.prm['nTurnpoints'][i], self.prm['totalTurnpoints'][i])
            currTotTurnpoints = currTotTurnpoints + self.prm['totalTurnpoints'][i]
        pcDone = (currNTurnpoints / currTotTurnpoints) * 100
        bp = int(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'])
        pcThisRep = (bp-1) / self.prm['storedBlocks']*100 + 1 / self.prm['storedBlocks']*pcDone
        pcTot = (self.prm['currentRepetition'] - 1) / self.prm['allBlocks']['repetitions']*100 + 1 / self.prm['allBlocks']['repetitions']*pcThisRep
        self.gauge.setValue(pcTot)

        finished = 0
        for i in range(self.prm['nDifferences']):
            if self.prm['nTurnpoints'][i] >=  self.prm['totalTurnpoints'][i]:
                finished = finished + 1
        if finished == self.prm['nDifferences']:
            self.writeResultsHeader('standard')
            #process results
            self.fullFileLog.write('\n')
            self.fullFileLines.append('\n')
            for i in range(len(self.fullFileLines)):
                self.fullFile.write(self.fullFileLines[i])
            turnpointMeanList = []
            turnpointSdList = []
            for j in range(self.prm['nDifferences']):
                self.resFile.write('TRACK %d:\n' %(j+1))
                self.resFileLog.write('TRACK %d:\n' %(j+1))
                if self.prm['turnpointsToAverage'] == self.tr('All final stepsize (even)'):
                    tnpStart = self.prm['initialTurnpoints'][j]
                    tnpEnd = len(self.prm['turnpointVal'][j])
                    if (tnpEnd-tnpStart)%2 > 0: #odd number of turnpoints
                        tnpStart = self.prm['initialTurnpoints'][j] + 1
                elif self.prm['turnpointsToAverage'] == self.tr('First N final stepsize'):
                    tnpStart = self.prm['initialTurnpoints'][j]
                    tnpEnd = self.prm['totalTurnpoints'][j]
                elif self.prm['turnpointsToAverage'] == self.tr('Last N final stepsize'):
                    tnpStart = len(self.prm['turnpointVal'][j]) - (self.prm['totalTurnpoints'][j] - self.prm['initialTurnpoints'][j])
                    tnpEnd = len(self.prm['turnpointVal'][j])
                for i in range(len(self.prm['turnpointVal'][j])):
                    if i == (tnpStart):
                        self.resFile.write('| ')
                        self.resFileLog.write('| ')
                    self.resFile.write('%5.2f ' %self.prm['turnpointVal'][j][i])
                    self.resFileLog.write('%5.2f ' %self.prm['turnpointVal'][j][i])
                    if i == (tnpEnd-1):
                        self.resFile.write('| ')
                        self.resFileLog.write('| ')
                if self.prm['adaptiveType'] == self.tr("Arithmetic"):
                    turnpointMean = mean(self.prm['turnpointVal'][j][tnpStart : tnpEnd])
                    turnpointSd = std(self.prm['turnpointVal'][j][tnpStart : tnpEnd], ddof=1)
                    self.resFile.write('\n\n')
                    self.resFile.write('turnpointMean = %5.2f, s.d. = %5.2f \n' %(turnpointMean,turnpointSd))
                    self.resFileLog.write('\n\n')
                    self.resFileLog.write('turnpointMean = %5.2f, s.d. = %5.2f \n' %(turnpointMean,turnpointSd))
                    turnpointMeanList.append(turnpointMean)
                    turnpointSdList.append(turnpointSd)
                elif self.prm['adaptiveType'] == self.tr("Geometric"):
                    turnpointMean = geoMean(self.prm['turnpointVal'][j][tnpStart : tnpEnd])
                    turnpointSd = geoSd(self.prm['turnpointVal'][j][tnpStart : tnpEnd])
                    self.resFile.write('\n\n')
                    self.resFile.write('geometric turnpointMean = %5.2f, s.d. = %5.2f \n' %(turnpointMean,turnpointSd))
                    self.resFileLog.write('\n\n')
                    self.resFileLog.write('geometric turnpointMean = %5.2f, s.d. = %5.2f \n' %(turnpointMean,turnpointSd))
                    turnpointMeanList.append(turnpointMean)
                    turnpointSdList.append(turnpointSd)
                for a in range(self.prm['nAlternatives']):
                    self.resFile.write("B{0} = {1}".format(a+1, self.prm['buttonCounter'][j][a]))
                    self.resFileLog.write("B{0} = {1}".format(a+1, self.prm['buttonCounter'][j][a]))
                    if a != self.prm['nAlternatives']-1:
                        self.resFile.write(', ')
                        self.resFileLog.write(', ')
                if j != self.prm['nDifferences']-1:
                    self.resFile.write('\n\n')
                    self.resFileLog.write('\n\n')
            self.resFile.write('\n.\n')
            self.resFile.flush()
            self.resFileLog.write('\n.\n')
            self.resFileLog.flush()
            self.getEndTime()


            currBlock = 'b' + str(self.prm['currentBlock'])
            durString = '{0:5.3f}'.format(self.prm['blockEndTime'] - self.prm['blockStartTime'])
            resLineToWrite = ''
            for j in range(self.prm['nDifferences']):
                 resLineToWrite = resLineToWrite + '{0:5.3f}'.format(turnpointMeanList[j]) + self.prm['pref']["general"]["csvSeparator"] + \
                                  '{0:5.3f}'.format(turnpointSdList[j]) + self.prm['pref']["general"]["csvSeparator"] 
           
            resLineToWrite = resLineToWrite + self.prm[currBlock]['conditionLabel'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm['listener'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm['sessionLabel'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm['allBlocks']['experimentLabel'] + self.prm['pref']["general"]["csvSeparator"] +\
                             self.prm['blockEndDateString'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm['blockEndTimeString'] + self.prm['pref']["general"]["csvSeparator"] + \
                             durString + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm[currBlock]['blockPosition'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm[currBlock]['experiment'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm[currBlock]['paradigm'] + self.prm['pref']["general"]["csvSeparator"]

            resLineToWrite = self.getCommonTabFields(resLineToWrite)
            resLineToWrite = resLineToWrite + '\n'
            
            if method == 'transformedUpDown':
                self.writeResultsSummaryLine('Adaptive Interleaved', resLineToWrite)
            elif  method == 'weightedUpDown':
                self.writeResultsSummaryLine('Weighted Up/Down Interleaved', resLineToWrite)
            
            self.atBlockEnd()
          
        else:
            self.doTrial()

    def sortResponseConstantMIntervalsNAlternatives(self, buttonClicked):
        if self.prm['startOfBlock'] == True:
            self.prm['startOfBlock'] = False

            self.fullFileLines = []
            self.trialCount = 0
            self.correctCount = 0
            self.trialCountAll = 0

        self.trialCountAll = self.trialCountAll + 1
        if self.trialCountAll > self.prm['nPracticeTrials']:
            self.trialCount = self.trialCount + 1
        if buttonClicked == self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback('correct')
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback('neutral')
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback('off')

            if self.trialCountAll > self.prm['nPracticeTrials']:
                self.correctCount = self.correctCount + 1
            resp = '1'
        elif buttonClicked != self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback('incorrect')
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback('neutral')
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback('off')
            resp = '0'
        self.fullFileLog.write(resp + '; ')
        self.fullFileLines.append(resp + '; ')
        if 'additional_parameters_to_write' in self.prm:
            for p in range(len(self.prm['additional_parameters_to_write'])):
                self.fullFileLog.write(str(self.prm['additional_parameters_to_write'][p]))
                self.fullFileLines.append(str(self.prm['additional_parameters_to_write'][p]))
                self.fullFileLog.write('; ')
                self.fullFileLines.append('; ')
        self.fullFileLog.write('\n')
        self.fullFileLines.append('\n')
        self.fullFileLog.flush()
       
        pcDone = self.trialCountAll / (self.prm['nTrials']+self.prm['nPracticeTrials']) * 100
        bp = int(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'])
        pcThisRep = (bp-1) / self.prm['storedBlocks']*100 + 1 / self.prm['storedBlocks']*pcDone
        pcTot = (self.prm['currentRepetition'] - 1) / self.prm['allBlocks']['repetitions']*100 + 1 / self.prm['allBlocks']['repetitions']*pcThisRep
        self.gauge.setValue(pcTot)
        
        if self.trialCountAll >= (self.prm['nTrials'] + self.prm['nPracticeTrials']): # Block is completed
            self.writeResultsHeader('standard')
            for i in range(len(self.fullFileLines)):
                self.fullFile.write(self.fullFileLines[i])
            self.fullFileLog.write('\n')
            self.fullFile.write('\n')
            
            propCorr = self.correctCount/self.trialCount
            dp = dprime_mAFC(propCorr, self.prm['nAlternatives'])
            for ftyp in [self.resFile, self.resFileLog]:
                ftyp.write('No. Correct = %d\n' %(self.correctCount))
                ftyp.write('No. Total = %d\n' %(self.trialCount))
                ftyp.write('Percent Correct = %5.2f \n' %(self.correctCount/self.trialCount))
                ftyp.write('d-prime = %5.3f \n' %(dp))
                ftyp.write('\n')
          
                ftyp.flush()
                ftyp.flush()
            
            self.fullFile.flush()
            self.fullFileLog.flush()

            self.getEndTime()

            currBlock = 'b' + str(self.prm['currentBlock'])
            durString = '{0:5.3f}'.format(self.prm['blockEndTime'] - self.prm['blockStartTime'])
            
            #'dprime condition listener session experimentLabel nCorrectA nTotalA nCorrectB nTotalB nCorrect nTotal date time duration block experiment'
            resLineToWrite = ''
            resLineToWrite = resLineToWrite + '{0:5.3f}'.format(dp) + self.prm['pref']["general"]["csvSeparator"] + \
                             '{0:5.2f}'.format(self.correctCount/self.trialCount*100) + self.prm['pref']["general"]["csvSeparator"] + \
                             str(self.correctCount) + self.prm['pref']["general"]["csvSeparator"] + \
                             str(self.trialCount) + self.prm['pref']["general"]["csvSeparator"] +\
                             self.prm[currBlock]['conditionLabel'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm['listener'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm['sessionLabel'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm['allBlocks']['experimentLabel'] + self.prm['pref']["general"]["csvSeparator"] +\
                             self.prm['blockEndDateString'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm['blockEndTimeString'] + self.prm['pref']["general"]["csvSeparator"] + \
                             durString + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm[currBlock]['blockPosition'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm[currBlock]['experiment'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm[currBlock]['paradigm'] + self.prm['pref']["general"]["csvSeparator"]

            resLineToWrite = resLineToWrite + str(self.prm[currBlock]['nIntervals']) + self.prm['pref']["general"]["csvSeparator"] 
            resLineToWrite = resLineToWrite + str(self.prm[currBlock]['nAlternatives']) + self.prm['pref']["general"]["csvSeparator"]
            resLineToWrite = self.getCommonTabFields(resLineToWrite)

            resLineToWrite = resLineToWrite + '\n'
            self.writeResultsSummaryLine('Constant m-Intervals n-Alternatives', resLineToWrite)

            self.atBlockEnd()
           
        else: #block is not finished, move on to next trial
            self.doTrial()

    def sortResponseMultipleConstantsMIntervalsNAlternatives(self, buttonClicked):
        if self.prm['startOfBlock'] == True:
            self.prm['startOfBlock'] = False

            self.fullFileLines = []
            self.trialCount = {}
            self.correctCount = {}
            self.trialCountCnds = {}
            self.correctCountCnds = {}
            self.trialCountAllCnds = {}
            for i in range(len(self.prm['conditions'])):
                self.trialCountCnds[self.prm['conditions'][i]] = 0
                self.correctCountCnds[self.prm['conditions'][i]] = 0
                self.trialCountAllCnds[self.prm['conditions'][i]] = 0
                self.trialCount[i] = 0
                self.correctCount[i] = 0
            self.trialCountAll = 0

        self.trialCountAll = self.trialCountAll + 1
        self.trialCountAllCnds[self.currentCondition] = self.trialCountAllCnds[self.currentCondition] + 1
        if self.trialCountAllCnds[self.currentCondition] > self.prm['nPracticeTrials']:
            self.trialCountCnds[self.currentCondition] = self.trialCountCnds[self.currentCondition] + 1
            self.trialCount[self.prm['currentDifference']] = self.trialCount[self.prm['currentDifference']] + 1
        if buttonClicked == self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback('correct')
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback('neutral')
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback('off')

            if self.trialCountAllCnds[self.currentCondition] > self.prm['nPracticeTrials']:#if self.trialCountAll > self.prm['nPracticeTrials']:
                self.correctCountCnds[self.currentCondition] = self.correctCountCnds[self.currentCondition] + 1
                self.correctCount[self.prm['currentDifference']] = self.correctCount[self.prm['currentDifference']] + 1
            resp = '1'
        elif buttonClicked != self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback('incorrect')
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback('neutral')
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback('off')
            resp = '0'
        self.fullFileLog.write(self.currentCondition + '; ' + resp + '; ')
        self.fullFileLines.append(self.currentCondition + '; ' + resp + '; ')
        if 'additional_parameters_to_write' in self.prm:
            for p in range(len(self.prm['additional_parameters_to_write'])):
                self.fullFileLog.write(str(self.prm['additional_parameters_to_write'][p]))
                self.fullFileLines.append(str(self.prm['additional_parameters_to_write'][p]))
                self.fullFileLog.write('; ')
                self.fullFileLines.append('; ')
        self.fullFileLog.write('\n')
        self.fullFileLines.append('\n')
        self.fullFileLog.flush()
      
        pcDone = self.trialCountAll / (self.prm['nTrials'] + self.prm['nPracticeTrials'])*100
        bp = int(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'])
        pcThisRep = (bp-1) / self.prm['storedBlocks']*100 + 1 / self.prm['storedBlocks']*pcDone
        pcTot = (self.prm['currentRepetition'] - 1) / self.prm['allBlocks']['repetitions']*100 + 1 / self.prm['allBlocks']['repetitions']*pcThisRep
        self.gauge.setValue(pcTot)

        if self.trialCountAll >= (self.prm['nTrials'] + self.prm['nPracticeTrials'])*len(self.prm['conditions']): # Block is completed
            totalCorrectCount = 0
            totalTrialCount = 0
            for i in range(len(self.prm['conditions'])):
                totalTrialCount = totalTrialCount + self.trialCount[i]
                totalCorrectCount = totalCorrectCount + self.correctCountCnds[self.prm['conditions'][i]]
            self.writeResultsHeader('standard')
            for i in range(len(self.fullFileLines)):
                self.fullFile.write(self.fullFileLines[i])
            self.fullFileLog.write('\n')
            self.fullFile.write('\n')

            dprimeList = []
            for i in range(len(self.prm['conditions'])):
                thisPropCorr = (self.correctCountCnds[self.prm['conditions'][i]])/self.trialCountCnds[self.prm['conditions'][i]]
                thisdprime = dprime_mAFC(thisPropCorr, self.prm['nAlternatives'])
                dprimeList.append(thisdprime)
                for ftyp in [self.resFile, self.resFileLog]:
                    ftyp.write('CONDITION, ' + str(i+1) + '; ' + self.prm['conditions'][i] + '\n')
                    ftyp.write('No. Correct = %d\n' %(self.correctCountCnds[self.prm['conditions'][i]]))
                    ftyp.write('No. Total = %d \n' %((self.trialCountCnds[self.prm['conditions'][i]])))
                    ftyp.write('Percent Correct = %5.2f \n' %(thisPropCorr*100))
                    ftyp.write('d-prime = %5.3f \n' %(thisdprime))
                    ftyp.write('\n')

            propCorrAll = totalCorrectCount/totalTrialCount
            dprimeAll = dprime_mAFC(propCorrAll, self.prm['nAlternatives'])
            for ftyp in [self.resFile, self.resFileLog]:
                ftyp.write('CONDITION, ALL \n')
                ftyp.write('No. Correct = %d\n' %(totalCorrectCount))
                ftyp.write('No. Total = %d\n' %(totalTrialCount))
                ftyp.write('Percent Correct = %5.2f \n' %(propCorrAll*100))
                ftyp.write('d-prime = %5.3f \n' %(dprimeAll))
          
                ftyp.write('\n.\n\n')
                ftyp.flush()
            self.fullFile.flush()
            self.fullFileLog.flush()

            self.getEndTime()

            currBlock = 'b' + str(self.prm['currentBlock'])
            durString = '{0:5.3f}'.format(self.prm['blockEndTime'] - self.prm['blockStartTime'])
            
            resLineToWrite = ''
            for i in range(len(self.prm['conditions'])):
                resLineToWrite = resLineToWrite + '{0:5.3f}'.format(dprimeList[i]) + self.prm['pref']["general"]["csvSeparator"] + \
                                 '{0:5.2f}'.format((self.correctCountCnds[self.prm['conditions'][i]]*100)/self.trialCountCnds[self.prm['conditions'][i]]) + self.prm['pref']["general"]["csvSeparator"] + \
                                 str(self.correctCountCnds[self.prm['conditions'][i]]) + self.prm['pref']["general"]["csvSeparator"] + \
                                 str(self.trialCountCnds[self.prm['conditions'][i]]) + self.prm['pref']["general"]["csvSeparator"] 

            resLineToWrite = resLineToWrite + '{0:5.3f}'.format(dprimeAll) + self.prm['pref']["general"]["csvSeparator"] + \
                             str(totalCorrectCount/totalTrialCount*100) + self.prm['pref']["general"]["csvSeparator"] + \
                             str(totalCorrectCount) + self.prm['pref']["general"]["csvSeparator"] + \
                             str(totalTrialCount) + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm[currBlock]['conditionLabel'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm['listener'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm['sessionLabel'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm['allBlocks']['experimentLabel'] + self.prm['pref']["general"]["csvSeparator"] +\
                             self.prm['blockEndDateString'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm['blockEndTimeString'] + self.prm['pref']["general"]["csvSeparator"] + \
                             durString + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm[currBlock]['blockPosition'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm[currBlock]['experiment'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm[currBlock]['paradigm'] + self.prm['pref']["general"]["csvSeparator"]

            resLineToWrite = resLineToWrite + str(self.prm[currBlock]['nIntervals']) + self.prm['pref']["general"]["csvSeparator"] 
            resLineToWrite = resLineToWrite + str(self.prm[currBlock]['nAlternatives']) + self.prm['pref']["general"]["csvSeparator"]
            resLineToWrite = self.getCommonTabFields(resLineToWrite)

            resLineToWrite = resLineToWrite + '\n'
            self.writeResultsSummaryLine('Multiple Constants m-Intervals n-Alternatives', resLineToWrite)

            self.atBlockEnd()
            
        else: #block is not finished, move on to next trial
            remainingDifferences = []
            for key in self.trialCount.keys():
                if self.trialCount[key] < self.prm['nTrials']:
                    remainingDifferences.append(key)
            self.prm['currentDifference'] = random.choice(remainingDifferences)
            self.doTrial()
            

    def sortResponseConstant1Interval2Alternatives(self, buttonClicked):
        if self.prm['startOfBlock'] == True: #Initialize counts and data structures
            self.prm['startOfBlock'] = False

            self.fullFileLines = []
            self.correctCount = 0 #count of correct trials 
            self.trialCount = 0 #count of total trials 
            self.correctCountCnds = {} #count of correct trials by condition
            self.trialCountCnds = {} #count of total trials by condition
            
            for i in range(len(self.prm['conditions'])):
                self.trialCountCnds[self.prm['conditions'][i]] = 0
                self.correctCountCnds[self.prm['conditions'][i]] = 0
            self.trialCountAll = 0

        #Add one to trial counts
        self.trialCountAll = self.trialCountAll + 1
        if self.trialCountAll > self.prm['nPracticeTrials']:
            self.trialCountCnds[self.currentCondition] = self.trialCountCnds[self.currentCondition] + 1
            self.trialCount = self.trialCount + 1
        
        #if correct response, add one to correct resp. count
        if buttonClicked == self.correctButton: 
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback("correct")
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback("neutral")
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback("off")
            if self.trialCountAll > self.prm["nPracticeTrials"]:
                self.correctCountCnds[self.currentCondition] = self.correctCountCnds[self.currentCondition] + 1
                self.correctCount = self.correctCount + 1
            resp = '1'
        elif buttonClicked != self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback('incorrect')
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback('neutral')
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback('off')
            resp = '0'
            
        self.fullFileLog.write(self.currentCondition + '; ' + resp + '; ')
        self.fullFileLines.append(self.currentCondition + '; ' + resp + '; ')
        if 'additional_parameters_to_write' in self.prm:
            for p in range(len(self.prm['additional_parameters_to_write'])):
                self.fullFileLog.write(str(self.prm['additional_parameters_to_write'][p]))
                self.fullFileLines.append(str(self.prm['additional_parameters_to_write'][p]))
                self.fullFileLog.write('; ')
                self.fullFileLines.append('; ')
        self.fullFileLog.write('\n')
        self.fullFileLines.append('\n')
        self.fullFileLog.flush()

        #move percent done bar
        pcDone = self.trialCountAll/(self.prm['nTrials'] + self.prm['nPracticeTrials'])*100
        bp = int(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'])
        pcThisRep = (bp-1) / self.prm['storedBlocks']*100 + 1 / self.prm['storedBlocks']*pcDone
        pcTot = (self.prm['currentRepetition'] - 1) / self.prm['allBlocks']['repetitions']*100 + 1 / self.prm['allBlocks']['repetitions']*pcThisRep
        self.gauge.setValue(pcTot)

        #Completed all trials, compute stats
        if self.trialCountAll >= self.prm['nPracticeTrials'] + self.prm['nTrials']: # Block is completed
            self.writeResultsHeader('standard')
            for i in range(len(self.fullFileLines)):
                self.fullFile.write(self.fullFileLines[i])
            self.fullFileLog.write('\n')
            self.fullFile.write('\n')
            self.fullFile.flush()
            self.fullFileLog.flush()
             
            A_correct = self.correctCountCnds[self.prm['conditions'][0]]
            A_total = self.trialCountCnds[self.prm['conditions'][0]]
            B_correct = self.correctCountCnds[self.prm['conditions'][1]]
            B_total = self.trialCountCnds[self.prm['conditions'][1]]

            try:
                dp = dprime_yes_no_from_counts(A_correct, A_total, B_correct, B_total, self.prm['pref']['general']['dprimeCorrection'])
            except:
                dp = nan

            for ftyp in [self.resFile, self.resFileLog]:
                ftyp.write('No. Correct = %d\n' %(self.correctCount))
                ftyp.write('No. Total = %d\n' %(self.trialCount))
                ftyp.write('Percent Correct = %5.2f \n' %(self.correctCount/self.trialCount*100))
                ftyp.write("d-prime = %5.3f \n\n" %(dp))
            
                for i in range(len(self.prm['conditions'])):
                    try:
                        thisPercentCorrect = (self.correctCountCnds[self.prm['conditions'][i]]*100)/self.trialCountCnds[self.prm['conditions'][i]]
                    except:
                        thisPercentCorrect = nan
                    ftyp.write('No. Correct Condition %s = %d\n' %(self.prm['conditions'][i], self.correctCountCnds[self.prm['conditions'][i]]))
                    ftyp.write('No. Total Condition %s = %d \n' %(self.prm['conditions'][i], self.trialCountCnds[self.prm['conditions'][i]]))
                    ftyp.write('Percent Correct Condition %s = %5.2f \n' %(self.prm['conditions'][i], thisPercentCorrect))
                
                ftyp.write('\n\n')
                ftyp.flush()
          
            self.getEndTime()
           
            
            currBlock = 'b' + str(self.prm['currentBlock'])
            durString = '{0:5.3f}'.format(self.prm['blockEndTime'] - self.prm['blockStartTime'])
            
            #'dprime condition listener session experimentLabel nCorrectA nTotalA nCorrectB nTotalB nCorrect nTotal date time duration block experiment'
            resLineToWrite = '{0:5.3f}'.format(dp) + self.prm['pref']["general"]["csvSeparator"] 
            resLineToWrite = resLineToWrite + str(self.trialCount) + self.prm['pref']["general"]["csvSeparator"]
            for i in range(len(self.prm['conditions'])):
                resLineToWrite = resLineToWrite + str(self.correctCountCnds[self.prm['conditions'][i]]) + self.prm['pref']["general"]["csvSeparator"] + \
                                 str(self.trialCountCnds[self.prm['conditions'][i]]) + self.prm['pref']["general"]["csvSeparator"]
            resLineToWrite = resLineToWrite + self.prm[currBlock]['conditionLabel'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm['listener'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm['sessionLabel'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm['allBlocks']['experimentLabel'] + self.prm['pref']["general"]["csvSeparator"] +\
                             self.prm['blockEndDateString'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm['blockEndTimeString'] + self.prm['pref']["general"]["csvSeparator"] + \
                             durString + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm[currBlock]['blockPosition'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm[currBlock]['experiment'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm[currBlock]['paradigm'] + self.prm['pref']["general"]["csvSeparator"]
            resLineToWrite = self.getCommonTabFields(resLineToWrite)
            resLineToWrite = resLineToWrite + '\n'
            
            self.writeResultsSummaryLine('Constant 1-Interval 2-Alternatives', resLineToWrite)

            self.atBlockEnd()
           
        else: #block is not finished, move on to next trial
            self.doTrial()

 

    def sortResponseMultipleConstants1Interval2Alternatives(self, buttonClicked):
        if self.prm['startOfBlock'] == True:
            self.prm['startOfBlock'] = False

            self.fullFileLines = []
            self.trialCount = {}
            self.correctCount = {}
            self.trialCountCnds = {}
            self.correctCountCnds = {}
            self.trialCountAllCnds = {}
            for i in range(len(self.prm['conditions'])):
                self.trialCount[i] = 0
                self.correctCount[i] = 0
                self.trialCountCnds[self.prm['conditions'][i]] = {}
                self.correctCountCnds[self.prm['conditions'][i]] = {}
                self.trialCountAllCnds[self.prm['conditions'][i]] = 0
                for j in range(len(self.prm['subconditions'])):
                    self.trialCountCnds[self.prm['conditions'][i]][self.prm['subconditions'][j]] = 0
                    self.correctCountCnds[self.prm['conditions'][i]][self.prm['subconditions'][j]] = 0
            self.trialCountAll = 0

        self.trialCountAll = self.trialCountAll + 1
        self.trialCountAllCnds[self.currentCondition] =  self.trialCountAllCnds[self.currentCondition] + 1
        if self.trialCountAllCnds[self.currentCondition] > self.prm['nPracticeTrials']:
            self.trialCountCnds[self.currentCondition][self.currentSubcondition] = self.trialCountCnds[self.currentCondition][self.currentSubcondition] + 1
            self.trialCount[self.prm['currentDifference']] = self.trialCount[self.prm['currentDifference']] + 1

        if buttonClicked == self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback('correct')
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback('neutral')
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback('off')
            if self.trialCountAllCnds[self.currentCondition] > self.prm['nPracticeTrials']:
                self.correctCountCnds[self.currentCondition][self.currentSubcondition] = self.correctCountCnds[self.currentCondition][self.currentSubcondition] + 1
                self.correctCount[self.prm['currentDifference']] = self.correctCount[self.prm['currentDifference']] + 1

            resp = '1'
        elif buttonClicked != self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback('incorrect')
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback('neutral')
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback('off')
            resp = '0'
        self.fullFileLog.write(self.currentCondition + '; ' + self.currentSubcondition + '; ' + resp + '; ')
        self.fullFileLines.append(self.currentCondition + '; ' + self.currentSubcondition + '; ' + resp + '; ')
        if 'additional_parameters_to_write' in self.prm:
            for p in range(len(self.prm['additional_parameters_to_write'])):
                self.fullFileLog.write(str(self.prm['additional_parameters_to_write'][p]))
                self.fullFileLines.append(str(self.prm['additional_parameters_to_write'][p]))
                self.fullFileLog.write('; ')
                self.fullFileLines.append('; ')
        self.fullFileLog.write('\n')
        self.fullFileLines.append('\n')
        self.fullFileLog.flush()
     
        pcDone = (self.trialCountAll / ((self.prm['nTrials']+self.prm['nPracticeTrials']) * len(self.prm['conditions'])))*100
        bp = int(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'])
        pcThisRep = (bp-1) / self.prm['storedBlocks']*100 + 1 / self.prm['storedBlocks']*pcDone
        pcTot = (self.prm['currentRepetition'] - 1) / self.prm['allBlocks']['repetitions']*100 + 1 / self.prm['allBlocks']['repetitions']*pcThisRep
        self.gauge.setValue(pcTot)

        
        if self.trialCountAll >= (self.prm['nTrials'] + self.prm['nPracticeTrials'])*len(self.prm['conditions']): # Block is completed

            self.writeResultsHeader('standard')
            for i in range(len(self.fullFileLines)):
                self.fullFile.write(self.fullFileLines[i])
            self.fullFileLog.write('\n')
            self.fullFile.write('\n')

            totalCorrectCount = 0
            subconditionTrialCount = [0 for number in range(len(self.prm['subconditions']))]
            subconditionCorrectCount = [0 for number in range(len(self.prm['subconditions']))]
            A_correct = []
            A_total = []
            B_correct = []
            B_total = []
            dp = []
            totalTrialCount = 0
            for i in range(len(self.prm['conditions'])):
                totalTrialCount = totalTrialCount + self.trialCount[i]
                thisCondTotalCorrectCount = 0
                for j in range(len(self.prm['subconditions'])):
                    thisCondTotalCorrectCount = thisCondTotalCorrectCount + self.correctCountCnds[self.prm['conditions'][i]][self.prm['subconditions'][j]]
                    subconditionCorrectCount[j] = subconditionCorrectCount[j] + self.correctCountCnds[self.prm['conditions'][i]][self.prm['subconditions'][j]]
                    subconditionTrialCount[j] = subconditionTrialCount[j] + self.trialCountCnds[self.prm['conditions'][i]][self.prm['subconditions'][j]]
                totalCorrectCount = totalCorrectCount + thisCondTotalCorrectCount

                #compute d-prime for each condition
                A_correct.append(self.correctCountCnds[self.prm['conditions'][i]][self.prm['subconditions'][0]]) 
                A_total.append(self.trialCountCnds[self.prm['conditions'][i]][self.prm['subconditions'][0]])
                B_correct.append(self.correctCountCnds[self.prm['conditions'][i]][self.prm['subconditions'][1]]) 
                B_total.append(self.trialCountCnds[self.prm['conditions'][i]][self.prm['subconditions'][1]])

                try:
                    this_dp = dprime_yes_no_from_counts(nCA=A_correct[i], nTA=A_total[i], nCB=B_correct[i], nTB=B_total[i], corr=self.prm['pref']['general']['dprimeCorrection'])
                except:
                    this_dp = nan
                dp.append(this_dp)
                
                for ftyp in [self.resFile, self.resFileLog]:
                    ftyp.write('CONDITION: %d; %s \n' %(i+1, self.prm['conditions'][i]))
                    ftyp.write('No. Correct = %d\n' %(thisCondTotalCorrectCount))
                    ftyp.write('No. Total = %d\n' %(self.prm['nTrials']))
                    ftyp.write('Percent Correct = %5.2f \n' %(thisCondTotalCorrectCount/self.trialCount[i]*100))
                    ftyp.write("d-prime = %5.3f \n\n" %(this_dp))
                    

                for j in range(len(self.prm['subconditions'])):
                    try:
                        thisPercentCorrect = self.correctCountCnds[self.prm['conditions'][i]][self.prm['subconditions'][j]]/self.trialCountCnds[self.prm['conditions'][i]][self.prm['subconditions'][j]]*100
                    except:
                        thisPercentCorrect = nan
                    for ftyp in [self.resFile, self.resFileLog]:
                        ftyp.write('No. Correct Subcondition %s = %d\n' %(self.prm['subconditions'][j], self.correctCountCnds[self.prm['conditions'][i]][self.prm['subconditions'][j]]))
                        ftyp.write('No. Total Subcondition %s = %d \n' %(self.prm['subconditions'][j], self.trialCountCnds[self.prm['conditions'][i]][self.prm['subconditions'][j]]))
                        ftyp.write('Percent Correct Subcondition %s = %5.2f \n' %(self.prm['subconditions'][j], thisPercentCorrect))
                
                self.resFile.write('\n\n')
                self.resFileLog.write('\n\n')


            A_correct_ALL = subconditionCorrectCount[0]
            A_total_ALL = subconditionTrialCount[0]
            B_correct_ALL = subconditionCorrectCount[1]
            B_total_ALL = subconditionTrialCount[1]
            try:
                dp_ALL = dprime_yes_no_from_counts(nCA=A_correct_ALL, nTA=A_total_ALL, nCB=B_correct_ALL, nTB=B_total_ALL, corr=self.prm['pref']['general']['dprimeCorrection'])
            except:
                dp_ALL = nan

            for ftyp in [self.resFile, self.resFileLog]:
                ftyp.write('CONDITION: ALL \n')
                ftyp.write('No. Correct = %d\n' %(totalCorrectCount))
                ftyp.write('No Total = %d\n' %(totalTrialCount))
                ftyp.write('Percent Correct = %5.2f \n' %(totalCorrectCount/totalTrialCount*100))
                ftyp.write("d-prime = %5.3f \n\n" %(dp_ALL))

            for j in range(len(self.prm['subconditions'])):
                try:
                    thisPercentCorrect = subconditionCorrectCount[j]/subconditionTrialCount[j]*100
                except:
                    thisPercentCorrect = nan

                for ftyp in [self.resFile, self.resFileLog]:
                    ftyp.write('No. Correct Subcondition %s = %d\n' %(self.prm['subconditions'][j], subconditionCorrectCount[j]))
                    ftyp.write('No. Total Subcondition %s = %d \n' %(self.prm['subconditions'][j], subconditionTrialCount[j]))
                    ftyp.write('Percent Correct Subcondition %s = %5.2f \n' %(self.prm['subconditions'][j], thisPercentCorrect))

            self.resFile.write('\n')
            self.resFileLog.write('\n')
     
            
            self.resFile.write('.\n\n')
            self.resFile.flush()
            self.resFileLog.write('.\n\n')
            self.resFileLog.flush()
            self.fullFile.flush()
            self.fullFileLog.flush()

            self.getEndTime()

            currBlock = 'b' + str(self.prm['currentBlock'])
            durString = '{0:5.3f}'.format(self.prm['blockEndTime'] - self.prm['blockStartTime'])
           
            
            ## #'dprime condition listener session experimentLabel nCorrectA nTotalA nCorrectB nTotalB nCorrect nTotal date time duration block experiment'
            resLineToWrite = '{0:5.3f}'.format(dp_ALL) + self.prm['pref']["general"]["csvSeparator"] 
            resLineToWrite = resLineToWrite + str(totalTrialCount) + self.prm['pref']["general"]["csvSeparator"]
            for j in range(len(self.prm['subconditions'])):
                resLineToWrite = resLineToWrite + str(subconditionCorrectCount[j]) + self.prm['pref']["general"]["csvSeparator"] + \
                                 str(subconditionTrialCount[j]) + self.prm['pref']["general"]["csvSeparator"]
            for i in range(len(self.prm['conditions'])):
                resLineToWrite = resLineToWrite + '{0:5.3f}'.format(dp[i]) + self.prm['pref']["general"]["csvSeparator"] 
                resLineToWrite = resLineToWrite + str(self.trialCountCnds[self.prm['conditions'][i]][self.prm['subconditions'][0]] + self.trialCountCnds[self.prm['conditions'][i]][self.prm['subconditions'][1]]) + self.prm['pref']["general"]["csvSeparator"]
                for j in range(len(self.prm['subconditions'])):
                    resLineToWrite = resLineToWrite + str(self.correctCountCnds[self.prm['conditions'][i]][self.prm['subconditions'][j]]) + self.prm['pref']["general"]["csvSeparator"] + \
                            str(self.trialCountCnds[self.prm['conditions'][i]][self.prm['subconditions'][j]])  + self.prm['pref']["general"]["csvSeparator"]

            resLineToWrite = resLineToWrite + self.prm[currBlock]['conditionLabel'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm['listener'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm['sessionLabel'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm['allBlocks']['experimentLabel'] + self.prm['pref']["general"]["csvSeparator"] +\
                             self.prm['blockEndDateString'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm['blockEndTimeString'] + self.prm['pref']["general"]["csvSeparator"] + \
                             durString + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm[currBlock]['blockPosition'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm[currBlock]['experiment'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm[currBlock]['paradigm'] + self.prm['pref']["general"]["csvSeparator"]
            resLineToWrite = self.getCommonTabFields(resLineToWrite)
            resLineToWrite = resLineToWrite + '\n'
            self.writeResultsSummaryLine('Multiple Constants 1-Interval 2-Alternatives', resLineToWrite)

            self.atBlockEnd()
           
        else: #block is not finished, move on to next trial
            remainingDifferences = []
            for key in self.trialCount.keys():
                if self.trialCount[key] < self.prm['nTrials']:
                    remainingDifferences.append(key)
            self.prm['currentDifference'] = random.choice(remainingDifferences)
            self.doTrial()


    def sortResponseConstant1PairSameDifferent(self, buttonClicked):
        if self.prm['startOfBlock'] == True:
            self.prm['startOfBlock'] = False

            self.fullFileLines = []
            self.trialCount = 0
            self.trialCountCnds = {}
            self.correctCountCnds = {}
            for i in range(len(self.prm['conditions'])):
                self.trialCountCnds[self.prm['conditions'][i]] = 0
                self.correctCountCnds[self.prm['conditions'][i]] = 0
            self.trialCountAll = 0 #this includes as well the practice trials

        self.trialCountAll = self.trialCountAll + 1
        if self.trialCountAll > self.prm['nPracticeTrials']:
            self.trialCountCnds[self.currentCondition] = self.trialCountCnds[self.currentCondition] + 1
            self.trialCount = self.trialCount + 1
        if buttonClicked == self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback('correct')
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback('neutral')
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback('off')
            if self.trialCountAll > self.prm['nPracticeTrials']:
                self.correctCountCnds[self.currentCondition] = self.correctCountCnds[self.currentCondition] + 1
            resp = '1'
        elif buttonClicked != self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback('incorrect')
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback('neutral')
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback('off')
            resp = '0'
        self.fullFileLog.write(self.currentCondition + '; ' + resp + '; ')
        self.fullFileLines.append(self.currentCondition + '; ' + resp + '; ')
        if 'additional_parameters_to_write' in self.prm:
            for p in range(len(self.prm['additional_parameters_to_write'])):
                self.fullFileLog.write(str(self.prm['additional_parameters_to_write'][p]))
                self.fullFileLines.append(str(self.prm['additional_parameters_to_write'][p]))
                self.fullFileLog.write('; ')
                self.fullFileLines.append('; ')
        self.fullFileLog.write('\n')
        self.fullFileLines.append('\n')
        self.fullFileLog.flush()
        cnt = 0
        for i in range(len(self.prm['conditions'])):
            cnt = cnt + self.trialCountCnds[self.prm['conditions'][i]]
        pcDone = cnt / self.prm['nTrials'] * 100
        bp = int(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'])
        pcThisRep = (bp-1) / self.prm['storedBlocks']*100 + 1 / self.prm['storedBlocks']*pcDone
        pcTot = (self.prm['currentRepetition'] - 1) / self.prm['allBlocks']['repetitions']*100 + 1 / self.prm['allBlocks']['repetitions']*pcThisRep
        self.gauge.setValue(pcTot)

        
        if self.trialCountAll >= self.prm['nTrials'] + self.prm['nPracticeTrials']: # Block is completed
            totalCorrectCount = 0
            for i in range(len(self.prm['conditions'])):
                totalCorrectCount = totalCorrectCount + self.correctCountCnds[self.prm['conditions'][i]]
            self.writeResultsHeader('standard')
            for i in range(len(self.fullFileLines)):
                self.fullFile.write(self.fullFileLines[i])
            self.fullFileLog.write('\n')
            self.fullFile.write('\n')
            self.fullFile.flush()
            self.fullFileLog.flush()
            
            A_correct = self.correctCountCnds[self.prm['conditions'][0]]
            A_total = self.trialCountCnds[self.prm['conditions'][0]]
            B_correct = self.correctCountCnds[self.prm['conditions'][1]]
            B_total = self.trialCountCnds[self.prm['conditions'][1]]

            try:
                dp_IO = dprime_SD_from_counts(nCA=A_correct, nTA=A_total, nCB=B_correct, nTB=B_total, meth='IO', corr=self.prm['pref']['general']['dprimeCorrection'])
            except:
                dp_IO = nan
            try:
                dp_diff = dprime_SD_from_counts(nCA=A_correct, nTA=A_total, nCB=B_correct, nTB=B_total, meth='diff', corr=self.prm['pref']['general']['dprimeCorrection'])
            except:
                dp_diff = nan

            for ftyp in [self.resFile, self.resFileLog]:
                ftyp.write('No. Correct = %d\n' %(totalCorrectCount))
                ftyp.write('No. Total = %d\n' %(self.trialCount))
                ftyp.write('Percent Correct = %5.2f \n' %(totalCorrectCount/self.trialCount*100))
                ftyp.write("d-prime IO = %5.3f \n" %(dp_IO))
                ftyp.write("d-prime diff = %5.3f \n\n" %(dp_diff))
                
                for i in range(len(self.prm['conditions'])):
                    try:
                        thisPercentCorrect = (self.correctCountCnds[self.prm['conditions'][i]]*100)/self.trialCountCnds[self.prm['conditions'][i]]
                    except:
                        thisPercentCorrect = nan
                    ftyp.write('No. Correct Condition %s = %d\n' %(self.prm['conditions'][i], self.correctCountCnds[self.prm['conditions'][i]]))
                    ftyp.write('No. Total Condition %s = %d \n' %(self.prm['conditions'][i], self.trialCountCnds[self.prm['conditions'][i]]))
                    ftyp.write('Percent Correct Condition %s= %5.2f \n' %(self.prm['conditions'][i], thisPercentCorrect))
            
                ftyp.write('\n\n')
                ftyp.flush()

            self.getEndTime()
           
            currBlock = 'b' + str(self.prm['currentBlock'])
            durString = '{0:5.3f}'.format(self.prm['blockEndTime'] - self.prm['blockStartTime'])
            
            #'dprime condition listener session experimentLabel nCorrectA nTotalA nCorrectB nTotalB nCorrect nTotal date time duration block experiment'
            resLineToWrite = '{0:5.3f}'.format(dp_IO) + self.prm['pref']["general"]["csvSeparator"]
            resLineToWrite = resLineToWrite + '{0:5.3f}'.format(dp_diff) + self.prm['pref']["general"]["csvSeparator"] 
            resLineToWrite = resLineToWrite + str(self.trialCount) + self.prm['pref']["general"]["csvSeparator"]
            for i in range(len(self.prm['conditions'])):
                resLineToWrite = resLineToWrite + str(self.correctCountCnds[self.prm['conditions'][i]]) + self.prm['pref']["general"]["csvSeparator"] + \
                                 str(self.trialCountCnds[self.prm['conditions'][i]]) + self.prm['pref']["general"]["csvSeparator"]
            resLineToWrite = resLineToWrite + self.prm[currBlock]['conditionLabel'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm['listener'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm['sessionLabel'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm['allBlocks']['experimentLabel'] + self.prm['pref']["general"]["csvSeparator"] +\
                             self.prm['blockEndDateString'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm['blockEndTimeString'] + self.prm['pref']["general"]["csvSeparator"] + \
                             durString + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm[currBlock]['blockPosition'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm[currBlock]['experiment'] + self.prm['pref']["general"]["csvSeparator"] + \
                             self.prm[currBlock]['paradigm'] + self.prm['pref']["general"]["csvSeparator"]
            resLineToWrite = self.getCommonTabFields(resLineToWrite)
            resLineToWrite = resLineToWrite + '\n'
            self.writeResultsSummaryLine('Constant 1-Pair Same/Different', resLineToWrite)

            self.atBlockEnd()
           
        else: #block is not finished, move on to next trial
            self.doTrial()


    def sortResponseSameDifferent4(self, buttonClicked):
        if self.prm['startOfBlock'] == True:
            self.prm['startOfBlock'] = False

            self.fullFileLines = []
            self.trialCount = {}
            self.correctCount = {}
            for i in range(len(self.prm['conditions'])):
                self.trialCount[self.prm['conditions'][i]] = 0
                self.correctCount[self.prm['conditions'][i]] = 0
            self.trialCountAll = 0
        
        self.trialCount[self.currentCondition] = self.trialCount[self.currentCondition] + 1
        self.trialCountAll = self.trialCountAll + 1
        if buttonClicked == self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback('correct')
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback('neutral')
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback('off')
            self.correctCount[self.currentCondition] = self.correctCount[self.currentCondition] + 1
            resp = '1'
        elif buttonClicked != self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback('incorrect')
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback('neutral')
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback('off')
            resp = '0'
        self.fullFileLog.write(self.currentCondition + '; ' + resp + '; ')
        self.fullFileLines.append(self.currentCondition + '; ' + resp + '; ')
        if 'additional_parameters_to_write' in self.prm:
            for p in range(len(self.prm['additional_parameters_to_write'])):
                self.fullFileLog.write(str(self.prm['additional_parameters_to_write'][p]))
                self.fullFileLines.append(str(self.prm['additional_parameters_to_write'][p]))
                self.fullFileLog.write('; ')
                self.fullFileLines.append('; ')
        self.fullFileLog.write('\n')
        self.fullFileLines.append('\n')
        self.fullFileLog.flush()
        cnt = 0
        for i in range(len(self.prm['conditions'])):
            cnt = cnt + self.trialCount[self.prm['conditions'][i]]
        pcDone = cnt / self.prm['nTrials'] * 100
        bp = int(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'])
        pcThisRep = (bp-1) / self.prm['storedBlocks']*100 + 1 / self.prm['storedBlocks']*pcDone
        pcTot = (self.prm['currentRepetition'] - 1) / self.prm['allBlocks']['repetitions']*100 + 1 / self.prm['allBlocks']['repetitions']*pcThisRep
        self.gauge.setValue(pcTot)

        
        if self.trialCountAll >= self.prm['nTrials']: # Block is completed
            totalCorrectCount = 0
            for i in range(len(self.prm['conditions'])):
                totalCorrectCount = totalCorrectCount + self.correctCount[self.prm['conditions'][i]]
            self.writeResultsHeader('standard')
            for i in range(len(self.fullFileLines)):
                self.fullFile.write(self.fullFileLines[i])
            self.fullFileLog.write('\n')
            self.resFile.write('Number of Trials(%s) = %d\n' %(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'], self.prm['nTrials']))
            self.resFileLog.write('Number of Trials(%s) = %d\n' %(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'], self.prm['nTrials']))

            self.resFileLog.write('number correct(%s) = %d\n' %(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'], totalCorrectCount))
            self.resFileLog.write('percent correct(%s) = %5.2f \n' %(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'], totalCorrectCount/self.trialCountAll))
            self.resFile.write('number correct(%s) = %d\n' %(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'], totalCorrectCount))
            self.resFile.write('percent correct(%s) = %5.2f \n' %(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'], totalCorrectCount/self.trialCountAll))
            
            for i in range(len(self.prm['conditions'])):
                self.resFile.write('number correct(%s) Condition %s = %d\n' %(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'], self.prm['conditions'][i], self.correctCount[self.prm['conditions'][i]]))
                self.resFile.write('number total(%s) = %5.2f \n' %(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'], (self.trialCount[self.prm['conditions'][i]])))
                self.resFile.write('percent correct(%s) = %5.2f \n' %(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'], (self.correctCount[self.prm['conditions'][i]]*100)/self.trialCount[self.prm['conditions'][i]]))
                self.resFileLog.write('number correct(%s) Condition %s = %d\n' %(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'], self.prm['conditions'][i], self.correctCount[self.prm['conditions'][i]]))
                self.resFileLog.write('number total(%s) = %5.2f \n' %(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'], (self.trialCount[self.prm['conditions'][i]])))
                self.resFileLog.write('percent correct(%s) = %5.2f \n' %(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'], (self.correctCount[self.prm['conditions'][i]]*100)/self.trialCount[self.prm['conditions'][i]]))
          
            self.resFile.write('\n\n')
            self.resFile.flush()
            self.resFileLog.write('\n\n')
            self.resFileLog.flush()
            self.fullFile.flush()
            self.fullFileLog.flush()

            self.getEndTime()
            self.atBlockEnd()
           
        else: #block is not finished, move on to next trial
            self.doTrial()
        
    def whenFinished(self):
        if self.prm['currentRepetition'] == self.prm['allBlocks']['repetitions']:
            self.statusButton.setText(self.prm['rbTrans'].translate("rb", "Finished"))
            self.gauge.setValue(100)
            QApplication.processEvents()
            self.fullFile.close()
            self.resFile.close()
            self.fullFileLog.close()
            self.resFileLog.close()
            self.prm['shuffled'] = False
            if self.prm["allBlocks"]["procRes"] == True:
                self.processResultsEnd()
            if self.prm["allBlocks"]["procResTable"] == True:
                self.processResultsTableEnd()
            if self.prm["allBlocks"]["winPlot"] == True or self.prm["allBlocks"]["pdfPlot"] == True:
               self.plotDataEnd(winPlot=self.prm["allBlocks"]["winPlot"], pdfPlot = self.prm["allBlocks"]["pdfPlot"])

            if self.prm["pref"]["general"]["playEndMessage"] == True:
                self.playEndMessage()
            if self.prm['pref']['email']['sendData'] == True:
                self.sendData()

       
            commandsToExecute = []
            cmd1 = self.parseCustomCommandArguments(self.prm['allBlocks']['endExpCommand'])
            cmd2 = self.parseCustomCommandArguments(self.prm['pref']["general"]["atEndCustomCommand"])
            if len(cmd1) > 0:
                commandsToExecute.append(cmd1)
            if len(cmd2) > 0:
                commandsToExecute.append(cmd2)
            if len(commandsToExecute) > 0:
                self.executerThread.executeCommand(commandsToExecute)
      
            if self.prm['quit'] == True:
                self.parent().deleteLater()
        else:
            self.prm['currentRepetition'] = self.prm['currentRepetition'] + 1
            self.parent().moveToBlockPosition(1)
            if self.prm['allBlocks']['shuffleMode'] == self.tr('Auto'):
                self.parent().onClickShuffleBlocksButton()
                self.prm["shuffled"] = True
            elif self.prm['allBlocks']['shuffleMode'] == self.tr('Ask') and self.prm['shuffled'] == True:
                #if user shuffled on first repetion, then shuffle on each repetition, otherwise don't shuffle
                self.parent().onClickShuffleBlocksButton()
                self.prm["shuffled"] = True

            if self.prm['allBlocks']['responseMode'] == self.tr("Automatic") or self.prm['allBlocks']['responseMode'] == self.tr("Simulated Listener"):
                self.onClickStatusButton()
                
    def atBlockEnd(self):
        self.writeResultsFooter('log');  self.writeResultsFooter('standard')

        bp = int(self.prm['b'+str(self.prm["currentBlock"])]["blockPosition"])
        cb = (self.prm['currentRepetition']-1)*self.prm["storedBlocks"]+bp
        self.blockGauge.setValue(cb)
        self.blockGauge.setFormat(self.prm['rbTrans'].translate('rb', "Blocks Completed") +  ': ' + str(cb) + '/' + str(self.prm['storedBlocks']*self.prm['allBlocks']['repetitions']))
        
        if self.prm['allBlocks']['sendTriggers'] == True:
            thisSnd = pureTone(440, 0, -200, 80, 10, "Both", self.prm['allBlocks']['sampRate'], 100)
            playCmd = self.prm['pref']['sound']['playCommand']
            time.sleep(1)
            self.audioManager.playSoundWithTrigger(thisSnd, self.prm['allBlocks']['sampRate'], self.prm['allBlocks']['nBits'], playCmd, False, 'OFFTrigger.wav', self.prm["pref"]["general"]["OFFTrigger"])
            print("SENDING END TRIGGER", self.prm["pref"]["general"]["OFFTrigger"])

        if self.prm['currentRepetition'] == self.prm['allBlocks']['repetitions'] and int(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition']) + self.prm['pref']['email']['nBlocksNotify'] == self.prm['storedBlocks']:
            cmd = self.parseCustomCommandArguments(self.prm['pref']["general"]["nBlocksCustomCommand"])
            if len(cmd) > 0:
                self.executerThread.executeCommand([cmd])
            if self.prm['pref']['email']['notifyEnd'] == True:
                self.sendEndNotification()
        if int(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition']) < self.prm['storedBlocks']:
            self.parent().onClickNextBlockPositionButton()
            if self.prm['allBlocks']['responseMode'] == self.tr("Automatic") or self.prm['allBlocks']['responseMode'] == self.tr("Simulated Listener"):
                self.onClickStatusButton()
            else:
                return
        else:
            self.whenFinished()
        self.prm['cmdOutFileHandle'].flush()
        
    def getEndTime(self):
        self.prm['blockEndTime'] = time.time()
        self.prm['blockEndTimeStamp'] = QDateTime.toString(QDateTime.currentDateTime(), self.currLocale.dateTimeFormat(self.currLocale.ShortFormat)) 
        self.prm['blockEndDateString'] = QDate.toString(QDate.currentDate(), self.currLocale.dateFormat(self.currLocale.ShortFormat)) 
        self.prm['blockEndTimeString'] = QTime.toString(QTime.currentTime(), self.currLocale.timeFormat(self.currLocale.ShortFormat)) 
        
    def getStartTime(self):
        self.prm['blockStartTime'] = time.time()
        self.prm['blockStartTimeStamp'] = QDateTime.toString(QDateTime.currentDateTime(), self.currLocale.dateTimeFormat(self.currLocale.ShortFormat)) 
        self.prm['blockStartDateString'] = QDate.toString(QDate.currentDate(), self.currLocale.dateFormat(self.currLocale.ShortFormat)) 
        self.prm['blockStartTimeString'] = QTime.toString(QTime.currentTime(), self.currLocale.timeFormat(self.currLocale.ShortFormat)) 
        

    def writeResultsHeader(self, fileType):
        if fileType == 'log':
            resLogFilePath = self.prm['backupDirectoryName']  + time.strftime("%y-%m-%d_%H-%M-%S", time.localtime()) + '_' + self.prm['listener'] + '_log'
            resLogFullFilePath = self.prm['backupDirectoryName']  + time.strftime("%y-%m-%d_%H-%M-%S", time.localtime()) + '_' + self.prm['listener'] + 'full_log'
            self.resFileLog = open(resLogFilePath, 'a')
            self.fullFileLog = open(resLogFullFilePath, 'a')
            filesToWrite = [self.resFileLog, self.fullFileLog]
        elif fileType == 'standard':
            resFilePath = self.prm['resultsFile']
            fullFilePath = self.prm['resultsFile'].split('.txt')[0] + self.prm['pref']["general"]["fullFileSuffix"] + '.txt'
            self.resFile = open(resFilePath, 'a')
            self.fullFile = open(fullFilePath, 'a')
            filesToWrite = [self.resFile, self.fullFile]
            
        currBlock = 'b' + str(self.prm['currentBlock'])
        for i in range(2):
            thisFile = filesToWrite[i]
            thisFile.write('*******************************************************\n')
            thisFile.write('pychoacoustics version: ' + self.prm['version'] + '; build date: ' +  self.prm['builddate'] + '\n')
            if 'version' in self.prm[self.parent().currExp]:
                thisFile.write('Experiment version: ' + self.prm[self.parent().currExp]['version'] + '\n') 
            thisFile.write('Block Number: ' + str(self.prm['currentBlock']) + '\n')
            thisFile.write('Block Position: ' + self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'] + '\n')
            thisFile.write('Start: ' + self.prm['blockStartTimeStamp']+ '\n') 
            thisFile.write('+++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n')
            thisFile.write('Experiment Label: ' + self.prm['allBlocks']['experimentLabel'] + '\n')
            thisFile.write('Session Label: ' + self.prm['sessionLabel'] + '\n')
            thisFile.write('Condition Label: ' + self.prm[currBlock]['conditionLabel'] + '\n')
            thisFile.write('Experiment:    ' + self.prm[currBlock]['experiment'] + '\n')
            thisFile.write('Listener:      ' + self.prm['listener'] + '\n')
            thisFile.write('Response Mode: ' + self.prm['allBlocks']['responseMode'] + '\n')
            if self.prm['allBlocks']['responseMode'] == self.tr("Automatic"):
                thisFile.write('Auto Resp. Mode Perc. Corr.: ' + str(self.prm['allBlocks']['autoPCCorr']) + '\n')
            thisFile.write('Paradigm:      ' + self.prm['paradigm'] +'\n')
            thisFile.write('Intervals:     ' + self.currLocale.toString(self.prm['nIntervals']) + '\n')
            thisFile.write('Alternatives:  ' + self.currLocale.toString(self.prm['nAlternatives']) + '\n')
            for j in range(len(self.prm[currBlock]['paradigmChooser'])):
                thisFile.write(self.prm[currBlock]['paradigmChooserLabel'][j] +  ' ' + self.prm[currBlock]['paradigmChooser'][j] + '\n')
            for j in range(len(self.prm[currBlock]['paradigmField'])):
                thisFile.write(self.prm[currBlock]['paradigmFieldLabel'][j] +  ': ' + self.currLocale.toString(self.prm[currBlock]['paradigmField'][j], precision=self.prm["pref"]["general"]["precision"]) + '\n')
            thisFile.write('Phones:        ' + self.prm['allBlocks']['currentPhones'] + '\n')
            thisFile.write('Sample Rate:   ' + self.currLocale.toString(self.prm['allBlocks']['sampRate']) + '\n')
            thisFile.write('Bits:          ' + self.currLocale.toString(self.prm['allBlocks']['nBits']) + '\n')
            thisFile.write('Pre-Trial Silence (ms): ' + self.currLocale.toString(self.prm[currBlock]['preTrialSilence']) + '\n')
            thisFile.write('Warning Interval: ' + str(self.prm[currBlock]['warningInterval']) + '\n')
            thisFile.write('Interval Lights: ' + self.prm[currBlock]['intervalLights'] + '\n')
            if self.prm[currBlock]['warningInterval'] == self.tr("Yes"):
                thisFile.write('Warning Interval Duration (ms): ' + self.currLocale.toString(self.prm[currBlock]['warningIntervalDur']) + '\n')
                thisFile.write('Warning Interval ISI (ms): ' + self.currLocale.toString(self.prm[currBlock]['warningIntervalISI']) + '\n')
            thisFile.write('Response Light: ' + self.prm['responseLight'] + '\n')
            thisFile.write('Response Light Duration (ms): ' + self.currLocale.toString(self.prm[currBlock]['responseLightDuration']) + '\n')
            if self.prm[self.parent().currExp]["hasISIBox"] == True:
                thisFile.write('ISI:           ' + self.currLocale.toString(self.prm['isi']) + '\n\n')
            if self.prm[self.parent().currExp]["hasPreTrialInterval"] == True:
                thisFile.write('Pre-Trial Interval:           ' + self.prm[currBlock]['preTrialInterval'] + '\n\n')
                if self.prm[currBlock]['preTrialInterval'] == self.tr("Yes"):
                    thisFile.write('Pre-Trial Interval ISI:           ' + self.currLocale.toString(self.prm[currBlock]['preTrialIntervalISI']) + '\n\n')
            if self.prm[self.parent().currExp]["hasPrecursorInterval"] == True:
                thisFile.write('Precursor Interval:           ' + self.prm[currBlock]['precursorInterval'] + '\n\n')
                if self.prm[currBlock]['precursorInterval'] == self.tr("Yes"):
                    thisFile.write('Precursor Interval ISI:           ' + self.currLocale.toString(self.prm[currBlock]['precursorIntervalISI']) + '\n\n')
            if self.prm[self.parent().currExp]["hasPostcursorInterval"] == True:
                thisFile.write('Postcursor Interval:           ' + self.prm[currBlock]['postcursorInterval'] + '\n\n')
                if self.prm[currBlock]['postcursorInterval'] == self.tr("Yes"):
                    thisFile.write('Postcursor Interval ISI:           ' + self.currLocale.toString(self.prm[currBlock]['postcursorIntervalISI']) + '\n\n')

            for j in range(len(self.prm[currBlock]['chooser'])):
                if j not in self.parent().choosersToHide:
                    thisFile.write(self.parent().chooserLabel[j].text() + ' ' + self.prm[currBlock]['chooser'][j] + '\n')
            for j in range(len(self.prm[currBlock]['fileChooser'])):
                if j not in self.parent().fileChoosersToHide:
                    thisFile.write(self.parent().fileChooserButton[j].text() + ' ' + self.prm[currBlock]['fileChooser'][j] + '\n')
            for j in range(len(self.prm[currBlock]['field'])):
                if j not in self.parent().fieldsToHide and self.parent().fieldLabel[j].text()!= "Random Seed":
                    thisFile.write(self.parent().fieldLabel[j].text() + ':  ' + self.currLocale.toString(self.prm[currBlock]['field'][j]) + '\n')
            thisFile.write('+++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n')

            thisFile.flush()

    def writeResultsFooter(self, fileType):
        if fileType == 'log':
            filesToWrite = [self.resFileLog, self.fullFileLog]
        elif fileType == 'standard':
            filesToWrite = [self.resFile, self.fullFile]
        for i in range(2):
            thisFile = filesToWrite[i]
            #thisFile.write('*******************************************************\n\n')
            thisFile.write('End: ' + self.prm['blockEndTimeStamp'] + '\n') 
            thisFile.write('Duration: {} min. \n'.format( (self.prm['blockEndTime'] - self.prm['blockStartTime']) / 60 ))
            thisFile.write('\n')
            thisFile.flush()
            
    def writeResultsSummaryLine(self, paradigm, resultsLine):
        if paradigm in ['Adaptive', 'Weighted Up/Down']:
            headerToWrite = 'threshold_' +  self.prm['adaptiveType'].lower() + self.prm['pref']["general"]["csvSeparator"] + \
                            'SD' + self.prm['pref']["general"]["csvSeparator"] + \
                            'condition' + self.prm['pref']["general"]["csvSeparator"] + \
                            'listener' + self.prm['pref']["general"]["csvSeparator"] + \
                            'session'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'experimentLabel'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'date'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'time'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'duration'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'block'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'experiment' + self.prm['pref']["general"]["csvSeparator"] + \
                            'paradigm' + self.prm['pref']["general"]["csvSeparator"] 

        elif paradigm in ['Adaptive Interleaved', 'Weighted Up/Down Interleaved']:
            headerToWrite = ''
            for j in range(self.prm['nDifferences']):
                headerToWrite = headerToWrite + 'threshold_' + self.prm['adaptiveType'].lower() + '_track' + str(j+1) +  self.prm['pref']["general"]["csvSeparator"] + \
                                'SD_track'+ str(j+1) + self.prm['pref']["general"]["csvSeparator"]
            headerToWrite =  headerToWrite + 'condition' + self.prm['pref']["general"]["csvSeparator"] + \
                            'listener' + self.prm['pref']["general"]["csvSeparator"] + \
                            'session'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'experimentLabel'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'date'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'time'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'duration'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'block'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'experiment' + self.prm['pref']["general"]["csvSeparator"] + \
                            'paradigm' + self.prm['pref']["general"]["csvSeparator"] 
        elif paradigm in ['Constant 1-Interval 2-Alternatives']:
            headerToWrite =  'dprime' +  self.prm['pref']["general"]["csvSeparator"] + \
                            'nTotal'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'nCorrectA'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'nTotalA'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'nCorrectB'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'nTotalB'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'condition' + self.prm['pref']["general"]["csvSeparator"] + \
                            'listener' + self.prm['pref']["general"]["csvSeparator"] + \
                            'session'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'experimentLabel'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'date'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'time'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'duration'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'block'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'experiment' + self.prm['pref']["general"]["csvSeparator"] +\
                            'paradigm' + self.prm['pref']["general"]["csvSeparator"]
        elif paradigm in ['Constant 1-Pair Same/Different']:
            headerToWrite =  'dprime_IO' +  self.prm['pref']["general"]["csvSeparator"] + \
                            'dprime_diff' +  self.prm['pref']["general"]["csvSeparator"] + \
                            'nTotal'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'nCorrectA'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'nTotalA'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'nCorrectB'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'nTotalB'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'condition' + self.prm['pref']["general"]["csvSeparator"] + \
                            'listener' + self.prm['pref']["general"]["csvSeparator"] + \
                            'session'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'experimentLabel'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'date'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'time'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'duration'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'block'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'experiment' + self.prm['pref']["general"]["csvSeparator"] + \
                            'paradigm' + self.prm['pref']["general"]["csvSeparator"]
        elif paradigm in ['Multiple Constants 1-Interval 2-Alternatives']:
            headerToWrite =  'dprime_ALL' +  self.prm['pref']["general"]["csvSeparator"] + \
                            'nTotal_ALL'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'nCorrectA_ALL'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'nTotalA_ALL'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'nCorrectB_ALL'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'nTotalB_ALL'+ self.prm['pref']["general"]["csvSeparator"] 
            for j in range(len(self.prm['conditions'])):
                headerToWrite =  headerToWrite +  'dprime_subc' + str(j+1)+ self.prm['pref']["general"]["csvSeparator"] + \
                                'nTotal_subc'+  str(j+1) + self.prm['pref']["general"]["csvSeparator"] + \
                                'nCorrectA_subc'+  str(j+1)+ self.prm['pref']["general"]["csvSeparator"] + \
                                'nTotalA_subc'+  str(j+1)+ self.prm['pref']["general"]["csvSeparator"] + \
                                'nCorrectB_subc'+  str(j+1)+ self.prm['pref']["general"]["csvSeparator"] + \
                                'nTotalB_subc'+  str(j+1)+ self.prm['pref']["general"]["csvSeparator"]
                                
            headerToWrite = headerToWrite + 'condition' + self.prm['pref']["general"]["csvSeparator"] + \
                            'listener' + self.prm['pref']["general"]["csvSeparator"] + \
                            'session'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'experimentLabel'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'date'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'time'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'duration'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'block'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'experiment' + self.prm['pref']["general"]["csvSeparator"] + \
                            'paradigm' + self.prm['pref']["general"]["csvSeparator"] 
        elif paradigm in ['Constant m-Intervals n-Alternatives']:
            headerToWrite = ''
          
            headerToWrite = headerToWrite + 'dprime' +  self.prm['pref']["general"]["csvSeparator"] + \
                            'perc_corr' +  self.prm['pref']["general"]["csvSeparator"] + \
                            'n_corr'+ self.prm['pref']["general"]["csvSeparator"] +\
                            'n_trials' + self.prm['pref']["general"]["csvSeparator"]+\
                            'condition' + self.prm['pref']["general"]["csvSeparator"] + \
                            'listener' + self.prm['pref']["general"]["csvSeparator"] + \
                            'session'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'experimentLabel'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'date'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'time'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'duration' + self.prm['pref']["general"]["csvSeparator"] + \
                            'block'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'experiment' + self.prm['pref']["general"]["csvSeparator"] +\
                            'paradigm' + self.prm['pref']["general"]["csvSeparator"] +\
                            'nIntervals' + self.prm['pref']["general"]["csvSeparator"] + \
                            'nAlternatives' + self.prm['pref']["general"]["csvSeparator"]

        elif paradigm in ['Multiple Constants m-Intervals n-Alternatives']:
            headerToWrite = ''
            for i in range(len(self.prm['conditions'])):
                headerToWrite = headerToWrite + 'dprime_subc' + str(i+1) +  self.prm['pref']["general"]["csvSeparator"] + \
                                'perc_corr_subc' + str(i+1) +  self.prm['pref']["general"]["csvSeparator"] + \
                                'n_corr_subc'+ str(i+1) + self.prm['pref']["general"]["csvSeparator"] +\
                                'n_trials_subc'+ str(i+1) + self.prm['pref']["general"]["csvSeparator"]
                
            headerToWrite =  headerToWrite + 'tot_dprime' + self.prm['pref']["general"]["csvSeparator"] + \
                            'tot_perc_corr' + self.prm['pref']["general"]["csvSeparator"] + \
                            'tot_n_corr' + self.prm['pref']["general"]["csvSeparator"] + \
                            'tot_n_trials' + self.prm['pref']["general"]["csvSeparator"] + \
                            'condition' + self.prm['pref']["general"]["csvSeparator"] + \
                            'listener' + self.prm['pref']["general"]["csvSeparator"] + \
                            'session'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'experimentLabel'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'date'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'time'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'duration'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'block'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'experiment' + self.prm['pref']["general"]["csvSeparator"] +\
                            'paradigm' + self.prm['pref']["general"]["csvSeparator"] +\
                            'nIntervals' + self.prm['pref']["general"]["csvSeparator"] + \
                            'nAlternatives' + self.prm['pref']["general"]["csvSeparator"]

        currBlock = 'b'+str(self.prm['currentBlock'])
        for i in range(len(self.prm[currBlock]['fieldCheckBox'])):
            if self.prm[currBlock]['fieldCheckBox'][i] == True:
                headerToWrite = headerToWrite + self.prm[currBlock]['fieldLabel'][i] + self.prm['pref']["general"]["csvSeparator"]
        for i in range(len(self.prm[currBlock]['chooserCheckBox'])):
            if self.prm[currBlock]['chooserCheckBox'][i] == True:
                headerToWrite = headerToWrite + self.prm[currBlock]['chooserLabel'][i] + self.prm['pref']["general"]["csvSeparator"]
        for i in range(len(self.prm[currBlock]['fileChooserCheckBox'])):
            if self.prm[currBlock]['fileChooserCheckBox'][i] == True:
                headerToWrite = headerToWrite + self.prm[currBlock]['fileChooserButton'][i] + self.prm['pref']["general"]["csvSeparator"]
        for i in range(len(self.prm[currBlock]['paradigmFieldCheckBox'])):
            if self.prm[currBlock]['paradigmFieldCheckBox'][i] == True:
                headerToWrite = headerToWrite + self.prm[currBlock]['paradigmFieldLabel'][i] + self.prm['pref']["general"]["csvSeparator"]
        for i in range(len(self.prm[currBlock]['paradigmChooserCheckBox'])):
            if self.prm[currBlock]['paradigmChooserCheckBox'][i] == True:
                headerToWrite = headerToWrite + self.prm[currBlock]['paradigmChooserLabel'][i] + self.prm['pref']["general"]["csvSeparator"]

        if self.prm[self.parent().currExp]["hasISIBox"] == True:
            if self.prm[currBlock]['ISIValCheckBox'] == True:
                headerToWrite = headerToWrite + 'ISI (ms)' + self.prm['pref']["general"]["csvSeparator"]

        if paradigm not in ['Constant m-Intervals n-Alternatives', 'Multiple Constants m-Intervals n-Alternatives']:
            if self.prm[self.parent().currExp]["hasAlternativesChooser"] == True:
                if self.prm[currBlock]['nIntervalsCheckBox'] == True:
                    headerToWrite = headerToWrite + 'Intervals' + self.prm['pref']["general"]["csvSeparator"] 
                if self.prm[currBlock]['nAlternativesCheckBox'] == True:
                    headerToWrite = headerToWrite + 'Alternatives' + self.prm['pref']["general"]["csvSeparator"]

        if self.prm[currBlock]['responseLightCheckBox'] == True:
            headerToWrite = headerToWrite + 'Response Light' + self.prm['pref']["general"]["csvSeparator"]
        if self.prm[currBlock]['responseLightDurationCheckBox'] == True:
            headerToWrite = headerToWrite + 'Response Light Duration' + self.prm['pref']["general"]["csvSeparator"]
              
        headerToWrite = headerToWrite + '\n'
        if os.path.exists(self.prm['resultsFile'].split('.txt')[0]+ self.prm['pref']["general"]["resTableFileSuffix"]+'.csv') == False: #case 1 file does not exist yet
            self.resFileSummary = open(self.prm['resultsFile'].split('.txt')[0]+ self.prm['pref']["general"]["resTableFileSuffix"]+'.csv', 'w')
            self.resFileSummary.write(headerToWrite)
            self.resFileSummary.write(resultsLine)
            self.resFileSummary.close()
        else:
            self.resFileSummary = open(self.prm['resultsFile'].split('.txt')[0]+ self.prm['pref']["general"]["resTableFileSuffix"]+'.csv', 'r')
            allLines = self.resFileSummary.readlines()
            self.resFileSummary.close()
            try:
                h1idx = allLines.index(headerToWrite)
                headerPresent = True
            except:
                headerPresent = False

            if headerPresent == True:
                #('Header already present')
                nextHeaderFound = False
                for i in range(h1idx+1, len(allLines)):
                    #look for next 'experiment or end of file'
                    if  allLines[i][0:6] == 'dprime' or allLines[i][0:4] == 'perc' or allLines[i][0:9] == 'threshold':
                        nextHeaderFound = True
                        h2idx = i
                        break
                if nextHeaderFound == True:
                    #('Next Header Found')
                    allLines.insert(h2idx, resultsLine)
                else:
                    allLines.append(resultsLine)
                    #('Next Header Not Found Appending')
            elif headerPresent == False:
                allLines.append(headerToWrite)
                allLines.append(resultsLine)
            self.resFileSummary = open(self.prm['resultsFile'].split('.txt')[0]+ self.prm['pref']["general"]["resTableFileSuffix"]+'.csv', 'w')
            self.resFileSummary.writelines(allLines)
            self.resFileSummary.close()
            
    def getCommonTabFields(self, resLineToWrite):
        currBlock = 'b' + str(self.prm['currentBlock'])
        for i in range(len(self.prm[currBlock]['fieldCheckBox'])):
            if self.prm[currBlock]['fieldCheckBox'][i] == True:
                resLineToWrite = resLineToWrite + self.currLocale.toString(self.prm[currBlock]['field'][i], precision=self.prm["pref"]["general"]["precision"]) + self.prm['pref']["general"]["csvSeparator"]
        for i in range(len(self.prm[currBlock]['chooserCheckBox'])):
            if self.prm[currBlock]['chooserCheckBox'][i] == True:
                resLineToWrite = resLineToWrite + self.prm[currBlock]['chooser'][i].split(':')[0] + self.prm['pref']["general"]["csvSeparator"]

        for i in range(len(self.prm[currBlock]['fileChooserCheckBox'])):
            if self.prm[currBlock]['fileChooserCheckBox'][i] == True:
                resLineToWrite = resLineToWrite + self.prm[currBlock]['fileChooser'][i].split(':')[0] + self.prm['pref']["general"]["csvSeparator"]

        for i in range(len(self.prm[currBlock]['paradigmFieldCheckBox'])):
            if self.prm[currBlock]['paradigmFieldCheckBox'][i] == True:
                resLineToWrite = resLineToWrite + self.currLocale.toString(self.prm[currBlock]['paradigmField'][i],
                                                                           precision=self.prm["pref"]["general"]["precision"]) + self.prm['pref']["general"]["csvSeparator"]

        for i in range(len(self.prm[currBlock]['paradigmChooserCheckBox'])):
            if self.prm[currBlock]['paradigmChooserCheckBox'][i] == True:
                resLineToWrite = resLineToWrite + self.prm[currBlock]['paradigmChooser'][i].split(':')[0] + self.prm['pref']["general"]["csvSeparator"]

        if self.prm[self.parent().currExp]["hasISIBox"] == True:
            if self.prm[currBlock]['ISIValCheckBox'] == True:
                resLineToWrite = resLineToWrite + str(self.prm[currBlock]['ISIVal']) + self.prm['pref']["general"]["csvSeparator"]

        if  self.prm['paradigm'] not in ['Constant m-Intervals n-Alternatives', 'Multiple Constants m-Intervals n-Alternatives']:
            if self.prm[self.parent().currExp]["hasAlternativesChooser"] == True:
                if self.prm[currBlock]['nIntervalsCheckBox'] == True:
                    resLineToWrite = resLineToWrite + str(self.prm[currBlock]['nIntervals']) + self.prm['pref']["general"]["csvSeparator"] 
                if self.prm[currBlock]['nAlternativesCheckBox'] == True:
                    resLineToWrite = resLineToWrite + str(self.prm[currBlock]['nAlternatives']) + self.prm['pref']["general"]["csvSeparator"]
       
        if self.prm[currBlock]['responseLightCheckBox'] == True:
            resLineToWrite = resLineToWrite + self.prm[currBlock]['responseLight'] + self.prm['pref']["general"]["csvSeparator"]

        if self.prm[currBlock]['responseLightDurationCheckBox'] == True:
                resLineToWrite = resLineToWrite + self.currLocale.toString(self.prm[currBlock]['responseLightDuration']) + self.prm['pref']["general"]["csvSeparator"]

        return resLineToWrite

    def sendEndNotification(self):
        currBlock = 'b'+ str(self.prm['currentBlock'])
        subject = self.tr("Pychoacoustics Notification: Listener ") + self.prm['listener'] + self.tr(" has ") \
               + str(self.prm['pref']['email']['nBlocksNotify']) + self.tr(" block(s) to go")
        body = subject + "\n" + self.tr("Experiment: ") + self.parent().currExp + \
              '\n' + self.tr("Completed Blocks: ") + str(self.prm['currentBlock']) + self.tr(" Stored Blocks: ") + str(self.prm['storedBlocks'])
        self.emailThread.sendEmail(subject, body)

    def sendData(self):
        currBlock = 'b'+ str(self.prm['currentBlock'])
        subject = 'Pychoacoustics Data, Listener: ' + self.prm['listener'] +  ', Experiment: ' + \
               self.parent().currExp
        body = ''
        filesToSend = [self.pychovariablesSubstitute[self.pychovariables.index("[resFile]")],
                       self.pychovariablesSubstitute[self.pychovariables.index("[resFileFull]")],
                       self.pychovariablesSubstitute[self.pychovariables.index("[resTable]")]] #self.prm['resultsFile'], self.prm['resultsFile'].split('.txt')[0]+self.prm['pref']["general"]["fullFileSuffix"]+'.txt']
        if self.prm["allBlocks"]["procRes"] == True:
            filesToSend.append(self.pychovariablesSubstitute[self.pychovariables.index("[resFileRes]")])#self.prm['resultsFile'].split('.txt')[0] + self.prm['pref']["general"]["resFileSuffix"]+'.txt')
        if self.prm["allBlocks"]["procResTable"] == True:
            filesToSend.append(self.pychovariablesSubstitute[self.pychovariables.index("[resTableProcessed]")])
        if self.prm["allBlocks"]["pdfPlot"] == True:
            filesToSend.append(self.pychovariablesSubstitute[self.pychovariables.index("[pdfPlot]")])
        filesToSendChecked = []
        for fName in filesToSend:
            if os.path.exists(fName):
                filesToSendChecked.append(fName)
            else:
                print('Could not find: ', fName)
                       
                
        self.emailThread.sendEmail(subject, body, filesToSendChecked)

    def processResultsEnd(self):
        resFilePath = self.prm['resultsFile']
        if self.prm['paradigm'] in [self.tr("Adaptive"), self.tr("Weighted Up/Down")]:
            processResultsAdaptive([resFilePath])
        elif self.prm['paradigm'] in [self.tr("Adaptive Interleaved"), self.tr("Weighted Up/Down Interleaved")]:
            processResultsAdaptiveInterleaved([resFilePath])
        elif self.prm['paradigm'] in [self.tr("Constant 1-Interval 2-Alternatives")]:
            processResultsConstant1Interval2Alternatives([resFilePath], dprimeCorrection=self.prm['pref']['general']['dprimeCorrection'])
        elif self.prm['paradigm'] in [self.tr("Multiple Constants 1-Interval 2-Alternatives")]:
            processResultsMultipleConstants1Interval2Alternatives([resFilePath], dprimeCorrection=self.prm['pref']['general']['dprimeCorrection'])
        elif self.prm['paradigm'] in [self.tr("Constant m-Intervals n-Alternatives")]:
            processResultsConstantMIntervalsNAlternatives([resFilePath])
        elif self.prm['paradigm'] in [self.tr("Multiple Constants m-Intervals n-Alternatives")]:
            processResultsMultipleConstantsMIntervalsNAlternatives([resFilePath])
        elif self.prm['paradigm'] in [self.tr("Constant 1-Pair Same/Different")]:
            processResultsConstant1PairSameDifferent([resFilePath], dprimeCorrection=self.prm['pref']['general']['dprimeCorrection'])

    def processResultsTableEnd(self):
        separator = self.parent().prm['pref']["general"]["csvSeparator"]
        resFilePath = self.pychovariablesSubstitute[self.pychovariables.index("[resTable]")]
        if self.prm['paradigm'] in [self.tr("Adaptive"), self.tr("Weighted Up/Down")]:
            processResultsTableAdaptive([resFilePath], fout=None, separator=separator)
        elif self.prm['paradigm'] in [self.tr("Adaptive Interleaved"), self.tr("Weighted Up/Down Interleaved")]:
            processResultsTableAdaptiveInterleaved([resFilePath], fout=None, separator=separator)
        elif self.prm['paradigm'] in [self.tr("Constant 1-Interval 2-Alternatives")]:
            processResultsTableConstant1Int2Alt([resFilePath], fout=None, separator=separator, dprimeCorrection=self.prm['pref']['general']['dprimeCorrection'])
        elif self.prm['paradigm'] in [self.tr("Multiple Constants 1-Interval 2-Alternatives")]:
            processResultsTableMultipleConstants1Int2Alt([resFilePath], fout=None, separator=separator, dprimeCorrection=self.prm['pref']['general']['dprimeCorrection'])
        elif self.prm['paradigm'] in [self.tr("Constant m-Intervals n-Alternatives")]:
            processResultsTableConstantMIntNAlt([resFilePath], fout=None, separator=separator)
        elif self.prm['paradigm'] in [self.tr("Multiple Constants m-Intervals n-Alternatives")]:
            processResultsTableMultipleConstantsMIntNAlt([resFilePath], fout=None, separator=separator)
        elif self.prm['paradigm'] in [self.tr("Constant 1-Pair Same/Different")]:
            processResultsTableConstant1PairSameDifferent([resFilePath], fout=None, separator=separator, dprimeCorrection=self.prm['pref']['general']['dprimeCorrection'])

    def plotDataEnd(self, winPlot, pdfPlot):
        if self.prm['appData']['plotting_available']: 
            resFilePath = self.pychovariablesSubstitute[self.pychovariables.index("[resTable]")]
            summaryResFilePath = resFilePath.split('.csv')[0] + '_processed.csv'
            separator = self.parent().prm['pref']["general"]["csvSeparator"]

            if self.prm['paradigm'] in [self.tr("Adaptive"), self.tr("Weighted Up/Down")]:
                paradigm = 'adaptive'
            elif self.prm['paradigm'] in [self.tr("Adaptive Interleaved"), self.tr("Weighted Up/Down Interleaved")]:
                paradigm = 'adaptive_interleaved'
            elif self.prm['paradigm'] in [self.tr("Constant 1-Interval 2-Alternatives")]:
                paradigm = 'constant1Interval2Alternatives'
            elif self.prm['paradigm'] in [self.tr("Multiple Constants 1-Interval 2-Alternatives")]:
                paradigm = 'multipleConstants1Interval2Alternatives'
            elif self.prm['paradigm'] in [self.tr("Constant m-Intervals n-Alternatives")]:
                paradigm ='constantMIntervalsNAlternatives'
            elif self.prm['paradigm'] in [self.tr("Multiple Constants m-Intervals n-Alternatives")]:
                paradigm = 'multipleConstantsMIntervalsNAlternatives'
            elif self.prm['paradigm'] in [self.tr("Constant 1-Pair Same/Different")]:
                paradigm = 'constant1PairSD'

            categoricalPlot(self, 'average', summaryResFilePath, winPlot, pdfPlot, paradigm, separator, None, self.prm)
                
    def parseCustomCommandArguments(self, cmd):
        cmdList = []
        cmdSplit = cmd.split()
        for i in range(len(cmdSplit)):
            if cmdSplit[i] in self.pychovariables:
                idx = self.pychovariables.index(cmdSplit[i])
                cmdList.append(self.pychovariablesSubstitute[idx])
            else:
                cmdList.append(cmdSplit[i])
        parsedCmd = " ".join(cmdList)
        return parsedCmd
                
    def playEndMessage(self):
        idx = get_list_indices(self.prm['pref']['general']['endMessageFilesUse'], "\u2713")
        idChosen = random.choice(idx)
        msgSnd, fs = self.audioManager.loadWavFile(self.prm['pref']['general']['endMessageFiles'][idChosen], self.prm['pref']['general']['endMessageLevels'][idChosen], self.prm['allBlocks']['maxLevel'], 'Both')
        self.playThread.playThreadedSound(msgSnd, fs, self.prm['allBlocks']['nBits'], self.prm['pref']['sound']['playCommand'], False, 'foo.wav')

          
class responseLight(QWidget):
    def __init__(self, parent):
        super(responseLight, self).__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,
                                       QSizePolicy.Expanding))
        self.borderColor = Qt.black
        self.lightColor = Qt.black
    def giveFeedback(self, feedback):
        self.setStatus(feedback)
        self.parent().repaint()
        QApplication.processEvents()
        currBlock = 'b'+ str(self.parent().parent().prm['currentBlock'])
        time.sleep(self.parent().parent().prm[currBlock]['responseLightDuration']/1000.)
        self.setStatus('off')
        self.parent().repaint()
        QApplication.processEvents()
    def setStatus(self, status):
        if status == 'correct':
            self.lightColor = Qt.green
        elif status == 'incorrect':
            self.lightColor = Qt.red
        elif status == 'neutral':
            self.lightColor = Qt.white
        elif status == 'off':
            self.lightColor = Qt.black
    def paintEvent(self, event=None):
        painter = QPainter(self)
        painter.setViewport(0,0,self.width(),self.height())
        painter.setPen(self.borderColor)
        painter.setBrush(self.lightColor)
        painter.drawRect(self.width()/60, self.height()/60, self.width()-self.width()/30, self.height())

class intervalLight(QFrame):

    def __init__(self, parent):
        QFrame.__init__(self, parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.borderColor = Qt.red
        self.lightColor = Qt.black
    def setStatus(self, status):
        if status == 'on':
            self.lightColor = Qt.white
        elif status == 'off':
            self.lightColor = Qt.black
        self.parent().repaint()
        QApplication.processEvents()
    def paintEvent(self, event=None):
        painter = QPainter(self)
        painter.setViewport(0, 0, self.width(),self.height())
        painter.setPen(self.borderColor)
        painter.setBrush(self.lightColor)
        painter.fillRect(self.width()/60, self.height()/60, self.width()-self.width()/30, self.height(), self.lightColor)

class threadedPlayer(QThread):
    def __init__(self, parent):
        QThread.__init__(self, parent)
    def playThreadedSound(self, sound, sampRate, bits, cmd, writewav, fName):
        self.sound = sound
        self.sampRate = sampRate
        self.bits = bits
        self.cmd = cmd
        self.writewav = writewav
        self.fName = fName
        self.start()
        self.audioManager = self.parent().audioManager
    def run(self):
        self.audioManager.playSound(self.sound, self.sampRate, self.bits, self.cmd, self.writewav, self.fName)

class commandExecuter(QThread):
    def __init__(self, parent):
        QThread.__init__(self, parent)
    def executeCommand(self, cmd):
        self.cmd = cmd
        self.start()
    def run(self):
        for i in range(len(self.cmd)):
            os.system(self.cmd[i])

class emailSender(QThread):
    def __init__(self, parent):
        QThread.__init__(self, parent)
    def sendEmail(self, subject='', body='', attachments=[]):
        self.subject = subject
        self.body = body
        self.attachments = attachments
        self.start()
    def run(self):
        experimenterIdx = self.parent().prm['experimenter']['experimenter_id'].index(self.parent().prm['allBlocks']['currentExperimenter'])
        decoded_passwd = bytes(self.parent().prm['pref']['email']['fromPassword'], "utf-8")
        decoded_passwd = base64.b64decode(decoded_passwd)
        decoded_passwd = str(decoded_passwd, "utf-8")
        msg = MIMEMultipart()
        msg["From"] = self.parent().prm['pref']['email']['fromUsername']
        msg["To"] =  self.parent().prm['experimenter']['experimenter_email'][experimenterIdx]
        msg["Subject"] = self.subject
        part1 = MIMEText(self.body, 'plain')
        msg.attach(part1)

        for item in self.attachments:
            part = MIMEBase('application', "octet-stream")
            filePath = item
            part.set_payload(open(filePath, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(filePath))
            msg.attach(part)
        
        if checkEmailValid(msg["To"]) == False:
            errMsg = self.parent().tr("Experimenter {} e-mail's address {} not valid \n Please specify a valid address for the current experimenter \n in the Edit -> Experimenters dialog".format(self.parent().parent().prm['experimenter']['experimenter_id'][experimenterIdx], msg["To"]))
            print(errMsg, file=sys.stderr)
            return
        elif checkUsernameValid(msg["From"]) == False:
            errMsg = self.parent().tr("username invalid")
            print(errMsg, file=sys.stderr)
            return
        elif checkServerValid(self.parent().prm["pref"]["email"]['SMTPServer']) == False:
            errMsg = self.parent().tr("SMTP server name invalid")
            print(errMsg, file=sys.stderr)
            return

       
        if self.parent().prm["pref"]["email"]["serverRequiresAuthentication"] == True:
            if  self.parent().prm["pref"]["email"]['SMTPServerSecurity'] == "TLS/SSL (a)":
                try:
                    server = smtplib.SMTP_SSL(self.parent().prm["pref"]["email"]['SMTPServer'], self.parent().prm["pref"]["email"]['SMTPServerPort'])
                except Exception as ex:
                    errMsg = self.parent().tr("Something went wrong, try to change server settings \n {}".format(ex))
                    print(errMsg, file=sys.stderr)
                    return 
            elif self.parent().prm["pref"]["email"]['SMTPServerSecurity'] == "TLS/SSL (b)":
                try:
                    server = smtplib.SMTP(self.parent().prm["pref"]["email"]['SMTPServer'], self.parent().prm["pref"]["email"]['SMTPServerPort'])
                    server.ehlo()
                    server.starttls()
                except Exception as ex:
                    errMsg = self.parent().tr("Something went wrong, try to change server settings \n {}".format(ex))
                    print(errMsg, file=sys.stderr)
                    return 
            elif self.parent().prm["pref"]["email"]['SMTPServerSecurity'] == "none":
                try:
                    server = smtplib.SMTP(self.parent().prm["pref"]["email"]['SMTPServer'], self.parent().prm["pref"]["email"]['SMTPServerPort'])
                except Exception as ex:
                    errMsg = self.parent().tr("Something went wrong, try to change server settings \n {}".format(ex))
                    print(errMsg, file=sys.stderr)
                    return 
            # now attempt login    
            try:
                server.login(self.parent().prm['pref']['email']['fromUsername'],  decoded_passwd)
            except Exception as ex:
                errMsg = self.parent().tr("Something went wrong, try to change server settings \n {}".format(ex))
                print(errMsg, file=sys.stderr)
                return 
        else:
            try:
                server = smtplib.SMTP(self.parent().prm["pref"]["email"]['SMTPServer'], self.parent().prm["pref"]["email"]['SMTPServerPort'])
            except Exception as ex:
                errMsg = self.parent().tr("Something went wrong, try to change server settings \n {}".format(ex))
                print(errMsg, file=sys.stderr)
                return 
        try:
            server.sendmail(msg["From"], msg["To"], msg.as_string())
            print('e-mail sent successfully', file=sys.stdout)
        except Exception as ex:
            errMsg = self.parent().tr("Something went wrong, try to change server settings \n {}".format(ex))
            print(errMsg, file=sys.stderr)
            return 

