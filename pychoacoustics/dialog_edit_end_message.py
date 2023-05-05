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
    from PyQt5.QtWidgets import QAbstractItemView, QDialog, QDialogButtonBox, QFileDialog, QGridLayout, QInputDialog, QMessageBox, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtCore import QLocale, QThread
    from PyQt6.QtWidgets import QAbstractItemView, QDialog, QDialogButtonBox, QFileDialog, QGridLayout, QInputDialog, QMessageBox, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout
import copy, pickle
from numpy import unique
from .audio_manager import*

class wavListDialog(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.prm = self.parent().parent().prm
        self.audioManager = audioManager(self)
        self.currLocale = self.parent().parent().prm['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.NumberOption.OmitGroupSeparator | self.currLocale.NumberOption.RejectGroupSeparator)
        self.isPlaying = False
      
        self.sizer = QGridLayout() 
        self.v1Sizer = QVBoxLayout()
        
        self.wavsTableWidget = QTableWidget()
        self.wavsTableWidget.setColumnCount(4)
        self.wavsTableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.wavsTableWidget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        
        self.wavsTableWidget.setHorizontalHeaderLabels([self.tr("File"), self.tr('Use'), self.tr("RMS Level"), 'id'])
        self.quidColumn = 3
        self.wavsTableWidget.hideColumn(self.quidColumn)
        self.wavsTableWidget.cellDoubleClicked[int,int].connect(self.onCellDoubleClicked)

        
        #ADD wav BUTTON
        self.addWavButton = QPushButton(self.tr("Add Wav"), self)
        self.addWavButton.clicked.connect(self.onClickAddWavButton)
        #REMOVE wav BUTTON
        self.removeWavButton = QPushButton(self.tr("Remove Wav"), self)
        self.removeWavButton.clicked.connect(self.onClickRemoveWavButton)

        #PLAY wav BUTTON
        self.playWavButton = QPushButton(self.tr("Play Wav"), self)
        self.playWavButton.clicked.connect(self.onClickPlayWavButton)
        #STOP wav BUTTON
        self.stopWavButton = QPushButton(self.tr("Stop Playing"), self)
        self.stopWavButton.clicked.connect(self.onClickStopWavButton)
       
        self.v1Sizer.addWidget(self.addWavButton)
        self.v1Sizer.addWidget(self.removeWavButton)
        self.v1Sizer.addWidget(self.playWavButton)
        self.v1Sizer.addWidget(self.stopWavButton)
     
        self.v1Sizer.addStretch()

        self.wavsList = {}
    
        for i in range(len(self.parent().wavsPref['endMessageFiles'])):
            currCount = i+1
            thisID = self.parent().wavsPref['endMessageFilesID'][i]
            self.wavsList[thisID] = {}
            self.wavsList[thisID]['file'] = self.parent().wavsPref['endMessageFiles'][i]
            self.wavsList[thisID]['use'] = self.parent().wavsPref['endMessageFilesUse'][i]
            self.wavsList[thisID]['level'] = self.parent().wavsPref['endMessageLevels'][i]
            self.wavsTableWidget.setRowCount(currCount)
            n = 0
            newItem = QTableWidgetItem(self.wavsList[thisID]['file'])
            newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.wavsTableWidget.setItem(currCount-1, n, newItem)
            n = n+1
            newItem = QTableWidgetItem(self.wavsList[thisID]['use'])
            newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.wavsTableWidget.setItem(currCount-1, n, newItem)
            n = n+1
            newItem = QTableWidgetItem(self.currLocale.toString(self.wavsList[thisID]['level']))
            newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.wavsTableWidget.setItem(currCount-1, n, newItem)
            n = n+1
            self.wavsList[thisID]['qid'] = QTableWidgetItem(thisID)
            self.wavsTableWidget.setItem(currCount-1, n, self.wavsList[thisID]['qid'])

     
        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Apply|QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        self.sizer.addLayout(self.v1Sizer, 0, 0)
        self.sizer.addWidget(self.wavsTableWidget,0,1)
        self.sizer.addWidget(buttonBox, 1,1)
        self.setLayout(self.sizer)
        self.setWindowTitle(self.tr("Edit Wavs"))
        self.show()


    def onCellDoubleClicked(self, row, col):
        if col == 0:
            pass
        elif col == 1:
            self.onEditUse()
        elif col == 2:
            self.onEditLevel()

    def onEditLevel(self):
        ids = self.findSelectedItemIds()
        if len(ids) > 1:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('Only one item can be edited at a time'))
        elif len(ids) < 1:
            pass
        else:
            selectedSound = ids[0]
            msg = self.tr('RMS Level:')
            text, ok = QInputDialog.getDouble(self, self.tr('Input Dialog'), msg, self.wavsList[selectedSound]['level'])
            if ok:
                self.wavsTableWidget.item(self.wavsList[selectedSound]['qid'].row(), 2).setText(self.currLocale.toString(text))
                self.wavsList[selectedSound]['level'] = text

    def onEditUse(self):
        ids = self.findSelectedItemIds()
        if len(ids) > 1:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('Only one item can be edited at a time'))
        elif len(ids) < 1:
            pass
        else:
            selectedSound = ids[0]
            if self.wavsTableWidget.item(self.wavsList[selectedSound]['qid'].row(), 1).text() == "\u2012":
                self.wavsTableWidget.item(self.wavsList[selectedSound]['qid'].row(), 1).setText("\u2713")
                self.wavsList[selectedSound]['use'] = "\u2713"
            else:
                self.wavsTableWidget.item(self.wavsList[selectedSound]['qid'].row(), 1).setText("\u2012")
                self.wavsList[selectedSound]['use'] = "\u2012"
    def findSelectedItemIds(self):
        selItems = self.wavsTableWidget.selectedItems()
        selItemsRows = []
        for i in range(len(selItems)):
            selItemsRows.append(selItems[i].row())
        selItemsRows = unique(selItemsRows)
        selItemsIds = []
        for i in range(len(selItemsRows)):
            selItemsIds.append(str(self.wavsTableWidget.item(selItemsRows[i], self.quidColumn).text()))
        return selItemsIds

    def permanentApply(self):
        self.wavListToPass = {}
        self.wavListToPass['endMessageFiles'] = []
        self.wavListToPass['endMessageFilesUse'] = []
        self.wavListToPass['endMessageFilesID'] = []
        self.wavListToPass['endMessageLevels'] = []

        keys = sorted(self.wavsList.keys())
        for key in keys:
            self.wavListToPass['endMessageFiles'].append(str(self.wavsList[key]['file']))
            self.wavListToPass['endMessageFilesUse'].append(self.wavsList[key]['use'])
            self.wavListToPass['endMessageLevels'].append(self.wavsList[key]['level'])
            self.wavListToPass['endMessageFilesID'].append(key)
      

    def onClickAddWavButton(self):
        fName = QFileDialog.getOpenFileName(self, self.tr("Choose wav file to load"), '', self.tr("wav files (*.wav);;All Files (*)"))[0]
        if len(fName) > 0: #if the user didn't press cancel

            if len(self.wavsList.keys()) > 0:
                keys = sorted(self.wavsList.keys())
                thisID = str(int(keys[-1])+1)
            else:
                thisID = "1"
            currCount = self.wavsTableWidget.rowCount() + 1

            self.wavsList[thisID] = {}
            self.wavsList[thisID]['file'] = fName
            self.wavsList[thisID]['use'] = "\u2713"
            self.wavsList[thisID]['level'] = 60
            self.wavsTableWidget.setRowCount(currCount)
            n = 0
            newItem = QTableWidgetItem(self.wavsList[thisID]['file'])
            newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.wavsTableWidget.setItem(currCount-1, n, newItem)
            n = n+1
            newItem = QTableWidgetItem(self.wavsList[thisID]['use'])
            newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.wavsTableWidget.setItem(currCount-1, n, newItem)
            n = n+1
            newItem = QTableWidgetItem(self.currLocale.toString(self.wavsList[thisID]['level']))
            newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.wavsTableWidget.setItem(currCount-1, n, newItem)
            n = n+1
            self.wavsList[thisID]['qid'] = QTableWidgetItem(thisID)
            self.wavsTableWidget.setItem(currCount-1, n, self.wavsList[thisID]['qid'])
      

    def onClickRemoveWavButton(self):
        ids = self.findSelectedItemIds()
        for i in range(len(ids)):
            selectedWavs = ids[i]
            self.wavsTableWidget.removeRow(self.wavsList[selectedWavs]['qid'].row())
            del self.wavsList[selectedWavs]

    def onClickPlayWavButton(self):
        ids = self.findSelectedItemIds()
        if len(ids) < 1:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('No files selected for playing'))
        else:
            if len(ids) > 1:
                pass #maybe say on the status bar that only the first one will be played
            selectedWav = ids[0]
            fName = self.wavsList[selectedWav]['file']
            level = self.wavsList[selectedWav]['level']
            nBits = self.currLocale.toInt(self.parent().parent().nBitsChooser.currentText())[0]
            maxLevel = float(self.prm['phones']['phonesMaxLevel'][self.parent().parent().phonesChooser.currentIndex()])
            msgSnd, fs = self.audioManager.loadWavFile(fName, level, maxLevel, 'Both')
            self.isPlaying = True
            if self.prm['pref']['sound']['playCommand'] in ["alsaaudio","pyaudio"]:
                self.playThread = threadedAudioPlayer(self.parent().parent())
            else:
                self.playThread = threadedExternalAudioPlayer(self.parent().parent())
            self.playThread.playThreadedSound(msgSnd, fs, nBits, self.prm['pref']['sound']['playCommand'], False, 'tmp.wav')
            if self.playThread.isFinished == True:
                self.isPlaying = False
    def onClickStopWavButton(self):
        if self.isPlaying == True:
            self.playThread.terminate()
          
        
    def closeEvent(self, event):
        if self.isPlaying == True:
            self.playThread.terminate()
        event.accept()
        
    def accept(self): #reimplement accept (i.e. ok button)
        if self.isPlaying == True:
            self.playThread.terminate()
        QDialog.accept(self)
    def reject(self): #reimplement reject
        if self.isPlaying == True:
            self.playThread.terminate()
        QDialog.reject(self)
        
     
