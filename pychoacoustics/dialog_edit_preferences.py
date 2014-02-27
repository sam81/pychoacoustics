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
    from PyQt4.QtCore import QLocale, QThread, pyqtSignal
    from PyQt4.QtGui import QCheckBox, QComboBox, QDialog, QDialogButtonBox, QGridLayout, QIntValidator, QLabel, QLayout, QLineEdit, QSizePolicy, QSpacerItem, QWidget, QTabWidget, QVBoxLayout
    QtCore.Signal = QtCore.pyqtSignal
    QtCore.Slot = QtCore.pyqtSlot
elif pyqtversion == -4:
    from PySide import QtGui, QtCore
    from PySide.QtCore import QLocale, QThread, Signal
    from PySide.QtGui import QCheckBox, QComboBox, QDialog, QDialogButtonBox, QGridLayout, QIntValidator, QLabel, QLayout, QLineEdit, QSizePolicy, QSpacerItem, QWidget, QTabWidget, QVBoxLayout
elif pyqtversion == 5:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtCore import QLocale, QThread, pyqtSignal
    from PyQt5.QtWidgets import QCheckBox, QComboBox, QDialog, QDialogButtonBox, QGridLayout, QLabel, QLayout, QLineEdit, QSizePolicy, QSpacerItem, QWidget, QTabWidget, QVBoxLayout
    from PyQt5.QtGui import QIntValidator
    QtCore.Signal = QtCore.pyqtSignal
    QtCore.Slot = QtCore.pyqtSlot
    
import copy, pickle, hashlib, base64, smtplib, sys 
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from .dialog_edit_end_message import*
from .utils_general import*

if platform.system() == "Linux":
    try:
        import alsaaudio
    except ImportError:
        pass
try:
    import pyaudio
except ImportError:
    pass

