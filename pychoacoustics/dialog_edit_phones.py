# -*- coding: utf-8 -*-

#   Copyright (C) 2008-2012 Samuele Carcagno <sam.carcagno@gmail.com>
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
from PyQt4.QtCore import QLocale, QThread
import copy, pickle
from numpy import unique
from .audio_manager import*
#from .default_experiments.generate_stimuli import pureTone
#from .default_experiments.generate_stimuli import*
from .sndlib import*


class phonesDialog(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.prm = self.parent().prm
        self.currLocale = self.parent().prm['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.OmitGroupSeparator | self.currLocale.RejectGroupSeparator)
        screen = QtGui.QDesktopWidget().screenGeometry()
        self.resize(screen.width()/2.5,screen.height()/3)
        self.isPlaying = False
        #self.audioManager = audioManager(self)
        #self.playThread = threadedPlayer(self)
   
        self.sizer = QtGui.QGridLayout() 
        self.v1Sizer = QtGui.QVBoxLayout()
        self.v2Sizer = QtGui.QVBoxLayout()
        self.calibSizer = QtGui.QGridLayout()
        
        self.phonesTableWidget = QtGui.QTableWidget()
        self.phonesTableWidget.setColumnCount(4)
        self.phonesTableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.phonesTableWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        
        self.phonesTableWidget.setHorizontalHeaderLabels([self.tr('Phones'), self.tr('Max Level'), self.tr('Default'), 'id'])
        self.phonesTableWidget.hideColumn(3)
        #self.connect(self.phonesTableWidget, QtCore.SIGNAL("cellDoubleClicked(int,int)"), self.onCellDoubleClicked)
        self.phonesTableWidget.cellDoubleClicked[int,int].connect(self.onCellDoubleClicked)

        #RENAME Phones BUTTON
        self.renamePhonesButton = QtGui.QPushButton(self.tr("Rename Phones"), self)
        #QtCore.QObject.connect(self.renamePhonesButton,
        #                       QtCore.SIGNAL('clicked()'), self.onEditLabel)
        self.renamePhonesButton.clicked.connect(self.onEditLabel)
        #Change Level Phones BUTTON
        self.changeLevelPhonesButton = QtGui.QPushButton(self.tr("Change Max Level"), self)
        #QtCore.QObject.connect(self.changeLevelPhonesButton,
        #                       QtCore.SIGNAL('clicked()'), self.onEditMaxLevel)
        self.changeLevelPhonesButton.clicked.connect(self.onEditMaxLevel)
        
        #ADD Phones BUTTON
        self.addPhonesButton = QtGui.QPushButton(self.tr("Add Phones"), self)
        #QtCore.QObject.connect(self.addPhonesButton,
        #                       QtCore.SIGNAL('clicked()'), self.onClickAddPhonesButton)
        self.addPhonesButton.clicked.connect(self.onClickAddPhonesButton)
        #REMOVE Phones BUTTON
        self.removePhonesButton = QtGui.QPushButton(self.tr("Remove Phones"), self)
        #QtCore.QObject.connect(self.removePhonesButton,
        #                       QtCore.SIGNAL('clicked()'), self.onClickRemovePhonesButton)
        self.removePhonesButton.clicked.connect(self.onClickRemovePhonesButton)
        #Set Default Phones BUTTON
        self.setDefaultPhonesButton = QtGui.QPushButton(self.tr("Set Default"), self)
        #QtCore.QObject.connect(self.setDefaultPhonesButton,
        #                       QtCore.SIGNAL('clicked()'), self.onEditDefault)
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
            newItem = QtGui.QTableWidgetItem(self.phonesList[thisID]['label'])
            newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.phonesTableWidget.setItem(currCount-1, 0, newItem)
            newItem = QtGui.QTableWidgetItem(self.currLocale.toString(self.phonesList[thisID]['maxLevel']))
            newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.phonesTableWidget.setItem(currCount-1, 1, newItem)
            newItem = QtGui.QTableWidgetItem(self.phonesList[thisID]['default'])
            newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.phonesTableWidget.setItem(currCount-1, 2, newItem)
            self.phonesList[thisID]['qid'] = QtGui.QTableWidgetItem(thisID)
            self.phonesTableWidget.setItem(currCount-1, 3, self.phonesList[thisID]['qid'])



        ##CALIBRATION TONE
        n = 0
        self.calLabel = QtGui.QLabel(self.tr('Calibration Tone:'), self)
        self.calibSizer.addWidget(self.calLabel, n, 0, 1, 2)
        n = n+1
        self.toneFreqLabel = QtGui.QLabel(self.tr('Frequency (Hz)'), self)
        self.toneFreqTF = QtGui.QLineEdit("1000")
        self.toneFreqTF.setValidator(QtGui.QDoubleValidator(self))
        self.calibSizer.addWidget(self.toneFreqLabel, n, 0)
        self.calibSizer.addWidget(self.toneFreqTF, n, 1)
        n = n+1
        self.toneLevLabel = QtGui.QLabel(self.tr('Level (dB)'), self)
        self.toneLevTF = QtGui.QLineEdit("60")
        self.toneLevTF.setValidator(QtGui.QDoubleValidator(self))
        self.calibSizer.addWidget(self.toneLevLabel, n, 0)
        self.calibSizer.addWidget(self.toneLevTF, n, 1)
        n = n+1
        self.toneDurLabel = QtGui.QLabel(self.tr('Duration (ms)'), self)
        self.toneDurTF = QtGui.QLineEdit("4980")
        self.toneDurTF.setValidator(QtGui.QDoubleValidator(self))
        self.calibSizer.addWidget(self.toneDurLabel, n, 0)
        self.calibSizer.addWidget(self.toneDurTF, n, 1)
        n = n+1
        self.toneRampsLabel = QtGui.QLabel(self.tr('Ramps (ms)'), self)
        self.toneRampsTF = QtGui.QLineEdit("10")
        self.toneRampsTF.setValidator(QtGui.QDoubleValidator(self))
        self.calibSizer.addWidget(self.toneRampsLabel, n, 0)
        self.calibSizer.addWidget(self.toneRampsTF, n, 1)
        n = n+1
        self.earLabel = QtGui.QLabel(self.tr('Ear:'), self)
        self.earChooser = QtGui.QComboBox()
        self.earChooser.addItems([self.tr("Right"), self.tr("Left"), self.tr("Both")])
        self.calibSizer.addWidget(self.earLabel, n, 0)
        self.calibSizer.addWidget(self.earChooser, n, 1)
        n = n+1
        self.playCalibButton = QtGui.QPushButton(self.tr("Play"), self)
        #QtCore.QObject.connect(self.playCalibButton,
        #                       QtCore.SIGNAL('clicked()'), self.onClickPlayCalibButton)
        self.playCalibButton.clicked.connect(self.onClickPlayCalibButton)
        self.playCalibButton.setIcon(QtGui.QIcon.fromTheme("media-playback-start", QtGui.QIcon(":/media-playback-start")))
        self.calibSizer.addWidget(self.playCalibButton, n, 0, 1, 2)
        n = n+1
        self.stopCalibButton = QtGui.QPushButton(self.tr("Stop"), self)
        #QtCore.QObject.connect(self.stopCalibButton,
        #                       QtCore.SIGNAL('clicked()'), self.onClickStopCalibButton)
        self.stopCalibButton.clicked.connect(self.onClickStopCalibButton)
        self.stopCalibButton.setIcon(QtGui.QIcon.fromTheme("media-playback-stop", QtGui.QIcon(":/media-playback-stop")))
        self.calibSizer.addWidget(self.stopCalibButton, n, 0, 1, 2)

        
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Cancel)
        
        #self.connect(buttonBox, QtCore.SIGNAL("accepted()"),
        #             self, QtCore.SLOT("accept()"))
        #self.connect(buttonBox, QtCore.SIGNAL("rejected()"),
        #             self, QtCore.SLOT("reject()"))
        #self.connect(buttonBox.button(QtGui.QDialogButtonBox.Apply),
        #             QtCore.SIGNAL("clicked()"), self.permanentApply)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        buttonBox.button(QtGui.QDialogButtonBox.Apply).clicked.connect(self.permanentApply)

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
            QtGui.QMessageBox.warning(self, self.tr('Warning'), self.tr('Only one label can be renamed at a time'))
        elif len(ids) < 1:
            pass
        else:
            selectedSound = ids[0]
            msg = self.tr('New name:')
            text, ok = QtGui.QInputDialog.getText(self, self.tr('Input Dialog'), msg)
            if ok:
                self.phonesTableWidget.item(self.phonesList[selectedSound]['qid'].row(), 0).setText(text)
                self.phonesList[selectedSound]['label'] = text
    def onEditMaxLevel(self):
        ids = self.findSelectedItemIds()
        if len(ids) > 1:
            QtGui.QMessageBox.warning(self, self.tr('Warning'), self.tr('Only one item can be edited at a time'))
        elif len(ids) < 1:
            pass
        else:
            selectedSound = ids[0]
            msg = self.tr('Level:')
            text, ok = QtGui.QInputDialog.getDouble(self, self.tr('Input Dialog'), msg, self.phonesList[selectedSound]['maxLevel'])
            if ok:
                self.phonesTableWidget.item(self.phonesList[selectedSound]['qid'].row(), 1).setText(self.currLocale.toString(text))
                self.phonesList[selectedSound]['maxLevel'] = text

    def onEditDefault(self):
        ids = self.findSelectedItemIds()
        if len(ids) > 1:
            QtGui.QMessageBox.warning(self, self.tr('Warning'), self.tr('Only one item can be edited at a time'))
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
        newItem = QtGui.QTableWidgetItem(self.phonesList[thisID]['label'])
        newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.phonesTableWidget.setItem(currCount-1, 0, newItem)
        newItem = QtGui.QTableWidgetItem(self.currLocale.toString(self.phonesList[thisID]['maxLevel']))
        newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.phonesTableWidget.setItem(currCount-1, 1, newItem)
        newItem = QtGui.QTableWidgetItem(self.phonesList[thisID]['default'])
        newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.phonesTableWidget.setItem(currCount-1, 2, newItem)
        self.phonesList[thisID]['qid'] = QtGui.QTableWidgetItem(thisID)
        self.phonesTableWidget.setItem(currCount-1, 3, self.phonesList[thisID]['qid'])
      

    def onClickRemovePhonesButton(self):
        if self.phonesTableWidget.rowCount() == 1:
            ret = QtGui.QMessageBox.warning(self, self.tr("Warning"),
                                            self.tr("Only one phone left. Cannot remove!"),
                                            QtGui.QMessageBox.Ok)
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
            QtGui.QMessageBox.warning(self, self.tr('Warning'), self.tr('Only one label can be renamed at a time'))
            return
        elif len(ids) < 1:
            QtGui.QMessageBox.warning(self, self.tr('Warning'), self.tr('Please, select a phone in the table'))
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
        QtGui.QDialog.accept(self)
    def reject(self): #reimplement reject
        if self.isPlaying == True:
            #self.playThread.__del__()
            self.playThread.terminate()
        QtGui.QDialog.reject(self)

   
