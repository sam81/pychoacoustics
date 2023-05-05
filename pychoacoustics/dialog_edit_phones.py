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
    from PyQt5.QtCore import QLocale, QThread
    from PyQt5.QtWidgets import QAbstractItemView, QComboBox, QDesktopWidget, QDialog, QDialogButtonBox, QGridLayout, QInputDialog, QLabel, QLineEdit, QMessageBox, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout
    from PyQt5.QtGui import QDoubleValidator, QIcon
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtCore import QLocale, QThread
    from PyQt6.QtWidgets import QAbstractItemView, QComboBox, QDialog, QDialogButtonBox, QGridLayout, QInputDialog, QLabel, QLineEdit, QMessageBox, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout
    from PyQt6.QtGui import QDoubleValidator, QIcon
import copy, pickle
from numpy import unique
from .audio_manager import*
#from .default_experiments.generate_stimuli import pureTone
#from .default_experiments.generate_stimuli import*
from .sndlib import*

class phonesDialog(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.prm = self.parent().prm
        self.currLocale = self.parent().prm['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.NumberOption.OmitGroupSeparator | self.currLocale.NumberOption.RejectGroupSeparator)
        if pyqtversion == 5:
            screen = QDesktopWidget().screenGeometry()
        elif pyqtversion == 6:
            screen = self.screen().geometry()
        self.resize(int(screen.width()/2.5), int(screen.height()/3))
        self.isPlaying = False
        #self.audioManager = audioManager(self)
        #self.playThread = threadedPlayer(self)
   
        self.sizer = QGridLayout() 
        self.v1Sizer = QVBoxLayout()
        self.v2Sizer = QVBoxLayout()
        self.calibSizer = QGridLayout()
        
        self.phonesTableWidget = QTableWidget()
        self.phonesTableWidget.setColumnCount(4)
        self.phonesTableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.phonesTableWidget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        
        self.phonesTableWidget.setHorizontalHeaderLabels([self.tr('Phones'), self.tr('Max Level'), self.tr('Default'), 'id'])
        self.phonesTableWidget.hideColumn(3)
        self.phonesTableWidget.cellDoubleClicked[int,int].connect(self.onCellDoubleClicked)

        #RENAME Phones BUTTON
        self.renamePhonesButton = QPushButton(self.tr("Rename Phones"), self)
        self.renamePhonesButton.clicked.connect(self.onEditLabel)
        #Change Level Phones BUTTON
        self.changeLevelPhonesButton = QPushButton(self.tr("Change Max Level"), self)
        self.changeLevelPhonesButton.clicked.connect(self.onEditMaxLevel)
        
        #ADD Phones BUTTON
        self.addPhonesButton = QPushButton(self.tr("Add Phones"), self)
        self.addPhonesButton.clicked.connect(self.onClickAddPhonesButton)
        #REMOVE Phones BUTTON
        self.removePhonesButton = QPushButton(self.tr("Remove Phones"), self)
        self.removePhonesButton.clicked.connect(self.onClickRemovePhonesButton)
        #Set Default Phones BUTTON
        self.setDefaultPhonesButton = QPushButton(self.tr("Set Default"), self)
        self.setDefaultPhonesButton.clicked.connect(self.onEditDefault)

        self.v1Sizer.addWidget(self.renamePhonesButton)
        self.v1Sizer.addWidget(self.changeLevelPhonesButton)
        self.v1Sizer.addWidget(self.addPhonesButton)
        self.v1Sizer.addWidget(self.removePhonesButton)
        self.v1Sizer.addWidget(self.setDefaultPhonesButton)
        self.v1Sizer.addStretch()
        self.phonesList = {}
    
        for i in range(len(self.prm['phones']['phonesChoices'])):
            currCount = i+1
            thisID = self.prm['phones']['phonesID'][i]
            self.phonesList[thisID] = {}
            self.phonesList[thisID]['label'] = self.prm['phones']['phonesChoices'][i]
            self.phonesList[thisID]['maxLevel'] = self.prm['phones']['phonesMaxLevel'][i]
            self.phonesList[thisID]['default'] = self.prm['phones']['defaultPhones'][i]
            self.phonesTableWidget.setRowCount(currCount)
            newItem = QTableWidgetItem(self.phonesList[thisID]['label'])
            newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.phonesTableWidget.setItem(currCount-1, 0, newItem)
            newItem = QTableWidgetItem(self.currLocale.toString(self.phonesList[thisID]['maxLevel']))
            newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.phonesTableWidget.setItem(currCount-1, 1, newItem)
            newItem = QTableWidgetItem(self.phonesList[thisID]['default'])
            newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.phonesTableWidget.setItem(currCount-1, 2, newItem)
            self.phonesList[thisID]['qid'] = QTableWidgetItem(thisID)
            self.phonesTableWidget.setItem(currCount-1, 3, self.phonesList[thisID]['qid'])

        ##CALIBRATION TONE
        n = 0
        self.calLabel = QLabel(self.tr('Calibration Tone:'), self)
        self.calibSizer.addWidget(self.calLabel, n, 0, 1, 2)
        n = n+1
        self.toneFreqLabel = QLabel(self.tr('Frequency (Hz)'), self)
        self.toneFreqTF = QLineEdit("1000")
        self.toneFreqTF.setValidator(QDoubleValidator(self))
        self.calibSizer.addWidget(self.toneFreqLabel, n, 0)
        self.calibSizer.addWidget(self.toneFreqTF, n, 1)
        n = n+1
        self.toneLevLabel = QLabel(self.tr('Level (dB)'), self)
        self.toneLevTF = QLineEdit("60")
        self.toneLevTF.setValidator(QDoubleValidator(self))
        self.calibSizer.addWidget(self.toneLevLabel, n, 0)
        self.calibSizer.addWidget(self.toneLevTF, n, 1)
        n = n+1
        self.toneDurLabel = QLabel(self.tr('Duration (ms)'), self)
        self.toneDurTF = QLineEdit("980")
        self.toneDurTF.setValidator(QDoubleValidator(self))
        self.calibSizer.addWidget(self.toneDurLabel, n, 0)
        self.calibSizer.addWidget(self.toneDurTF, n, 1)
        n = n+1
        self.toneRampsLabel = QLabel(self.tr('Ramps (ms)'), self)
        self.toneRampsTF = QLineEdit("10")
        self.toneRampsTF.setValidator(QDoubleValidator(self))
        self.calibSizer.addWidget(self.toneRampsLabel, n, 0)
        self.calibSizer.addWidget(self.toneRampsTF, n, 1)
        n = n+1
        self.earLabel = QLabel(self.tr('Ear:'), self)
        self.earChooser = QComboBox()
        self.earChooser.addItems([self.tr("Right"), self.tr("Left"), self.tr("Both")])
        self.calibSizer.addWidget(self.earLabel, n, 0)
        self.calibSizer.addWidget(self.earChooser, n, 1)
        n = n+1
        self.playCalibButton = QPushButton(self.tr("Play"), self)
        self.playCalibButton.clicked.connect(self.onClickPlayCalibButton)
        self.playCalibButton.setIcon(QIcon.fromTheme("media-playback-start", QIcon(":/media-playback-start")))
        self.calibSizer.addWidget(self.playCalibButton, n, 0, 1, 2)
        n = n+1
        self.stopCalibButton = QPushButton(self.tr("Stop"), self)
        self.stopCalibButton.clicked.connect(self.onClickStopCalibButton)
        self.stopCalibButton.setIcon(QIcon.fromTheme("media-playback-stop", QIcon(":/media-playback-stop")))
        self.calibSizer.addWidget(self.stopCalibButton, n, 0, 1, 2)
        if self.prm['pref']['sound']['playCommand'] in ["alsaaudio","pyaudio"]:
            self.stopCalibButton.show()
        else:
            self.stopCalibButton.hide()
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Apply|QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        buttonBox.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self.permanentApply)

        self.sizer.addLayout(self.v1Sizer, 0, 0)
        self.v2Sizer.addLayout(self.calibSizer)
        self.v2Sizer.addStretch()
        self.sizer.addWidget(self.phonesTableWidget, 0, 1)
        self.sizer.addLayout(self.v2Sizer, 0, 2)
        self.sizer.addWidget(buttonBox, 1,1,1,2)
        self.sizer.setColumnStretch(1,2)
        self.setLayout(self.sizer)
        self.setWindowTitle(self.tr("Edit Phones"))
        self.show()

    def onCellDoubleClicked(self, row, col):
        if col == 0:
            self.onEditLabel()
        elif col == 1:
            self.onEditMaxLevel()
        elif col == 2:
            self.onEditDefault()

    def onEditLabel(self):
        ids = self.findSelectedItemIds()
        if len(ids) > 1:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('Only one label can be renamed at a time'))
        elif len(ids) < 1:
            pass
        else:
            selectedSound = ids[0]
            msg = self.tr('New name:')
            text, ok = QInputDialog.getText(self, self.tr('Input Dialog'), msg)
            if ok:
                self.phonesTableWidget.item(self.phonesList[selectedSound]['qid'].row(), 0).setText(text)
                self.phonesList[selectedSound]['label'] = text
    def onEditMaxLevel(self):
        ids = self.findSelectedItemIds()
        if len(ids) > 1:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('Only one item can be edited at a time'))
        elif len(ids) < 1:
            pass
        else:
            selectedSound = ids[0]
            msg = self.tr('Level:')
            text, ok = QInputDialog.getDouble(self, self.tr('Input Dialog'), msg, self.phonesList[selectedSound]['maxLevel'])
            if ok:
                self.phonesTableWidget.item(self.phonesList[selectedSound]['qid'].row(), 1).setText(self.currLocale.toString(text))
                self.phonesList[selectedSound]['maxLevel'] = text

    def onEditDefault(self):
        ids = self.findSelectedItemIds()
        if len(ids) > 1:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('Only one item can be edited at a time'))
        elif len(ids) < 1:
            pass
        else:
            selectedSound = ids[0]
            for i in range(self.phonesTableWidget.rowCount()):
                 self.phonesTableWidget.item(i, 2).setText("\u2012")
                 self.phonesList[str(self.phonesTableWidget.item(i, 3).text())]['default'] = "\u2012"
            self.phonesTableWidget.item(self.phonesList[selectedSound]['qid'].row(), 2).setText("\u2713")
            self.phonesList[selectedSound]['default'] = "\u2713"

    def findSelectedItemIds(self):
        selItems = self.phonesTableWidget.selectedItems()
        selItemsRows = []
        for i in range(len(selItems)):
            selItemsRows.append(selItems[i].row())
        selItemsRows = unique(selItemsRows)
        selItemsIds = []
        for i in range(len(selItemsRows)):
            selItemsIds.append(str(self.phonesTableWidget.item(selItemsRows[i], 3).text()))
        return selItemsIds

    def permanentApply(self):
        self.prm['phones']['phonesChoices'] = []
        self.prm['phones']['phonesMaxLevel'] = []
        self.prm['phones']['defaultPhones'] = []
        self.prm['phones']['phonesID'] = []

        keys = sorted(self.phonesList.keys())
        for key in keys:
            self.prm['phones']['phonesChoices'].append(str(self.phonesList[key]['label']))
            self.prm['phones']['phonesMaxLevel'].append(self.phonesList[key]['maxLevel'])
            self.prm['phones']['defaultPhones'].append(self.phonesList[key]['default'])
            self.prm['phones']['phonesID'].append(key)
        f = open(self.parent().prm['phonesPrefFile'], 'wb')
        pickle.dump(self.parent().prm['phones'], f)
        f.close()
        for i in range(self.parent().phonesChooser.count()):
            self.parent().phonesChooser.removeItem(0)
        self.parent().phonesChooser.addItems(self.prm['phones']['phonesChoices'])

    def onClickAddPhonesButton(self):
        keys = sorted(self.phonesList.keys())
        thisID = str(int(keys[-1])+1)
        currCount = self.phonesTableWidget.rowCount() + 1

        self.phonesList[thisID] = {}
        self.phonesList[thisID]['label'] = 'Phones' + ' ' + str(currCount)
        self.phonesList[thisID]['maxLevel'] = 100
        self.phonesList[thisID]['default'] = "\u2012"
        self.phonesTableWidget.setRowCount(currCount)
        newItem = QTableWidgetItem(self.phonesList[thisID]['label'])
        newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
        self.phonesTableWidget.setItem(currCount-1, 0, newItem)
        newItem = QTableWidgetItem(self.currLocale.toString(self.phonesList[thisID]['maxLevel']))
        newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
        self.phonesTableWidget.setItem(currCount-1, 1, newItem)
        newItem = QTableWidgetItem(self.phonesList[thisID]['default'])
        newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
        self.phonesTableWidget.setItem(currCount-1, 2, newItem)
        self.phonesList[thisID]['qid'] = QTableWidgetItem(thisID)
        self.phonesTableWidget.setItem(currCount-1, 3, self.phonesList[thisID]['qid'])
      

    def onClickRemovePhonesButton(self):
        if self.phonesTableWidget.rowCount() == 1:
            ret = QMessageBox.warning(self, self.tr("Warning"),
                                            self.tr("Only one phone left. Cannot remove!"),
                                            QMessageBox.StandardButton.Ok)
        else:
            ids = self.findSelectedItemIds()
            wasDefault = False
            for i in range(len(ids)):
                selectedPhones = ids[i]
                if self.phonesTableWidget.item(self.phonesList[selectedPhones]['qid'].row(), 2).text() == "\u2713":
                    wasDefault = True 
                self.phonesTableWidget.removeRow(self.phonesList[selectedPhones]['qid'].row())
                del self.phonesList[selectedPhones]
            if wasDefault == True:
                self.phonesTableWidget.item(0, 2).setText("\u2713")
                self.phonesList[str(self.phonesTableWidget.item(0, 3).text())]['default'] = "\u2713"


    def onClickPlayCalibButton(self):
        ids = self.findSelectedItemIds()
        if len(ids) > 1:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('Only one label can be renamed at a time'))
            return
        elif len(ids) < 1:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('Please, select a phone in the table'))
            return
        else:
            selectedSound = ids[0]
            calMaxLev = self.phonesList[selectedSound]['maxLevel']
            frequency = self.currLocale.toDouble(self.toneFreqTF.text())[0]
            level = self.currLocale.toDouble(self.toneLevTF.text())[0]
            duration = self.currLocale.toDouble(self.toneDurTF.text())[0]
            ramp = self.currLocale.toDouble(self. toneRampsTF.text())[0]
            channel =  self.earChooser.currentText()
            fs = self.currLocale.toInt(self.parent().sampRateTF.text())[0]
            nBits = self.currLocale.toInt(self.parent().nBitsChooser.currentText())[0]
            calTone = pureTone(frequency, 0, level, duration, ramp, channel, fs, calMaxLev)
            self.isPlaying = True
            if self.prm['pref']['sound']['playCommand'] in ["alsaaudio","pyaudio"]:
                self.playThread = threadedAudioPlayer(self.parent())
            else:
                self.playThread = threadedExternalAudioPlayer(self.parent())
            self.playThread.playThreadedSound(calTone, fs, nBits, self.prm['pref']['sound']['playCommand'], True, 'calibrationTone.wav')
            if self.playThread.isFinished() == True:
                self.isPlaying = False

    def onClickStopCalibButton(self):
        if self.isPlaying == True:
            self.playThread.terminate()
            #self.playThread.__del__()

    def closeEvent(self, event):
        if self.isPlaying == True:
            #self.playThread.__del__()
            self.playThread.terminate()
        event.accept()
        
    def accept(self): #reimplement accept (i.e. ok button)
        if self.isPlaying == True:
            #self.playThread.__del__()
            self.playThread.terminate()
        QDialog.accept(self)
    def reject(self): #reimplement reject
        if self.isPlaying == True:
            #self.playThread.__del__()
            self.playThread.terminate()
        QDialog.reject(self)

   
