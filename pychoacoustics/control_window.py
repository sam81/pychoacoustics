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
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL, Qt, QEvent
from PyQt4.QtGui import QLabel, QLineEdit, QComboBox, QScrollArea, QSizePolicy, QCheckBox
from .audio_manager import*
from .global_parameters import*
from .response_box import*
from .dialog_edit_preferences import*
from .dialog_edit_phones import*
from .dialog_edit_experimenters import*
from .dialog_process_results import*
from .dialog_show_fortune import*
from .dialog_swap_blocks import*



#from redirect_out import*
from . import default_experiments
import fnmatch
from ._version_info import*
__version__ = pychoacoustics_version

homeExperimentsPath = os.path.expanduser("~") +'/pychoacoustics_exp/'
if os.path.exists(homeExperimentsPath + 'labexp/__init__.py') == True:
    sys.path.append(homeExperimentsPath)

try:
    import labexp
    from labexp import*
    labexp_exists = True
except:
    labexp_exists = False

class pychControlWin(QtGui.QMainWindow):
    def __init__(self, parent=None, prm=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.prm = prm
        self.audioManager = audioManager(self)
        self.audioManager.initializeAudio()
        #
        self.prm['version'] = __version__
        #self.prm['revno'] = pychoacoustics_revno
        self.prm['builddate'] = pychoacoustics_builddate
        #
        screen = QtGui.QDesktopWidget().screenGeometry()
        self.setGeometry(80, 100, int((2/3)*screen.width()), int((7/10)*screen.height()))
        #self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint)
        self.currLocale = prm['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.OmitGroupSeparator | self.currLocale.RejectGroupSeparator)
        self.setWindowTitle(self.tr("Pychoacoustics - Control Window"))
        self.menubar = self.menuBar()
        self.statusBar()
        self.parametersFile = None 
        self.prm['currentRepetition'] = 1
        #FILE MENU
        self.fileMenu = self.menubar.addMenu(self.tr('&File'))
        self.exitButton = QtGui.QAction(QtGui.QIcon.fromTheme("application-exit", QtGui.QIcon(":/application-exit")), self.tr('Exit'), self)
        self.exitButton.setShortcut('Ctrl+Q')
        self.exitButton.setStatusTip(self.tr('Exit application'))

        self.exitButton.triggered.connect(self.close)

        self.processResultsMenu = self.fileMenu.addMenu(self.tr('&Process Results'))
        
        self.processResultsLinearButton = QtGui.QAction(self.tr('&Process Results (Plain Text)'), self)
        self.processResultsLinearButton.setStatusTip(self.tr('Process Results (Plain Text)'))
        #self.connect(self.processResultsLinearButton, QtCore.SIGNAL('triggered()'), self.processResultsLinearDialog)
        self.processResultsLinearButton.triggered.connect(self.processResultsLinearDialog)

        self.processResultsTableButton = QtGui.QAction(self.tr('&Process Results Table'), self)
        self.processResultsTableButton.setStatusTip(self.tr('Process Results Table'))
        #self.connect(self.processResultsTableButton, QtCore.SIGNAL('triggered()'), self.processResultsTableDialog)
        self.processResultsTableButton.triggered.connect(self.processResultsTableDialog)


        self.openResultsButton = QtGui.QAction(QtGui.QIcon.fromTheme("document-open", QtGui.QIcon(":/document-open")), self.tr('Open Results File'), self)
        self.openResultsButton.setStatusTip(self.tr('Open Results File'))
        #self.connect(self.openResultsButton, QtCore.SIGNAL('triggered()'), self.onClickOpenResultsButton)
        self.openResultsButton.triggered.connect(self.onClickOpenResultsButton)

        self.processResultsMenu.addAction(self.processResultsLinearButton)
        self.processResultsMenu.addAction(self.processResultsTableButton)
        
        self.fileMenu.addAction(self.openResultsButton)
        self.fileMenu.addAction(self.exitButton)
        
        #EDIT MENU
        self.editMenu = self.menubar.addMenu(self.tr('&Edit'))
        self.editPrefAction = QtGui.QAction(QtGui.QIcon.fromTheme("preferences-other", QtGui.QIcon(":/preferences-other")), self.tr('Preferences'), self)
        self.editMenu.addAction(self.editPrefAction)
        #self.connect(self.editPrefAction, QtCore.SIGNAL('triggered()'), self.onEditPref)
        self.editPrefAction.triggered.connect(self.onEditPref)

        self.editPhonesAction = QtGui.QAction(QtGui.QIcon.fromTheme("audio-headphones", QtGui.QIcon(":/audio-headphones")), self.tr('Phones'), self)
        self.editMenu.addAction(self.editPhonesAction)
        #self.connect(self.editPhonesAction, QtCore.SIGNAL('triggered()'), self.onEditPhones)
        self.editPhonesAction.triggered.connect(self.onEditPhones)

        self.editExperimentersAction = QtGui.QAction(QtGui.QIcon.fromTheme("system-users", QtGui.QIcon(":/system-users")), self.tr('Experimenters'), self)
        self.editMenu.addAction(self.editExperimentersAction)
        #self.connect(self.editExperimentersAction, QtCore.SIGNAL('triggered()'), self.onEditExperimenters)
        self.editExperimentersAction.triggered.connect(self.onEditExperimenters)

        #TOOLS MENU
        self.toolsMenu = self.menubar.addMenu(self.tr('&Tools'))
        self.swapBlocksAction = QtGui.QAction(self.tr('Swap Blocks'), self)
        self.toolsMenu.addAction(self.swapBlocksAction)
        #self.connect(self.swapBlocksAction, QtCore.SIGNAL('triggered()'), self.onSwapBlocksAction)
        self.swapBlocksAction.triggered.connect(self.onSwapBlocksAction)

        #HELP MENU
        self.helpMenu = self.menubar.addMenu(self.tr('&Help'))

        self.onShowManualPdfAction = QtGui.QAction(self.tr('Manual (pdf)'), self)
        self.helpMenu.addAction(self.onShowManualPdfAction)
        self.connect(self.onShowManualPdfAction, QtCore.SIGNAL('triggered()'), self.onShowManualPdf)

        self.onShowModulesDocAction = QtGui.QAction(self.tr('Manual (html)'), self)
        self.helpMenu.addAction(self.onShowModulesDocAction)
        self.connect(self.onShowModulesDocAction, QtCore.SIGNAL('triggered()'), self.onShowModulesDoc)

        self.onShowFortuneAction = QtGui.QAction(self.tr('Fortunes'), self)
        self.helpMenu.addAction(self.onShowFortuneAction)
        self.connect(self.onShowFortuneAction, QtCore.SIGNAL('triggered()'), self.onShowFortune)
        
        self.onAboutAction = QtGui.QAction(QtGui.QIcon.fromTheme("help-about", QtGui.QIcon(":/help-about")), self.tr('About pychoacoustics'), self)
        self.helpMenu.addAction(self.onAboutAction)
        self.connect(self.onAboutAction, QtCore.SIGNAL('triggered()'), self.onAbout)

        #TOOLBAR???
        ## self.toolbar = self.addToolBar('Control Window Toolbar')
        ## self.saveResultsAction = QtGui.QAction(QtGui.QIcon.fromTheme("document-save", QtGui.QIcon(":/document-save")), self.tr("Save results"), self)
        ## self.connect(self.saveResultsAction, QtCore.SIGNAL('triggered()'), self.onClickSaveResultsButton)
        ## self.toolbar.addAction(self.saveResultsAction)
        ## self.toolbar.addAction(self.editPhonesAction)
        
        self.currExp = None 
        self.prevExp = None

        self.currParadigm = None 
        self.prevParadigm = None

        self.prm["currentBlock"] = 1
        self.prm["storedBlocks"] = 0
        self.par = {}

        self.cw = QtGui.QFrame()
        self.pw = dropFrame(None)
        self.cw.setFrameStyle(QtGui.QFrame.StyledPanel|QtGui.QFrame.Sunken)
        self.pw.setFrameStyle(QtGui.QFrame.StyledPanel|QtGui.QFrame.Sunken)
        self.splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        QtCore.QObject.connect(self.pw, QtCore.SIGNAL("dropped"), self.onDropPrmFile)

        self.onWhatsThisAction = QtGui.QAction(QtGui.QIcon.fromTheme("help-contextual", QtGui.QIcon(":/help-contextual")), self.tr('?'), self)
        self.menubar.addAction(self.onWhatsThisAction)
        self.connect(self.onWhatsThisAction, QtCore.SIGNAL('triggered()'), self.onWhatsThis)

        #STATUS BAR
        if "resultsFile" not in self.prm:
            self.statusBar().showMessage(self.tr('No results file selected, saving to file: test.txt'))
        else:
            self.statusBar().showMessage(self.tr('Saving results to file: ') + self.prm["resultsFile"])
       

        self.cw_sizer = QtGui.QVBoxLayout()
        self.def_widg_sizer = QtGui.QGridLayout()
        n = 0

        #LISTENER
        self.listenerLabel = QLabel(self.tr('Listener:'), self)
        self.def_widg_sizer.addWidget(self.listenerLabel,n, 0)
        self.listenerTF = QLineEdit("")
        if 'listener' in self.prm:
            self.listenerTF.setText(self.prm['listener'])
        self.connect(self.listenerTF, QtCore.SIGNAL('editingFinished()'), self.onListenerChange)
        self.listenerTF.setWhatsThis(self.tr("Set a label (e.g. initials, or full name) for the listener being tested."))
        self.def_widg_sizer.addWidget(self.listenerTF, n, 1)
        #EXPERIMENT LABEL
        n = n+1
        self.experimentLabelLabel = QLabel(self.tr('Experiment Label:'), self)
        self.def_widg_sizer.addWidget(self.experimentLabelLabel, n, 0)
        self.experimentLabelTF = QLineEdit("")
        self.experimentLabelTF.setWhatsThis(self.tr("Set a label for the current experiment."))
        self.def_widg_sizer.addWidget(self.experimentLabelTF, n, 1)
        #SESSION LABEL
        self.sessionLabelLabel = QLabel(self.tr('Session:'), self)
        self.def_widg_sizer.addWidget(self.sessionLabelLabel, n, 2)
        self.sessionLabelTF = QLineEdit("")
        if 'sessionLabel' in self.prm:
            self.sessionLabelTF.setText(self.prm['sessionLabel'])
        self.def_widg_sizer.addWidget(self.sessionLabelTF, n, 3)
        self.sessionLabelTF.setWhatsThis(self.tr("Set a label for the current experimental session. It can be a number or a descriptive word."))
        self.connect(self.sessionLabelTF, QtCore.SIGNAL('editingFinished()'), self.onSessionLabelChange)
        #CONDITION LABEL
        n = n+1
        self.conditionLabelLabel = QLabel(self.tr('Condition Label:'), self)
        self.def_widg_sizer.addWidget(self.conditionLabelLabel, n, 0)
        self.conditionLabelTF = QLineEdit("")
        self.conditionLabelTF.setWhatsThis(self.tr("Set a label for the current experimental condition. This label applies only to the current experimental block."))
        self.def_widg_sizer.addWidget(self.conditionLabelTF, n, 1, 1, 3)
        #END COMMAND
        n = n+1
        self.endExpCommandLabel = QLabel(self.tr('End Command:'), self)
        self.def_widg_sizer.addWidget(self.endExpCommandLabel, n, 0)
        self.endExpCommandTF = QLineEdit("")
        self.endExpCommandTF.setWhatsThis(self.tr("Allows you to specify an operating system command at the end of the experiment (e.g. to process the results files, make a backup copy, etc...). Consult the pychoacoustics manual for further info."))
        self.def_widg_sizer.addWidget(self.endExpCommandTF, n, 1, 1, 3)
        #SHUFFLE ORDER
        n = n+1
        self.shufflingSchemeLabel = QLabel(self.tr('Shuffling Scheme:'), self)
        self.def_widg_sizer.addWidget(self.shufflingSchemeLabel, n, 0)
        self.shufflingSchemeTF = QLineEdit("")
        self.shufflingSchemeTF.setWhatsThis(self.tr("Give a blocks shuffling scheme. Example ([1,2,3],(4,5,6)) runs the first group of blocks '1,2,3' in random order, before running the second group of blocks '4,5,6', in linearorder. Consult the pychoacoustics manual for further info."))
        self.def_widg_sizer.addWidget(self.shufflingSchemeTF, n, 1, 1, 3)
        n = n+1
        #PROC RES
        self.procResCheckBox = QtGui.QCheckBox(self.tr('Proc. Res.'))
        self.def_widg_sizer.addWidget(self.procResCheckBox, n, 0)
        #PROC RES TABLE
        self.procResTableCheckBox = QtGui.QCheckBox(self.tr('Proc. Res. Table'))
        self.connect(self.procResTableCheckBox, QtCore.SIGNAL('stateChanged(int)'), self.toggleResTableCheckBox)
        self.def_widg_sizer.addWidget(self.procResTableCheckBox, n, 1)
        n = n+1
        #PLOT
        self.winPlotCheckBox = QtGui.QCheckBox(self.tr('Plot'))
        self.connect(self.winPlotCheckBox, QtCore.SIGNAL('stateChanged(int)'), self.toggleWinPlotCheckBox)
        self.def_widg_sizer.addWidget(self.winPlotCheckBox, n, 0)
        if self.prm['appData']['plotting_available'] == False:
            self.winPlotCheckBox.hide()
        #PDF PLOT
        self.pdfPlotCheckBox = QtGui.QCheckBox(self.tr('PDF Plot'))
        self.connect(self.pdfPlotCheckBox, QtCore.SIGNAL('stateChanged(int)'), self.togglePdfPlotCheckBox)
        self.def_widg_sizer.addWidget(self.pdfPlotCheckBox, n, 1)
        if self.prm['appData']['plotting_available'] == False:
            self.pdfPlotCheckBox.hide()
        #EXPERIMENTER
        n = n+1
        self.experimenterLabel =  QLabel(self.tr("Experimenter:"), self)
        self.def_widg_sizer.addWidget(self.experimenterLabel, n, 0)
        self.experimenterChooser = QComboBox()
        self.experimenterChooser.addItems(self.prm['experimenter']['experimenter_id'])
        self.experimenterChooser.setCurrentIndex(self.prm['experimenter']['defaultExperimenter'].index("\u2713"))
        self.experimenterChooser.setWhatsThis(self.tr("Allows choosing the experimenter identifier. This must have been previously stored in the experimenters database. On the toolbar click on the Edit > Experimenters to modify the experimenters database"))
        self.def_widg_sizer.addWidget(self.experimenterChooser, n, 1)
        #EXPERIMENT
        n = n+1
        self.experimentLabel =  QLabel(self.tr("Experiment:"), self)
        self.def_widg_sizer.addWidget(self.experimentLabel, n, 0)
        self.experimentChooser = QComboBox()
        self.experimentChooser.addItems(self.prm['experimentsChoices'])
        self.def_widg_sizer.addWidget(self.experimentChooser, n, 1)
        self.connect(self.experimentChooser, SIGNAL('activated(QString)'), self.onExperimentChange)
        #PARADIGM
        n = n+1
        self.paradigmLabel = QLabel(self.tr("Paradigm:"), self)
        self.def_widg_sizer.addWidget(self.paradigmLabel, n, 0)
        self.paradigmChooser = QComboBox()
        self.paradigmChooser.addItems(self.prm[self.tr('Audiogram')]['paradigmChoices'])
        self.paradigmChooser.setCurrentIndex(1)
        self.def_widg_sizer.addWidget(self.paradigmChooser, n, 1)
        self.connect(self.paradigmChooser, SIGNAL('activated(QString)'), self.onParadigmChange)
        #PHONES
        n = n+1
        self.phonesLabel = QLabel(self.tr("Phones:"), self)
        self.def_widg_sizer.addWidget(self.phonesLabel, n, 0)
        self.phonesChooser = QComboBox()
        self.phonesChooser.addItems(self.prm['phones']['phonesChoices'])
        self.phonesChooser.setCurrentIndex(self.prm['phones']['defaultPhones'].index("\u2713"))
        self.def_widg_sizer.addWidget(self.phonesChooser, n, 1)
        #SAMPLING RATE
        n = n+1
        self.sampRateLabel = QLabel(self.tr("Sample Rate (Hz):"), self)
        self.def_widg_sizer.addWidget(self.sampRateLabel, n, 0)
        self.sampRateTF = QLineEdit()
        self.sampRateTF.setText(self.prm["pref"]["sound"]["defaultSampleRate"])
        self.sampRateTF.setValidator(QtGui.QIntValidator(self))
        self.def_widg_sizer.addWidget(self.sampRateTF, n, 1)
        self.prm['sampRate'] =  self.currLocale.toInt(self.sampRateTF.text())[0]
        #BITS
        n = n+1
        self.nBitsLabel = QLabel(self.tr("Bits:"))
        self.def_widg_sizer.addWidget(self.nBitsLabel, n, 0)
        self.nBitsChooser = QComboBox()
        self.nBitsChooser.addItems(self.prm["nBitsChoices"])
        self.nBitsChooser.setCurrentIndex(self.prm["nBitsChoices"].index(self.prm["pref"]["sound"]["defaultNBits"])) 
        self.def_widg_sizer.addWidget(self.nBitsChooser, n, 1)
        #self.def_widg_sizer.addItem(QtGui.QSpacerItem(10,10,QtGui.QSizePolicy.Expanding), 0, 2)
        #self.def_widg_sizer.addItem(QtGui.QSpacerItem(10,10,QtGui.QSizePolicy.Expanding), 0, 3)
        #REPETITIONS
        n = n+1
        self.repetitionsLabel = QLabel(self.tr("No. Repetitions:"), self)
        self.def_widg_sizer.addWidget(self.repetitionsLabel, n, 0)
        self.repetitionsTF = QLineEdit()
        self.repetitionsTF.setText('1')
        self.repetitionsTF.setValidator(QtGui.QIntValidator(self))
        self.repetitionsTF.setWhatsThis(self.tr("Sets the number of times the series of blocks is repeated"))
        self.def_widg_sizer.addWidget(self.repetitionsTF, n, 1)
        #PRE-TRIAL Silence
        n = n+1
        self.preTrialSilenceLabel = QLabel(self.tr("Pre-Trial Silence (ms):"), self)
        self.def_widg_sizer.addWidget(self.preTrialSilenceLabel, n, 0)
        self.preTrialSilenceTF = QLineEdit()
        self.preTrialSilenceTF.setText(self.prm["pref"]["general"]["preTrialSilence"])
        self.preTrialSilenceTF.setValidator(QtGui.QIntValidator(self))
        self.preTrialSilenceTF.setWhatsThis(self.tr("Sets the duration of a silent pause between the moment the listener has given the response and the start of the next trial"))
        self.def_widg_sizer.addWidget(self.preTrialSilenceTF, n, 1)
        #Warning Interval
        n = n+1
        ## self.warningInterval = QCheckBox(self.tr("Warning Interval"), self)
        ## self.warningInterval.setChecked(False)
        ## self.connect(self.warningInterval, QtCore.SIGNAL('stateChanged(int)'), self.onWarningIntervalChange)
        ## self.def_widg_sizer.addWidget(self.warningInterval, n, 0)
        self.warningIntervalLabel =  QLabel(self.tr("Warning Interval:"), self)
        self.warningIntervalChooser = QComboBox()
        self.warningIntervalChooser.addItems([self.tr("Yes"), self.tr("No")])
        self.warningIntervalChooser.setCurrentIndex(self.warningIntervalChooser.findText(self.tr("No")))
        self.connect(self.warningIntervalChooser, SIGNAL('activated(QString)'), self.onWarningIntervalChange)
        self.def_widg_sizer.addWidget(self.warningIntervalLabel, n, 0)
        self.def_widg_sizer.addWidget(self.warningIntervalChooser, n, 1)
        n = n+1
        self.warningIntervalDurLabel = QLabel(self.tr("Warning Interval Duration (ms):"), self)
        self.def_widg_sizer.addWidget(self.warningIntervalDurLabel, n, 0)
        self.warningIntervalDurLabel.hide()
        self.warningIntervalDurTF = QLineEdit()
        self.warningIntervalDurTF.setText("500")
        self.warningIntervalDurTF.setValidator(QtGui.QIntValidator(self))
        self.warningIntervalDurTF.setWhatsThis(self.tr("Sets the duration of the warning interval light"))
        self.warningIntervalDurTF.hide()
        self.def_widg_sizer.addWidget(self.warningIntervalDurTF, n, 1)
        n = n+1
        self.warningIntervalISILabel = QLabel(self.tr("Warning Interval ISI (ms):"), self)
        self.def_widg_sizer.addWidget(self.warningIntervalISILabel, n, 0)
        self.warningIntervalISILabel.hide()
        self.warningIntervalISITF = QLineEdit()
        self.warningIntervalISITF.setText("500")
        self.warningIntervalISITF.setValidator(QtGui.QIntValidator(self))
        self.warningIntervalISITF.setWhatsThis(self.tr("Sets the duration of the silent interval between the warning interval and the first observation interval"))
        self.warningIntervalISITF.hide()
        self.def_widg_sizer.addWidget(self.warningIntervalISITF, n, 1)
        #INTERVAL LIGHTS
        n = n+1
        self.intervalLightsLabel = QLabel(self.tr("Interval Lights:"))
        self.def_widg_sizer.addWidget(self.intervalLightsLabel, n, 0)
        self.intervalLightsChooser = QComboBox()
        self.intervalLightsChooser.addItems([self.tr("Yes"), self.tr("No")])
        self.intervalLightsChooser.setCurrentIndex(self.intervalLightsChooser.findText(self.prm['intervalLights']))
        self.def_widg_sizer.addWidget(self.intervalLightsChooser, n, 1)
        self.connect(self.intervalLightsChooser, SIGNAL('activated(QString)'), self.onIntervalLightsChange)
        #RESULTS FILE
        n = n+1
        self.saveResultsLabel =  QLabel(self.tr("Results File:"), self)
        self.def_widg_sizer.addWidget(self.saveResultsLabel, n, 0)
        min_pw_butt_size = 22
        min_pw_icon_size = 20
        
        self.def_widg_sizer.setRowMinimumHeight(0, min_pw_butt_size)
        self.saveResultsButton = QtGui.QPushButton(self.tr("Choose Results File"), self)
        QtCore.QObject.connect(self.saveResultsButton,
                               QtCore.SIGNAL('clicked()'), self.onClickSaveResultsButton)
        self.saveResultsButton.setIcon(QtGui.QIcon.fromTheme("document-save", QtGui.QIcon(":/document-save")))
        self.saveResultsButton.setIconSize(QtCore.QSize(min_pw_icon_size, min_pw_icon_size))
        self.saveResultsButton.setToolTip(self.tr("Choose file to save results"))
        self.def_widg_sizer.addWidget(self.saveResultsButton, n, 1, 1, 1)
        #Additional Widgets
        self.add_widg_sizer = QtGui.QGridLayout()
        self.add_widg_sizer.addItem(QtGui.QSpacerItem(10,10, QtGui.QSizePolicy.Expanding), 0, 2)
        self.add_widg_sizer.addItem(QtGui.QSpacerItem(10,10, QtGui.QSizePolicy.Expanding), 0, 3)
        #self.setAdditionalWidgets(self.currExp, self.prevExp) later

        #def widgets 2
        self.def_widg_sizer2 = QtGui.QGridLayout()
      
        # SHUFFLE MODE
        self.shuffleLabel = QLabel(self.tr("Shuffle Mode:"))
        self.def_widg_sizer2.addWidget(self.shuffleLabel, 1, 0)
        self.shuffleChooser = QComboBox()
        self.shuffleChooser.addItems(self.prm['shuffleChoices'])
        self.shuffleChooser.setCurrentIndex(self.prm['shuffleChoices'].index(QApplication.translate("",self.prm['pref']['general']['defaultShuffle'],"", QApplication.UnicodeUTF8)))   
        self.def_widg_sizer2.addWidget(self.shuffleChooser, 1, 1)
        self.def_widg_sizer2.addItem(QtGui.QSpacerItem(10,10,QtGui.QSizePolicy.Expanding), 0, 4)

        #ONOFF Trigger
        self.triggerCheckBox = QtGui.QCheckBox(self.tr('EEG ON/OFF Trigger'))
        self.def_widg_sizer2.addWidget(self.triggerCheckBox, 1, 2)

        #RESPONSE MODE
        self.responseModeLabel = QLabel(self.tr("Response Mode:"))
        self.def_widg_sizer2.addWidget(self.responseModeLabel, 2, 0)
        self.responseModeChooser = QComboBox()
        self.responseModeChooser.addItems(self.prm['responseModeChoices'])
        self.responseModeChooser.setCurrentIndex(self.prm['responseModeChoices'].index(QApplication.translate("",self.prm['pref']['general']['defaultResponseMode'],"", QApplication.UnicodeUTF8)))
        self.connect(self.responseModeChooser, SIGNAL('activated(QString)'), self.onResponseModeChange)
        self.def_widg_sizer2.addWidget(self.responseModeChooser, 2, 1)
        

        self.autoPCorrLabel = QLabel(self.tr("Percent Correct (%):"), self)
        self.def_widg_sizer2.addWidget(self.autoPCorrLabel, 2, 2)
        self.autoPCorrTF = QLineEdit()
        self.autoPCorrTF.setText('75')
        self.autoPCorrTF.setValidator(QtGui.QDoubleValidator(0, 100, 6, self))
        self.def_widg_sizer2.addWidget(self.autoPCorrTF, 2, 3)
        self.autoPCorrLabel.hide()
        self.autoPCorrTF.hide()
        #PARADIGM WIDGETS SIZER
        self.paradigm_widg_sizer = QtGui.QGridLayout()


        #PARAMETERS WINDOW
        self.pw_sizer = QtGui.QVBoxLayout()
        self.pw_buttons_sizer = QtGui.QGridLayout()
        min_pw_butt_size = 22
        min_pw_icon_size = 20
        self.pw_buttons_sizer.setRowMinimumHeight(0, min_pw_butt_size)
        self.pw_buttons_sizer.setRowMinimumHeight(1, min_pw_butt_size)
        self.pw_buttons_sizer.setRowMinimumHeight(2, min_pw_butt_size)
    
        #---- FIRST ROW
        n = 0
        #LOAD PARAMETERS BUTTON
        self.loadParametersButton = QtGui.QPushButton(self.tr("Load Prm"), self)
        self.loadParametersButton.setIcon(QtGui.QIcon.fromTheme("document-open", QtGui.QIcon(":/document-open")))
        self.loadParametersButton.setIconSize(QtCore.QSize(min_pw_icon_size, min_pw_icon_size))
        QtCore.QObject.connect(self.loadParametersButton,
                               QtCore.SIGNAL('clicked()'), self.onClickLoadParametersButton)
        self.loadParametersButton.setToolTip(self.tr("Load a parameters file"))
        self.loadParametersButton.setWhatsThis(self.tr("Load a file containing the parameters for an experimental session"))
        self.loadParametersButton.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.pw_buttons_sizer.addWidget(self.loadParametersButton, n, 0)

        #SAVE PARAMETERS BUTTON
        self.saveParametersButton = QtGui.QPushButton(self.tr("Save Prm"), self)
        self.saveParametersButton.setIcon(QtGui.QIcon.fromTheme("document-save", QtGui.QIcon(":/document-save")))
        self.saveParametersButton.setIconSize(QtCore.QSize(min_pw_icon_size, min_pw_icon_size))
        QtCore.QObject.connect(self.saveParametersButton,
                               QtCore.SIGNAL('clicked()'), self.onClickSaveParametersButton)
        self.saveParametersButton.setToolTip(self.tr("Save a parameters file"))
        self.saveParametersButton.setWhatsThis(self.tr("Save the current experimental parameters to a file"))
        self.saveParametersButton.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.pw_buttons_sizer.addWidget(self.saveParametersButton, n, 1)

        #DELETE PARAMETERS BUTTON
        self.deleteParametersButton = QtGui.QPushButton(self.tr("Delete"), self)
        QtCore.QObject.connect(self.deleteParametersButton,
                               QtCore.SIGNAL('clicked()'), self.onClickDeleteParametersButton)
        self.deleteParametersButton.setIcon(QtGui.QIcon.fromTheme("edit-delete", QtGui.QIcon(":/edit-delete")))
        self.deleteParametersButton.setIconSize(QtCore.QSize(min_pw_icon_size, min_pw_icon_size))
        self.deleteParametersButton.setToolTip(self.tr("Delete current Block"))
        self.deleteParametersButton.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.pw_buttons_sizer.addWidget(self.deleteParametersButton, n, 2)

     
        self.undoUnsavedButton = QtGui.QPushButton(self.tr("Undo Unsaved"), self)
        QtCore.QObject.connect(self.undoUnsavedButton,
                               QtCore.SIGNAL('clicked()'), self.onClickUndoUnsavedButton)
        self.undoUnsavedButton.setIcon(QtGui.QIcon.fromTheme("edit-undo", QtGui.QIcon(":/edit-undo")))
        self.undoUnsavedButton.setIconSize(QtCore.QSize(min_pw_icon_size, min_pw_icon_size))
        self.undoUnsavedButton.setToolTip(self.tr("Undo unsaved changes"))
        self.undoUnsavedButton.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.pw_buttons_sizer.addWidget(self.undoUnsavedButton, n, 3)

        #---- SECOND ROW
        n = n+1
        self.storeParametersButton = QtGui.QPushButton(self.tr("Store"), self)
        QtCore.QObject.connect(self.storeParametersButton,
                               QtCore.SIGNAL('clicked()'), self.onClickStoreParametersButton)
        self.storeParametersButton.setIcon(QtGui.QIcon.fromTheme("media-flash-memory-stick", QtGui.QIcon(":/media-flash-memory-stick")))
        self.storeParametersButton.setIconSize(QtCore.QSize(min_pw_icon_size, min_pw_icon_size))
        self.storeParametersButton.setToolTip(self.tr("Store current Block"))
        self.storeParametersButton.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.pw_buttons_sizer.addWidget(self.storeParametersButton, n, 0)

        self.storeandaddParametersButton = QtGui.QPushButton(self.tr("Store 'n' add!"), self)
        QtCore.QObject.connect(self.storeandaddParametersButton,
                               QtCore.SIGNAL('clicked()'), self.onClickStoreandaddParametersButton)
        self.storeandaddParametersButton.setToolTip(self.tr("Store current Block and add a new one"))
        self.storeandaddParametersButton.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.pw_buttons_sizer.addWidget(self.storeandaddParametersButton, n, 1)
        
        self.storeandgoParametersButton = QtGui.QPushButton(self.tr("Store 'n' go!"), self)
        QtCore.QObject.connect(self.storeandgoParametersButton,
                               QtCore.SIGNAL('clicked()'), self.onClickStoreandgoParametersButton)
        self.storeandgoParametersButton.setToolTip(self.tr("Store current Block and move to the next"))
        self.storeandgoParametersButton.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.pw_buttons_sizer.addWidget(self.storeandgoParametersButton, n, 2)

        self.newBlockButton = QtGui.QPushButton(self.tr("New Block"), self)
        QtCore.QObject.connect(self.newBlockButton,
                               QtCore.SIGNAL('clicked()'), self.onClickNewBlockButton)
        self.newBlockButton.setIcon(QtGui.QIcon.fromTheme("document-new", QtGui.QIcon(":/document-new")))
        self.newBlockButton.setIconSize(QtCore.QSize(min_pw_icon_size, min_pw_icon_size))
        self.newBlockButton.setToolTip(self.tr("Append a new block"))
        self.newBlockButton.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.pw_buttons_sizer.addWidget(self.newBlockButton, n, 3)

      
      

        #---- THIRD ROW
        n = n+1
        self.prevBlockButton = QtGui.QPushButton(self.tr("Previous"), self)
        QtCore.QObject.connect(self.prevBlockButton,
                               QtCore.SIGNAL('clicked()'), self.onClickPrevBlockButton)
        self.prevBlockButton.setIcon(QtGui.QIcon.fromTheme("go-previous", QtGui.QIcon(":/go-previous")))
        self.prevBlockButton.setIconSize(QtCore.QSize(min_pw_icon_size, min_pw_icon_size))
        self.prevBlockButton.setToolTip(self.tr("Move to previous block"))
        self.prevBlockButton.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.pw_buttons_sizer.addWidget(self.prevBlockButton, n, 0)

        self.nextBlockButton = QtGui.QPushButton(self.tr("Next"), self)
        QtCore.QObject.connect(self.nextBlockButton,
                               QtCore.SIGNAL('clicked()'), self.onClickNextBlockButton)
        self.nextBlockButton.setIcon(QtGui.QIcon.fromTheme("go-next", QtGui.QIcon(":/go-next")))
        self.nextBlockButton.setIconSize(QtCore.QSize(min_pw_icon_size, min_pw_icon_size))
        self.nextBlockButton.setToolTip(self.tr("Move to next block"))
        self.nextBlockButton.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.pw_buttons_sizer.addWidget(self.nextBlockButton, n, 1)

        self.shuffleBlocksButton = QtGui.QPushButton(self.tr("Shuffle"), self)
        QtCore.QObject.connect(self.shuffleBlocksButton,
                               QtCore.SIGNAL('clicked()'), self.onClickShuffleBlocksButton)
        self.shuffleBlocksButton.setIcon(QtGui.QIcon.fromTheme("media-playlist-shuffle", QtGui.QIcon(":/media-playlist-shuffle")))
        self.shuffleBlocksButton.setIconSize(QtCore.QSize(min_pw_icon_size, min_pw_icon_size))
        self.shuffleBlocksButton.setToolTip(self.tr("Shuffle blocks"))
        self.shuffleBlocksButton.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.pw_buttons_sizer.addWidget(self.shuffleBlocksButton, n, 2)
        
        self.resetParametersButton = QtGui.QPushButton(self.tr("Reset"), self)
        QtCore.QObject.connect(self.resetParametersButton,
                               QtCore.SIGNAL('clicked()'), self.onClickResetParametersButton)
        self.resetParametersButton.setIcon(QtGui.QIcon.fromTheme("go-home", QtGui.QIcon(":/go-home")))
        self.resetParametersButton.setIconSize(QtCore.QSize(min_pw_icon_size, min_pw_icon_size))
        self.resetParametersButton.setToolTip(self.tr("Reset parameters"))
        self.resetParametersButton.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.pw_buttons_sizer.addWidget(self.resetParametersButton, n, 3)

     
       
        n = n+1
        self.pw_buttons_sizer.addItem(QtGui.QSpacerItem(10,10,QtGui.QSizePolicy.Expanding), n, 0, 1, 4)


        #----FOURTH ROW
        n = n+1
        self.currentBlockLabel = QLabel(self.tr("Current Block:"))
        self.pw_buttons_sizer.addWidget(self.currentBlockLabel, n, 0)

        self.currentBlockCountLabel = QLabel(str(self.prm["currentBlock"]))
        self.pw_buttons_sizer.addWidget(self.currentBlockCountLabel, n, 1)

        self.storedBlocksLabel = QLabel(self.tr("Stored Blocks:"))
        self.pw_buttons_sizer.addWidget(self.storedBlocksLabel, n, 2)

        self.storedBlocksCountLabel = QLabel(str(self.prm["storedBlocks"]))
        self.pw_buttons_sizer.addWidget(self.storedBlocksCountLabel, n, 3)

        #FIFTH ROW
        n = n+1
        self.currentBlockPositionLabelLabel = QLabel(self.tr("Block Position:"))
        self.pw_buttons_sizer.addWidget(self.currentBlockPositionLabelLabel, n, 0)
        self.currentBlockPositionLabel = QLabel(str(self.prm["currentBlock"]))
        self.pw_buttons_sizer.addWidget(self.currentBlockPositionLabel, n, 1)
        
        self.jumpToBlockLabel = QLabel(self.tr("Jump to Block:"))
        self.jumpToBlockChooser = QComboBox()
        self.connect(self.jumpToBlockChooser, QtCore.SIGNAL('activated(QString)'), self.onJumpToBlockChange)
        self.pw_buttons_sizer.addWidget(self.jumpToBlockLabel, n, 2)
        self.pw_buttons_sizer.addWidget(self.jumpToBlockChooser, n, 3)
        # SIXTH ROW
        n = n+1
        self.prevBlockPositionButton = QtGui.QPushButton(self.tr("Previous Position"), self)
        QtCore.QObject.connect(self.prevBlockPositionButton,
                               QtCore.SIGNAL('clicked()'), self.onClickPrevBlockPositionButton)
        self.prevBlockPositionButton.setIcon(QtGui.QIcon.fromTheme("go-previous", QtGui.QIcon(":/go-previous")))
        self.prevBlockPositionButton.setToolTip(self.tr("Move to previous block position"))
        self.pw_buttons_sizer.addWidget(self.prevBlockPositionButton, n, 0)

        self.nextBlockPositionButton = QtGui.QPushButton(self.tr("Next Position"), self)
        QtCore.QObject.connect(self.nextBlockPositionButton,
                               QtCore.SIGNAL('clicked()'), self.onClickNextBlockPositionButton)
        self.nextBlockPositionButton.setIcon(QtGui.QIcon.fromTheme("go-next", QtGui.QIcon(":/go-next")))
        self.nextBlockPositionButton.setToolTip(self.tr("Move to next block position"))
        self.pw_buttons_sizer.addWidget(self.nextBlockPositionButton, n, 1)

        self.jumpToPositionLabel = QLabel(self.tr("Jump to Position:"))
        self.jumpToPositionChooser = QComboBox()
        self.connect(self.jumpToPositionChooser, QtCore.SIGNAL('activated(QString)'), self.onJumpToPositionChange)
        self.pw_buttons_sizer.addWidget(self.jumpToPositionLabel, n, 2)
        self.pw_buttons_sizer.addWidget(self.jumpToPositionChooser, n, 3)

        # SEVENTH ROW
        n = n+1
        self.shiftBlockDownButton = QtGui.QPushButton(self.tr("< Shift Blk. Down"), self)
        QtCore.QObject.connect(self.shiftBlockDownButton,
                               QtCore.SIGNAL('clicked()'), self.onClickShiftBlockDownButton)
        self.shiftBlockDownButton.setToolTip(self.tr("Shift Block. Down"))
        self.pw_buttons_sizer.addWidget(self.shiftBlockDownButton, n, 2)

        self.shiftBlockUpButton = QtGui.QPushButton(self.tr("Shift Blk. Up >"), self)
        QtCore.QObject.connect(self.shiftBlockUpButton,
                               QtCore.SIGNAL('clicked()'), self.onClickShiftBlockUpButton)
        self.shiftBlockUpButton.setToolTip(self.tr("Shift Block Up"))
        self.pw_buttons_sizer.addWidget(self.shiftBlockUpButton, n, 3)
        
        
        n = n+1
        #spacer
        self.pw_buttons_sizer.addItem(QtGui.QSpacerItem(10,10,QtGui.QSizePolicy.Expanding), n, 5)

        #PARAMETERS AREA
        self.pw_prm_sizer = QtGui.QHBoxLayout()
        self.pw_prm_sizer_0 = QtGui.QGridLayout()
        self.pw_prm_sizer_1 = QtGui.QGridLayout()
        #self.pw_prm_sizer_0.setVerticalSpacing(-20)
        #self.pw_prm_sizer_1.setVerticalSpacing(-20)
        self.pw_prm_sizer_0.setAlignment(Qt.AlignTop)
        self.pw_prm_sizer_1.setAlignment(Qt.AlignTop)
        self.cw_sizer.addLayout(self.def_widg_sizer)
        self.cw_sizer.addLayout(self.add_widg_sizer)
        self.cw_sizer.addLayout(self.def_widg_sizer2)
        self.cw_sizer.addLayout(self.paradigm_widg_sizer)
        self.cw.setLayout(self.cw_sizer)

        #self.pw.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        self.setDefaultParameters(self.tr("Audiogram"), self.tr("Adaptive"), self.par)
        self.cw_scrollarea = QScrollArea()
        self.cw_scrollarea.setWidget(self.cw)
        self.splitter.addWidget(self.cw_scrollarea)
        self.pw_sizer.addLayout(self.pw_buttons_sizer)
        self.pw_sizer.addSpacing(20)
        self.pw_prm_sizer.addLayout(self.pw_prm_sizer_0)
        self.pw_prm_sizer.addLayout(self.pw_prm_sizer_1)
        self.pw_sizer.addLayout(self.pw_prm_sizer)
        self.pw.setLayout(self.pw_sizer)
        self.pw.layout().setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.cw.layout().setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.pw_scrollarea = QScrollArea()
        self.pw_scrollarea.setWidget(self.pw)
        self.splitter.addWidget(self.pw_scrollarea)
        self.splitter.setSizes([(2/6)*screen.width(), (2/6)*screen.width()])
        #self.splitter.setStretchFactor(1, 1.5)
        #self.splitter.setStretchFactor(2, 1.5)
        self.setCentralWidget(self.splitter)
        
        
        self.show()
       
        self.responseBox = responseBox(self)
        self.responseBox.resize(int((1/4)*screen.width()), int((1/3)*screen.height()))
        if self.prm['calledWithPrm'] == True:
            self.loadParameters(self.prm['prmFile'])
        if self.prm['calledWithReset'] == True:
            self.onClickResetParametersButton()
        if self.prm['calledWithRecursionDepth'] == True:
            sys.setrecursionlimit(self.prm['cmdLineMaxRecursionDepth'])
        else:
            sys.setrecursionlimit(self.prm["pref"]["general"]["maxRecursionDepth"])
        if self.prm['calledWithAutostart'] == True:
            self.responseBox.onClickStatusButton()
      
     
    def setAdditionalWidgets(self, currExp, prevExp):
        if prevExp != None:
            for i in range(len(self.additionalWidgetsIntFieldList)):
                self.add_widg_sizer.removeWidget(self.additionalWidgetsIntFieldLabelList[i])
                self.additionalWidgetsIntFieldLabelList[i].setParent(None)
                self.add_widg_sizer.removeWidget(self.additionalWidgetsIntFieldList[i])
                self.additionalWidgetsIntFieldList[i].setParent(None)
                self.add_widg_sizer.removeWidget(self.additionalWidgetsIntFieldCheckBoxList[i])
                self.additionalWidgetsIntFieldCheckBoxList[i].setParent(None)
            for i in range(len(self.additionalWidgetsChooserList)):
                self.add_widg_sizer.removeWidget(self.additionalWidgetsChooserLabelList[i])
                self.additionalWidgetsChooserLabelList[i].setParent(None)
                self.add_widg_sizer.removeWidget(self.additionalWidgetsChooserList[i])
                self.additionalWidgetsChooserList[i].setParent(None)
                self.add_widg_sizer.removeWidget(self.additionalWidgetsChooserCheckBoxList[i])
                self.additionalWidgetsChooserCheckBoxList[i].setParent(None)


        #ADD ADDITIONAL WIDGETS
        n = 0
        self.additionalWidgetsIntFieldList = []
        self.additionalWidgetsIntFieldLabelList = []
        self.additionalWidgetsIntFieldCheckBoxList = []
        self.additionalWidgetsChooserList = []
        self.additionalWidgetsChooserLabelList = []
        self.additionalWidgetsChooserCheckBoxList = []

        if self.prm[self.currExp]["hasISIBox"] == True:
            self.ISILabel = QLabel(self.tr("ISI (ms):"), self)
            self.add_widg_sizer.addWidget(self.ISILabel, n, 1)
            self.ISIBox = QLineEdit()
            self.ISIBox.setText('500')
            self.ISIBox.setValidator(QtGui.QIntValidator(self))
            self.add_widg_sizer.addWidget(self.ISIBox, n, 2)
            self.ISIBoxCheckBox = QCheckBox()
            self.add_widg_sizer.addWidget(self.ISIBoxCheckBox, n, 0)
            self.additionalWidgetsIntFieldList.append(self.ISIBox)
            self.additionalWidgetsIntFieldLabelList.append(self.ISILabel)
            self.additionalWidgetsIntFieldCheckBoxList.append(self.ISIBoxCheckBox)
            n = n+1
        if self.prm[self.currExp]["hasAlternativesChooser"] == True:
            self.nIntervalsLabel = QLabel(self.tr("Intervals:"), self)
            self.add_widg_sizer.addWidget(self.nIntervalsLabel, n, 1)
            self.nIntervalsChooser = QComboBox()
            self.nIntervalsChooser.addItems(self.prm['nIntervalsChoices'])
            if 'nIntervals' in self.prm:
                self.nIntervalsChooser.setCurrentIndex(self.prm['nIntervalsChoices'].index(str(self.prm['nIntervals'])))
            else:
                self.nIntervalsChooser.setCurrentIndex(0)
            self.add_widg_sizer.addWidget(self.nIntervalsChooser, n, 2)
            self.connect(self.nIntervalsChooser, SIGNAL('activated(QString)'), self.onNIntervalsChange)
            self.nIntervalsCheckBox = QCheckBox()
            self.add_widg_sizer.addWidget(self.nIntervalsCheckBox, n, 0)
            self.additionalWidgetsChooserList.append(self.nIntervalsChooser)
            self.additionalWidgetsChooserLabelList.append(self.nIntervalsLabel)
            self.additionalWidgetsChooserCheckBoxList.append(self.nIntervalsCheckBox)
            n = n+1
            self.nAlternativesLabel = QLabel(self.tr("Alternatives:"), self)
            self.add_widg_sizer.addWidget(self.nAlternativesLabel, n, 1)
            self.nAlternativesChooser = QComboBox()
            self.nAlternativesChooser.addItems([str(self.currLocale.toInt(self.nIntervalsChooser.currentText())[0]-1), self.nIntervalsChooser.currentText()])
            self.nAlternativesChooser.setCurrentIndex(self.nAlternativesChooser.findText(str(self.prm['nAlternatives'])))
            self.add_widg_sizer.addWidget(self.nAlternativesChooser, n, 2)
            self.connect(self.nAlternativesChooser, SIGNAL('activated(QString)'), self.onNAlternativesChange)
            self.nAlternativesCheckBox = QCheckBox()
            self.add_widg_sizer.addWidget(self.nAlternativesCheckBox, n, 0)
            self.additionalWidgetsChooserList.append(self.nAlternativesChooser)
            self.additionalWidgetsChooserLabelList.append(self.nAlternativesLabel)
            self.additionalWidgetsChooserCheckBoxList.append(self.nAlternativesCheckBox)
            n = n+1

        #Pre-Trial Interval
        if self.prm[self.currExp]["hasPreTrialInterval"] == True:
            self.preTrialIntervalChooserLabel = QLabel(self.tr("Pre-Trial Interval:"), self)
            self.add_widg_sizer.addWidget(self.preTrialIntervalChooserLabel, n, 1)
            self.preTrialIntervalChooser = QComboBox()
            self.preTrialIntervalChooser.addItems([self.tr("Yes"), self.tr("No")])
            self.preTrialIntervalChooser.setCurrentIndex(1)
            self.connect(self.preTrialIntervalChooser, SIGNAL('activated(QString)'), self.onPreTrialIntervalChange)
            self.add_widg_sizer.addWidget(self.preTrialIntervalChooser, n, 2)
            self.preTrialIntervalCheckBox = QCheckBox()
            self.add_widg_sizer.addWidget(self.preTrialIntervalCheckBox, n, 0)
            self.additionalWidgetsChooserList.append(self.preTrialIntervalChooser)
            self.additionalWidgetsChooserLabelList.append(self.preTrialIntervalChooserLabel)
            self.additionalWidgetsChooserCheckBoxList.append(self.preTrialIntervalCheckBox)
            n = n+1
            self.preTrialIntervalISILabel = QLabel(self.tr("Pre-Trial Interval ISI (ms):"), self)
            self.add_widg_sizer.addWidget(self.preTrialIntervalISILabel, n, 1)
           
            self.preTrialIntervalISITF = QLineEdit()
            self.preTrialIntervalISITF.setText("500")
            self.preTrialIntervalISITF.setValidator(QtGui.QIntValidator(self))
            self.preTrialIntervalISITF.setWhatsThis(self.tr("Sets the duration of the silent interval between the pre-trial interval and the first observation interval"))
         
            self.add_widg_sizer.addWidget(self.preTrialIntervalISITF, n, 2)
            self.preTrialIntervalISICheckBox = QCheckBox()
            self.add_widg_sizer.addWidget(self.preTrialIntervalISICheckBox, n, 0)

            self.preTrialIntervalISILabel.hide()
            self.preTrialIntervalISITF.hide()
            self.preTrialIntervalISICheckBox.hide()
            
            self.additionalWidgetsIntFieldList.append(self.preTrialIntervalISITF)
            self.additionalWidgetsIntFieldLabelList.append(self.preTrialIntervalISILabel)
            self.additionalWidgetsIntFieldCheckBoxList.append(self.preTrialIntervalISICheckBox)
            n = n+1

        #Precursor Interval
        if self.prm[self.currExp]["hasPrecursorInterval"] == True:
            self.precursorIntervalChooserLabel = QLabel(self.tr("Precursor Interval:"), self)
            self.add_widg_sizer.addWidget(self.precursorIntervalChooserLabel, n, 1)
            self.precursorIntervalChooser = QComboBox()
            self.precursorIntervalChooser.addItems([self.tr("Yes"), self.tr("No")])
            self.precursorIntervalChooser.setCurrentIndex(1)
            self.connect(self.precursorIntervalChooser, SIGNAL('activated(QString)'), self.onPrecursorIntervalChange)
            self.add_widg_sizer.addWidget(self.precursorIntervalChooser, n, 2)
            self.precursorIntervalCheckBox = QCheckBox()
            self.add_widg_sizer.addWidget(self.precursorIntervalCheckBox, n, 0)
            self.additionalWidgetsChooserList.append(self.precursorIntervalChooser)
            self.additionalWidgetsChooserLabelList.append(self.precursorIntervalChooserLabel)
            self.additionalWidgetsChooserCheckBoxList.append(self.precursorIntervalCheckBox)
            n = n+1
            self.precursorIntervalISILabel = QLabel(self.tr("Precursor Interval ISI (ms):"), self)
            self.add_widg_sizer.addWidget(self.precursorIntervalISILabel, n, 1)
           
            self.precursorIntervalISITF = QLineEdit()
            self.precursorIntervalISITF.setText("500")
            self.precursorIntervalISITF.setValidator(QtGui.QIntValidator(self))
            self.precursorIntervalISITF.setWhatsThis(self.tr("Sets the duration of the silent interval between the precursor interval and the observation interval"))
         
            self.add_widg_sizer.addWidget(self.precursorIntervalISITF, n, 2)
            self.precursorIntervalISICheckBox = QCheckBox()
            self.add_widg_sizer.addWidget(self.precursorIntervalISICheckBox, n, 0)

            self.precursorIntervalISILabel.hide()
            self.precursorIntervalISITF.hide()
            self.precursorIntervalISICheckBox.hide()
            
            self.additionalWidgetsIntFieldList.append(self.precursorIntervalISITF)
            self.additionalWidgetsIntFieldLabelList.append(self.precursorIntervalISILabel)
            self.additionalWidgetsIntFieldCheckBoxList.append(self.precursorIntervalISICheckBox)
            n = n+1

        #Postcursor Interval
        if self.prm[self.currExp]["hasPostcursorInterval"] == True:
            self.postcursorIntervalChooserLabel = QLabel(self.tr("Postcursor Interval:"), self)
            self.add_widg_sizer.addWidget(self.postcursorIntervalChooserLabel, n, 1)
            self.postcursorIntervalChooser = QComboBox()
            self.postcursorIntervalChooser.addItems([self.tr("Yes"), self.tr("No")])
            self.postcursorIntervalChooser.setCurrentIndex(1)
            self.connect(self.postcursorIntervalChooser, SIGNAL('activated(QString)'), self.onPostcursorIntervalChange)
            self.add_widg_sizer.addWidget(self.postcursorIntervalChooser, n, 2)
            self.postcursorIntervalCheckBox = QCheckBox()
            self.add_widg_sizer.addWidget(self.postcursorIntervalCheckBox, n, 0)
            self.additionalWidgetsChooserList.append(self.postcursorIntervalChooser)
            self.additionalWidgetsChooserLabelList.append(self.postcursorIntervalChooserLabel)
            self.additionalWidgetsChooserCheckBoxList.append(self.postcursorIntervalCheckBox)
            n = n+1
            self.postcursorIntervalISILabel = QLabel(self.tr("Postcursor Interval ISI (ms):"), self)
            self.add_widg_sizer.addWidget(self.postcursorIntervalISILabel, n, 1)
           
            self.postcursorIntervalISITF = QLineEdit()
            self.postcursorIntervalISITF.setText("500")
            self.postcursorIntervalISITF.setValidator(QtGui.QIntValidator(self))
            self.postcursorIntervalISITF.setWhatsThis(self.tr("Sets the duration of the silent interval between the observation interval and the postcursor interval"))
         
            self.add_widg_sizer.addWidget(self.postcursorIntervalISITF, n, 2)
            self.postcursorIntervalISICheckBox = QCheckBox()
            self.add_widg_sizer.addWidget(self.postcursorIntervalISICheckBox, n, 0)

            self.postcursorIntervalISILabel.hide()
            self.postcursorIntervalISITF.hide()
            self.postcursorIntervalISICheckBox.hide()
            
            self.additionalWidgetsIntFieldList.append(self.postcursorIntervalISITF)
            self.additionalWidgetsIntFieldLabelList.append(self.postcursorIntervalISILabel)
            self.additionalWidgetsIntFieldCheckBoxList.append(self.postcursorIntervalISICheckBox)
            n = n+1
      
            
        if self.prm[self.currExp]["hasFeedback"] == True:
            self.responseLightLabel =  QLabel(self.tr("Response Light:"), self)
            self.responseLightChooser = QComboBox()
            self.responseLightChooser.addItems([self.tr("Feedback"), self.tr("Neutral"), self.tr("None")])
            self.add_widg_sizer.addWidget(self.responseLightLabel, n, 1)
            self.add_widg_sizer.addWidget(self.responseLightChooser, n, 2)
            self.responseLightCheckBox = QCheckBox()
            self.add_widg_sizer.addWidget(self.responseLightCheckBox, n, 0)
            self.additionalWidgetsChooserList.append(self.responseLightChooser)
            self.additionalWidgetsChooserLabelList.append(self.responseLightLabel)
            self.additionalWidgetsChooserCheckBoxList.append(self.responseLightCheckBox)
            n = n+1
            self.responseLightDurationLabel = QLabel(self.tr("Response Light Duration (ms):"), self)
            self.add_widg_sizer.addWidget(self.responseLightDurationLabel, n, 1)
            self.responseLightDurationTF = QLineEdit()
            self.responseLightDurationTF.setText(self.prm["pref"]["general"]["responseLightDuration"])
            self.responseLightDurationTF.setValidator(QtGui.QIntValidator(self))

            self.add_widg_sizer.addWidget(self.responseLightDurationTF, n, 2)
            self.responseLightDurationCheckBox = QCheckBox()
            self.add_widg_sizer.addWidget(self.responseLightDurationCheckBox, n, 0)
            self.additionalWidgetsIntFieldList.append(self.responseLightDurationTF)
            self.additionalWidgetsIntFieldLabelList.append(self.responseLightDurationLabel)
            self.additionalWidgetsIntFieldCheckBoxList.append(self.responseLightDurationCheckBox)
            n = n+1
        else:
            self.responseLightLabel =  QLabel(self.tr("Response Light:"), self)
            self.responseLightChooser = QComboBox()
            self.responseLightChooser.addItems([self.tr("Neutral"), self.tr("None")])
            self.add_widg_sizer.addWidget(self.responseLightLabel, n, 1)
            self.add_widg_sizer.addWidget(self.responseLightChooser, n, 2)
            self.responseLightCheckBox = QCheckBox()
            self.add_widg_sizer.addWidget(self.responseLightCheckBox, n, 0)
            self.additionalWidgetsChooserList.append(self.responseLightChooser)
            self.additionalWidgetsChooserLabelList.append(self.responseLightLabel)
            self.additionalWidgetsChooserCheckBoxList.append(self.responseLightCheckBox)
            n = n+1
            self.responseLightDurationLabel = QLabel(self.tr("Response Light Duration (ms):"), self)
            self.add_widg_sizer.addWidget(self.responseLightDurationLabel, n, 1)
            self.responseLightDurationTF = QLineEdit()
            self.responseLightDurationTF.setText(self.prm["pref"]["general"]["responseLightDuration"])
            self.responseLightDurationTF.setValidator(QtGui.QIntValidator(self))
            self.additionalWidgetsIntFieldList.append(self.responseLightDurationTF)
            self.additionalWidgetsIntFieldLabelList.append(self.responseLightDurationLabel)

            self.add_widg_sizer.addWidget(self.responseLightDurationTF, n, 2)
            self.responseLightDurationCheckBox = QCheckBox()
            self.add_widg_sizer.addWidget(self.responseLightDurationCheckBox, n, 0)
            self.additionalWidgetsIntFieldCheckBoxList.append(self.responseLightDurationCheckBox)
            n = n+1
       

    def setParadigmWidgets(self, currParadigm, prevParadigm):
        if prevParadigm != None:
            for i in range(len(self.paradigmChooserList)):
                self.paradigm_widg_sizer.removeWidget(self.paradigmChooserList[i])
                self.paradigmChooserList[i].setParent(None)
                self.paradigm_widg_sizer.removeWidget(self.paradigmChooserLabelList[i])
                self.paradigmChooserLabelList[i].setParent(None)
                self.paradigm_widg_sizer.removeWidget(self.paradigmChooserCheckBoxList[i])
                self.paradigmChooserCheckBoxList[i].setParent(None)
            for i in range(len(self.paradigmFieldList)):
                self.paradigm_widg_sizer.removeWidget(self.paradigmFieldList[i])
                self.paradigmFieldList[i].setParent(None)
                self.paradigm_widg_sizer.removeWidget(self.paradigmFieldLabelList[i])
                self.paradigmFieldLabelList[i].setParent(None)
                self.paradigm_widg_sizer.removeWidget(self.paradigmFieldCheckBoxList[i])
                self.paradigmFieldCheckBoxList[i].setParent(None)

         
        #------------------------------------
        #ADAPTIVE PARADIGM WIDGETS
        if self.currParadigm == self.tr("Adaptive"):
            n = 0
            self.adaptiveTypeChooserLabel = QLabel(self.tr("Procedure:"), self)
            self.paradigm_widg_sizer.addWidget(self.adaptiveTypeChooserLabel, n, 1)
            self.adaptiveTypeChooser = QComboBox()
            self.adaptiveTypeChooser.addItems(self.prm["adaptiveTypeChoices"])
            self.adaptiveTypeChooser.setCurrentIndex(0)
            self.paradigm_widg_sizer.addWidget(self.adaptiveTypeChooser, n, 2)
            self.adaptiveTypeCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.adaptiveTypeCheckBox, n, 0)

            n = n+1
            self.initialTrackDirChooserLabel = QLabel(self.tr("Initial Track Direction:"), self)
            self.paradigm_widg_sizer.addWidget(self.initialTrackDirChooserLabel, n, 1)
            self.initialTrackDirChooser = QComboBox()
            self.initialTrackDirChooser.addItems([self.tr("Up"), self.tr("Down")])
            self.initialTrackDirChooser.setCurrentIndex(1)
            self.paradigm_widg_sizer.addWidget(self.initialTrackDirChooser, n, 2)
            self.initialTrackDirCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.initialTrackDirCheckBox, n, 0)

            n = n+1
            self.ruleDownLabel = QLabel(self.tr("Rule Down"), self)
            self.paradigm_widg_sizer.addWidget(self.ruleDownLabel, n, 1)
            self.ruleDownTF = QLineEdit()
            self.ruleDownTF.setText('2')
            self.ruleDownTF.setValidator(QtGui.QIntValidator(self))
            self.paradigm_widg_sizer.addWidget(self.ruleDownTF, n, 2)
            self.ruleDownCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.ruleDownCheckBox, n, 0)

            self.ruleUpLabel = QLabel(self.tr("Rule Up"), self)
            self.paradigm_widg_sizer.addWidget(self.ruleUpLabel, n, 5)
            self.ruleUpTF = QLineEdit()
            self.ruleUpTF.setText('1')
            self.ruleUpTF.setValidator(QtGui.QIntValidator(self))
            self.paradigm_widg_sizer.addWidget(self.ruleUpTF, n, 4)
            self.ruleUpCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.ruleUpCheckBox, n, 3)
            n = n+1
            self.initialTurnpointsLabel = QLabel(self.tr("Initial Turnpoints"), self)
            self.paradigm_widg_sizer.addWidget(self.initialTurnpointsLabel, n, 1)
            self.initialTurnpointsTF = QLineEdit()
            self.initialTurnpointsTF.setText('4')
            self.initialTurnpointsTF.setValidator(QtGui.QIntValidator(self))
            self.paradigm_widg_sizer.addWidget(self.initialTurnpointsTF, n, 2)
            self.initialTurnpointsCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.initialTurnpointsCheckBox, n, 0)

            self.totalTurnpointsLabel = QLabel(self.tr("Total Turnpoints"), self)
            self.paradigm_widg_sizer.addWidget(self.totalTurnpointsLabel, n, 5)
            self.totalTurnpointsTF = QLineEdit()
            self.totalTurnpointsTF.setText('16')
            self.totalTurnpointsTF.setValidator(QtGui.QIntValidator(self))
            self.paradigm_widg_sizer.addWidget(self.totalTurnpointsTF, n, 4)
            self.totalTurnpointsCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.totalTurnpointsCheckBox, n, 3)
            n = n+1
            self.stepSize1Label = QLabel(self.tr("Step Size 1"), self)
            self.paradigm_widg_sizer.addWidget(self.stepSize1Label, n, 1)
            self.stepSize1TF = QLineEdit()
            self.stepSize1TF.setText('4')
            self.stepSize1TF.setValidator(QtGui.QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.stepSize1TF, n, 2)
            self.stepSize1CheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.stepSize1CheckBox, n, 0)

            self.stepSize2Label = QLabel(self.tr("Step Size 2"), self)
            self.paradigm_widg_sizer.addWidget(self.stepSize2Label, n, 5)
            self.stepSize2TF = QLineEdit()
            self.stepSize2TF.setText('2')
            self.stepSize2TF.setValidator(QtGui.QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.stepSize2TF, n, 4)
            self.stepSize2CheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.stepSize2CheckBox, n, 3)

            self.paradigmChooserList = [self.adaptiveTypeChooser, self.initialTrackDirChooser]
            self.paradigmChooserLabelList = [self.adaptiveTypeChooserLabel, self.initialTrackDirChooserLabel]
            self.paradigmChooserOptionsList = [self.prm["adaptiveTypeChoices"], [self.tr("Up"), self.tr("Down")]]
            self.paradigmChooserCheckBoxList = [self.adaptiveTypeCheckBox, self.initialTrackDirCheckBox]

            self.paradigmFieldList = [self.ruleDownTF, self.ruleUpTF, self.initialTurnpointsTF, self.totalTurnpointsTF, self.stepSize1TF, self.stepSize2TF]
            self.paradigmFieldLabelList = [self.ruleDownLabel, self.ruleUpLabel, self.initialTurnpointsLabel, self.totalTurnpointsLabel, self.stepSize1Label, self.stepSize2Label]
            self.paradigmFieldCheckBoxList = [self.ruleDownCheckBox, self.ruleUpCheckBox, self.initialTurnpointsCheckBox, self.totalTurnpointsCheckBox, self.stepSize1CheckBox, self.stepSize2CheckBox]

        #------------------------------------
        #WEIGHTED UP/DOWN PARADIGM WIDGETS
        if self.currParadigm == self.tr("Weighted Up/Down"):
            n = 0
            self.adaptiveTypeChooserLabel = QLabel(self.tr("Procedure:"), self)
            self.paradigm_widg_sizer.addWidget(self.adaptiveTypeChooserLabel, n, 1)
            self.adaptiveTypeChooser = QComboBox()
            self.adaptiveTypeChooser.addItems(self.prm["adaptiveTypeChoices"])
            self.adaptiveTypeChooser.setCurrentIndex(0)
            self.paradigm_widg_sizer.addWidget(self.adaptiveTypeChooser, n, 2)
            self.adaptiveTypeCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.adaptiveTypeCheckBox, n, 0)

            n = n+1
            self.initialTrackDirChooserLabel = QLabel(self.tr("Initial Track Direction:"), self)
            self.paradigm_widg_sizer.addWidget(self.initialTrackDirChooserLabel, n, 1)
            self.initialTrackDirChooser = QComboBox()
            self.initialTrackDirChooser.addItems([self.tr("Up"), self.tr("Down")])
            self.initialTrackDirChooser.setCurrentIndex(1)
            self.paradigm_widg_sizer.addWidget(self.initialTrackDirChooser, n, 2)
            self.initialTrackDirCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.initialTrackDirCheckBox, n, 0)
            n = n+1
            self.pcTrackedLabel = QLabel(self.tr("Percent Correct Tracked"), self)
            self.paradigm_widg_sizer.addWidget(self.pcTrackedLabel, n, 1)
            self.pcTrackedTF = QLineEdit()
            self.pcTrackedTF.setText('75')
            self.paradigm_widg_sizer.addWidget(self.pcTrackedTF, n, 2)
            self.pcTrackedCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.pcTrackedCheckBox, n, 0)
            
            n = n+1
            self.initialTurnpointsLabel = QLabel(self.tr("Initial Turnpoints"), self)
            self.paradigm_widg_sizer.addWidget(self.initialTurnpointsLabel, n, 1)
            self.initialTurnpointsTF = QLineEdit()
            self.initialTurnpointsTF.setText('4')
            self.paradigm_widg_sizer.addWidget(self.initialTurnpointsTF, n, 2)
            self.initialTurnpointsCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.initialTurnpointsCheckBox, n, 0)

            self.totalTurnpointsLabel = QLabel(self.tr("Total Turnpoints"), self)
            self.paradigm_widg_sizer.addWidget(self.totalTurnpointsLabel, n, 4)
            self.totalTurnpointsTF = QLineEdit()
            self.totalTurnpointsTF.setText('16')
            self.paradigm_widg_sizer.addWidget(self.totalTurnpointsTF, n, 5)
            self.totalTurnpointsCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.totalTurnpointsCheckBox, n, 3)
            n = n+1
            self.stepSize1Label = QLabel(self.tr("Step Size 1"), self)
            self.paradigm_widg_sizer.addWidget(self.stepSize1Label, n, 1)
            self.stepSize1TF = QLineEdit()
            self.stepSize1TF.setText('4')
            self.paradigm_widg_sizer.addWidget(self.stepSize1TF, n, 2)
            self.stepSize1CheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.stepSize1CheckBox, n, 0)

            self.stepSize2Label = QLabel(self.tr("Step Size 2"), self)
            self.paradigm_widg_sizer.addWidget(self.stepSize2Label, n, 4)
            self.stepSize2TF = QLineEdit()
            self.stepSize2TF.setText('2')
            self.paradigm_widg_sizer.addWidget(self.stepSize2TF, n, 5)
            self.stepSize2CheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.stepSize2CheckBox, n, 3)
            n = n+1
            
            self.paradigmChooserList = [self.adaptiveTypeChooser, self.initialTrackDirChooser]
            self.paradigmChooserLabelList = [self.adaptiveTypeChooserLabel, self.initialTrackDirChooserLabel]
            self.paradigmChooserOptionsList = [self.prm["adaptiveTypeChoices"], [self.tr("Up"), self.tr("Down")]]
            self.paradigmChooserCheckBoxList = [self.adaptiveTypeCheckBox, self.initialTrackDirCheckBox]

            self.paradigmFieldList = [self.pcTrackedTF, self.initialTurnpointsTF, self.totalTurnpointsTF, self.stepSize1TF, self.stepSize2TF]
            self.paradigmFieldLabelList = [self.pcTrackedLabel, self.initialTurnpointsLabel, self.totalTurnpointsLabel, self.stepSize1Label, self.stepSize2Label]
            self.paradigmFieldCheckBoxList = [self.pcTrackedCheckBox, self.initialTurnpointsCheckBox, self.totalTurnpointsCheckBox, self.stepSize1CheckBox, self.stepSize2CheckBox]

        #------------------------------------
        #ADAPTIVE INTERLEAVED PARADIGM WIDGETS
        if self.currParadigm == self.tr("Adaptive Interleaved"):
            n = 0
            self.adaptiveTypeChooserLabel = QLabel(self.tr("Procedure:"), self)
            self.paradigm_widg_sizer.addWidget(self.adaptiveTypeChooserLabel, n, 1)
            self.adaptiveTypeChooser = QComboBox()
            self.adaptiveTypeChooser.addItems(self.prm["adaptiveTypeChoices"])
            self.adaptiveTypeChooser.setCurrentIndex(0)
            self.paradigm_widg_sizer.addWidget(self.adaptiveTypeChooser, n, 2)
            self.adaptiveTypeCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.adaptiveTypeCheckBox, n, 0)

            n = n+1

            self.nTracksLabel = QLabel(self.tr("No. Tracks:"), self)
            self.paradigm_widg_sizer.addWidget(self.nTracksLabel, n, 1)
            self.nTracksChooser = QComboBox()
            self.nTracksOptionsList = list(range(1,101))
            self.nTracksOptionsList = [str(el) for el in self.nTracksOptionsList]
            self.nTracksChooser.addItems(self.nTracksOptionsList)
            nTracks = self.par['nDifferences']
            self.nTracksChooser.setCurrentIndex(self.nTracksOptionsList.index(str(nTracks)))
            self.paradigm_widg_sizer.addWidget(self.nTracksChooser, n, 2)
            self.connect(self.nTracksChooser, SIGNAL('activated(QString)'), self.onChangeNTracks)
            self.nTracksCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.nTracksCheckBox, n, 0)
            if self.prm[self.currExp]["hasNTracksChooser"] == True:
                self.nTracksLabel.show()
                self.nTracksChooser.show()
                self.nTracksCheckBox.show()
            else:
                self.nTracksLabel.hide()
                self.nTracksChooser.hide()
                self.nTracksCheckBox.hide()
            n = n+1
            self.maxConsecutiveTrialsLabel = QLabel(self.tr("Max. Consecutive Trials x Track:"), self)
            self.paradigm_widg_sizer.addWidget(self.maxConsecutiveTrialsLabel, n, 1)
            self.maxConsecutiveTrials = QComboBox()
            self.maxConsecutiveTrialsOptionsList = list(range(1,101))
            self.maxConsecutiveTrialsOptionsList = [str(el) for el in self.maxConsecutiveTrialsOptionsList]
            self.maxConsecutiveTrialsOptionsList.insert(0, self.tr('unlimited'))
          
            self.maxConsecutiveTrials.addItems(self.maxConsecutiveTrialsOptionsList)
            self.paradigm_widg_sizer.addWidget(self.maxConsecutiveTrials, n, 2)
            self.maxConsecutiveTrialsCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.maxConsecutiveTrialsCheckBox, n, 0)
            if nTracks > 1:
                self.maxConsecutiveTrialsLabel.show()
                self.maxConsecutiveTrials.show()
                self.maxConsecutiveTrialsCheckBox.show()
            else:
                self.maxConsecutiveTrials.setCurrentIndex(0)#'unlimited'
                self.maxConsecutiveTrialsLabel.hide()
                self.maxConsecutiveTrials.hide()
                self.maxConsecutiveTrialsCheckBox.hide()
           

            n = n+1

            self.tnpToAverageLabel = QLabel(self.tr("Turnpoints to average:"), self)
            self.paradigm_widg_sizer.addWidget(self.tnpToAverageLabel, n, 1)
            self.tnpToAverageChooser = QComboBox()
            self.tnpToAverageChooser.addItems(self.prm["tnpToAverageChoices"])
            self.tnpToAverageChooser.setCurrentIndex(0)
            self.paradigm_widg_sizer.addWidget(self.tnpToAverageChooser, n, 2)
            self.tnpToAverageCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.tnpToAverageCheckBox, n, 0)

            n = n+1
            self.initialTrackDirChooserLabel = []
            self.initialTrackDirChooser = []
            self.trackDirOptionsList = []
            self.initialTrackDirCheckBox = []
            
            self.ruleDownTF = []
            self.ruleUpTF = []
            self.initialTurnpointsTF = []
            self.totalTurnpointsTF = []
            self.stepSize1TF = []
            self.stepSize2TF = []
            
            self.ruleDownLabel = []
            self.ruleUpLabel = []
            self.initialTurnpointsLabel = []
            self.totalTurnpointsLabel = []
            self.stepSize1Label = []
            self.stepSize2Label = []

            self.ruleDownCheckBox = []
            self.ruleUpCheckBox = []
            self.initialTurnpointsCheckBox = []
            self.totalTurnpointsCheckBox = []
            self.stepSize1CheckBox = []
            self.stepSize2CheckBox = []
            
            for i in range(self.par['nDifferences']):
                self.initialTrackDirChooserLabel.append(QLabel(self.tr("Initial Track {0} Direction:".format(str(i+1))), self))
                self.paradigm_widg_sizer.addWidget(self.initialTrackDirChooserLabel[i], n, 1)
                self.initialTrackDirChooser.append(QComboBox())
                self.initialTrackDirChooser[i].addItems([self.tr("Up"), self.tr("Down")])
                self.initialTrackDirChooser[i].setCurrentIndex(1)
                self.paradigm_widg_sizer.addWidget(self.initialTrackDirChooser[i], n, 2)
                self.trackDirOptionsList.append([self.tr("Up"), self.tr("Down")])
                self.initialTrackDirCheckBox.append(QCheckBox())
                self.paradigm_widg_sizer.addWidget(self.initialTrackDirCheckBox[i], n, 0)
                n = n+1
                self.ruleDownLabel.append(QLabel(self.tr("Rule Down Track " + str(i+1)), self))
                self.paradigm_widg_sizer.addWidget(self.ruleDownLabel[i], n, 1)
                self.ruleDownTF.append(QLineEdit())
                self.ruleDownTF[i].setText('2')
                self.ruleDownTF[i].setValidator(QtGui.QIntValidator(self))
                self.paradigm_widg_sizer.addWidget(self.ruleDownTF[i], n, 2)
                self.ruleDownCheckBox.append(QCheckBox())
                self.paradigm_widg_sizer.addWidget(self.ruleDownCheckBox[i], n, 0)

                self.ruleUpLabel.append(QLabel(self.tr("Rule Up Track " + str(i+1)), self))
                self.paradigm_widg_sizer.addWidget(self.ruleUpLabel[i], n, 4)
                self.ruleUpTF.append(QLineEdit())
                self.ruleUpTF[i].setText('1')
                self.ruleUpTF[i].setValidator(QtGui.QIntValidator(self))
                self.paradigm_widg_sizer.addWidget(self.ruleUpTF[i], n, 5)
                self.ruleUpCheckBox.append(QCheckBox())
                self.paradigm_widg_sizer.addWidget(self.ruleUpCheckBox[i], n, 3)

                n = n+1
              
                self.initialTurnpointsLabel.append(QLabel(self.tr("Initial Turnpoints Track " + str(i+1)), self))
                self.paradigm_widg_sizer.addWidget(self.initialTurnpointsLabel[i], n, 1)
                self.initialTurnpointsTF.append(QLineEdit())
                self.initialTurnpointsTF[i].setText('4')
                self.initialTurnpointsTF[i].setValidator(QtGui.QIntValidator(self))
                self.paradigm_widg_sizer.addWidget(self.initialTurnpointsTF[i], n, 2)
                self.initialTurnpointsCheckBox.append(QCheckBox())
                self.paradigm_widg_sizer.addWidget(self.initialTurnpointsCheckBox[i], n, 0)

                self.totalTurnpointsLabel.append(QLabel(self.tr("Total Turnpoints Track " + str(i+1)), self))
                self.paradigm_widg_sizer.addWidget(self.totalTurnpointsLabel[i], n, 4)
                self.totalTurnpointsTF.append(QLineEdit())
                self.totalTurnpointsTF[i].setText('16')
                self.totalTurnpointsTF[i].setValidator(QtGui.QIntValidator(self))
                self.paradigm_widg_sizer.addWidget(self.totalTurnpointsTF[i], n, 5)
                self.totalTurnpointsCheckBox.append(QCheckBox())
                self.paradigm_widg_sizer.addWidget(self.totalTurnpointsCheckBox[i], n, 3)
                
                n = n+1
                self.stepSize1Label.append(QLabel(self.tr("Step Size 1 Track " + str(i+1)), self))
                self.paradigm_widg_sizer.addWidget(self.stepSize1Label[i], n, 1)
                self.stepSize1TF.append(QLineEdit())
                self.stepSize1TF[i].setText('4')
                self.stepSize1TF[i].setValidator(QtGui.QDoubleValidator(self))
                self.paradigm_widg_sizer.addWidget(self.stepSize1TF[i], n, 2)
                self.stepSize1CheckBox.append(QCheckBox())
                self.paradigm_widg_sizer.addWidget(self.stepSize1CheckBox[i], n, 0)
                
                self.stepSize2Label.append(QLabel(self.tr("Step Size 2 Track " + str(i+1)), self))
                self.paradigm_widg_sizer.addWidget(self.stepSize2Label[i], n, 4)
                self.stepSize2TF.append(QLineEdit())
                self.stepSize2TF[i].setText('2')
                self.stepSize2TF[i].setValidator(QtGui.QDoubleValidator(self))
                self.paradigm_widg_sizer.addWidget(self.stepSize2TF[i], n, 5)
                self.stepSize2CheckBox.append(QCheckBox())
                self.paradigm_widg_sizer.addWidget(self.stepSize2CheckBox[i], n, 3)
                n = n+1
           
                
            self.paradigmChooserList = [self.adaptiveTypeChooser, self.nTracksChooser, self.maxConsecutiveTrials, self.tnpToAverageChooser]
            self.paradigmChooserLabelList = [self.adaptiveTypeChooserLabel, self.nTracksLabel, self.maxConsecutiveTrialsLabel, self.tnpToAverageLabel]
            self.paradigmChooserOptionsList = [self.prm["adaptiveTypeChoices"], self.nTracksOptionsList, self.maxConsecutiveTrialsOptionsList, self.prm["tnpToAverageChoices"]]
            self.paradigmChooserCheckBoxList = [self.adaptiveTypeCheckBox, self.nTracksCheckBox, self.maxConsecutiveTrialsCheckBox, self.tnpToAverageCheckBox]
            self.paradigmChooserList.extend(self.initialTrackDirChooser)
            self.paradigmChooserLabelList.extend(self.initialTrackDirChooserLabel)
            self.paradigmChooserOptionsList.extend(self.trackDirOptionsList)
            self.paradigmChooserCheckBoxList.extend(self.initialTrackDirCheckBox)

            self.paradigmFieldList = self.ruleDownTF
            self.paradigmFieldList.extend(self.ruleUpTF)
            self.paradigmFieldList.extend(self.initialTurnpointsTF)
            self.paradigmFieldList.extend(self.totalTurnpointsTF)
            self.paradigmFieldList.extend(self.stepSize1TF)
            self.paradigmFieldList.extend(self.stepSize2TF)
            self.paradigmFieldLabelList = self.ruleDownLabel
            self.paradigmFieldLabelList.extend(self.ruleUpLabel)
            self.paradigmFieldLabelList.extend(self.initialTurnpointsLabel)
            self.paradigmFieldLabelList.extend(self.totalTurnpointsLabel)
            self.paradigmFieldLabelList.extend(self.stepSize1Label)
            self.paradigmFieldLabelList.extend(self.stepSize2Label)
            self.paradigmFieldCheckBoxList = self.ruleDownCheckBox
            self.paradigmFieldCheckBoxList.extend(self.ruleUpCheckBox)
            self.paradigmFieldCheckBoxList.extend(self.initialTurnpointsCheckBox)
            self.paradigmFieldCheckBoxList.extend(self.totalTurnpointsCheckBox)
            self.paradigmFieldCheckBoxList.extend(self.stepSize1CheckBox)
            self.paradigmFieldCheckBoxList.extend(self.stepSize2CheckBox)

        #--------------------------
        #WEIGHTED UP/DOWN INTERLEAVED PARADIGM WIDGETS
        if self.currParadigm == self.tr("Weighted Up/Down Interleaved"):
            n = 0
            self.adaptiveTypeChooserLabel = QLabel(self.tr("Procedure:"), self)
            self.paradigm_widg_sizer.addWidget(self.adaptiveTypeChooserLabel, n, 1)
            self.adaptiveTypeChooser = QComboBox()
            self.adaptiveTypeChooser.addItems(self.prm["adaptiveTypeChoices"])
            self.adaptiveTypeChooser.setCurrentIndex(0)
            self.paradigm_widg_sizer.addWidget(self.adaptiveTypeChooser, n, 2)
            self.adaptiveTypeCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.adaptiveTypeCheckBox, n, 0)
            n = n+1

            self.nTracksLabel = QLabel(self.tr("No. Tracks:"), self)
            self.paradigm_widg_sizer.addWidget(self.nTracksLabel, n, 1)
            self.nTracksChooser = QComboBox()
            self.nTracksOptionsList = list(range(1,101))
            self.nTracksOptionsList = [str(el) for el in self.nTracksOptionsList]
            self.nTracksChooser.addItems(self.nTracksOptionsList)
            nTracks = self.par['nDifferences']
            self.nTracksChooser.setCurrentIndex(self.nTracksOptionsList.index(str(nTracks)))
            self.paradigm_widg_sizer.addWidget(self.nTracksChooser, n, 2)
            self.connect(self.nTracksChooser, SIGNAL('activated(QString)'), self.onChangeNTracks)
            self.nTracksCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.nTracksCheckBox, n, 0)
            if self.prm[self.currExp]["hasNTracksChooser"] == True:
                self.nTracksLabel.show()
                self.nTracksChooser.show()
                self.nTracksCheckBox.show()
            else:
                self.nTracksLabel.hide()
                self.nTracksChooser.hide()
                self.nTracksCheckBox.hide()
            n = n+1
            self.maxConsecutiveTrialsLabel = QLabel(self.tr("Max. Consecutive Trials x Track:"), self)
            self.paradigm_widg_sizer.addWidget(self.maxConsecutiveTrialsLabel, n, 1)
            self.maxConsecutiveTrials = QComboBox()
            self.maxConsecutiveTrialsOptionsList = list(range(1,101))
            self.maxConsecutiveTrialsOptionsList = [str(el) for el in self.maxConsecutiveTrialsOptionsList]
            self.maxConsecutiveTrialsOptionsList.insert(0, self.tr('unlimited'))
          
            self.maxConsecutiveTrials.addItems(self.maxConsecutiveTrialsOptionsList)
            self.paradigm_widg_sizer.addWidget(self.maxConsecutiveTrials, n, 2)
            self.maxConsecutiveTrialsCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.maxConsecutiveTrialsCheckBox, n, 0)
            if nTracks > 1:
                self.maxConsecutiveTrialsLabel.show()
                self.maxConsecutiveTrials.show()
                self.maxConsecutiveTrialsCheckBox.show()
            else:
                self.maxConsecutiveTrials.setCurrentIndex(0)#'unlimited'
                self.maxConsecutiveTrialsLabel.hide()
                self.maxConsecutiveTrials.hide()
                self.maxConsecutiveTrialsCheckBox.hide()
           

            n = n+1
            self.tnpToAverageLabel = QLabel(self.tr("Turnpoints to average:"), self)
            self.paradigm_widg_sizer.addWidget(self.tnpToAverageLabel, n, 1)
            self.tnpToAverageChooser = QComboBox()
            self.tnpToAverageChooser.addItems(self.prm["tnpToAverageChoices"])
            self.tnpToAverageChooser.setCurrentIndex(0)
            self.paradigm_widg_sizer.addWidget(self.tnpToAverageChooser, n, 2)
            self.tnpToAverageCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.tnpToAverageCheckBox, n, 0)

            n = n+1
            self.initialTrackDirChooserLabel = []
            self.initialTrackDirChooser = []
            self.trackDirOptionsList = []
            self.initialTrackDirCheckBox = []
             
            self.pcTrackedTF = []
            self.initialTurnpointsTF = []
            self.totalTurnpointsTF = []
            self.stepSize1TF = []
            self.stepSize2TF = []
            
            self.pcTrackedLabel = []
            self.initialTurnpointsLabel = []
            self.totalTurnpointsLabel = []
            self.stepSize1Label = []
            self.stepSize2Label = []

            self.pcTrackedCheckBox = []
            self.initialTurnpointsCheckBox = []
            self.totalTurnpointsCheckBox = []
            self.stepSize1CheckBox = []
            self.stepSize2CheckBox = []
            
            for i in range(self.par['nDifferences']):
                self.initialTrackDirChooserLabel.append(QLabel(self.tr("Initial Track {0} Direction:".format(str(i+1))), self))
                self.paradigm_widg_sizer.addWidget(self.initialTrackDirChooserLabel[i], n, 1)
                self.initialTrackDirChooser.append(QComboBox())
                self.initialTrackDirChooser[i].addItems([self.tr("Up"), self.tr("Down")])
                self.initialTrackDirChooser[i].setCurrentIndex(1)
                self.paradigm_widg_sizer.addWidget(self.initialTrackDirChooser[i], n, 2)
                self.trackDirOptionsList.append([self.tr("Up"), self.tr("Down")])
                self.initialTrackDirCheckBox.append(QCheckBox())
                self.paradigm_widg_sizer.addWidget(self.initialTrackDirCheckBox[i], n, 0)
                n = n+1
                self.pcTrackedLabel.append(QLabel(self.tr("Percent Correct Tracked Track " + str(i+1)), self))
                self.paradigm_widg_sizer.addWidget(self.pcTrackedLabel[i], n, 1)
                self.pcTrackedTF.append(QLineEdit())
                self.pcTrackedTF[i].setText('75')
                self.pcTrackedTF[i].setValidator(QtGui.QDoubleValidator(self))
                self.paradigm_widg_sizer.addWidget(self.pcTrackedTF[i], n, 2)
                self.pcTrackedCheckBox.append(QCheckBox())
                self.paradigm_widg_sizer.addWidget(self.pcTrackedCheckBox[i], n, 0)

                n = n+1
                self.initialTurnpointsLabel.append(QLabel(self.tr("Initial Turnpoints Track " + str(i+1)), self))
                self.paradigm_widg_sizer.addWidget(self.initialTurnpointsLabel[i], n, 1)
                self.initialTurnpointsTF.append(QLineEdit())
                self.initialTurnpointsTF[i].setText('4')
                self.initialTurnpointsTF[i].setValidator(QtGui.QIntValidator(self))
                self.paradigm_widg_sizer.addWidget(self.initialTurnpointsTF[i], n, 2)
                self.initialTurnpointsCheckBox.append(QCheckBox())
                self.paradigm_widg_sizer.addWidget(self.initialTurnpointsCheckBox[i], n, 0)

                self.totalTurnpointsLabel.append(QLabel(self.tr("Total Turnpoints Track " + str(i+1)), self))
                self.paradigm_widg_sizer.addWidget(self.totalTurnpointsLabel[i], n, 4)
                self.totalTurnpointsTF.append(QLineEdit())
                self.totalTurnpointsTF[i].setText('16')
                self.totalTurnpointsTF[i].setValidator(QtGui.QIntValidator(self))
                self.paradigm_widg_sizer.addWidget(self.totalTurnpointsTF[i], n, 5)
                self.totalTurnpointsCheckBox.append(QCheckBox())
                self.paradigm_widg_sizer.addWidget(self.totalTurnpointsCheckBox[i], n, 3)
                
                n = n+1
                self.stepSize1Label.append(QLabel(self.tr("Step Size 1 Track " + str(i+1)), self))
                self.paradigm_widg_sizer.addWidget(self.stepSize1Label[i], n, 1)
                self.stepSize1TF.append(QLineEdit())
                self.stepSize1TF[i].setText('4')
                self.stepSize1TF[i].setValidator(QtGui.QDoubleValidator(self))
                self.paradigm_widg_sizer.addWidget(self.stepSize1TF[i], n, 2)
                self.stepSize1CheckBox.append(QCheckBox())
                self.paradigm_widg_sizer.addWidget(self.stepSize1CheckBox[i], n, 0)
                
                self.stepSize2Label.append(QLabel(self.tr("Step Size 2 Track " + str(i+1)), self))
                self.paradigm_widg_sizer.addWidget(self.stepSize2Label[i], n, 4)
                self.stepSize2TF.append(QLineEdit())
                self.stepSize2TF[i].setText('2')
                self.stepSize2TF[i].setValidator(QtGui.QDoubleValidator(self))
                self.paradigm_widg_sizer.addWidget(self.stepSize2TF[i], n, 5)
                self.stepSize2CheckBox.append(QCheckBox())
                self.paradigm_widg_sizer.addWidget(self.stepSize2CheckBox[i], n, 3)
                n = n+1
           
                
            self.paradigmChooserList = [self.adaptiveTypeChooser, self.nTracksChooser, self.maxConsecutiveTrials, self.tnpToAverageChooser]
            self.paradigmChooserLabelList = [self.adaptiveTypeChooserLabel, self.nTracksLabel, self.maxConsecutiveTrialsLabel, self.tnpToAverageLabel]
            self.paradigmChooserOptionsList = [self.prm["adaptiveTypeChoices"], self.nTracksOptionsList, self.maxConsecutiveTrialsOptionsList, self.prm["tnpToAverageChoices"]]
            self.paradigmChooserCheckBoxList = [self.adaptiveTypeCheckBox, self.nTracksCheckBox, self.maxConsecutiveTrialsCheckBox, self.tnpToAverageCheckBox]
            self.paradigmChooserList.extend(self.initialTrackDirChooser)
            self.paradigmChooserLabelList.extend(self.initialTrackDirChooserLabel)
            self.paradigmChooserOptionsList.extend(self.trackDirOptionsList)
            self.paradigmChooserCheckBoxList.extend(self.initialTrackDirCheckBox)

            self.paradigmFieldList = self.pcTrackedTF
            self.paradigmFieldList.extend(self.initialTurnpointsTF)
            self.paradigmFieldList.extend(self.totalTurnpointsTF)
            self.paradigmFieldList.extend(self.stepSize1TF)
            self.paradigmFieldList.extend(self.stepSize2TF)
            self.paradigmFieldLabelList = self.pcTrackedLabel
            self.paradigmFieldLabelList.extend(self.initialTurnpointsLabel)
            self.paradigmFieldLabelList.extend(self.totalTurnpointsLabel)
            self.paradigmFieldLabelList.extend(self.stepSize1Label)
            self.paradigmFieldLabelList.extend(self.stepSize2Label)
            self.paradigmFieldCheckBoxList = self.pcTrackedCheckBox
            self.paradigmFieldCheckBoxList.extend(self.initialTurnpointsCheckBox)
            self.paradigmFieldCheckBoxList.extend(self.totalTurnpointsCheckBox)
            self.paradigmFieldCheckBoxList.extend(self.stepSize1CheckBox)
            self.paradigmFieldCheckBoxList.extend(self.stepSize2CheckBox)

        #------------------------
        #ONE CONSTANT PARADIGM WIDGETS
        if self.currParadigm in [self.tr("Constant 1-Interval 2-Alternatives"), self.tr("Constant 1-Pair Same/Different"), self.tr("Constant m-Intervals n-Alternatives"), self.tr("Same Different 4")]:
            n = 0
            self.nTrialsLabel = QLabel(self.tr("No. Trials"), self)
            self.paradigm_widg_sizer.addWidget(self.nTrialsLabel, n, 1)
            self.nTrialsTF = QLineEdit()
            self.nTrialsTF.setText('25')
            self.nTrialsTF.setValidator(QtGui.QIntValidator(self))
            self.paradigm_widg_sizer.addWidget(self.nTrialsTF, n, 2)
            self.nTrialsCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.nTrialsCheckBox, n, 0)

            n = n+1
            self.nPracticeTrialsLabel = QLabel(self.tr("No. Practice Trials"), self)
            self.paradigm_widg_sizer.addWidget(self.nPracticeTrialsLabel, n, 1)
            self.nPracticeTrialsTF = QLineEdit()
            self.nPracticeTrialsTF.setText('0')
            self.nPracticeTrialsTF.setValidator(QtGui.QIntValidator(self))
            self.paradigm_widg_sizer.addWidget(self.nPracticeTrialsTF, n, 2)
            self.nPracticeTrialsCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.nPracticeTrialsCheckBox, n, 0)

            self.paradigmChooserList = []
            self.paradigmChooserLabelList = []
            self.paradigmChooserOptionsList = []
            self.paradigmChooserCheckBoxList = []

            self.paradigmFieldList = [self.nTrialsTF, self.nPracticeTrialsTF]
            self.paradigmFieldLabelList = [self.nTrialsLabel, self.nPracticeTrialsLabel]
            self.paradigmFieldCheckBoxList = [self.nTrialsCheckBox, self.nPracticeTrialsCheckBox]

      
        #------------------------
        #MULTIPLE CONSTANTS PARADIGM WIDGETS
        if self.currParadigm in [self.tr("Multiple Constants 1-Interval 2-Alternatives"), self.tr("Multiple Constants m-Intervals n-Alternatives")]:
            n = 0
            self.nTrialsLabel = QLabel(self.tr("No. Trials"), self)
            self.paradigm_widg_sizer.addWidget(self.nTrialsLabel, n, 1)
            self.nTrialsTF = QLineEdit()
            self.nTrialsTF.setText('25')
            self.nTrialsTF.setValidator(QtGui.QIntValidator(self))
            self.paradigm_widg_sizer.addWidget(self.nTrialsTF, n, 2)
            self.nTrialsCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.nTrialsCheckBox, n, 0)

            n = n+1
            self.nPracticeTrialsLabel = QLabel(self.tr("No. Practice Trials"), self)
            self.paradigm_widg_sizer.addWidget(self.nPracticeTrialsLabel, n, 1)
            self.nPracticeTrialsTF = QLineEdit()
            self.nPracticeTrialsTF.setText('0')
            self.nPracticeTrialsTF.setValidator(QtGui.QIntValidator(self))
            self.paradigm_widg_sizer.addWidget(self.nPracticeTrialsTF, n, 2)
            self.nPracticeTrialsCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.nPracticeTrialsCheckBox, n, 0)

            n = n+1
            self.nDifferencesLabel = QLabel(self.tr("No. Differences:"), self)
            self.paradigm_widg_sizer.addWidget(self.nDifferencesLabel, n, 1)
            self.nDifferencesChooser = QComboBox()
            self.nDifferencesOptionsList = list(range(1,101))
            self.nDifferencesOptionsList = [str(el) for el in self.nDifferencesOptionsList]
            self.nDifferencesChooser.addItems(self.nDifferencesOptionsList)
          
            self.nDifferencesChooser.setCurrentIndex(self.nDifferencesOptionsList.index(str(self.par["nDifferences"])))
            self.paradigm_widg_sizer.addWidget(self.nDifferencesChooser, n, 2)
            self.connect(self.nDifferencesChooser, SIGNAL('activated(QString)'), self.onChangeNDifferences)

            self.nDifferencesCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.nDifferencesCheckBox, n, 0)
            if self.prm[self.currExp]["hasNDifferencesChooser"] == True:
                self.nDifferencesLabel.show()
                self.nDifferencesChooser.show()
                self.nDifferencesCheckBox.show()
            else:
                self.nDifferencesLabel.hide()
                self.nDifferencesChooser.hide()
                self.nDifferencesCheckBox.hide()

            self.paradigmChooserList = [self.nDifferencesChooser]
            self.paradigmChooserLabelList = [self.nDifferencesLabel]
            self.paradigmChooserOptionsList = [self.nDifferencesOptionsList]
            self.paradigmChooserCheckBoxList = [self.nDifferencesCheckBox]

            self.paradigmFieldList = [self.nTrialsTF, self.nPracticeTrialsTF]
            self.paradigmFieldLabelList = [self.nTrialsLabel, self.nPracticeTrialsLabel]
            self.paradigmFieldCheckBoxList = [self.nTrialsCheckBox, self.nPracticeTrialsCheckBox]

            
    def onExperimentChange(self, experimentSelected):
        for i in range(self.paradigmChooser.count()):
            self.paradigmChooser.removeItem(0)
        self.paradigmChooser.addItems(self.prm[self.tr(experimentSelected)]['paradigmChoices'])
        self.setDefaultParameters(experimentSelected, self.prm[self.tr(experimentSelected)]['paradigmChoices'][0], self.par)
        self.responseBox.setupLights()


    def onParadigmChange(self, paradigmSelected):
        self.prevParadigm = self.currParadigm
        self.currParadigm = self.tr(paradigmSelected)
        self.setParadigmWidgets(self.currParadigm, self.prevParadigm)
        self.responseBox.setupLights()

    def onNIntervalsChange(self, nIntervalsSelected):
        for i in range(self.nAlternativesChooser.count()):
            self.nAlternativesChooser.removeItem(0)
        self.nAlternativesChooser.addItems([str(self.currLocale.toInt(self.nIntervalsChooser.currentText())[0]-1), self.nIntervalsChooser.currentText()])
        self.nAlternativesChooser.setCurrentIndex(1)
        self.prm['nIntervals'] = self.currLocale.toInt(self.nIntervalsChooser.currentText())[0]
        self.responseBox.setupLights()

    def onNAlternativesChange(self, nAlternativesSelected):
        self.prm['nAlternatives'] = self.currLocale.toInt(self.nAlternativesChooser.currentText())[0]
        self.responseBox.setupLights()

    def onIntervalLightsChange(self):
        self.prm['intervalLights'] = self.intervalLightsChooser.currentText()
        self.responseBox.setupLights()
        
    def onWarningIntervalChange(self):
        if self.warningIntervalChooser.currentText() == self.tr("Yes"):
            self.prm["warningInterval"] = True
            self.warningIntervalDurLabel.show()
            self.warningIntervalDurTF.show()
            self.warningIntervalISILabel.show()
            self.warningIntervalISITF.show()
        else:
            self.prm["warningInterval"] = False
            self.warningIntervalDurLabel.hide()
            self.warningIntervalDurTF.hide()
            self.warningIntervalISILabel.hide()
            self.warningIntervalISITF.hide()
        self.responseBox.setupLights()

    ## def onWarningIntervalChange(self):
    ##     if self.warningInterval.isChecked():
    ##         self.prm["warningInterval"] = True
    ##         self.warningIntervalDurLabel.show()
    ##         self.warningIntervalDurTF.show()
    ##         self.warningIntervalISILabel.show()
    ##         self.warningIntervalISITF.show()
    ##     else:
    ##         self.prm["warningInterval"] = False
    ##         self.warningIntervalDurLabel.hide()
    ##         self.warningIntervalDurTF.hide()
    ##         self.warningIntervalISILabel.hide()
    ##         self.warningIntervalISITF.hide()
    ##     self.responseBox.setupLights()

    def onPreTrialIntervalChange(self):
        if self.preTrialIntervalChooser.currentText() == self.tr("Yes"):
            self.prm["preTrialInterval"] = True
            self.preTrialIntervalISILabel.show()
            self.preTrialIntervalISITF.show()
            self.preTrialIntervalISICheckBox.show()
        else:
            self.prm["preTrialInterval"] = False
            self.preTrialIntervalISILabel.hide()
            self.preTrialIntervalISITF.hide()
            self.preTrialIntervalISICheckBox.hide()
        self.onChooserChange(None)
        self.responseBox.setupLights()
    def onPrecursorIntervalChange(self):
        if self.precursorIntervalChooser.currentText() == self.tr("Yes"):
            self.prm["precursorInterval"] = True
            self.precursorIntervalISILabel.show()
            self.precursorIntervalISITF.show()
            self.precursorIntervalISICheckBox.show()
        else:
            self.prm["precursorInterval"] = False
            self.precursorIntervalISILabel.hide()
            self.precursorIntervalISITF.hide()
            self.precursorIntervalISICheckBox.hide()
        self.onChooserChange(None)
        self.responseBox.setupLights()
    def onPostcursorIntervalChange(self):
        if self.postcursorIntervalChooser.currentText() == self.tr("Yes"):
            self.prm["postcursorInterval"] = True
            self.postcursorIntervalISILabel.show()
            self.postcursorIntervalISITF.show()
            self.postcursorIntervalISICheckBox.show()
        else:
            self.prm["postcursorInterval"] = False
            self.postcursorIntervalISILabel.hide()
            self.postcursorIntervalISITF.hide()
            self.postcursorIntervalISICheckBox.hide()
        self.onChooserChange(None)
        self.responseBox.setupLights()
    def onListenerChange(self):
        self.prm['listener'] = self.listenerTF.text()
    def onSessionLabelChange(self):
        self.prm['sessionLabel'] = self.sessionLabelTF.text()
    def onResponseModeChange(self, selectedMode):
        if selectedMode != self.tr("Automatic"):
            self.autoPCorrLabel.hide()
            self.autoPCorrTF.hide()
        else:
            self.autoPCorrLabel.show()
            self.autoPCorrTF.show()
            
    def onDropPrmFile(self, l):
        lastFileDropped = l[len(l)-1]
        if os.path.exists(lastFileDropped):
            reply = QtGui.QMessageBox.question(self, self.tr('Message'), self.tr("Do you want to load the parameters file {0} ?").format(lastFileDropped), QtGui.QMessageBox.Yes | 
                                               QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
            if reply == QtGui.QMessageBox.Yes:
                self.loadParameters(lastFileDropped)
            else:
                pass
                
            
    def setDefaultParameters(self, experiment, paradigm, par):
        self.prevExp = self.currExp
        self.currExp = experiment
        self.removePrmWidgets()
        
        if paradigm in [self.tr("Adaptive Interleaved"), self.tr("Weighted Up/Down Interleaved")]:
            if self.prm[self.currExp]['hasNTracksChooser'] == False:
                self.par['nDifferences'] = self.prm[self.currExp]['defaultNTracks']
            else:
                if 'nDifferences' not in par:
                    if 'defaultNTracks' in self.prm[self.currExp]:
                        self.par['nDifferences'] = self.prm[self.currExp]['defaultNTracks']
                    else:
                        self.par['nDifferences'] = 2

        if paradigm in [self.tr("Multiple Constants 1-Interval 2-Alternatives"), self.tr("Multiple Constants m-Intervals n-Alternatives")]:
            if self.prm[self.currExp]['hasNDifferencesChooser'] == False:
                self.par['nDifferences'] = self.prm[self.currExp]['defaultNDifferences']
            else:
                if 'nDifferences' not in par:
                    if 'defaultNDifferences' in self.prm[self.currExp]:
                        self.par['nDifferences'] = self.prm[self.currExp]['defaultNDifferences']
                    else:
                        self.par['nDifferences'] = 2
                    
        execString = self.prm[self.currExp]['execString']
     
        try:
            methodToCall1 = getattr(default_experiments, execString)
        except:
            pass
        try:
            methodToCall1 = getattr(labexp, execString)
        except:
            pass
        methodToCall2 = getattr(methodToCall1, 'select_default_parameters_'+ execString)
        tmp = methodToCall2(self, self.par)
        
        
        self.prm['field'] = tmp['field']
        self.prm['fieldLabel'] = tmp['fieldLabel']
        self.prm['nFields'] = len(self.prm['fieldLabel'])
        self.prm['chooser'] = tmp['chooser']
        self.prm['chooserLabel'] = tmp['chooserLabel']
        self.prm['nChoosers'] = len(self.prm['chooserLabel'])
        self.prm['chooserOptions'] = tmp['chooserOptions']

        if 'fileChooser' in tmp:
            self.prm['fileChooser'] = tmp['fileChooser']
            self.prm['fileChooserButton'] = tmp['fileChooserButton']
        else:
            self.prm['fileChooser'] = []
            self.prm['fileChooserButton'] = []
        self.prm['nFileChoosers'] = len(self.prm['fileChooser'])
        # SET UP TEXT FIELDS
        self.field = list(range(self.prm['nFields']))
        self.fieldLabel = list(range(self.prm['nFields']))
        self.fieldCheckBox = list(range(self.prm['nFields']))
        for f in range(self.prm['nFields']):
            self.fieldLabel[f] = QLabel(self.tr(self.prm['fieldLabel'][f]))
            self.pw_prm_sizer_0.addWidget(self.fieldLabel[f], f, 1)
            self.field[f] = QLineEdit()
            self.field[f].setText(str(self.prm['field'][f]))
            self.field[f].setValidator(QtGui.QDoubleValidator(self))
            self.pw_prm_sizer_0.addWidget(self.field[f], f, 2)
            self.fieldCheckBox[f] = QCheckBox()
            self.pw_prm_sizer_0.addWidget(self.fieldCheckBox[f], f, 0)
        # SET UP CHOOSERS
        self.chooser = list(range(self.prm['nChoosers']))
        self.chooserLabel = list(range(self.prm['nChoosers']))
        self.chooserOptions = list(range(self.prm['nChoosers']))
        self.chooserCheckBox = list(range(self.prm['nChoosers']))
        for c in range(self.prm['nChoosers']):
            self.chooserLabel[c] = QLabel(self.tr(self.prm['chooserLabel'][c]))
            self.pw_prm_sizer_1.addWidget(self.chooserLabel[c], c, 4)
            self.chooserOptions[c] = self.prm['chooserOptions'][c]
            self.chooser[c] = QComboBox()  
            self.chooser[c].addItems(self.chooserOptions[c])
            self.chooser[c].setCurrentIndex(self.chooserOptions[c].index(self.prm['chooser'][c]))
            self.pw_prm_sizer_1.addWidget(self.chooser[c], c, 5)
            self.chooserCheckBox[c] = QCheckBox()
            self.pw_prm_sizer_1.addWidget(self.chooserCheckBox[c], c, 3)
        for c in range(len(self.chooser)):
            self.connect(self.chooser[c], SIGNAL('activated(QString)'), self.onChooserChange)
        #self.prm['nFields'] = len(self.field)
        #self.prm['nChoosers'] = len(self.chooser)
        #SET UP FILE CHOOSERS
        self.fileChooser = list(range(self.prm['nFileChoosers']))
        self.fileChooserButton = list(range(self.prm['nFileChoosers']))
        self.fileChooserCheckBox = list(range(self.prm['nFileChoosers']))
        for f in range(self.prm['nFileChoosers']):
            self.fileChooser[f] = QLineEdit()
            self.fileChooser[f].setText(str(self.prm['fileChooser'][f]))
            self.pw_prm_sizer_0.addWidget(self.fileChooser[f], self.prm['nFields']+f, 2)
            self.fileChooserButton[f] =  QtGui.QPushButton(self.tr(self.prm['fileChooserButton'][f]), self)
            self.fileChooserButton[f].clicked.connect(self.fileChooserButtonClicked)
            self.pw_prm_sizer_0.addWidget(self.fileChooserButton[f], self.prm['nFields']+f, 1)
            self.fileChooserCheckBox[f] = QCheckBox()
            self.pw_prm_sizer_0.addWidget(self.fileChooserCheckBox[f], self.prm['nFields']+f, 0)
        
        self.prevParadigm = self.currParadigm
        self.currParadigm = paradigm 
        self.paradigmChooser.setCurrentIndex(self.prm[self.currExp]["paradigmChoices"].index(self.currParadigm))
        self.preTrialSilenceTF.setText(self.prm["pref"]["general"]["preTrialSilence"])

        self.setParadigmWidgets(self.currParadigm, self.prevParadigm)
        if self.currParadigm == self.tr("Adaptive"):
            self.adaptiveTypeChooser.setCurrentIndex(self.prm["adaptiveTypeChoices"].index(self.prm[self.currExp]['defaultAdaptiveType']))

        self.prm['nIntervals'] = self.prm[self.currExp]['defaultNIntervals']  #tmp['nIntervals']
        self.prm['nAlternatives'] = self.prm[self.currExp]['defaultNAlternatives']#tmp['nAlternatives']
        self.setAdditionalWidgets(self.currExp, self.prevExp)
        self.onChooserChange(None)
        
    def removePrmWidgets(self):
        if self.prevExp != None:
            for f in range(len(self.field)):
                self.pw_prm_sizer_0.removeWidget(self.fieldLabel[f])
                self.fieldLabel[f].setParent(None)
                self.pw_prm_sizer_0.removeWidget(self.field[f])
                self.field[f].setParent(None)
                self.pw_prm_sizer_0.removeWidget(self.fieldCheckBox[f])
                self.fieldCheckBox[f].setParent(None)
            for c in range(len(self.chooser)):
                self.pw_prm_sizer_1.removeWidget(self.chooserLabel[c])
                self.chooserLabel[c].setParent(None)
                self.pw_prm_sizer_1.removeWidget(self.chooser[c])
                self.chooser[c].setParent(None)
                self.pw_prm_sizer_1.removeWidget(self.chooserCheckBox[c])
                self.chooserCheckBox[c].setParent(None)
            for f in range(len(self.fileChooser)):
                self.pw_prm_sizer_0.removeWidget(self.fileChooser[f])
                self.fileChooser[f].setParent(None)
                self.pw_prm_sizer_0.removeWidget(self.fileChooserButton[f])
                self.fileChooserButton[f].setParent(None)
                self.pw_prm_sizer_0.removeWidget(self.fileChooserCheckBox[f])
                self.fileChooserCheckBox[f].setParent(None)
    def updateParametersWin(self):
        #if the next block is already stored show it, otherwise copy the values from the previous block
        currBlock = 'b' + str(self.prm["currentBlock"])
        prevBlock = 'b' + str(self.prm["currentBlock"]-1)
       
        if self.prm["currentBlock"] > self.prm["storedBlocks"] and self.prm["storedBlocks"] > 0: #copy values from previous block
            block = prevBlock
        else:
            block = currBlock
        self.prm["tmpBlockPosition"] = self.prm[currBlock]["blockPosition"]
        self.setNewBlock(block)
    def setNewBlock(self, block):
        self.removePrmWidgets()
        self.conditionLabelTF.setText(self.prm[block]['conditionLabel'])

        currExp = self.tr(self.prm[block]['experiment'])
        paradigm = self.tr(self.prm[block]['paradigm'])
        self.experimentChooser.setCurrentIndex(self.prm['experimentsChoices'].index(currExp))
        for i in range(self.paradigmChooser.count()):
            self.paradigmChooser.removeItem(0)
        self.paradigmChooser.addItems(self.prm[currExp]['paradigmChoices'])
        self.paradigmChooser.setCurrentIndex(self.prm[currExp]["paradigmChoices"].index(paradigm))

        if paradigm in [self.tr("Multiple Constants 1-Interval 2-Alternatives"), self.tr("Multiple Constants m-Intervals n-Alternatives")]:
            self.par['nDifferences'] = int(self.prm[block]['paradigmChooser'][self.prm[block]['paradigmChooserLabel'].index(self.tr("No. Differences:"))])
        if paradigm in [self.tr("Adaptive Interleaved"), self.tr("Weighted Up/Down Interleaved")]:
            self.par['nDifferences'] = int(self.prm[block]['paradigmChooser'][self.prm[block]['paradigmChooserLabel'].index(self.tr("No. Tracks:"))])
      
        
        self.setDefaultParameters(currExp, self.tr(self.prm[block]['paradigm']), self.par)
        for f in range(len(self.field)):
            self.field[f].setText(self.currLocale.toString(self.prm[block]['field'][f], precision=self.prm["pref"]["general"]["precision"]))
            self.fieldCheckBox[f].setChecked(self.prm[block]['fieldCheckBox'][f])
        for c in range(len(self.chooser)):
            self.chooser[c].setCurrentIndex(self.prm['chooserOptions'][c].index(self.prm[block]['chooser'][c]))
            self.chooserCheckBox[c].setChecked(self.prm[block]['chooserCheckBox'][c])
        for f in range(len(self.fileChooser)):
            self.fileChooser[f].setText(self.prm[block]['fileChooser'][f])
            self.fileChooserCheckBox[f].setChecked(self.prm[block]['fileChooserCheckBox'][f])

        for f in range(len(self.paradigmFieldList)):
            self.paradigmFieldList[f].setText(self.currLocale.toString(self.prm[block]['paradigmField'][f], precision=self.prm["pref"]["general"]["precision"]))
            self.paradigmFieldCheckBoxList[f].setChecked(self.prm[block]['paradigmFieldCheckBox'][f])
        for c in range(len(self.paradigmChooserList)):
            self.paradigmChooserList[c].setCurrentIndex(self.paradigmChooserList[c].findText(self.prm[block]['paradigmChooser'][c]))
            self.paradigmChooserCheckBoxList[c].setChecked(self.prm[block]['paradigmChooserCheckBox'][c])

        self.preTrialSilenceTF.setText(self.currLocale.toString(self.prm[block]['preTrialSilence']))
        self.warningIntervalChooser.setCurrentIndex(self.warningIntervalChooser.findText(self.prm[block]['warningInterval']))
        self.warningIntervalDurTF.setText(self.currLocale.toString(self.prm[block]['warningIntervalDur']))
        self.warningIntervalISITF.setText(self.currLocale.toString(self.prm[block]['warningIntervalISI']))
        self.intervalLightsChooser.setCurrentIndex(self.intervalLightsChooser.findText(self.prm[block]['intervalLights']))
        self.onIntervalLightsChange()

        if self.prm[currExp]["hasISIBox"] == True:
            self.ISIBox.setText(self.currLocale.toString(self.prm[block]['ISIVal']))
            self.ISIBoxCheckBox.setChecked(self.prm[block]['ISIValCheckBox'])
        if self.prm[currExp]["hasPreTrialInterval"] == True:
            self.preTrialIntervalChooser.setCurrentIndex(self.preTrialIntervalChooser.findText(self.prm[block]['preTrialInterval']))
            self.preTrialIntervalCheckBox.setChecked(self.prm[block]['preTrialIntervalCheckBox'])
            self.onPreTrialIntervalChange()
            self.preTrialIntervalISITF.setText(self.currLocale.toString(self.prm[block]['preTrialIntervalISI']))
            self.preTrialIntervalISICheckBox.setChecked(self.prm[block]['preTrialIntervalISICheckBox'])
        if self.prm[currExp]["hasPrecursorInterval"] == True:
            self.precursorIntervalChooser.setCurrentIndex(self.precursorIntervalChooser.findText(self.prm[block]['precursorInterval']))
            self.precursorIntervalCheckBox.setChecked(self.prm[block]['precursorIntervalCheckBox'])
            self.onPrecursorIntervalChange()
            self.precursorIntervalISITF.setText(self.currLocale.toString(self.prm[block]['precursorIntervalISI']))
            self.precursorIntervalISICheckBox.setChecked(self.prm[block]['precursorIntervalISICheckBox'])
        if self.prm[currExp]["hasPostcursorInterval"] == True:
            self.postcursorIntervalChooser.setCurrentIndex(self.postcursorIntervalChooser.findText(self.prm[block]['postcursorInterval']))
            self.postcursorIntervalCheckBox.setChecked(self.prm[block]['postcursorIntervalCheckBox'])
            self.onPostcursorIntervalChange()
            self.postcursorIntervalISITF.setText(self.currLocale.toString(self.prm[block]['postcursorIntervalISI']))
            self.postcursorIntervalISICheckBox.setChecked(self.prm[block]['postcursorIntervalISICheckBox'])
        if self.prm[currExp]["hasAlternativesChooser"] == True:
            self.nIntervalsChooser.setCurrentIndex(self.nIntervalsChooser.findText(str(self.prm[block]['nIntervals'])))
            self.nIntervalsCheckBox.setChecked(self.prm[block]['nIntervalsCheckBox'])
            self.onNIntervalsChange(self.nIntervalsChooser.findText(str(self.prm[block]['nIntervals'])))
            self.nAlternativesChooser.setCurrentIndex(self.nAlternativesChooser.findText(str(self.prm[block]['nAlternatives'])))
            self.nAlternativesCheckBox.setChecked(self.prm[block]['nAlternativesCheckBox'])
     
        self.responseLightChooser.setCurrentIndex(self.responseLightChooser.findText(self.prm[block]['responseLight']))
        self.responseLightCheckBox.setChecked(self.prm[block]['responseLightCheckBox'])
        self.responseLightDurationTF.setText(self.currLocale.toString(self.prm[block]['responseLightDuration']))
        self.responseLightDurationCheckBox.setChecked(self.prm[block]['responseLightDurationCheckBox'])
        self.currentBlockCountLabel.setText(str(self.prm["currentBlock"]))
        self.currentBlockPositionLabel.setText(str(self.prm["tmpBlockPosition"]))
        self.storedBlocksCountLabel.setText(str(self.prm["storedBlocks"]))
        for i in range(self.jumpToBlockChooser.count()):
            self.jumpToBlockChooser.removeItem(0)
            self.jumpToPositionChooser.removeItem(0)
        for i in range(self.prm["storedBlocks"]):
            self.jumpToBlockChooser.addItem(str(i+1))
            self.jumpToPositionChooser.addItem(str(i+1))
        self.jumpToBlockChooser.setCurrentIndex(self.prm["currentBlock"]-1)
        self.jumpToPositionChooser.setCurrentIndex(int(self.prm[block]['blockPosition'])-1)
   
        for c in range(len(self.chooser)):
            self.connect(self.chooser[c], SIGNAL('activated(QString)'), self.onChooserChange)
        self.onChooserChange(None)
        self.responseBox.setupLights()


    def onClickSaveResultsButton(self):
        ftow = QtGui.QFileDialog.getSaveFileName(self, self.tr('Choose file to write results'), "", self.tr('All Files (*)'), QtGui.QFileDialog.DontConfirmOverwrite)
        if len(ftow) > 0:
            if fnmatch.fnmatch(ftow, '*.txt') == False:
                ftow = ftow + '.txt'
            self.prm['resultsFile'] = ftow
            if os.path.exists(ftow) == False:
                fName = open(ftow, 'w')
                fName.write('')
                fName.close()

            self.statusBar().showMessage(self.tr('Saving results to file: ') + self.prm["resultsFile"])
           

    def onClickStoreParametersButton(self):
        currExp =  self.tr(self.experimentChooser.currentText())
        currParadigm = self.tr(self.paradigmChooser.currentText())
        currBlock = 'b' + str(self.prm["currentBlock"])

        #FOR ALL BLOCKS
        self.prm['allBlocks'] = {}
        self.prm['allBlocks']['experimentLabel'] = self.experimentLabelTF.text()
        self.prm['allBlocks']['endExpCommand'] = self.endExpCommandTF.text()
        self.prm['allBlocks']['currentExperimenter'] = self.experimenterChooser.currentText()
        self.prm['allBlocks']['currentPhones'] = self.phonesChooser.currentText()
        self.prm['allBlocks']['maxLevel'] = float(self.prm['phones']['phonesMaxLevel'][self.phonesChooser.currentIndex()])
        self.prm['allBlocks']['sampRate'] =  self.currLocale.toInt(self.sampRateTF.text())[0]
        self.prm['allBlocks']['nBits'] = self.currLocale.toInt(self.nBitsChooser.currentText())[0]
        self.prm['allBlocks']['responseMode'] = self.responseModeChooser.currentText()
        self.prm['allBlocks']['autoPCCorr'] = self.currLocale.toDouble(self.autoPCorrTF.text())[0]/100
        self.prm['allBlocks']['sendTriggers'] = self.triggerCheckBox.isChecked()
        self.prm['allBlocks']['shuffleMode'] = self.shuffleChooser.currentText()
        self.prm['allBlocks']['repetitions'] =  self.currLocale.toInt(self.repetitionsTF.text())[0]
        self.prm['allBlocks']['procRes'] = self.procResCheckBox.isChecked()
        self.prm['allBlocks']['procResTable'] = self.procResTableCheckBox.isChecked()
        self.prm['allBlocks']['winPlot'] = self.winPlotCheckBox.isChecked()
        self.prm['allBlocks']['pdfPlot'] = self.pdfPlotCheckBox.isChecked()
        #self.prm['allBlocks']['listener'] = self.listenerTF.text()
        #self.prm['allBlocks']['sessionLabel'] = self.sessionLabelTF.text()


        #BLOCK SPECIFIC
        self.prm[currBlock] = {}
        self.prm[currBlock]['conditionLabel'] = self.conditionLabelTF.text()
        self.prm[currBlock]['experiment'] = currExp
        self.prm[currBlock]['paradigm'] = currParadigm
        self.prm[currBlock]['field'] = list(range(self.prm['nFields']))
        self.prm[currBlock]['fieldLabel'] = list(range(self.prm['nFields']))
        self.prm[currBlock]['fieldCheckBox'] = list(range(self.prm['nFields']))
        self.prm[currBlock]['chooser'] = list(range(self.prm['nChoosers']))
        self.prm[currBlock]['chooserOptions'] = list(range(self.prm['nChoosers']))
        self.prm[currBlock]['chooserCheckBox'] = list(range(self.prm['nChoosers']))
        self.prm[currBlock]['chooserLabel'] = list(range(self.prm['nChoosers']))
        self.prm[currBlock]['fileChooser'] = list(range(self.prm['nFileChoosers']))
        self.prm[currBlock]['fileChooserButton'] = list(range(self.prm['nFileChoosers']))
        self.prm[currBlock]['fileChooserCheckBox'] = list(range(self.prm['nFileChoosers']))
        self.prm[currBlock]['paradigmChooser'] = []
        self.prm[currBlock]['paradigmChooserCheckBox'] = []
        self.prm[currBlock]['paradigmField'] = []
        self.prm[currBlock]['paradigmFieldCheckBox'] = []
        self.prm[currBlock]['paradigmChooserLabel'] = []
        self.prm[currBlock]['paradigmChooserOptions'] = []
        self.prm[currBlock]['paradigmFieldLabel'] = []
        self.prm[currBlock]['blockPosition'] = self.currentBlockPositionLabel.text()
        
        self.prm[currBlock]['preTrialSilence'] = self.currLocale.toInt(self.preTrialSilenceTF.text())[0]
        self.prm[currBlock]['intervalLights'] = self.intervalLightsChooser.currentText()
        self.prm[currBlock]['warningInterval'] = self.warningIntervalChooser.currentText()
        self.prm[currBlock]['warningIntervalDur'] = self.currLocale.toInt(self.warningIntervalDurTF.text())[0]
        self.prm[currBlock]['warningIntervalISI'] = self.currLocale.toInt(self.warningIntervalISITF.text())[0]
        if self.prm[currExp]["hasISIBox"] == True:
            self.prm[currBlock]['ISIVal'] = self.currLocale.toInt(self.ISIBox.text())[0]
            self.prm[currBlock]['ISIValCheckBox'] = self.ISIBoxCheckBox.isChecked()
        if self.prm[currExp]["hasPreTrialInterval"] == True:
            self.prm[currBlock]['preTrialInterval'] = self.preTrialIntervalChooser.currentText()
            self.prm[currBlock]['preTrialIntervalCheckBox'] = self.preTrialIntervalCheckBox.isChecked()
            self.prm[currBlock]['preTrialIntervalISI'] = self.currLocale.toInt(self.preTrialIntervalISITF.text())[0]
            self.prm[currBlock]['preTrialIntervalISICheckBox'] = self.preTrialIntervalISICheckBox.isChecked()
        if self.prm[currExp]["hasPrecursorInterval"] == True:
            self.prm[currBlock]['precursorInterval'] = self.precursorIntervalChooser.currentText()
            self.prm[currBlock]['precursorIntervalCheckBox'] = self.precursorIntervalCheckBox.isChecked()
            self.prm[currBlock]['precursorIntervalISI'] = self.currLocale.toInt(self.precursorIntervalISITF.text())[0]
            self.prm[currBlock]['precursorIntervalISICheckBox'] = self.precursorIntervalISICheckBox.isChecked()
        if self.prm[currExp]["hasPostcursorInterval"] == True:
            self.prm[currBlock]['postcursorInterval'] = self.postcursorIntervalChooser.currentText()
            self.prm[currBlock]['postcursorIntervalCheckBox'] = self.postcursorIntervalCheckBox.isChecked()
            self.prm[currBlock]['postcursorIntervalISI'] = self.currLocale.toInt(self.postcursorIntervalISITF.text())[0]
            self.prm[currBlock]['postcursorIntervalISICheckBox'] = self.postcursorIntervalISICheckBox.isChecked()
        if self.prm[currExp]["hasAlternativesChooser"] == True:
            self.prm[currBlock]['nIntervals'] = self.currLocale.toInt(self.nIntervalsChooser.currentText())[0]
            self.prm[currBlock]['nIntervalsCheckBox'] = self.nIntervalsCheckBox.isChecked()
            self.prm[currBlock]['nAlternatives'] = self.currLocale.toInt(self.nAlternativesChooser.currentText())[0]
            self.prm[currBlock]['nAlternativesCheckBox'] = self.nAlternativesCheckBox.isChecked()
        
        self.prm[currBlock]['responseLight'] = self.responseLightChooser.currentText()
        self.prm[currBlock]['responseLightCheckBox'] = self.responseLightCheckBox.isChecked()
        self.prm[currBlock]['responseLightDuration'] = self.currLocale.toInt(self.responseLightDurationTF.text())[0]
        self.prm[currBlock]['responseLightDurationCheckBox'] = self.responseLightDurationCheckBox.isChecked()
        
        for f in range(self.prm['nFields']):
            self.prm[currBlock]['field'][f] = self.currLocale.toDouble(self.field[f].text())[0]
            self.prm[currBlock]['fieldLabel'][f] =  self.fieldLabel[f].text()
            self.prm[currBlock]['fieldCheckBox'][f] =  self.fieldCheckBox[f].isChecked()
            
        for c in range(self.prm['nChoosers']):
            self.prm[currBlock]['chooser'][c] =  self.chooserOptions[c][self.chooser[c].currentIndex()]
            self.prm[currBlock]['chooserOptions'][c] =  self.chooserOptions[c]
            self.prm[currBlock]['chooserLabel'][c] =  self.chooserLabel[c].text()
            self.prm[currBlock]['chooserCheckBox'][c] =  self.chooserCheckBox[c].isChecked()

        for f in range(self.prm['nFileChoosers']):
            self.prm[currBlock]['fileChooser'][f] = self.fileChooser[f].text()
            self.prm[currBlock]['fileChooserButton'][f] =  self.fileChooserButton[f].text()
            self.prm[currBlock]['fileChooserCheckBox'][f] =  self.fileChooserCheckBox[f].isChecked()

        for i in range(len(self.paradigmFieldList)):
            self.prm[currBlock]['paradigmField'].append(self.currLocale.toDouble(self.paradigmFieldList[i].text())[0])
            self.prm[currBlock]['paradigmFieldLabel'].append(self.paradigmFieldLabelList[i].text())
            self.prm[currBlock]['paradigmFieldCheckBox'].append(self.paradigmFieldCheckBoxList[i].isChecked())
        for i in range(len(self.paradigmChooserList)):
            self.prm[currBlock]['paradigmChooser'].append(self.paradigmChooserOptionsList[i][self.paradigmChooserList[i].currentIndex()])
            self.prm[currBlock]['paradigmChooserLabel'].append(self.paradigmChooserLabelList[i].text())
            self.prm[currBlock]['paradigmChooserOptions'].append(self.paradigmChooserOptionsList[i])
            self.prm[currBlock]['paradigmChooserCheckBox'].append(self.paradigmChooserCheckBoxList[i].isChecked())
                                                                
        if self.prm["currentBlock"] > self.prm["storedBlocks"]:    
            self.prm["storedBlocks"] = self.prm["storedBlocks"] + 1
        self.storedBlocksCountLabel.setText(str(self.prm["storedBlocks"]))
        for i in range(self.jumpToBlockChooser.count()):
            self.jumpToBlockChooser.removeItem(0)
            self.jumpToPositionChooser.removeItem(0)
        for i in range(self.prm["storedBlocks"]):
            self.jumpToBlockChooser.addItem(str(i+1))
            self.jumpToPositionChooser.addItem(str(i+1))
        self.jumpToBlockChooser.setCurrentIndex(self.prm["currentBlock"]-1)
        self.jumpToPositionChooser.setCurrentIndex(int(self.prm[currBlock]['blockPosition'])-1)
        self.responseBox.statusButton.setText(self.prm['rbTrans'].translate("rb", "Start"))
        self.saveParametersToFile(self.prm["tmpParametersFile"])
        
    def onClickStoreandgoParametersButton(self):
        self.onClickStoreParametersButton()
        self.moveNextBlock()
    def onClickStoreandaddParametersButton(self):
        self.onClickStoreParametersButton()
        self.onClickNewBlockButton()

    def compareGuiStoredParameters(self):
        tmpPrm = copy.copy(self.prm)
        nStoredDifferent = False
        prmChanged = False
        
        if tmpPrm["currentBlock"] > tmpPrm["storedBlocks"]:
            #this needs to be controlled first of all, because otherwise we may indavertently call an unstored block
            nStoredDifferent = True
        elif self.tr(self.experimentChooser.currentText()) != self.prm['b' + str(tmpPrm["currentBlock"])]['experiment']:
            #the experiment has changed, this needs to be checked before the other things, because the keys to compare differ between different experiments
            # and anyway if the experiment is different we can skip all other checks
            prmChanged = True
        ## elif self.warningInterval.isChecked() != self.prm['b' + str(tmpPrm["currentBlock"])]['warningInterval']:
        ##     prmChanged = True
        else:
            currExp =  self.tr(self.experimentChooser.currentText())

            tmpPrm['allBlocks'] = {}
            tmpPrm['allBlocks']['experimentLabel'] = self.experimentLabelTF.text()
            tmpPrm['allBlocks']['endExpCommand'] = self.endExpCommandTF.text()
            tmpPrm['allBlocks']['currentExperimenter'] = self.experimenterChooser.currentText()
            tmpPrm['allBlocks']['currentPhones'] = self.phonesChooser.currentText()
            tmpPrm['allBlocks']['maxLevel'] = float(self.prm['phones']['phonesMaxLevel'][self.phonesChooser.currentIndex()])
            tmpPrm['allBlocks']['sampRate'] =  self.currLocale.toInt(self.sampRateTF.text())[0]
            tmpPrm['allBlocks']['nBits'] = self.currLocale.toInt(self.nBitsChooser.currentText())[0]
            tmpPrm['allBlocks']['responseMode'] = self.responseModeChooser.currentText()
            tmpPrm['allBlocks']['autoPCCorr'] = self.currLocale.toDouble(self.autoPCorrTF.text())[0]/100
            tmpPrm['allBlocks']['sendTriggers'] = self.triggerCheckBox.isChecked()
            tmpPrm['allBlocks']['shuffleMode'] = self.shuffleChooser.currentText()
            tmpPrm['allBlocks']['repetitions'] =  self.currLocale.toInt(self.repetitionsTF.text())[0]
            tmpPrm['allBlocks']['procRes'] = self.procResCheckBox.isChecked()
            tmpPrm['allBlocks']['procResTable'] = self.procResTableCheckBox.isChecked()
            tmpPrm['allBlocks']['winPlot'] = self.winPlotCheckBox.isChecked()
            tmpPrm['allBlocks']['pdfPlot'] = self.pdfPlotCheckBox.isChecked()
            


            currParadigm = self.tr(self.paradigmChooser.currentText())
            currBlock = 'b' + str(tmpPrm["currentBlock"])
            tmpPrm[currBlock] = {}
            tmpPrm[currBlock]['conditionLabel'] = self.conditionLabelTF.text()
            tmpPrm[currBlock]['experiment'] = currExp
            tmpPrm[currBlock]['paradigm'] = currParadigm
            tmpPrm[currBlock]['field'] = list(range(tmpPrm['nFields']))
            tmpPrm[currBlock]['fieldCheckBox'] = list(range(tmpPrm['nFields']))
            tmpPrm[currBlock]['chooser'] = list(range(tmpPrm['nChoosers']))
            tmpPrm[currBlock]['chooserCheckBox'] = list(range(tmpPrm['nChoosers']))
            tmpPrm[currBlock]['fileChooser'] = list(range(tmpPrm['nFileChoosers']))
            tmpPrm[currBlock]['fileChooserCheckBox'] = list(range(tmpPrm['nFileChoosers']))
            tmpPrm[currBlock]['paradigmChooser'] = []
            tmpPrm[currBlock]['paradigmField'] = []
            tmpPrm[currBlock]['paradigmChooserCheckBox'] = []
            tmpPrm[currBlock]['paradigmFieldCheckBox'] = []
         

            otherKeysToCompare = ['preTrialSilence', 'intervalLights', 'responseLight', 'responseLightDuration', 'conditionLabel', 'warningInterval', 'warningIntervalDur', 'warningIntervalISI']
        
            tmpPrm[currBlock]['preTrialSilence'] = self.currLocale.toInt(self.preTrialSilenceTF.text())[0]
            tmpPrm[currBlock]['intervalLights'] = self.intervalLightsChooser.currentText()
            tmpPrm[currBlock]['warningInterval'] = self.warningIntervalChooser.currentText()
            tmpPrm[currBlock]['warningIntervalDur'] = self.currLocale.toInt(self.warningIntervalDurTF.text())[0]
            tmpPrm[currBlock]['warningIntervalISI'] = self.currLocale.toInt(self.warningIntervalISITF.text())[0]
            tmpPrm[currBlock]['responseLight'] = self.responseLightChooser.currentText()
            tmpPrm[currBlock]['responseLightCheckBox'] = self.responseLightCheckBox.isChecked()
            tmpPrm[currBlock]['responseLightDuration'] = self.currLocale.toInt(self.responseLightDurationTF.text())[0]
            tmpPrm[currBlock]['responseLightDurationCheckBox'] = self.responseLightDurationCheckBox.isChecked()
        
            if tmpPrm[currExp]["hasISIBox"] == True:
                tmpPrm[currBlock]['ISIVal'] = self.currLocale.toInt(self.ISIBox.text())[0]
                tmpPrm[currBlock]['ISIValCheckBox'] = self.ISIBoxCheckBox.isChecked()
                otherKeysToCompare.append('ISIVal')
            if tmpPrm[currExp]["hasPreTrialInterval"] == True:
                tmpPrm[currBlock]['preTrialInterval'] = self.preTrialIntervalChooser.currentText()
                tmpPrm[currBlock]['preTrialIntervalCheckBox'] = self.preTrialIntervalCheckBox.isChecked()
                otherKeysToCompare.append('preTrialInterval')
                tmpPrm[currBlock]['preTrialIntervalISI'] = self.currLocale.toInt(self.preTrialIntervalISITF.text())[0]
                tmpPrm[currBlock]['preTrialIntervalISICheckBox'] = self.preTrialIntervalISICheckBox.isChecked()
                otherKeysToCompare.append('preTrialIntervalISI')
            if tmpPrm[currExp]["hasPrecursorInterval"] == True:
                tmpPrm[currBlock]['precursorInterval'] = self.precursorIntervalChooser.currentText()
                tmpPrm[currBlock]['precursorIntervalCheckBox'] = self.precursorIntervalCheckBox.isChecked()
                otherKeysToCompare.append('precursorInterval')
                tmpPrm[currBlock]['precursorIntervalISI'] = self.currLocale.toInt(self.precursorIntervalISITF.text())[0]
                tmpPrm[currBlock]['precursorIntervalISICheckBox'] = self.precursorIntervalISICheckBox.isChecked()
                otherKeysToCompare.append('precursorIntervalISI')
            if tmpPrm[currExp]["hasPostcursorInterval"] == True:
                tmpPrm[currBlock]['postcursorInterval'] = self.postcursorIntervalChooser.currentText()
                tmpPrm[currBlock]['postcursorIntervalCheckBox'] = self.postcursorIntervalCheckBox.isChecked()
                otherKeysToCompare.append('postcursorInterval')
                tmpPrm[currBlock]['postcursorIntervalISI'] = self.currLocale.toInt(self.postcursorIntervalISITF.text())[0]
                tmpPrm[currBlock]['postcursorIntervalISICheckBox'] = self.postcursorIntervalISICheckBox.isChecked()
                otherKeysToCompare.append('postcursorIntervalISI')
            if tmpPrm[currExp]["hasAlternativesChooser"] == True:
                tmpPrm[currBlock]['nIntervals'] = self.currLocale.toInt(self.nIntervalsChooser.currentText())[0]
                tmpPrm[currBlock]['nIntervalsCheckBox'] = self.nIntervalsCheckBox.isChecked()
                tmpPrm[currBlock]['nAlternatives'] = self.currLocale.toInt(self.nAlternativesChooser.currentText())[0]
                tmpPrm[currBlock]['nAlternativesCheckBox'] = self.nAlternativesCheckBox.isChecked()
                otherKeysToCompare.extend(['nIntervals', 'nAlternatives'])
          

            for f in range(tmpPrm['nFields']):
                tmpPrm[currBlock]['field'][f] = self.currLocale.toDouble(self.field[f].text())[0]
                tmpPrm[currBlock]['fieldCheckBox'][f] = self.fieldCheckBox[f].isChecked()
            
            for c in range(tmpPrm['nChoosers']):
                tmpPrm[currBlock]['chooser'][c] =  self.chooserOptions[c][self.chooser[c].currentIndex()]
                tmpPrm[currBlock]['chooserCheckBox'][c] =  self.chooserCheckBox[c].isChecked()

            for f in range(tmpPrm['nFileChoosers']):
                tmpPrm[currBlock]['fileChooser'][f] = self.fileChooser[f].text()
                tmpPrm[currBlock]['fileChooserCheckBox'][f] = self.fileChooserCheckBox[f].isChecked()
            
            for i in range(len(self.paradigmFieldList)):
                tmpPrm[currBlock]['paradigmField'].append(self.currLocale.toDouble(self.paradigmFieldList[i].text())[0])
                tmpPrm[currBlock]['paradigmFieldCheckBox'].append(self.paradigmFieldCheckBoxList[i].isChecked())

            for i in range(len(self.paradigmChooserList)):
                tmpPrm[currBlock]['paradigmChooser'].append(self.paradigmChooserOptionsList[i][self.paradigmChooserList[i].currentIndex()])
                tmpPrm[currBlock]['paradigmChooserCheckBox'].append(self.paradigmChooserCheckBoxList[i].isChecked())


            i = tmpPrm["currentBlock"] -1
            if tmpPrm['b'+str(i+1)]['field'] != self.prm['b'+str(i+1)]['field']:
                prmChanged = True
            if tmpPrm['b'+str(i+1)]['chooser'] != self.prm['b'+str(i+1)]['chooser']:
                prmChanged = True
            if tmpPrm['b'+str(i+1)]['fileChooser'] != self.prm['b'+str(i+1)]['fileChooser']:
                prmChanged = True
            if tmpPrm['b'+str(i+1)]['fieldCheckBox'] != self.prm['b'+str(i+1)]['fieldCheckBox']:
                prmChanged = True
            if tmpPrm['b'+str(i+1)]['chooserCheckBox'] != self.prm['b'+str(i+1)]['chooserCheckBox']:
                prmChanged = True
            if tmpPrm['b'+str(i+1)]['fileChooserCheckBox'] != self.prm['b'+str(i+1)]['fileChooserCheckBox']:
                prmChanged = True
            if tmpPrm['b'+str(i+1)]['paradigmField'] != self.prm['b'+str(i+1)]['paradigmField']:
                prmChanged = True
            if tmpPrm['b'+str(i+1)]['paradigmFieldCheckBox'] != self.prm['b'+str(i+1)]['paradigmFieldCheckBox']:
                prmChanged = True
            if tmpPrm['b'+str(i+1)]['paradigmChooser'] != self.prm['b'+str(i+1)]['paradigmChooser']:
                prmChanged = True
            if tmpPrm['b'+str(i+1)]['paradigmChooserCheckBox'] != self.prm['b'+str(i+1)]['paradigmChooserCheckBox']:
                prmChanged = True

            for j in range(len(otherKeysToCompare)):
                thisKey = otherKeysToCompare[j]
                if tmpPrm['b'+str(i+1)][otherKeysToCompare[j]] != self.prm['b'+str(i+1)][thisKey]:
                    prmChanged = True
                if thisKey not in ['conditionLabel', 'preTrialSilence', 'warningInterval', #these ones don't have check boxes
                                   'warningIntervalDur', 'warningIntervalISI', 'intervalLights']:
                    if tmpPrm['b'+str(i+1)][otherKeysToCompare[j]+'CheckBox'] != self.prm['b'+str(i+1)][thisKey+'CheckBox']:
                        prmChanged = True

            for key in tmpPrm['allBlocks']:
                if tmpPrm['allBlocks'][key] != self.prm['allBlocks'][key]:
                    prmChanged = True

                
        if nStoredDifferent == True:
            ret = QtGui.QMessageBox.warning(self, self.tr("Warning"),
                                            self.tr("Last block has not been stored. Do you want to store it?"),
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if ret == QtGui.QMessageBox.Yes:
                self.onClickStoreParametersButton()
        elif prmChanged == True:
           
            ret = QtGui.QMessageBox.warning(self, self.tr("Warning"),
                                            self.tr("Some parameters have been modified but not stored. Do you want to store them?"),
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if ret == QtGui.QMessageBox.Yes:
                self.onClickStoreParametersButton()
                
    def onClickNewBlockButton(self):
        if self.prm["storedBlocks"] >= self.prm["currentBlock"]:
            self.compareGuiStoredParameters()
            block =  currBlock = 'b' + str(self.prm["currentBlock"])
            self.prm["currentBlock"] = self.prm["storedBlocks"] + 1
            self.prm["tmpBlockPosition"] = self.prm["storedBlocks"] + 1
            self.setNewBlock(block)
        else:
            ret = QtGui.QMessageBox.warning(self, self.tr("Warning"),
                                            self.tr("You need to store the current block before adding a new one."),
                                            QtGui.QMessageBox.Ok)
          
        
    def onClickDeleteParametersButton(self):
        if self.prm["storedBlocks"] > 1:
            if self.prm["currentBlock"] <= self.prm["storedBlocks"] and self.prm["storedBlocks"] > 0:
                currBlock = 'b' + str(self.prm["currentBlock"])
                
                if self.prm["currentBlock"] < (self.prm["storedBlocks"] -1):
                    blockPosition = self.prm[currBlock]['blockPosition']
                    del self.prm[currBlock]
                    self.prm["storedBlocks"] = self.prm["storedBlocks"] -1
                    for i in range(self.prm["storedBlocks"]-self.prm["currentBlock"]+1):
                        self.prm['b'+str(self.prm["currentBlock"]+i)] = self.prm['b'+str(self.prm["currentBlock"]+i+1)]
                    del self.prm['b'+str(self.prm["currentBlock"]+i+1)]
                    self.updateParametersWin()
                elif self.prm["currentBlock"] == (self.prm["storedBlocks"] -1):
                    blockPosition = self.prm[currBlock]['blockPosition']
                    del self.prm[currBlock]
                    self.prm["storedBlocks"] = self.prm["storedBlocks"] -1
                    self.prm['b'+str(self.prm["currentBlock"])] =  self.prm['b'+str(self.prm["storedBlocks"]+1)]
                    del self.prm['b'+str(self.prm["storedBlocks"]+1)]
                    self.updateParametersWin()
                elif self.prm["currentBlock"] > (self.prm["storedBlocks"] -1):
                    self.moveNextBlock()
                    blockPosition = self.prm[currBlock]['blockPosition']
                    del self.prm[currBlock]
                    self.prm["storedBlocks"] = self.prm["storedBlocks"] -1
                    self.storedBlocksCountLabel.setText(str(self.prm["storedBlocks"]))

                for i in range(self.prm["storedBlocks"]):
                    if int(self.prm['b'+str(i+1)]['blockPosition']) > int(blockPosition):
                        self.prm['b'+str(i+1)]['blockPosition'] = str(int(self.prm['b'+str(i+1)]['blockPosition']) -1)
                self.shufflingSchemeTF.setText("")
                self.updateParametersWin()
            else:
                self.moveNextBlock()
        elif self.prm["storedBlocks"] == 1 and self.prm["currentBlock"] > self.prm["storedBlocks"]: #created a new 2nd block, not saved, and now wants to delete, since for a single stored block you should do nothing it does nothing, so move to next block
            self.moveNextBlock()

    def onClickResetParametersButton(self):
        if self.prm["storedBlocks"] == 0:
            pass
        else:
            self.prm["currentBlock"] = 1
            for i in range(self.prm["storedBlocks"]):
                self.prm['b'+str(i+1)]['blockPosition'] = str(i+1)
            self.updateParametersWin()
            self.prm['shuffled'] = False
            self.saveParametersToFile(self.prm["tmpParametersFile"])
            self.prm['currentRepetition'] = 1
            self.autoSetGaugeValue()
            self.responseBox.statusButton.setText(self.prm['rbTrans'].translate("rb", "Start"))
    def onClickUndoUnsavedButton(self):
        if self.prm["currentBlock"] > self.prm["storedBlocks"]:
            self.onExperimentChange(self.experimentChooser.currentText())
        else:
            self.updateParametersWin()
   
    def onClickLoadParametersButton(self):
        fName = QtGui.QFileDialog.getOpenFileName(self, self.tr("Choose parameters file to load"), '', self.tr("prm files (*.prm *PRM *Prm);;All Files (*)"))
        if len(fName) > 0: #if the user didn't press cancel
            self.loadParameters(fName)
               
    def loadParameters(self, fName):
        self.parametersFile = fName
        self.prm['shuffled'] = False
        self.prm['currentRepetition'] = 1
        fStream = open(fName, 'r')
        allLines = fStream.readlines()
        fStream.close()
        tmp = {}
        foo = {}
        blockNumber = 0
        for i in range(len(allLines)):
            if allLines[i].split(':')[0] == 'Phones':
                phonesToSelect = allLines[i].split(':')[1].strip()
                try:
                    self.phonesChooser.setCurrentIndex(self.prm['phones']['phonesChoices'].index(phonesToSelect))
                except:
                    errMsg = self.tr("Phones stored in prm file {} not found in database\n Leaving phones chooser untouched".format(phonesToSelect))
                    print(errMsg, file=sys.stderr)
                    QtGui.QMessageBox.warning(self, self.tr("Warning"), errMsg)
            elif allLines[i].split(':')[0] == 'Shuffle Mode':
                shuffleMode = allLines[i].split(':')[1].strip()
                self.shuffleChooser.setCurrentIndex(self.prm['shuffleChoices'].index(shuffleMode))
            elif allLines[i].split(':')[0] == 'Response Mode':
                responseMode = allLines[i].split(':')[1].strip()
                self.responseModeChooser.setCurrentIndex(self.prm['responseModeChoices'].index(responseMode))
            elif allLines[i].split(':')[0] == 'Auto Resp. Mode Perc. Corr.':
                autoRespPercCorr = allLines[i].split(':')[1].strip()
                self.autoPCorrTF.setText(autoRespPercCorr)
            elif allLines[i].split(':')[0] == 'Sample Rate':
                sampRateToSet = allLines[i].split(':')[1].strip()
                self.sampRateTF.setText(sampRateToSet)
            elif allLines[i].split(':')[0] == 'No. Repetitions':
                repetitionsToSet = allLines[i].split(':')[1].strip()
                self.repetitionsTF.setText(repetitionsToSet)
            elif allLines[i].split(':')[0] == 'Bits':
                bitsToSet = allLines[i].split(':')[1].strip()
                self.nBitsChooser.setCurrentIndex(self.prm["nBitsChoices"].index(bitsToSet))
            elif allLines[i].split(':')[0] == 'Experiment Label':
                experimentLabelToSet = allLines[i].split(':')[1].strip()
                self.experimentLabelTF.setText(experimentLabelToSet)
            elif allLines[i].split(':')[0] == 'End Command':
                endExpCommandToSet = allLines[i].split(':')[1].strip()
                self.endExpCommandTF.setText(endExpCommandToSet)
            elif allLines[i].split(':')[0] == 'Shuffling Scheme':
                shufflingSchemeToSet = allLines[i].split(':')[1].strip()
                self.shufflingSchemeTF.setText(shufflingSchemeToSet)
            elif allLines[i].split(':')[0] == 'Trigger On/Off':
                triggerOnOff = allLines[i].split(':')[1].strip()
                if triggerOnOff == "True":
                    self.triggerCheckBox.setChecked(True)
                else:
                    self.triggerCheckBox.setChecked(False)
            elif allLines[i].split(':')[0] == 'Proc. Res.':
                procResOnOff = allLines[i].split(':')[1].strip()
                if procResOnOff == "True":
                    self.procResCheckBox.setChecked(True)
                else:
                    self.procResCheckBox.setChecked(False)
            elif allLines[i].split(':')[0] == 'Proc. Res. Table':
                procResTableOnOff = allLines[i].split(':')[1].strip()
                if procResTableOnOff == "True":
                    self.procResTableCheckBox.setChecked(True)
                else:
                    self.procResTableCheckBox.setChecked(False)
            elif allLines[i].split(':')[0] == 'Plot':
                winPlotOnOff = allLines[i].split(':')[1].strip()
                ## if self.prm['appData']['plotting_available'] == False:
                ##      winPlotOnOff = "False"
                if winPlotOnOff == "True":
                    self.winPlotCheckBox.setChecked(True)
                else:
                    self.winPlotCheckBox.setChecked(False)
            elif allLines[i].split(':')[0] == 'PDF Plot':
                pdfPlotOnOff = allLines[i].split(':')[1].strip()
                ## if self.prm['appData']['plotting_available'] == False:
                ##      pdfPlotOnOff = "False"
                if pdfPlotOnOff == "True":
                    self.pdfPlotCheckBox.setChecked(True)
                else:
                    self.pdfPlotCheckBox.setChecked(False)
            if allLines[i] == '*******************************************************\n':
                startBlock = True
                blockNumber = blockNumber + 1
                currBlock = 'b'+str(blockNumber)
                tmp['b'+str(blockNumber)] = {}
                foo['b'+str(blockNumber)] = {}

                #assign some default values to be overwritten if present in file
                tmp['b'+str(blockNumber)]['warningIntervalDur'] = 500
                tmp['b'+str(blockNumber)]['warningIntervalISI'] = 500
                tmp['b'+str(blockNumber)]['preTrialIntervalISI'] = 500
                tmp['b'+str(blockNumber)]['preTrialIntervalISICheckBox'] = False
                tmp['b'+str(blockNumber)]['precursorIntervalISI'] = 500
                tmp['b'+str(blockNumber)]['precursorIntervalISICheckBox'] = False
                tmp['b'+str(blockNumber)]['postcursorIntervalISI'] = 500
                tmp['b'+str(blockNumber)]['postcursorIntervalISICheckBox'] = False
                
            if allLines[i].split(':')[0] == 'Block Position':
                tmp['b'+str(blockNumber)]['blockPosition'] = allLines[i].split(':')[1].strip()
            if allLines[i].split(':')[0] == 'Condition Label':
                tmp['b'+str(blockNumber)]['conditionLabel'] = allLines[i].split(':')[1].strip()
            if allLines[i].split(':')[0] == 'Experiment':
                tmp['b'+str(blockNumber)]['experiment'] = allLines[i].split(':')[1].strip()
            if allLines[i].split(':')[0] == 'Paradigm':
                tmp['b'+str(blockNumber)]['paradigm'] = allLines[i].split(':')[1].strip()
            if allLines[i].split(':')[0] == 'Alternatives':
                tmp['b'+str(blockNumber)]['nAlternatives'] = self.currLocale.toInt(allLines[i].split(':')[1].strip())[0]
                tmp['b'+str(blockNumber)]['nAlternativesCheckBox'] = strToBoolean(allLines[i].split(':')[2].strip())
            if allLines[i].split(':')[0] == 'Intervals':
                tmp['b'+str(blockNumber)]['nIntervals'] = self.currLocale.toInt(allLines[i].split(':')[1].strip())[0]
                tmp['b'+str(blockNumber)]['nIntervalsCheckBox'] = strToBoolean(allLines[i].split(':')[2].strip())
            if allLines[i].split(':')[0] == 'Pre-Trial Silence (ms)':
                tmp['b'+str(blockNumber)]['preTrialSilence'] = self.currLocale.toInt(allLines[i].split(':')[1].strip())[0]
            if allLines[i].split(':')[0] == 'Interval Lights':
                tmp['b'+str(blockNumber)]['intervalLights'] = allLines[i].split(':')[1].strip()
            if allLines[i].split(':')[0] == 'Warning Interval':
                 tmp['b'+str(blockNumber)]['warningInterval'] = allLines[i].split(':')[1].strip()#strToBoolean(allLines[i].split(':')[1].strip())
            if allLines[i].split(':')[0] == 'Warning Interval Duration (ms)':
                tmp['b'+str(blockNumber)]['warningIntervalDur'] = self.currLocale.toInt(allLines[i].split(':')[1].strip())[0]
            if allLines[i].split(':')[0] == 'Warning Interval ISI (ms)':
                tmp['b'+str(blockNumber)]['warningIntervalISI'] = self.currLocale.toInt(allLines[i].split(':')[1].strip())[0]
            if allLines[i].split(':')[0] == 'ISI (ms)':
                tmp['b'+str(blockNumber)]['ISIVal'] = self.currLocale.toInt(allLines[i].split(':')[1].strip())[0]
                tmp['b'+str(blockNumber)]['ISIValCheckBox'] = strToBoolean(allLines[i].split(':')[2].strip())
            if allLines[i].split(':')[0] == 'Pre-Trial Interval':
                tmp['b'+str(blockNumber)]['preTrialInterval'] = allLines[i].split(':')[1].strip()
                tmp['b'+str(blockNumber)]['preTrialIntervalCheckBox'] = strToBoolean(allLines[i].split(':')[2].strip())
            if allLines[i].split(':')[0] == 'Pre-Trial Interval ISI (ms)':
                tmp['b'+str(blockNumber)]['preTrialIntervalISI'] = self.currLocale.toInt(allLines[i].split(':')[1].strip())[0]
                tmp['b'+str(blockNumber)]['preTrialIntervalISICheckBox'] = strToBoolean(allLines[i].split(':')[2].strip())
            if allLines[i].split(':')[0] == 'Precursor Interval':
                tmp['b'+str(blockNumber)]['precursorInterval'] = allLines[i].split(':')[1].strip()
                tmp['b'+str(blockNumber)]['precursorIntervalCheckBox'] = strToBoolean(allLines[i].split(':')[2].strip())
            if allLines[i].split(':')[0] == 'Precursor Interval ISI (ms)':
                tmp['b'+str(blockNumber)]['precursorIntervalISI'] = self.currLocale.toInt(allLines[i].split(':')[1].strip())[0]
                tmp['b'+str(blockNumber)]['precursorIntervalISICheckBox'] = strToBoolean(allLines[i].split(':')[2].strip())
            if allLines[i].split(':')[0] == 'Postcursor Interval':
                tmp['b'+str(blockNumber)]['postcursorInterval'] = allLines[i].split(':')[1].strip()
                tmp['b'+str(blockNumber)]['postcursorIntervalCheckBox'] = strToBoolean(allLines[i].split(':')[2].strip())
            if allLines[i].split(':')[0] == 'Postcursor Interval ISI (ms)':
                tmp['b'+str(blockNumber)]['postcursorIntervalISI'] = self.currLocale.toInt(allLines[i].split(':')[1].strip())[0]
                tmp['b'+str(blockNumber)]['postcursorIntervalISICheckBox'] = strToBoolean(allLines[i].split(':')[2].strip())
            if allLines[i].split(':')[0] == 'Response Light':
                tmp['b'+str(blockNumber)]['responseLight'] = allLines[i].split(':')[1].strip()
                tmp['b'+str(blockNumber)]['responseLightCheckBox'] = strToBoolean(allLines[i].split(':')[2].strip())
            if allLines[i].split(':')[0] == 'Response Light Duration (ms)':
                tmp['b'+str(blockNumber)]['responseLightDuration'] = self.currLocale.toInt(allLines[i].split(':')[1].strip())[0]
                tmp['b'+str(blockNumber)]['responseLightDurationCheckBox'] = strToBoolean(allLines[i].split(':')[2].strip())
            if allLines[i].strip() == '.':
                foo['b'+str(blockNumber)]['startParadigmChooser'] = i+1
            if allLines[i].strip() == '..':
                foo['b'+str(blockNumber)]['startParadigmField'] = i+1
            if allLines[i].strip() == '...':
                foo['b'+str(blockNumber)]['startChooser'] = i+1
            if allLines[i].strip() == '....':
                foo['b'+str(blockNumber)]['startFileChooser'] = i+1
            if allLines[i].strip() == '.....':
                foo['b'+str(blockNumber)]['startField'] = i+1
            if allLines[i] == ('+++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'):
                foo['b'+str(blockNumber)]['endField'] = i

        nBlocks = blockNumber
        for j in range(blockNumber):
            blockNumber = j+1
            tmp['b'+str(blockNumber)]['paradigmChooser'] = []
            tmp['b'+str(blockNumber)]['paradigmChooserCheckBox'] = []
            tmp['b'+str(blockNumber)]['paradigmChooserLabel'] = []
            tmp['b'+str(blockNumber)]['paradigmField'] = []
            tmp['b'+str(blockNumber)]['paradigmFieldLabel'] = []
            tmp['b'+str(blockNumber)]['paradigmFieldCheckBox'] = []
            tmp['b'+str(blockNumber)]['chooser'] = []
            tmp['b'+str(blockNumber)]['chooserLabel'] = []
            tmp['b'+str(blockNumber)]['chooserCheckBox'] = []
            tmp['b'+str(blockNumber)]['field'] = []
            tmp['b'+str(blockNumber)]['fieldCheckBox'] = []
            tmp['b'+str(blockNumber)]['fieldLabel'] = []
            tmp['b'+str(blockNumber)]['fileChooser'] = []
            tmp['b'+str(blockNumber)]['fileChooserCheckBox'] = []
            tmp['b'+str(blockNumber)]['fileChooserButton'] = []
            for i in range(foo['b'+str(blockNumber)]['startParadigmField'] - foo['b'+str(blockNumber)]['startParadigmChooser'] -1):
                tmp['b'+str(blockNumber)]['paradigmChooser'].append(allLines[foo['b'+str(blockNumber)]['startParadigmChooser']+i].split(':')[1].strip())
                tmp['b'+str(blockNumber)]['paradigmChooserLabel'].append(allLines[foo['b'+str(blockNumber)]['startParadigmChooser']+i].split(':')[0].strip()+':')
                tmp['b'+str(blockNumber)]['paradigmChooserCheckBox'].append(strToBoolean(allLines[foo['b'+str(blockNumber)]['startParadigmChooser']+i].split(':')[2].strip()))

            for i in range(foo['b'+str(blockNumber)]['startChooser'] - foo['b'+str(blockNumber)]['startParadigmField'] -1):
                tmp['b'+str(blockNumber)]['paradigmField'].append(self.currLocale.toDouble(allLines[foo['b'+str(blockNumber)]['startParadigmField']+i].split(':')[1].strip())[0])
                tmp['b'+str(blockNumber)]['paradigmFieldLabel'].append(allLines[foo['b'+str(blockNumber)]['startParadigmField']+i].split(':')[0].strip())
                tmp['b'+str(blockNumber)]['paradigmFieldCheckBox'].append(strToBoolean(allLines[foo['b'+str(blockNumber)]['startParadigmField']+i].split(':')[2].strip()))

            for i in range(foo['b'+str(blockNumber)]['startFileChooser'] - foo['b'+str(blockNumber)]['startChooser'] -1):
                tmp['b'+str(blockNumber)]['chooser'].append(allLines[foo['b'+str(blockNumber)]['startChooser']+i].split(':')[1].strip())
                tmp['b'+str(blockNumber)]['chooserLabel'].append(allLines[foo['b'+str(blockNumber)]['startChooser']+i].split(':')[0].strip()+':')
                tmp['b'+str(blockNumber)]['chooserCheckBox'].append(strToBoolean(allLines[foo['b'+str(blockNumber)]['startChooser']+i].split(':')[2].strip()))

            for i in range(foo['b'+str(blockNumber)]['startField'] - foo['b'+str(blockNumber)]['startFileChooser'] -1):
                tmp['b'+str(blockNumber)]['fileChooser'].append(allLines[foo['b'+str(blockNumber)]['startFileChooser']+i].split(':')[1].strip())
                tmp['b'+str(blockNumber)]['fileChooserButton'].append(allLines[foo['b'+str(blockNumber)]['startFileChooser']+i].split(':')[0].strip()+':')
                tmp['b'+str(blockNumber)]['fileChooserCheckBox'].append(strToBoolean(allLines[foo['b'+str(blockNumber)]['startFileChooser']+i].split(':')[2].strip()))

            for i in range(foo['b'+str(blockNumber)]['endField'] - foo['b'+str(blockNumber)]['startField'] ):
                tmp['b'+str(blockNumber)]['field'].append(self.currLocale.toDouble(allLines[foo['b'+str(blockNumber)]['startField']+i].split(':')[1].strip())[0])
                tmp['b'+str(blockNumber)]['fieldLabel'].append(allLines[foo['b'+str(blockNumber)]['startField']+i].split(':')[0].strip())
                tmp['b'+str(blockNumber)]['fieldCheckBox'].append(strToBoolean(allLines[foo['b'+str(blockNumber)]['startField']+i].split(':')[2].strip()))


              
                    
        for i in range(self.prm["storedBlocks"]):
            del self.prm['b'+str(i+1)]
        for i in range(nBlocks):
            self.prm['b'+str(i+1)] = tmp['b'+str(i+1)]
        self.prm["storedBlocks"] = nBlocks

        self.prm['allBlocks'] = {}
        self.prm['allBlocks']['experimentLabel'] = self.experimentLabelTF.text()
        self.prm['allBlocks']['endExpCommand'] = self.endExpCommandTF.text()
        self.prm['allBlocks']['currentExperimenter'] = self.experimenterChooser.currentText()
        self.prm['allBlocks']['currentPhones'] = self.phonesChooser.currentText()
        self.prm['allBlocks']['maxLevel'] = float(self.prm['phones']['phonesMaxLevel'][self.phonesChooser.currentIndex()])
        self.prm['allBlocks']['sampRate'] =  self.currLocale.toInt(self.sampRateTF.text())[0]
        self.prm['allBlocks']['nBits'] = self.currLocale.toInt(self.nBitsChooser.currentText())[0]
        self.prm['allBlocks']['responseMode'] = self.responseModeChooser.currentText()
        self.prm['allBlocks']['autoPCCorr'] = self.currLocale.toDouble(self.autoPCorrTF.text())[0]/100
        self.prm['allBlocks']['sendTriggers'] = self.triggerCheckBox.isChecked()
        self.prm['allBlocks']['shuffleMode'] = self.shuffleChooser.currentText()
        self.prm['allBlocks']['repetitions'] =  self.currLocale.toInt(self.repetitionsTF.text())[0]
        self.prm['allBlocks']['procRes'] = self.procResCheckBox.isChecked()
        self.prm['allBlocks']['procResTable'] = self.procResTableCheckBox.isChecked()
        self.prm['allBlocks']['winPlot'] = self.winPlotCheckBox.isChecked()
        self.prm['allBlocks']['pdfPlot'] = self.pdfPlotCheckBox.isChecked()
        #self.prm['allBlocks']['listener'] = self.listenerTF.text()
        #self.prm['allBlocks']['sessionLabel'] = self.sessionLabelTF.text()


        
        self.moveToBlockPosition(1)
        self.updateParametersWin()
        #for the moment here, but maybe should have a function for updating all possible dynamic default control widgets
        self.onResponseModeChange(responseMode)
        self.autoSetGaugeValue()
        self.responseBox.statusButton.setText(self.prm['rbTrans'].translate("rb", "Start"))
        self.saveParametersToFile(self.prm["tmpParametersFile"])

      
    def onClickSaveParametersButton(self):
        if self.prm["storedBlocks"] < 1:
            ret = QtGui.QMessageBox.warning(self, self.tr("Warning"),
                                      self.tr("There are no stored parameters to save."),
                                      QtGui.QMessageBox.Ok)
        else:
            if self.parametersFile == None:
                ftow = QtGui.QFileDialog.getSaveFileName(self, self.tr('Choose file to write prm'), ".prm", self.tr('All Files (*)'))
            else:
                ftow = QtGui.QFileDialog.getSaveFileName(self, self.tr('Choose file to write prm'), self.parametersFile, self.tr('All Files (*)'))
        if len(ftow) > 0 and self.prm["storedBlocks"] > 0:
            self.saveParametersToFile(ftow)
            self.saveParametersToFile(self.prm["tmpParametersFile"])
            #if self.parametersFile == self.prm["tmpParametersFile"]:
            #    if os.path.exists(self.parametersFile) == True:
            #        os.remove(self.parametersFile)
            self.parametersFile = ftow
    def saveParametersToFile(self, ftow):
        fName = open(ftow, 'w')
        fName.write('Phones: ' + self.phonesChooser.currentText() + '\n')
        fName.write('Shuffle Mode: ' + self.shuffleChooser.currentText() + '\n')
        fName.write('Response Mode: ' + self.responseModeChooser.currentText() + '\n')
        fName.write('Auto Resp. Mode Perc. Corr.: ' + self.autoPCorrTF.text() + '\n')
        fName.write('Sample Rate: ' + self.sampRateTF.text() + '\n')
        fName.write('Bits: ' + self.nBitsChooser.currentText() + '\n')
        fName.write('Trigger On/Off: ' + str(self.triggerCheckBox.isChecked()) + '\n')
        fName.write('Experiment Label: ' + self.experimentLabelTF.text() + '\n')
        fName.write('End Command: ' + self.endExpCommandTF.text() + '\n')
        fName.write('Shuffling Scheme: ' + self.shufflingSchemeTF.text() + '\n')
        fName.write('No. Repetitions: ' + self.repetitionsTF.text() + '\n')
        fName.write('Proc. Res.: ' + str(self.procResCheckBox.isChecked()) + '\n')
        fName.write('Proc. Res. Table: ' + str(self.procResTableCheckBox.isChecked()) + '\n')
        fName.write('Plot: ' + str(self.winPlotCheckBox.isChecked()) + '\n')
        fName.write('PDF Plot: ' + str(self.pdfPlotCheckBox.isChecked()) + '\n')
        for i in range(self.prm["storedBlocks"]):
            currBlock = 'b'+str(i+1)
            currExp = self.tr(self.prm[currBlock]['experiment'])
            currParadigm = self.tr(self.prm[currBlock]['paradigm'])
            fName.write('*******************************************************\n')
            fName.write(self.tr('Block Position: ') + self.prm[currBlock]['blockPosition']+ '\n')
            fName.write(self.tr('Condition Label: ') + self.prm[currBlock]['conditionLabel']+ '\n')
            fName.write(self.tr('Experiment: ') + self.prm[currBlock]['experiment']+ '\n')
            fName.write(self.tr('Paradigm: ') + self.prm[currBlock]['paradigm']+ '\n')
            if self.prm[currExp]["hasAlternativesChooser"] == True:
                fName.write(self.tr('Intervals: ') + self.currLocale.toString(self.prm[currBlock]['nIntervals']) + ' :' + str(self.prm[currBlock]['nIntervalsCheckBox']) + '\n')
                fName.write(self.tr('Alternatives: ') + self.currLocale.toString(self.prm[currBlock]['nAlternatives']) + ' :' + str(self.prm[currBlock]['nAlternativesCheckBox']) + '\n')
            fName.write(self.tr('Pre-Trial Silence (ms): ') + self.currLocale.toString(self.prm[currBlock]['preTrialSilence']) + '\n')
            fName.write(self.tr('Warning Interval: ') + str(self.prm[currBlock]['warningInterval']) + '\n')
            if self.prm[currBlock]['warningInterval'] == self.tr("Yes"):
                fName.write(self.tr('Warning Interval Duration (ms): ') + self.currLocale.toString(self.prm[currBlock]['warningIntervalDur']) + '\n')
                fName.write(self.tr('Warning Interval ISI (ms): ') + self.currLocale.toString(self.prm[currBlock]['warningIntervalISI']) + '\n')
            fName.write(self.tr('Interval Lights: ') + self.prm[currBlock]['intervalLights'] + '\n')
            if self.prm[currExp]["hasISIBox"] == True:
                fName.write(self.tr('ISI (ms): ') + self.currLocale.toString(self.prm[currBlock]['ISIVal']) + ' :' + str(self.prm[currBlock]['ISIValCheckBox']) + '\n')
            if self.prm[currExp]["hasPreTrialInterval"] == True:
                fName.write(self.tr('Pre-Trial Interval: ') + self.prm[currBlock]['preTrialInterval'] + ' :' + str(self.prm[currBlock]['preTrialIntervalCheckBox']) + '\n')
                if self.prm[currBlock]['preTrialInterval'] == self.tr("Yes"):
                    fName.write(self.tr('Pre-Trial Interval ISI (ms): ') + self.currLocale.toString(self.prm[currBlock]['preTrialIntervalISI']) + ' :' + str(self.prm[currBlock]['preTrialIntervalISICheckBox']) + '\n')
            if self.prm[currExp]["hasPrecursorInterval"] == True:
                fName.write(self.tr('Precursor Interval: ') + self.prm[currBlock]['precursorInterval'] + ' :' + str(self.prm[currBlock]['precursorIntervalCheckBox']) + '\n')
                if self.prm[currBlock]['precursorInterval'] == self.tr("Yes"):
                    fName.write(self.tr('Precursor Interval ISI (ms): ') + self.currLocale.toString(self.prm[currBlock]['precursorIntervalISI']) + ' :' + str(self.prm[currBlock]['precursorIntervalISICheckBox']) + '\n')
            if self.prm[currExp]["hasPostcursorInterval"] == True:
                fName.write(self.tr('Postcursor Interval: ') + self.prm[currBlock]['postcursorInterval'] + ' :' + str(self.prm[currBlock]['postcursorIntervalCheckBox']) + '\n')
                if self.prm[currBlock]['postcursorInterval'] == self.tr("Yes"):
                    fName.write(self.tr('Postcursor Interval ISI (ms): ') + self.currLocale.toString(self.prm[currBlock]['postcursorIntervalISI']) + ' :' + str(self.prm[currBlock]['postcursorIntervalISICheckBox']) + '\n')
             

            fName.write(self.tr('Response Light: ') + str(self.prm[currBlock]['responseLight']) + ' :' + str(self.prm[currBlock]['responseLightCheckBox']) + '\n')
            fName.write(self.tr('Response Light Duration (ms): ') + self.currLocale.toString(self.prm[currBlock]['responseLightDuration']) + ' :' + str(self.prm[currBlock]['responseLightDurationCheckBox']) + '\n')
            fName.write('.\n')
            for k in range(len(self.prm[currBlock]['paradigmChooser'])):
                fName.write(self.prm[currBlock]['paradigmChooserLabel'][k] +' ' + self.prm[currBlock]['paradigmChooser'][k] + ' :' + str(self.prm[currBlock]['paradigmChooserCheckBox'][k]) + '\n')
            fName.write('..\n')
            for k in range(len(self.prm[currBlock]['paradigmField'])):
                fName.write(self.prm[currBlock]['paradigmFieldLabel'][k] + ': ' +  self.currLocale.toString(self.prm[currBlock]['paradigmField'][k], precision=self.prm["pref"]["general"]["precision"]) + ' :' + str(self.prm[currBlock]['paradigmFieldCheckBox'][k]) + '\n')
            fName.write('...\n')
            for k in range(len(self.prm[currBlock]['chooser'])):
                fName.write(self.prm[currBlock]['chooserLabel'][k] +' ' + self.prm[currBlock]['chooser'][k] + ' :' + str(self.prm[currBlock]['chooserCheckBox'][k]) + '\n')
            fName.write('....\n')
            for k in range(len(self.prm[currBlock]['fileChooser'])):
                fName.write(self.prm[currBlock]['fileChooserButton'][k] +': ' + self.prm[currBlock]['fileChooser'][k] + ' :' + str(self.prm[currBlock]['fileChooserCheckBox'][k]) + '\n')
            fName.write('.....\n')
            for k in range(len(self.prm[currBlock]['field'])):
                fName.write(self.prm[currBlock]['fieldLabel'][k] + ': ' + self.currLocale.toString(self.prm[currBlock]['field'][k], precision=self.prm["pref"]["general"]["precision"]) + ' :' + str(self.prm[currBlock]['fieldCheckBox'][k]) + '\n')
            fName.write('+++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n')
        fName.close()
        
    def onClickPrevBlockButton(self):
        self.compareGuiStoredParameters()
        if self.prm["storedBlocks"] > 0:
            lastBlock = 'b' + str(self.prm["currentBlock"])
            if self.prm["currentBlock"] < 2 and self.prm["storedBlocks"] > 0:
                self.prm["currentBlock"] = self.prm["storedBlocks"]
            elif self.prm["currentBlock"] < 2 and self.prm["storedBlocks"] == 0:
                self.prm["currentBlock"] = 1
            else:
                if self.prm["currentBlock"] > self.prm["storedBlocks"]:
                    lastBlock = 'b' + str(self.prm["currentBlock"]-1)
                self.prm["currentBlock"] = self.prm["currentBlock"] -1
                
            if self.prm["storedBlocks"] > 0:
                self.responseBox.statusButton.setText(self.prm['rbTrans'].translate("rb", "Start"))
            self.updateParametersWin()
            self.autoSetGaugeValue()
            
    def onClickNextBlockButton(self):
        self.compareGuiStoredParameters()
        self.moveNextBlock()
        
    def moveNextBlock(self):
        if self.prm["storedBlocks"] > 0:
            lastBlock = 'b' + str(self.prm["currentBlock"])
            if self.prm["currentBlock"] >= self.prm["storedBlocks"]:
                self.prm["currentBlock"] = 1
                lastBlock = 'b' + str(self.prm["storedBlocks"])
            else:
                self.prm["currentBlock"] = self.prm["currentBlock"] +1
            if self.prm["storedBlocks"] > 0:
                self.responseBox.statusButton.setText(self.prm['rbTrans'].translate("rb", "Start"))
            self.updateParametersWin()
            self.autoSetGaugeValue()
            
    def onJumpToBlockChange(self):
        blockToJumpTo = self.jumpToBlockChooser.currentIndex() + 1
        self.compareGuiStoredParameters()
        self.prm["currentBlock"] = blockToJumpTo
        self.prm["tmpBlockPosition"] = self.prm['b'+str(self.prm["currentBlock"])]["blockPosition"]
        self.setNewBlock('b'+str(self.prm["currentBlock"]))
        if self.prm["storedBlocks"] > 0:
            self.responseBox.statusButton.setText(self.prm['rbTrans'].translate("rb", "Start"))
            self.updateParametersWin()
            self.autoSetGaugeValue()
            
    def onJumpToPositionChange(self):
        position = self.jumpToPositionChooser.currentIndex() + 1
        self.compareGuiStoredParameters()
        self.moveToBlockPosition(position)
        
    def onClickPrevBlockPositionButton(self):
        self.compareGuiStoredParameters()
        if self.prm["currentBlock"] > self.prm["storedBlocks"]:
            position = self.prm["currentBlock"]-1
        else:
            position = int(self.prm["b"+str(self.prm["currentBlock"])]["blockPosition"])-1
        self.moveToBlockPosition(position)
        
    def onClickNextBlockPositionButton(self):
        self.compareGuiStoredParameters()
        if self.prm["currentBlock"] > self.prm["storedBlocks"]:
            position = 1
        else:
            position = int(self.prm["b"+str(self.prm["currentBlock"])]["blockPosition"])+1
        self.moveToBlockPosition(position)
        
    def moveToBlockPosition(self, position):
        if self.prm["storedBlocks"] < 1:
            return
        if position > self.prm["storedBlocks"]:
            position = 1
        elif position < 1:
            position = self.prm["storedBlocks"]
     
        for k in range(self.prm["storedBlocks"]):
             if self.prm['b'+str(k+1)]['blockPosition'] == str(position):
                blockNumber = k+1
                
        self.prm["currentBlock"] = blockNumber
        self.prm["tmpBlockPosition"] = self.prm['b'+str(self.prm["currentBlock"])]["blockPosition"]
        self.setNewBlock('b'+str(self.prm["currentBlock"]))
        if self.prm["storedBlocks"] > 0:
            self.responseBox.statusButton.setText(self.prm['rbTrans'].translate("rb", "Start"))
            self.autoSetGaugeValue()
            
    def onClickShuffleBlocksButton(self):
        self.compareGuiStoredParameters()
        if self.prm["storedBlocks"] > 1:
            if len(self.shufflingSchemeTF.text()) == 0:
                blockPositions = list(range(self.prm["storedBlocks"]))
                random.shuffle(blockPositions)
                for k in range(self.prm["storedBlocks"]):
                    self.prm['b'+str(k+1)]['blockPosition'] = str(blockPositions[k]+1)
            else:
                try:
                    shuffledSeq = self.advanced_shuffle(self.shufflingSchemeTF.text())
                    blockPositions = self.unpack_seq(shuffledSeq)
                except:
                    ret = QtGui.QMessageBox.warning(self, self.tr("Warning"),
                                                    self.tr("Shuffling failed :-( Something may be wrong with your shuffling scheme."),
                                                    QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
                    return
                if len(numpy.unique(blockPositions)) != self.prm['storedBlocks']:
                    ret = QtGui.QMessageBox.warning(self, self.tr("Warning"),
                                                    self.tr("Shuffling failed :-( The length of the shuffling sequence seems to be different than the number of stored blocks. Maybe you recently added of deleted a block."),
                                                    QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
                    return
                    
                for k in range(self.prm["storedBlocks"]):
                    self.prm['b'+str(k+1)]['blockPosition'] = str(blockPositions[k])

            self.moveToBlockPosition(1)
            self.prm['shuffled'] = True
            self.saveParametersToFile(self.prm["tmpParametersFile"])
            self.updateParametersWin()
            self.responseBox.statusButton.setText(self.prm['rbTrans'].translate("rb", "Start"))
            self.autoSetGaugeValue()
            
    def autoSetGaugeValue(self):
        bp = int(self.prm['b'+str(self.prm["currentBlock"])]["blockPosition"])
        pcThisRep = (bp-1)/self.prm["storedBlocks"]*100
        pcTot = (self.prm['currentRepetition'] - 1) / self.prm['allBlocks']['repetitions']*100 + 1 / self.prm['allBlocks']['repetitions']*pcThisRep
        self.responseBox.gauge.setValue(pcTot)
        self.responseBox.blockGauge.setRange(0, self.prm['storedBlocks']*self.prm['allBlocks']['repetitions'])

        cb = (self.prm['currentRepetition']-1)*self.prm["storedBlocks"]+bp
        self.responseBox.blockGauge.setValue(cb-1)
        self.responseBox.blockGauge.setFormat(self.prm['rbTrans'].translate('rb', "Completed") +  ' ' + str(cb-1) + '/' + str(self.prm['storedBlocks']*self.prm['allBlocks']['repetitions']) + ' ' + self.prm['rbTrans'].translate('rb', "Blocks"))
        
    def swapBlocks(self, b1, b2):
        self.compareGuiStoredParameters()
        if self.prm["storedBlocks"] < 1:
            return
        if b1 > self.prm["storedBlocks"] or b2 > self.prm["storedBlocks"]:
            ret = QtGui.QMessageBox.warning(self, self.tr("Warning"),
                                            self.tr("You're trying to swap the position of a block that has not been stored yet. Please, store the block first."),
                                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
            return
        if self.prm["storedBlocks"] > 1 and b1 <= self.prm["storedBlocks"] and b2 <= self.prm["storedBlocks"]:
            ol=copy.deepcopy(self.prm['b'+str(b1)])
            self.prm['b'+str(b1)] = copy.deepcopy(self.prm['b'+str(b2)])
            self.prm['b'+str(b2)] = copy.deepcopy(ol)
            self.saveParametersToFile(self.prm["tmpParametersFile"])
        #
            #self.updateParametersWin()
            self.moveToBlockPosition(int(self.prm['b'+str(b2)]["blockPosition"]))
        return
    
    def shiftBlock(self, blockNumber, direction):
        if direction == "up":
            if blockNumber == self.prm["storedBlocks"]:
                newBlockNumber = 1
            else:
                newBlockNumber = blockNumber + 1
        elif direction == "down":
            if blockNumber == 1:
                newBlockNumber = self.prm["storedBlocks"]
            else:
                newBlockNumber = blockNumber - 1
        self.swapBlocks(blockNumber, newBlockNumber)
        
    def onClickShiftBlockDownButton(self):
        self.shiftBlock(self.prm['currentBlock'], 'down')
        
    def onClickShiftBlockUpButton(self):
        self.shiftBlock(self.prm['currentBlock'], 'up')
        
    def onChangeNDifferences(self):
        nDifferences = self.currLocale.toInt(self.nDifferencesChooser.currentText())[0]
        self.removePrmWidgets()
        self.par['nDifferences'] = nDifferences
        self.setDefaultParameters(self.currExp, self.currParadigm, self.par)
        
    def onChangeNTracks(self):
        nTracks = self.currLocale.toInt(self.nTracksChooser.currentText())[0]
        self.removePrmWidgets()
        self.par['nDifferences'] = nTracks
        self.setDefaultParameters(self.currExp, self.currParadigm, self.par)

    def onChooserChange(self, selectedOption):
        self.fieldsToHide = []; self.fieldsToShow = []
        self.choosersToHide = []; self.choosersToShow = [];
        self.fileChoosersToHide = []; self.fileChoosersToShow = [];

        execString = self.prm[self.currExp]['execString']

        try:
            methodToCall1 = getattr(default_experiments, execString)
        except:
            pass
        try:
            methodToCall1 = getattr(labexp, execString)
        except:
            pass

        if hasattr(methodToCall1, 'get_fields_to_hide_'+ execString):
            methodToCall2 = getattr(methodToCall1, 'get_fields_to_hide_'+ execString)
            tmp = methodToCall2(self)

            for i in range(len(self.fieldsToHide)):
                self.field[self.fieldsToHide[i]].hide()
                self.fieldLabel[self.fieldsToHide[i]].hide()
                self.fieldCheckBox[self.fieldsToHide[i]].hide()
            for i in range(len(self.fieldsToShow)):
                self.field[self.fieldsToShow[i]].show()
                self.fieldLabel[self.fieldsToShow[i]].show()
                self.fieldCheckBox[self.fieldsToShow[i]].show()
            for i in range(len(self.choosersToHide)):
                self.chooser[self.choosersToHide[i]].hide()
                self.chooserLabel[self.choosersToHide[i]].hide()
                self.chooserCheckBox[self.choosersToHide[i]].hide()
            for i in range(len(self.choosersToShow)):
                self.chooser[self.choosersToShow[i]].show()
                self.chooserLabel[self.choosersToShow[i]].show()
                self.chooserCheckBox[self.choosersToShow[i]].show()
            for i in range(len(self.fileChoosersToHide)):
                self.fileChooser[self.fileChoosersToHide[i]].hide()
                self.fileChooserButton[self.fileChoosersToHide[i]].hide()
                self.fileChooserCheckBox[self.fileChoosersToHide[i]].hide()
            for i in range(len(self.fileChoosersToShow)):
                self.fileChooser[self.fileChoosersToHide[i]].show()
                self.fileChooserButton[self.fileChoosersToHide[i]].show()
                self.fileChooserCheckBox[self.fileChoosersToHide[i]].show()

    def fileChooserButtonClicked(self):
        sender = self.sender()
        fName = QtGui.QFileDialog.getOpenFileName(self, self.tr("Choose file"), '', self.tr("files (*);;All Files (*)"))
        lbls = []
 
        if len(fName) > 0: #if the user didn't press cancel
            for i in range(self.prm['nFileChoosers']):
                lbls.append(self.fileChooserButton[i].text())
            self.fileChooser[lbls.index(sender.text())].setText(fName)
        #print(sender.text())
        
    def onEditPref(self):
        dialog = preferencesDialog(self)
        if dialog.exec_():
            dialog.permanentApply()
            self.audioManager.initializeAudio()
            
    def onEditPhones(self):
        currIdx = self.phonesChooser.currentIndex()
        dialog = phonesDialog(self)
        if dialog.exec_():
            dialog.permanentApply()
     
        self.phonesChooser.setCurrentIndex(currIdx)
        if self.phonesChooser.currentIndex() == -1:
            self.phonesChooser.setCurrentIndex(0)

    def onEditExperimenters(self):
        dialog = experimentersDialog(self)
        if dialog.exec_():
            dialog.onClickApplyButton()

    ## def onCalibrationDialog(self):
    ##     dialog = preferencesDialog(self)
    ##     if dialog.exec_():
    ##         dialog.permanentApply()

    def processResultsLinearDialog(self):
        fList = QtGui.QFileDialog.getOpenFileNames(self, self.tr("Choose results file to load"), '', self.tr("All Files (*)"))
        sep = None
        if len(fList) > 0:
            resformat = 'linear'

            f = open(fList[0], 'r')
            allLines = f.readlines()
            f.close()
            paradigmFound = False
            lineNum = 0
            while paradigmFound == False:
                if allLines[lineNum].split(':')[0] == "Paradigm":
                    paradigm = allLines[lineNum].split(':')[1].strip()
                    paradigmFound = True
                lineNum = lineNum+1
                
            dialog = processResultsDialog(self, fList, resformat, paradigm, sep)
            

    def processResultsTableDialog(self):
        fList = QtGui.QFileDialog.getOpenFileNames(self, self.tr("Choose results file to load"), '', self.tr("All Files (*)"))
        sep = None
        if len(fList) > 0:
           
            resformat = 'table'
        #Determine paradigm

            f = open(fList[0], "r")
            thisLines = f.readlines()
            f.close()

            seps = [';', ',', ':', ' ']
            for sep in seps:
                try:
                    prdgCol = thisLines[0].split(sep).index('paradigm')
                except:
                    prdgCol = None
                if prdgCol != None:
                    break
            if prdgCol == None:
                sep, ok = QtGui.QInputDialog.getText(self, self.tr('Input Dialog'), "CSV separator")
                if ok == False:
                    return

            paradigm = thisLines[1].split(sep)[prdgCol]
                
            dialog = processResultsDialog(self, fList, resformat, paradigm, sep)
   

    def onClickOpenResultsButton(self):
        if "resultsFile" in self.prm:
            fileToOpen = self.prm["resultsFile"]
            QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(fileToOpen))
        else:
            ret = QtGui.QMessageBox.information(self, self.tr("message"),
                                                self.tr("No results file has been selected"),
                                                QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
            
    def onAbout(self):
        QtGui.QMessageBox.about(self, self.tr("About pychoacoustics"),
                                self.tr("""<b>Python app for psychoacoustics</b> <br>
                                - version: {0}; <br>
                                - build date: {1} <br>
                                <p> Copyright &copy; 2010-2013 Samuele Carcagno. <a href="mailto:sam.carcagno@gmail.com">sam.carcagno@gmail.com</a> 
                                All rights reserved. <p>
                                This program is free software: you can redistribute it and/or modify
                                it under the terms of the GNU General Public License as published by
                                the Free Software Foundation, either version 3 of the License, or
                                (at your option) any later version.
                                <p>
                                This program is distributed in the hope that it will be useful,
                                but WITHOUT ANY WARRANTY; without even the implied warranty of
                                MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
                                GNU General Public License for more details.
                                <p>
                                You should have received a copy of the GNU General Public License
                                along with this program.  If not, see <a href="http://www.gnu.org/licenses/">http://www.gnu.org/licenses/</a>
                                <p>Python {2} - Qt {3} - PyQt {4} on {5}""").format(__version__, self.prm['builddate'], platform.python_version(), QtCore.QT_VERSION_STR, QtCore.PYQT_VERSION_STR, platform.system()))
    def closeEvent(self, event):
        #here we need to check if parameters file and temporary parameters file are the same or not
        self.compareGuiStoredParameters()
        if self.prm['storedBlocks'] > 0:
            if self.parametersFile == None:
                ret = QtGui.QMessageBox.warning(self, self.tr("Warning"),
                                                self.tr("The parameters have not been saved to a file. \n Do you want to save them before exiting?"),
                                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
                if ret == QtGui.QMessageBox.Yes:
                    self.onClickSaveParametersButton()
            else:
                f1 = open(self.parametersFile, 'r'); f2 = open(self.prm["tmpParametersFile"], 'r')
                l1c = f1.readlines(); l2c = f2.readlines()
                f1.close(); f2.close()
                l1 = []; l2 = []

                for line in l1c:
                    if line[0:14] != 'Block Position':
                        l1.append(line)
                for line in l2c:
                    if line[0:14] != 'Block Position':
                        l2.append(line)
                if  l1 != l2:
                    ret = QtGui.QMessageBox.warning(self, self.tr("Warning"),
                                                    self.tr("The parameters in memory differ from the parameters on file. \n Do you want to save the parameters stored in memory them before exiting?"),
                                                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
                    if ret == QtGui.QMessageBox.Yes:
                        self.onClickSaveParametersButton()
            #else:
            #    if os.path.exists(self.parametersFile) == True:
            #        os.remove(self.parametersFile)

        event.accept()

    def onWhatsThis(self):
        if QtGui.QWhatsThis.inWhatsThisMode() == True:
            QtGui.QWhatsThis.leaveWhatsThisMode()
        else:
            QtGui.QWhatsThis.enterWhatsThisMode()

    def onShowFortune(self):
        dialog = showFortuneDialog(self)
        
    def onShowManualPdf(self):
        fileToOpen = os.path.abspath(os.path.dirname(__file__)) + '/doc/_build/latex/pychoacoustics.pdf'
        QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(fileToOpen))
        
    def onShowModulesDoc(self):
        fileToOpen = os.path.abspath(os.path.dirname(__file__)) + '/doc/_build/html/index.html'
        QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(fileToOpen))
        
    def onSwapBlocksAction(self):
        dialog = swapBlocksDialog(self)
        if dialog.exec_():
            blockA = self.currLocale.toInt(dialog.blockAWidget.text())[0]
            blockB = self.currLocale.toInt(dialog.blockBWidget.text())[0]
            if self.prm['storedBlocks'] < 1:
                ret = QtGui.QMessageBox.warning(self, self.tr("Warning"),
                                                self.tr("There are no stored blocks to swap."),
                                                QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
                return
            if blockA < 1 or blockB < 1 or blockA > self.prm['storedBlocks'] or blockB > self.prm['storedBlocks']:
                ret = QtGui.QMessageBox.warning(self, self.tr("Warning"),
                                                self.tr("Block numbers specified out of range."),
                                                QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
                return
            else:
                self.swapBlocks(blockA, blockB)
        return

    def parseShuffleSeq(self, seq):
        seq = seq.replace(' ', '') #remove white space
        seqLen = len(seq)
        allowedChars = list(string.digits)
        allowedChars.extend([',', '-', '(', ')', '[', ']'])
        outSeq = ''
        for i in range(len(seq)):
            if seq[i] not in allowedChars:
                ret = QtGui.QMessageBox.warning(self, self.tr("Warning"),
                                                self.tr("Shuffling scheme contains non-allowed characters."),
                                                QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
                return
        seqFound = False
        k = 0
        while seqFound == False:        
            if seq[k] in ['(', ')', '[', ']', ',']:
                outSeq = outSeq + seq[k]
                k = k+1
            elif seq[k] == '-':
                prevDig = seq[k-1]
                nextDig = seq[k+1]
                delimiterFound = False
                n = 2
                while delimiterFound == False:
                    if seq[k-n] not in ['(', '[', ',']:
                        prevDig = seq[k-n] + prevDig
                        n = n+1
                    else:
                        delimiterFound = True
                delimiterFound = False
                n = 2
                while delimiterFound == False:
                    if seq[k+n] not in [')', ']', ',']:
                        nextDig = nextDig + seq[k+n]
                        n = n+1
                    else:
                        delimiterFound = True
                nextDigitLength = n-1
                prevDig = int(prevDig)
                nextDig = int(nextDig)
                for j in range(prevDig+1, nextDig+1):
                    outSeq = outSeq + ',' + str(j)
                k = k+n
            else:
                outSeq = outSeq + seq[k]
                k = k+1
            if k == len(seq):
                seqFound = True
        return outSeq

    def check_and_shuffle(self, seq):
        if isinstance(seq, list) == True:
            random.shuffle(seq)
        for i in range(len(seq)):
            if isinstance(seq[i], list) == True or isinstance(seq[i], tuple) == True:
                self.check_and_shuffle(seq[i])
        return seq

    def advanced_shuffle(self, seq):
        seq = self.parseShuffleSeq(seq)
        try:
            seq = eval(seq)
        except:
            print('could not evaluate seq')
            return

        x = self.check_and_shuffle(seq)

        return x

    def unpack_seq(self, seq):
        newSeq = []
        for i in range(len(seq)):
            if isinstance(seq[i], list) == True or isinstance(seq[i], tuple) == True:
                y = self.unpack_seq(seq[i])
                newSeq.extend(y)
            else:
                newSeq.append(seq[i])
        return newSeq
    
    def toggleWinPlotCheckBox(self, state):
     if self.winPlotCheckBox.isChecked() == True: #or self.pdfPlotCheckBox.isChecked() == True:
         self.procResTableCheckBox.setChecked(True)
         
    def togglePdfPlotCheckBox(self, state):
     if self.pdfPlotCheckBox.isChecked() == True: #or self.pdfPlotCheckBox.isChecked() == True:
         self.procResTableCheckBox.setChecked(True)
         
    def toggleResTableCheckBox(self, state):
        if self.procResTableCheckBox.isChecked() == False:
            self.winPlotCheckBox.setChecked(False)
            self.pdfPlotCheckBox.setChecked(False)


class dropFrame(QtGui.QFrame):
    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            l = []
            for url in event.mimeData().urls():
                l.append(str(url.toLocalFile()))
                self.emit(SIGNAL("dropped"), l)
        else:
            event.ignore()


  