class preferencesDialog(QDialog):
    newMailerMessage = QtCore.Signal(str, str)
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.tmpPref = {}
        self.tmpPref['pref'] = copy.deepcopy(self.parent().prm['pref'])
        self.currLocale = self.parent().prm['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.OmitGroupSeparator | self.currLocale.RejectGroupSeparator)
        self.audioManager = parent.audioManager
        self.mailer = emailSender(self)
        self.newMailerMessage.connect(self.popMailerMessage)
        
        self.tabWidget = QTabWidget()
        self.tabWidget.currentChanged.connect(self.tabChanged)
        self.appPrefWidget = QWidget()
        self.soundPrefWidget = QWidget()
        self.notificationPrefWidget = QWidget()
        self.eegPrefWidget = QWidget()

        #the gui widget for these are in an external dialog
        self.wavsPref = {}
        self.wavsPref['endMessageFiles'] = self.tmpPref['pref']['general']['endMessageFiles']
        self.wavsPref['endMessageFilesUse'] = self.tmpPref['pref']['general']['endMessageFilesUse']
        self.wavsPref['endMessageFilesID'] = self.tmpPref['pref']['general']['endMessageFilesID']
        self.wavsPref['endMessageLevels'] = self.tmpPref['pref']['general']['endMessageLevels']
        #GENERAL PREF
        appPrefGrid = QGridLayout()
        n = 0
        self.languageChooserLabel = QLabel(self.tr('Language (requires restart):'))
        appPrefGrid.addWidget(self.languageChooserLabel, n, 0)
        self.languageChooser = QComboBox()
        self.languageChooser.addItems(self.parent().prm['appData']['available_languages'])
        self.languageChooser.setCurrentIndex(self.languageChooser.findText(self.tmpPref['pref']['language']))
        self.languageChooser.currentIndexChanged[int].connect(self.onLanguageChooserChange)
        appPrefGrid.addWidget(self.languageChooser, n, 1)
        n = n+1
        self.countryChooserLabel = QLabel(self.tr('Country (requires restart):'))
        appPrefGrid.addWidget(self.countryChooserLabel, n, 0)
        self.countryChooser = QComboBox()
        self.countryChooser.addItems(self.parent().prm['appData']['available_countries'][self.tmpPref['pref']['language']])
        self.countryChooser.setCurrentIndex(self.countryChooser.findText(self.tmpPref['pref']['country']))
        appPrefGrid.addWidget(self.countryChooser, n, 1)
        n = n+1

        self.responseBoxLanguageChooserLabel = QLabel(self.tr('Response Box Language (requires restart):'))
        appPrefGrid.addWidget(self.responseBoxLanguageChooserLabel, n, 0)
        self.responseBoxLanguageChooser = QComboBox()
        self.responseBoxLanguageChooser.addItems(self.parent().prm['appData']['available_languages'])
        self.responseBoxLanguageChooser.setCurrentIndex(self.responseBoxLanguageChooser.findText(self.tmpPref['pref']['responseBoxLanguage']))
        self.responseBoxLanguageChooser.currentIndexChanged[int].connect(self.onResponseBoxLanguageChooserChange)
        appPrefGrid.addWidget(self.responseBoxLanguageChooser, n, 1)
        n = n+1
        self.responseBoxCountryChooserLabel = QLabel(self.tr('Response Box Country (requires restart):'))
        appPrefGrid.addWidget(self.responseBoxCountryChooserLabel, n, 0)
        self.responseBoxCountryChooser = QComboBox()
        self.responseBoxCountryChooser.addItems(self.parent().prm['appData']['available_countries'][self.tmpPref['pref']['responseBoxLanguage']])
        self.responseBoxCountryChooser.setCurrentIndex(self.responseBoxCountryChooser.findText(self.tmpPref['pref']['responseBoxCountry']))
        appPrefGrid.addWidget(self.responseBoxCountryChooser, n, 1)
        
        n = n+1
        self.csvSeparatorLabel = QLabel(self.tr('csv separator:'))
        appPrefGrid.addWidget(self.csvSeparatorLabel, n, 0)
        self.csvSeparatorWidget = QLineEdit(self.tmpPref['pref']["general"]["csvSeparator"])
        appPrefGrid.addWidget(self.csvSeparatorWidget, n, 1)
        n = n+1
        self.listenerNameWarnCheckBox = QCheckBox(self.tr('Warn if listener name missing'))
        self.listenerNameWarnCheckBox.setChecked(self.tmpPref["pref"]["general"]["listenerNameWarn"])
        appPrefGrid.addWidget(self.listenerNameWarnCheckBox, n, 0)
        n = n+1
        self.sessionLabelWarnCheckBox = QCheckBox(self.tr('Warn if session label missing'))
        self.sessionLabelWarnCheckBox.setChecked(self.tmpPref["pref"]["general"]["sessionLabelWarn"])
        appPrefGrid.addWidget(self.sessionLabelWarnCheckBox, n, 0)

        n = n+1
        self.dpCorrCheckBox = QCheckBox(self.tr('d-prime correction'))
        self.dpCorrCheckBox.setChecked(self.tmpPref['pref']['general']['dprimeCorrection'])
        self.dpCorrCheckBox.setWhatsThis(self.tr("If checked, when automatically processing result files, convert hit rates of 0 and 1 to 1/2N and 1-1/(2N) respectively, where N is the number of trials, to avoid infinite values of d'"))
        appPrefGrid.addWidget(self.dpCorrCheckBox, n, 0)

        n = n+1
        self.recursionLimitLabel = QLabel(self.tr('Max Recursion Depth (requires restart):'))
        appPrefGrid.addWidget(self.recursionLimitLabel, n, 0)
        self.recursionLimitWidget = QLineEdit(self.currLocale.toString(self.tmpPref["pref"]["general"]["maxRecursionDepth"]))
        self.recursionLimitWidget.setValidator(QIntValidator(self))
        appPrefGrid.addWidget(self.recursionLimitWidget, n, 1)
        n = n+1
        
        self.appPrefWidget.setLayout(appPrefGrid)
        self.appPrefWidget.layout().setSizeConstraint(QLayout.SetFixedSize)
        
        
        #SOUND PREF
        soundPrefGrid = QGridLayout()
        n = 0
        self.playChooser = QComboBox()
        self.playChooser.addItems(self.parent().prm['appData']['available_play_commands'])
        self.playChooser.setCurrentIndex(self.playChooser.findText(self.tmpPref['pref']['sound']['playCommandType']))
        self.playChooser.currentIndexChanged[int].connect(self.onPlayChooserChange)
        self.playChooserLabel = QLabel(self.tr('Play Command:'))
        soundPrefGrid.addWidget(self.playChooserLabel, 0, 0)
        soundPrefGrid.addWidget(self.playChooser, 0, 1)
        n = n+1

        self.playCommandLabel = QLabel(self.tr('Command:'))
        soundPrefGrid.addWidget(self.playCommandLabel, n, 0)
        self.playCommandWidget = QLineEdit(self.tmpPref['pref']['sound']['playCommand'])
        if self.playChooser.currentText() != self.tr('custom'):
            self.playCommandWidget.setReadOnly(True)
        soundPrefGrid.addWidget(self.playCommandWidget, n, 1)
        n = n+1
        foo = self.playChooser.currentText()
        if foo != self.tr('custom'):
            self.playCommandLabel.hide()
            self.playCommandWidget.hide()

        #if pyalsaaudio is selected, provide device list chooser
        if self.parent().prm["appData"]["alsaaudioAvailable"] == True:
            self.alsaaudioPlaybackCardList = self.listAlsaaudioPlaybackCards()
            self.alsaaudioDeviceLabel = QLabel(self.tr('Device:'))
            soundPrefGrid.addWidget(self.alsaaudioDeviceLabel, n, 0)
            self.alsaaudioDeviceChooser = QComboBox()
            self.alsaaudioDeviceChooser.addItems(self.alsaaudioPlaybackCardList)
            self.alsaaudioDeviceChooser.setCurrentIndex(self.alsaaudioDeviceChooser.findText(self.tmpPref["pref"]["sound"]["alsaaudioDevice"]))
            soundPrefGrid.addWidget(self.alsaaudioDeviceChooser, n, 1)
            n = n+1
            if self.tmpPref['pref']['sound']['playCommandType'] != "alsaaudio":
                self.alsaaudioDeviceLabel.hide()
                self.alsaaudioDeviceChooser.hide()

        #if pyalsaaudio is selected, provide device list chooser
        if self.parent().prm["appData"]["pyaudioAvailable"] == True:
            self.listPyaudioPlaybackDevices()
            self.pyaudioDeviceLabel = QLabel(self.tr('Device:'))
            soundPrefGrid.addWidget(self.pyaudioDeviceLabel, n, 0)
            self.pyaudioDeviceChooser = QComboBox()
            self.pyaudioDeviceChooser.addItems(self.pyaudioDeviceListName)
            try:
                self.pyaudioDeviceChooser.setCurrentIndex(self.pyaudioDeviceListIdx.index(self.tmpPref["pref"]["sound"]["pyaudioDevice"]))
            except:
                self.tmpPref["pref"]["sound"]["pyaudioDevice"] = self.pyaudioDeviceListIdx[0]
                self.parent().prm["pref"]["sound"]["pyaudioDevice"] = self.pyaudioDeviceListIdx[0]
                self.pyaudioDeviceChooser.setCurrentIndex(self.pyaudioDeviceListIdx.index(self.tmpPref["pref"]["sound"]["pyaudioDevice"]))
            soundPrefGrid.addWidget(self.pyaudioDeviceChooser, n, 1)
            n = n+1
            if self.tmpPref['pref']['sound']['playCommandType'] != "pyaudio":
                self.pyaudioDeviceLabel.hide()
                self.pyaudioDeviceChooser.hide()

        if self.parent().prm["appData"]["pactypesAvailable"] == True:
            self.audioManager.listPactypesPlaybackDevices()
            self.pactypesDeviceLabel = QLabel(self.tr('Device:'))
            soundPrefGrid.addWidget(self.pactypesDeviceLabel, n, 0)
            self.pactypesDeviceChooser = QComboBox()
            self.pactypesDeviceChooser.addItems(self.audioManager.pactypesDeviceListName)
            print(self.audioManager.pactypesDeviceListIdx)
            try:
                self.pactypesDeviceChooser.setCurrentIndex(self.audioManager.pactypesDeviceListIdx.index(self.tmpPref["pref"]["sound"]["pactypesDevice"]))
            except:
                self.tmpPref["pref"]["sound"]["pactypesDevice"] = self.audioManager.pactypesDeviceListIdx[0]
                self.parent().prm["pref"]["sound"]["pactypesDevice"] = self.pactypesDeviceListIdx[0]
                self.pactypesDeviceChooser.setCurrentIndex(self.audioManager.pactypesDeviceListIdx.index(self.tmpPref["pref"]["sound"]["pactypesDevice"]))
            soundPrefGrid.addWidget(self.pactypesDeviceChooser, n, 1)
            n = n+1
            if self.tmpPref['pref']['sound']['playCommandType'] != "pactypes":
                self.pactypesDeviceLabel.hide()
                self.pactypesDeviceChooser.hide()


        if self.parent().prm["appData"]["alsaaudioAvailable"] == True or self.parent().prm["appData"]["pyaudioAvailable"] == True or self.parent().prm["appData"]["pactypesAvailable"] == True:
            self.bufferSizeLabel = QLabel(self.tr('Buffer Size (samples):'))
            soundPrefGrid.addWidget(self.bufferSizeLabel, n, 0)
            self.bufferSizeWidget =  QLineEdit(self.currLocale.toString(self.tmpPref["pref"]["sound"]["bufferSize"]))
            self.bufferSizeWidget.setValidator(QIntValidator(self))
            soundPrefGrid.addWidget(self.bufferSizeWidget, n, 1)
            n = n+1
            if self.tmpPref['pref']['sound']['playCommandType'] not in ["alsaaudio", "pyaudio", "pactypes"]:
                self.bufferSizeLabel.hide()
                self.bufferSizeWidget.hide()

        self.samplerateLabel = QLabel(self.tr('Default Sampling Rate:'))
        soundPrefGrid.addWidget(self.samplerateLabel, n, 0)
        self.samplerateWidget = QLineEdit(self.tmpPref["pref"]["sound"]["defaultSampleRate"])
        #self.samplerateWidget.setValidator(QIntValidator(self))
        soundPrefGrid.addWidget(self.samplerateWidget, n, 1)
        n = n+1

        self.nbitsLabel = QLabel(self.tr('Default Bits:'))
        self.nbitsChooser = QComboBox()
        self.nbitsChooser.addItems(self.parent().prm["nBitsChoices"])
        self.nbitsChooser.setCurrentIndex(self.parent().prm["nBitsChoices"].index(self.tmpPref["pref"]["sound"]["defaultNBits"])) 
        soundPrefGrid.addWidget(self.nbitsLabel, n, 0)
        soundPrefGrid.addWidget(self.nbitsChooser, n, 1)
        n = n+1

        self.wavmanagerLabel = QLabel(self.tr('Wav Manager (requires restart):'))
        self.wavmanagerChooser = QComboBox()
        self.wavmanagerChooser.addItems(self.parent().prm['appData']['wavmanagers'])
        self.wavmanagerChooser.setCurrentIndex(self.wavmanagerChooser.findText(self.tmpPref['pref']['sound']['wavmanager']))
        soundPrefGrid.addWidget(self.wavmanagerLabel, n, 0)
        soundPrefGrid.addWidget(self.wavmanagerChooser, n, 1)
        n = n+1
        
        self.writewav = QCheckBox(self.tr('Write wav file'))
        self.writewav.setChecked(self.tmpPref["pref"]["sound"]["writewav"])
        soundPrefGrid.addWidget(self.writewav, n, 0)
        n = n+1
        self.writeSndSeqSegments = QCheckBox(self.tr('Write sound sequence segments wavs'))
        self.writeSndSeqSegments.setChecked(self.tmpPref["pref"]["sound"]["writeSndSeqSegments"])
        soundPrefGrid.addWidget(self.writeSndSeqSegments, n, 0)
        n = n+1

        self.appendSilenceLabel = QLabel(self.tr('Append silence to each sound (ms):'))
        soundPrefGrid.addWidget(self.appendSilenceLabel, n, 0)
        self.appendSilenceWidget = QLineEdit(self.currLocale.toString(self.tmpPref["pref"]["sound"]["appendSilence"]))
        soundPrefGrid.addWidget(self.appendSilenceWidget, n, 1)
        n = n+1
        
        self.soundPrefWidget.setLayout(soundPrefGrid)
        self.soundPrefWidget.layout().setSizeConstraint(QLayout.SetFixedSize)
        # NOTIFICATION PREF
        notificationPrefGrid = QGridLayout()
        
        n = 0
        
        self.playEndMessage = QCheckBox(self.tr('Play End Message'))
        self.playEndMessage.setChecked(self.tmpPref["pref"]["general"]["playEndMessage"])
        notificationPrefGrid.addWidget(self.playEndMessage, n, 0)

        self.endMessageButton = QPushButton(self.tr("Choose Wav"), self)
        self.endMessageButton.clicked.connect(self.onClickEndMessageButton)
        notificationPrefGrid.addWidget(self.endMessageButton, n, 1)
        n = n+1

        notificationPrefGrid.addItem(QSpacerItem(20,20,QSizePolicy.Expanding), n, 0)
        n = n+1
        
        self.nBlocksLabel = QLabel(self.tr('blocks before end of experiment:'))
        notificationPrefGrid.addWidget(self.nBlocksLabel, n, 1)
        self.nBlocksWidget = QLineEdit(self.currLocale.toString(self.tmpPref['pref']['email']['nBlocksNotify']))
        notificationPrefGrid.addWidget(self.nBlocksWidget, n, 0)
        n = n+1

        self.emailNotify = QCheckBox(self.tr('Send Notification e-mail'))
        self.emailNotify.setChecked(self.tmpPref["pref"]["email"]["notifyEnd"])
        notificationPrefGrid.addWidget(self.emailNotify, n, 0)
        n = n+1

        self.nBlocksCustomCommandLabel = QLabel(self.tr('Execute custom command:'))
        notificationPrefGrid.addWidget(self.nBlocksCustomCommandLabel, n, 0)
        self.nBlocksCustomCommandWidget = QLineEdit(self.tmpPref["pref"]["general"]["nBlocksCustomCommand"])
        notificationPrefGrid.addWidget(self.nBlocksCustomCommandWidget, n, 1)
        n = n+1


        notificationPrefGrid.addItem(QSpacerItem(20,20,QSizePolicy.Expanding), n, 0)
        n = n+1
        self.atEndLabel = QLabel(self.tr('At the end of the experiment:'))
        notificationPrefGrid.addWidget(self.atEndLabel, n, 0)
        n = n+1
        
        self.sendData = QCheckBox(self.tr('Send data via e-mail'))
        self.sendData.setChecked(self.tmpPref["pref"]["email"]["sendData"])
        notificationPrefGrid.addWidget(self.sendData, n, 0)
        n = n+1

        self.atEndCustomCommandLabel = QLabel(self.tr('Execute custom command:'))
        notificationPrefGrid.addWidget(self.atEndCustomCommandLabel, n, 0)
        self.atEndCustomCommandWidget = QLineEdit(self.tmpPref["pref"]["general"]["atEndCustomCommand"])
        notificationPrefGrid.addWidget(self.atEndCustomCommandWidget, n, 1)
        n = n+1

        notificationPrefGrid.addItem(QSpacerItem(20,20,QSizePolicy.Expanding), n, 0)
        n = n+1
        self.serverLabel = QLabel(self.tr('Outgoing server (SMTP):'))
        notificationPrefGrid.addWidget(self.serverLabel, n, 0)
        self.serverWidget = QLineEdit(self.tmpPref['pref']['email']['SMTPServer'])
        notificationPrefGrid.addWidget(self.serverWidget, n, 1)
        n = n+1

        self.serverPortLabel = QLabel(self.tr('Port:'))
        notificationPrefGrid.addWidget(self.serverPortLabel, n, 0)
        self.serverPortWidget = QLineEdit(self.currLocale.toString(self.tmpPref['pref']['email']['SMTPServerPort']))
        self.serverPortWidget.setValidator(QIntValidator(self))
        notificationPrefGrid.addWidget(self.serverPortWidget, n, 1)
        n = n+1

        self.serverSecurityLabel = QLabel(self.tr('Security:'))
        notificationPrefGrid.addWidget(self.serverSecurityLabel, n, 0)
        self.serverSecurityChooser = QComboBox()
        self.serverSecurityChooser.addItems(["TLS/SSL (a)", "TLS/SSL (b)", "none"])
        self.serverSecurityChooser.setCurrentIndex(self.serverSecurityChooser.findText(self.tmpPref['pref']['email']['SMTPServerSecurity']))
        notificationPrefGrid.addWidget(self.serverSecurityChooser, n, 1)
        n = n+1

        self.serverRequiresAuthCheckBox = QCheckBox(self.tr('Server requires authentication'))
        self.serverRequiresAuthCheckBox.setChecked(self.tmpPref["pref"]["email"]["serverRequiresAuthentication"])
        notificationPrefGrid.addWidget(self.serverRequiresAuthCheckBox, n, 0, 1, 2)
        n = n+1
        
        self.usernameLabel = QLabel(self.tr('Username:'))
        notificationPrefGrid.addWidget(self.usernameLabel, n, 0)
        self.usernameWidget = QLineEdit(self.tmpPref['pref']['email']['fromUsername'])
        notificationPrefGrid.addWidget(self.usernameWidget, n, 1)
        n = n+1
        
        self.passwordLabel = QLabel(self.tr('Password:'))
        notificationPrefGrid.addWidget(self.passwordLabel, n, 0)
        self.passwordWidget = QLineEdit(self.tmpPref['pref']['email']['fromPassword'])
        self.passwordWidget.setEchoMode(QLineEdit.Password)
        notificationPrefGrid.addWidget(self.passwordWidget, n, 1)

        n = n+1
        self.passwordWarningLabel = QLabel(self.tr('Password is NOT stored safely (see manual), use at your own risk!'))
        notificationPrefGrid.addWidget(self.passwordWarningLabel, n, 0, 1, 2)
        n = n+1
        self.testEmailButton = QPushButton(self.tr("Send test e-mail"), self)
        self.testEmailButton.clicked.connect(self.onClickTestEmailButton)
        self.testEmailButton.setToolTip(self.tr("Send a test e-mail"))
        notificationPrefGrid.addWidget(self.testEmailButton, n, 0, 1, 2)
        
        self.notificationPrefWidget.setLayout(notificationPrefGrid)
        self.notificationPrefWidget.layout().setSizeConstraint(QLayout.SetFixedSize)


        ##--#--#--#--#--
        # EEG PREF GRID
        eegPrefGrid = QGridLayout()
        
        n = 0
        self.ONTriggerLabel = QLabel(self.tr('ON Trigger:'))
        eegPrefGrid.addWidget(self.ONTriggerLabel, n, 0)
        self.ONTriggerWidget = QLineEdit(self.currLocale.toString(self.tmpPref["pref"]["general"]["ONTrigger"]))
        eegPrefGrid.addWidget(self.ONTriggerWidget, n, 1)

        n = n+1
        self.OFFTriggerLabel = QLabel(self.tr('OFF Trigger:'))
        eegPrefGrid.addWidget(self.OFFTriggerLabel, n, 0)
        self.OFFTriggerWidget = QLineEdit(self.currLocale.toString(self.tmpPref["pref"]["general"]["OFFTrigger"]))
        eegPrefGrid.addWidget(self.OFFTriggerWidget, n, 1)

        n = n+1
        self.triggerDurLabel = QLabel(self.tr('Trigger Duration (ms):'))
        eegPrefGrid.addWidget(self.triggerDurLabel, n, 0)
        self.triggerDurWidget = QLineEdit(self.currLocale.toString(self.tmpPref["pref"]["general"]["triggerDur"]))
        eegPrefGrid.addWidget(self.triggerDurWidget, n, 1)
      
        
        self.eegPrefWidget.setLayout(eegPrefGrid)
        self.eegPrefWidget.layout().setSizeConstraint(QLayout.SetFixedSize)

        # ........................
        self.tabWidget.addTab(self.appPrefWidget, self.tr("Genera&l"))
        self.tabWidget.addTab(self.soundPrefWidget, self.tr("Soun&d"))
        self.tabWidget.addTab(self.notificationPrefWidget, self.tr("Notification&s"))
        self.tabWidget.addTab(self.eegPrefWidget, self.tr("EE&G"))

        buttonBox = QDialogButtonBox(QDialogButtonBox.Apply|QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.permanentApply)
        
        layout = QVBoxLayout()
        layout.addWidget(self.tabWidget)
        layout.addWidget(buttonBox)
        self.setLayout(layout)
       
    def onLanguageChooserChange(self):
        for i in range(self.countryChooser.count()):
            self.countryChooser.removeItem(0)
        self.countryChooser.addItems(self.parent().prm['appData']['available_countries'][self.languageChooser.currentText()])

    def onResponseBoxLanguageChooserChange(self):
        for i in range(self.responseBoxCountryChooser.count()):
            self.responseBoxCountryChooser.removeItem(0)
        self.responseBoxCountryChooser.addItems(self.parent().prm['appData']['available_countries'][self.responseBoxLanguageChooser.currentText()])

    def onPlayChooserChange(self):
        foo = self.playChooser.currentText()
        if foo != self.tr('custom'):
            self.playCommandLabel.hide()
            self.playCommandWidget.hide()
            self.playCommandWidget.setText(foo)
            self.playCommandWidget.setReadOnly(True)
        else:
            self.playCommandWidget.show()
            self.playCommandLabel.show()
            self.playCommandWidget.setReadOnly(False)

        if self.parent().prm["appData"]["alsaaudioAvailable"] == True:
            if foo == "alsaaudio":
                self.alsaaudioDeviceLabel.show()
                self.alsaaudioDeviceChooser.show()
               
            else:
                self.alsaaudioDeviceLabel.hide()
                self.alsaaudioDeviceChooser.hide()
             

        if self.parent().prm["appData"]["pyaudioAvailable"] == True:
            if foo == "pyaudio":
                self.pyaudioDeviceLabel.show()
                self.pyaudioDeviceChooser.show()
            else:
                self.pyaudioDeviceLabel.hide()
                self.pyaudioDeviceChooser.hide()

        if self.parent().prm["appData"]["pactypesAvailable"] == True:
            if foo == "pactypes":
                self.pactypesDeviceLabel.show()
                self.pactypesDeviceChooser.show()
            else:
                self.pactypesDeviceLabel.hide()
                self.pactypesDeviceChooser.hide()

        if self.parent().prm["appData"]["alsaaudioAvailable"] == True or self.parent().prm["appData"]["pyaudioAvailable"] == True or self.parent().prm["appData"]["pactypesAvailable"] == True:
            if foo in ["alsaaudio", "pyaudio", "pactypes"]:
                self.bufferSizeLabel.show()
                self.bufferSizeWidget.show()
            else:
                self.bufferSizeLabel.hide()
                self.bufferSizeWidget.hide()
            
    def onClickEndMessageButton(self):
        dialog = wavListDialog(self)
        if dialog.exec_():
            self.wavsList = dialog.wavsList
            self.wavsPref = {}
            self.wavsPref['endMessageFiles'] = []
            self.wavsPref['endMessageFilesUse'] = []
            self.wavsPref['endMessageFilesID'] = []
            self.wavsPref['endMessageLevels'] = []
            keys = sorted(self.wavsList.keys())
            for key in keys:
                self.wavsPref['endMessageFiles'].append(str(self.wavsList[key]['file']))
                self.wavsPref['endMessageFilesUse'].append(self.wavsList[key]['use'])
                self.wavsPref['endMessageLevels'].append(self.wavsList[key]['level'])
                self.wavsPref['endMessageFilesID'].append(key)

    def onClickTestEmailButton(self):
        self.mailer.sendTestEmail()
        
    def popMailerMessage(self, msg, msgtype):
        if msgtype == 'critical':
            QMessageBox.critical(self, self.tr("Error"), msg)
        elif msgtype == 'warning':
            QMessageBox.warning(self, self.tr("Warning"), msg)
        elif msgtype == 'information':
            QMessageBox.information(self, self.tr("Information"), msg)
            
    def tryApply(self):
        self.tmpPref['pref']['language'] = self.tr(self.languageChooser.currentText())
        self.tmpPref['pref']['country'] = self.tr(self.countryChooser.currentText())
        self.tmpPref['pref']['responseBoxLanguage'] = self.tr(self.responseBoxLanguageChooser.currentText())
        self.tmpPref['pref']['responseBoxCountry'] = self.tr(self.responseBoxCountryChooser.currentText())
        self.tmpPref['pref']['general']['csvSeparator'] = self.csvSeparatorWidget.text()
        self.tmpPref['pref']['general']['ONTrigger'] = self.currLocale.toInt(self.ONTriggerWidget.text())[0]
        self.tmpPref['pref']['general']['OFFTrigger'] = self.currLocale.toInt(self.OFFTriggerWidget.text())[0]
        self.tmpPref['pref']['general']['triggerDur'] = self.currLocale.toDouble(self.triggerDurWidget.text())[0]
        self.tmpPref['pref']['general']['maxRecursionDepth'] = self.currLocale.toInt(self.recursionLimitWidget.text())[0]
        
        self.tmpPref['pref']['sound']['playCommand'] = self.tr(self.playCommandWidget.text())
        self.tmpPref['pref']['sound']['playCommandType'] = self.tr(self.playChooser.currentText())
        if self.parent().prm["appData"]["alsaaudioAvailable"] == True:
            self.tmpPref['pref']['sound']['alsaaudioDevice'] = self.alsaaudioDeviceChooser.currentText()
        if self.parent().prm["appData"]["pyaudioAvailable"] == True:
            self.tmpPref['pref']['sound']['pyaudioDevice'] =  self.pyaudioDeviceListIdx[self.pyaudioDeviceChooser.currentIndex()]
        if self.parent().prm["appData"]["pactypesAvailable"] == True:
            self.tmpPref['pref']['sound']['pactypesDevice'] =  self.audioManager.pactypesDeviceListIdx[self.pactypesDeviceChooser.currentIndex()]
        self.tmpPref['pref']['sound']['wavmanager'] = str(self.wavmanagerChooser.currentText())
        if self.parent().prm["appData"]["alsaaudioAvailable"] == True or self.parent().prm["appData"]["pyaudioAvailable"] == True or self.parent().prm["appData"]["pactypesAvailable"] == True:
            self.tmpPref['pref']['sound']['bufferSize'] = self.currLocale.toInt(self.bufferSizeWidget.text())[0]
        self.tmpPref['pref']['sound']['defaultSampleRate'] = self.samplerateWidget.text()
        self.tmpPref['pref']['sound']['defaultNBits'] = self.nbitsChooser.currentText()
        self.tmpPref['pref']['sound']['appendSilence'] = self.currLocale.toInt(self.appendSilenceWidget.text())[0]
        
        self.tmpPref["pref"]["email"]["nBlocksNotify"] = self.currLocale.toInt(self.nBlocksWidget.text())[0]
        self.tmpPref["pref"]["general"]["nBlocksCustomCommand"] = self.nBlocksCustomCommandWidget.text()
        self.tmpPref["pref"]["general"]["atEndCustomCommand"] = self.atEndCustomCommandWidget.text()
        self.tmpPref["pref"]["email"]['SMTPServer'] = self.serverWidget.text()
        self.tmpPref["pref"]["email"]['SMTPServerPort'] = self.currLocale.toInt(self.serverPortWidget.text())[0]
        self.tmpPref["pref"]["email"]['fromUsername'] = self.usernameWidget.text()
        self.tmpPref["pref"]["email"]['SMTPServerSecurity'] = self.serverSecurityChooser.currentText()

        self.tmpPref["pref"]["general"]["endMessageFiles"] = self.wavsPref['endMessageFiles']
        self.tmpPref["pref"]["general"]["endMessageFilesUse"] = self.wavsPref['endMessageFilesUse']
        self.tmpPref["pref"]["general"]["endMessageFilesID"] = self.wavsPref['endMessageFilesID']
        self.tmpPref["pref"]["general"]["endMessageLevels"] = self.wavsPref['endMessageLevels']

        self.tmpPref["pref"]["email"]['fromPassword'] = self.passwordWidget.text()
        
        if self.writewav.isChecked():
            self.tmpPref['pref']['sound']['writewav'] = True
        else:
            self.tmpPref['pref']['sound']['writewav'] = False

        if self.writeSndSeqSegments.isChecked():
            self.tmpPref['pref']['sound']['writeSndSeqSegments'] = True
        else:
            self.tmpPref['pref']['sound']['writeSndSeqSegments'] = False

        if self.dpCorrCheckBox.isChecked():
            self.tmpPref['pref']['general']['dprimeCorrection'] = True
        else:
            self.tmpPref['pref']['general']['dprimeCorrection'] = False

        if self.listenerNameWarnCheckBox.isChecked():
            self.tmpPref['pref']['general']['listenerNameWarn'] = True
        else:
            self.tmpPref['pref']['general']['listenerNameWarn'] = False

        if self.sessionLabelWarnCheckBox.isChecked():
            self.tmpPref['pref']['general']['sessionLabelWarn'] = True
        else:
            self.tmpPref['pref']['general']['sessionLabelWarn'] = False

        if self.emailNotify.isChecked():
            self.tmpPref['pref']['email']['notifyEnd'] = True
        else:
            self.tmpPref['pref']['email']['notifyEnd'] = False

        if self.sendData.isChecked():
            self.tmpPref['pref']['email']['sendData'] = True
        else:
            self.tmpPref['pref']['email']['sendData'] = False

        if self.serverRequiresAuthCheckBox.isChecked():
            self.tmpPref['pref']['email']['serverRequiresAuthentication'] = True
        else:
            self.tmpPref['pref']['email']['serverRequiresAuthentication'] = False

        if self.playEndMessage.isChecked():
            self.tmpPref['pref']['general']['playEndMessage'] = True
        else:
            self.tmpPref['pref']['general']['playEndMessage'] = False

        if self.tmpPref['pref']['email']['notifyEnd'] == True or self.tmpPref['pref']['email']['sendData'] == True:
            if checkUsernameValid(self.tmpPref["pref"]["email"]['fromUsername']) == False:
                errMsg = self.tr("Username invalid. Disabling sending e-mails.")
                QMessageBox.warning(self, self.tr("Warning"), errMsg)
                self.emailNotify.setChecked(False)
                self.sendData.setChecked(False)
                self.tmpPref['pref']['email']['notifyEnd'] = False
                self.tmpPref['pref']['email']['sendData'] = False
            elif checkServerValid(self.tmpPref["pref"]["email"]['SMTPServer']) == False:
                errMsg = self.tr("SMTP server name invalid. Disabling sending e-mails.")
                QMessageBox.warning(self, self.tr("Warning"), errMsg)
                self.emailNotify.setChecked(False)
                self.sendData.setChecked(False)
                self.tmpPref['pref']['email']['notifyEnd'] = False
                self.tmpPref['pref']['email']['sendData'] = False
            
    def revertChanges(self):
        self.languageChooser.setCurrentIndex(self.languageChooser.findText(self.tmpPref['pref']['language']))
        self.countryChooser.setCurrentIndex(self.countryChooser.findText(self.tmpPref['pref']['country']))
        self.responseBoxLanguageChooser.setCurrentIndex(self.responseBoxLanguageChooser.findText(self.tmpPref['pref']['responseBoxLanguage']))
        self.responseBoxCountryChooser.setCurrentIndex(self.responseBoxCountryChooser.findText(self.tmpPref['pref']['responseBoxCountry']))
        self.csvSeparatorWidget.setText(self.tmpPref['pref']['general']['csvSeparator'])
        self.ONTriggerWidget.setText(self.currLocale.toString(self.tmpPref['pref']['general']['ONTrigger']))
        self.OFFTriggerWidget.setText(self.currLocale.toString(self.tmpPref['pref']['general']['OFFTrigger']))
        self.triggerDurWidget.setText(self.currLocale.toString(self.tmpPref['pref']['general']['triggerDur']))
        self.recursionLimitWidget.setText(self.currLocale.toString(self.tmpPref['pref']['general']['maxRecursionDepth']))
        
        self.playChooser.setCurrentIndex(self.playChooser.findText(self.tmpPref['pref']['sound']['playCommandType']))
        if self.parent().prm["appData"]["alsaaudioAvailable"] == True:
            self.alsaaudioDeviceChooser.setCurrentIndex(self.alsaaudioDeviceChooser.findText(self.tmpPref['pref']['sound']['alsaaudioDevice']))
        if self.parent().prm["appData"]["pyaudioAvailable"] == True:
            self.pyaudioDeviceChooser.setCurrentIndex(self.pyaudioDeviceListIdx.index(self.tmpPref['pref']['sound']['pyaudioDevice']))
        if self.parent().prm["appData"]["pactypesAvailable"] == True:
            self.pactypesDeviceChooser.setCurrentIndex(self.audioManager.pactypesDeviceListIdx.index(self.tmpPref['pref']['sound']['pactypesDevice']))
        self.wavmanagerChooser.setCurrentIndex(self.wavmanagerChooser.findText(self.tmpPref['pref']['sound']['wavmanager']))
        self.playCommandWidget.setText(self.tmpPref['pref']['sound']['playCommand'])
        if self.parent().prm["appData"]["alsaaudioAvailable"] == True or self.parent().prm["appData"]["pyaudioAvailable"] == True or self.parent().prm["appData"]["pactypesAvailable"] == True:
            self.bufferSizeWidget.setText(self.currLocale.toString(self.tmpPref['pref']['sound']['bufferSize']))
        self.samplerateWidget.setText(self.tmpPref['pref']['sound']['defaultSampleRate'])
        self.nbitsChooser.setCurrentIndex(self.nbitsChooser.findText(self.tmpPref['pref']['sound']['defaultNBits']))
        self.appendSilenceWidget.setText(self.currLocale.toString(self.tmpPref['pref']['sound']['appendSilence']))
       

        self.nBlocksWidget.setText(self.currLocale.toString(self.tmpPref['pref']['email']['nBlocksNotify']))
        self.nBlocksCustomCommandWidget.setText( self.tmpPref["pref"]["general"]["nBlocksCustomCommand"])
        self.atEndCustomCommandWidget.setText( self.tmpPref["pref"]["general"]["nBlocksCustomCommand"])
        self.serverWidget.setText(self.tmpPref['pref']['email']['SMTPServer'])
        self.serverPortWidget.setText(self.currLocale.toString(self.tmpPref['pref']['email']['SMTPServerPort']))
        self.usernameWidget.setText(self.tmpPref['pref']['email']['fromUsername'])
        self.passwordWidget.setText(self.tmpPref['pref']['email']['fromPassword'])
        self.serverSecurityChooser.setCurrentIndex(self.serverSecurityChooser.findText(self.tmpPref['pref']['email']['SMTPServerSecurity']))

        self.wavsPref["endMessageFiles"] = self.tmpPref["pref"]["general"]["endMessageFiles"]
        self.wavsPref["endMessageFilesUse"] = self.tmpPref["pref"]["general"]["endMessageFilesUse"]
        self.wavsPref["endMessageFilesID"] = self.tmpPref["pref"]["general"]["endMessageFilesID"]
        self.wavsPref["endMessageLevels"] = self.tmpPref["pref"]["general"]["endMessageLevels"]

        if self.playChooser.currentText() != self.tr('custom'):
            self.playCommandWidget.setReadOnly(True)
        self.writewav.setChecked(self.tmpPref["pref"]["sound"]["writewav"])
        self.writeSndSeqSegments.setChecked(self.tmpPref["pref"]["sound"]["writeSndSeqSegments"])
        self.dpCorrCheckBox.setChecked(self.tmpPref["pref"]["general"]["dprimeCorrection"])
        self.listenerNameWarnCheckBox.setChecked(self.tmpPref["pref"]["general"]["listenerNameWarn"])
        self.sessionLabelWarnCheckBox.setChecked(self.tmpPref["pref"]["general"]["sessionLabelWarn"])

        self.emailNotify.setChecked(self.tmpPref["pref"]["email"]["notifyEnd"])
        self.sendData.setChecked(self.tmpPref["pref"]["email"]["sendData"])
        self.serverRequiresAuthCheckBox.setChecked(self.tmpPref["pref"]["email"]["serverRequiresAuthentication"])
        self.playEndMessage.setChecked(self.tmpPref["pref"]["general"]["playEndMessage"])
        
    def permanentApply(self):
        self.tryApply()
        if self.parent().prm['pref']['email']['fromPassword'] != self.tmpPref['pref']['email']['fromPassword']:
            passwd = bytes(self.passwordWidget.text(),'utf-8')
            encoded_passwd = base64.b64encode(passwd)
            encoded_passwd = str(encoded_passwd, "utf-8")
            #passwd = hashlib.sha1(passwd).hexdigest()
            self.tmpPref["pref"]["email"]['fromPassword'] = encoded_passwd
            self.passwordWidget.setText(self.tmpPref['pref']['email']['fromPassword'])
        
        self.parent().prm['pref'] = copy.deepcopy(self.tmpPref['pref'])
        f = open(self.parent().prm['prefFile'], 'wb')
        pickle.dump(self.parent().prm['pref'], f)
        f.close()
        
    def tabChanged(self):
        self.tryApply()
        if self.tmpPref['pref'] != self.parent().prm['pref']:
            reply = QMessageBox.warning(self, self.tr("Warning"), self.tr('There are unsaved changes. Apply Changes?'), QMessageBox.Yes | 
                                            QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.permanentApply()
            else:
                self.tmpPref['pref'] = copy.deepcopy(self.parent().prm['pref'])
                self.revertChanges()

    def listAlsaaudioPlaybackCards(self):
        playbackCardList = ['default']
        for card in alsaaudio.cards():
            try:
                alsaaudio.PCM(type=alsaaudio.PCM_PLAYBACK, mode=alsaaudio.PCM_NORMAL, card=card)
                playbackCardList.append(card)
            except:
                pass
        return playbackCardList
    
    def listPyaudioPlaybackDevices(self):
        self.pyaudioHostApiListName = []
        self.pyaudioHostApiListIdx = []
        self.pyaudioDeviceListName = []
        self.pyaudioDeviceListIdx = []
        paManager = pyaudio.PyAudio()
        nDevices = paManager.get_device_count()
        nApi = paManager.get_host_api_count()
        for i in range(nApi):
            self.pyaudioHostApiListName.append(paManager.get_host_api_info_by_index(i)['name'])
            self.pyaudioHostApiListIdx.append(paManager.get_host_api_info_by_index(i)['index'])
        for i in range(nDevices):
            thisDevInfo = paManager.get_device_info_by_index(i)
            if thisDevInfo["maxOutputChannels"] > 0:
                self.pyaudioDeviceListName.append(thisDevInfo["name"] + ' - ' + self.pyaudioHostApiListName[thisDevInfo["hostApi"]])
                self.pyaudioDeviceListIdx.append(thisDevInfo["index"])
        return 
                

class emailSender(QThread):
    def __init__(self, parent):
        QThread.__init__(self, parent)

    def sendTestEmail(self):
        self.start()
    def run(self):
        experimenterIdx = self.parent().parent().prm['experimenter']['experimenter_id'].index(self.parent().parent().experimenterChooser.currentText())
        if self.parent().passwordWidget.text() != self.parent().tmpPref['pref']['email']['fromPassword']: #it is not encoded
            decoded_passwd = self.parent().passwordWidget.text()
        else:
            decoded_passwd = bytes(self.parent().passwordWidget.text(), "utf-8")
            decoded_passwd = base64.b64decode(decoded_passwd)
            decoded_passwd = str(decoded_passwd, "utf-8")
        msg = MIMEMultipart()
        msg["From"] = self.parent().usernameWidget.text()
        msg["To"] =  self.parent().parent().prm['experimenter']['experimenter_email'][experimenterIdx]
        msg["Subject"] = self.parent().tr("pychoacoustics test e-mail")
        body = "This is a test e-mail sent from pychoacoustics"
        part1 = MIMEText(body, 'plain')
        msg.attach(part1)

        if checkEmailValid(msg["To"]) == False:
            errMsg = self.parent().tr("Experimenter {} e-mail's address {} not valid \n Please specify a valid address for the current experimenter \n in the Edit -> Experimenters dialog".format(self.parent().parent().prm['experimenter']['experimenter_id'][experimenterIdx], msg["To"]))
            print(errMsg, file=sys.stderr)
            self.parent().newMailerMessage.emit(errMsg, 'critical')  
            return
        elif checkUsernameValid(msg["From"]) == False:
            errMsg = self.parent().tr("username invalid")
            print(errMsg, file=sys.stderr)
            self.parent().newMailerMessage.emit(errMsg, 'critical')  
            return
        elif checkServerValid(self.parent().serverWidget.text()) == False:
            errMsg = self.parent().tr("SMTP server name invalid")
            print(errMsg, file=sys.stderr)
            self.parent().newMailerMessage.emit(errMsg, 'critical')  
            return

        if self.parent().serverRequiresAuthCheckBox.isChecked() == True:
            if  self.parent().serverSecurityChooser.currentText() == "TLS/SSL (a)":
                try:
                    server = smtplib.SMTP_SSL(self.parent().serverWidget.text(), self.parent().currLocale.toInt(self.parent().serverPortWidget.text())[0])
                except Exception as ex:
                    errMsg = self.parent().tr("Something went wrong, try to change server settings \n {}".format(ex))
                    print(errMsg, file=sys.stderr)
                    self.parent().newMailerMessage.emit(errMsg, 'critical')  
                    return
              
            elif self.parent().serverSecurityChooser.currentText() == "TLS/SSL (b)":
                try:
                    server = smtplib.SMTP(self.parent().serverWidget.text(), self.parent().currLocale.toInt(self.parent().serverPortWidget.text())[0])
                    server.ehlo()
                    server.starttls()
                except Exception as ex:
                    errMsg = self.parent().tr("Something went wrong, try to change server settings \n {}".format(ex))
                    print(errMsg, file=sys.stderr)
                    self.parent().newMailerMessage.emit(errMsg, 'critical')  
                    return
        
            elif self.parent().serverSecurityChooser.currentText() == "none":
                try:
                    server = smtplib.SMTP(self.parent().serverWidget.text(), self.parent().currLocale.toInt(self.parent().serverPortWidget.text())[0])
                except Exception as ex:
                    errMsg = self.parent().tr("Something went wrong, try to change server settings \n {}".format(ex))
                    print(errMsg, file=sys.stderr)
                    self.parent().newMailerMessage.emit(errMsg, 'critical')  
                    return

            #attempt login
            try:
                server.login(self.parent().usernameWidget.text(),  decoded_passwd)
            except Exception as ex:
                errMsg = self.parent().tr("Something went wrong, try to change server settings \n {}".format(ex))
                print(errMsg, file=sys.stderr)
                self.parent().newMailerMessage.emit(errMsg, 'critical')  
                return
        else: # no auth requires
            try:
                server = smtplib.SMTP(self.parent().serverWidget.text(), self.parent().currLocale.toInt(self.parent().serverPortWidget.text())[0])
            except Exception as ex:
                errMsg = self.parent().tr("Something went wrong, try to change server settings \n {}".format(ex))
                print(errMsg, file=sys.stderr)
                self.parent().newMailerMessage.emit(errMsg, 'critical')  
                return
        try:
            server.sendmail(msg["From"], msg["To"], msg.as_string())
            infoMsg = self.parent().tr("e-mail sent successfully")
            self.parent().newMailerMessage.emit(infoMsg, 'information')  
        except Exception as ex:
            errMsg = self.parent().tr("Something went wrong, try to change server settings \n {}".format(ex))
            print(errMsg, file=sys.stderr)
            self.parent().newMailerMessage.emit(errMsg, 'critical')  
            return
