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
    from PyQt5 import QtCore, QtGui
    from PyQt5.QtCore import Qt, QEvent
    from PyQt5.QtWidgets import QAction, QCheckBox, QComboBox, QDesktopWidget, QFrame, QFileDialog, QGridLayout, QHBoxLayout, QLabel, QLayout, QLineEdit, QMainWindow, QMessageBox, QScrollArea, QSizePolicy, QSpacerItem, QSplitter, QPushButton, QTextEdit, QVBoxLayout, QWhatsThis, QWidget
    from PyQt5.QtGui import QDesktopServices, QDoubleValidator, QIcon, QIntValidator
    QtCore.Signal = QtCore.pyqtSignal
    QtCore.Slot = QtCore.pyqtSlot
    try:
        import matplotlib
        matplotlib_available = True
        matplotlib.rcParams['backend'] = "Qt5Agg"
    except:
        matplotlib_available = False
    try:
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
        matplotlib_available = True
    except:
        matplotlib_available = False
elif pyqtversion == 6:
    from PyQt6 import QtCore, QtGui
    from PyQt6.QtCore import Qt, QEvent
    from PyQt6.QtWidgets import QCheckBox, QComboBox, QFrame, QFileDialog, QGridLayout, QHBoxLayout, QLabel, QLayout, QLineEdit, QMainWindow, QMessageBox, QScrollArea, QSizePolicy, QSpacerItem, QSplitter, QPushButton, QTextEdit, QVBoxLayout, QWhatsThis, QWidget#, QDesktopWidget
    from PyQt6.QtGui import QAction, QDesktopServices, QDoubleValidator, QIcon, QIntValidator
    QtCore.Signal = QtCore.pyqtSignal
    QtCore.Slot = QtCore.pyqtSlot
    try:
        import matplotlib
        matplotlib_available = True
        matplotlib.rcParams['backend'] = "QtAgg"
    except:
        matplotlib_available = False
    try:
        from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
        matplotlib_available = True
    except:
        matplotlib_available = False
    
from .audio_manager import*
from .global_parameters import*
from .response_box import*
from .dialog_edit_preferences import*
from .dialog_edit_phones import*
from .dialog_edit_experimenters import*
from .dialog_process_results import*
from .dialog_show_exp_doc import*
from .dialog_show_fortune import*
from .dialog_swap_blocks import*
from .dialog_memory_file_parameters_differ import*
from .pysdt import*

if matplotlib_available == True:
    from .win_psychometric_listener_plot import*
    from .win_UML_parspace_plot import UMLParSpacePlot
    from .win_PSI_parspace_plot import PSIParSpacePlot
    from .win_UML_est_guess_parspace_plot import UMLEstGuessRateParSpacePlot
    from .win_PSI_est_guess_parspace_plot import PSIEstGuessRateParSpacePlot


#from redirect_out import*
from . import default_experiments
import difflib, fnmatch
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

class pychControlWin(QMainWindow):
    def __init__(self, parent=None, prm=None):
        QMainWindow.__init__(self, parent)
        self.prm = prm
        self.audioManager = audioManager(self)
        self.executerThread1 = commandExecuter1(self)
        if len(self.prm["pref"]["general"]["startupCommand"]) > 0:
            try:
                self.executerThread1.executeCommand([self.prm["pref"]["general"]["startupCommand"]])
            except:
                pass
        #
        self.prm['version'] = __version__
        self.prm['builddate'] = pychoacoustics_builddate
        #
        if pyqtversion == 5:
            screen = QDesktopWidget().screenGeometry()
        elif pyqtversion == 6:
            screen = self.screen().geometry()
        self.setGeometry(25, 50, int((2/3)*screen.width()), int((7/10)*screen.height())) #was 80, 100
        #self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint)
        self.currLocale = prm['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.NumberOption.OmitGroupSeparator | self.currLocale.NumberOption.RejectGroupSeparator)
        self.setWindowTitle(self.tr("Pychoacoustics - Control Window"))
        self.menubar = self.menuBar()
        self.statusBar()
        self.parametersFile = None 
        self.prm['currentRepetition'] = 1
        #FILE MENU
        self.fileMenu = self.menubar.addMenu(self.tr('&File'))
        self.exitButton = QAction(QIcon.fromTheme("application-exit", QIcon(":/application-exit")), self.tr('Exit'), self)
        self.exitButton.setShortcut('Ctrl+Q')
        self.exitButton.setStatusTip(self.tr('Exit application'))

        self.exitButton.triggered.connect(self.close)

        self.processResultsMenu = self.fileMenu.addMenu(self.tr('&Process Results'))
        
        self.processResultsLinearButton = QAction(self.tr('&Process Results (Plain Text)'), self)
        self.processResultsLinearButton.setStatusTip(self.tr('Process Results (Plain Text)'))
        self.processResultsLinearButton.triggered.connect(self.processResultsLinearDialog)

        self.processResultsTableButton = QAction(self.tr('&Process Results Table'), self)
        self.processResultsTableButton.setStatusTip(self.tr('Process Results Table'))
        self.processResultsTableButton.triggered.connect(self.processResultsTableDialog)


        self.openResultsButton = QAction(QIcon.fromTheme("document-open", QIcon(":/document-open")), self.tr('Open Results File'), self)
        self.openResultsButton.setStatusTip(self.tr('Open Results File'))
        self.openResultsButton.triggered.connect(self.onClickOpenResultsButton)

        self.processResultsMenu.addAction(self.processResultsLinearButton)
        self.processResultsMenu.addAction(self.processResultsTableButton)
        
        self.fileMenu.addAction(self.openResultsButton)
        self.fileMenu.addAction(self.exitButton)
        
        #EDIT MENU
        self.editMenu = self.menubar.addMenu(self.tr('&Edit'))
        self.editPrefAction = QAction(QIcon.fromTheme("preferences-other", QIcon(":/preferences-other")), self.tr('Preferences'), self)
        self.editMenu.addAction(self.editPrefAction)
        self.editPrefAction.triggered.connect(self.onEditPref)

        self.editPhonesAction = QAction(QIcon.fromTheme("audio-headphones", QIcon(":/audio-headphones")), self.tr('Phones'), self)
        self.editMenu.addAction(self.editPhonesAction)
        self.editPhonesAction.triggered.connect(self.onEditPhones)

        self.editExperimentersAction = QAction(QIcon.fromTheme("system-users", QIcon(":/system-users")), self.tr('Experimenters'), self)
        self.editMenu.addAction(self.editExperimentersAction)
        self.editExperimentersAction.triggered.connect(self.onEditExperimenters)

        #TOOLS MENU
        self.toolsMenu = self.menubar.addMenu(self.tr('&Tools'))
        self.swapBlocksAction = QAction(self.tr('Swap Blocks'), self)
        self.toolsMenu.addAction(self.swapBlocksAction)
        self.swapBlocksAction.triggered.connect(self.onSwapBlocksAction)

        #HELP MENU
        self.helpMenu = self.menubar.addMenu(self.tr('&Help'))

        self.onShowModulesDocAction = QAction(self.tr('Manual (html)'), self)
        self.helpMenu.addAction(self.onShowModulesDocAction)
        self.onShowModulesDocAction.triggered.connect(self.onShowModulesDoc)

        self.onShowManualPdfAction = QAction(self.tr('Manual (pdf)'), self)
        self.helpMenu.addAction(self.onShowManualPdfAction)
        self.onShowManualPdfAction.triggered.connect(self.onShowManualPdf)

        self.onShowFortuneAction = QAction(self.tr('Fortunes'), self)
        self.helpMenu.addAction(self.onShowFortuneAction)
        self.onShowFortuneAction.triggered.connect(self.onShowFortune)
        
        self.onAboutAction = QAction(QIcon.fromTheme("help-about", QIcon(":/help-about")), self.tr('About pychoacoustics'), self)
        self.helpMenu.addAction(self.onAboutAction)
        self.onAboutAction.triggered.connect(self.onAbout)

        #TOOLBAR???
        ## self.toolbar = self.addToolBar('Control Window Toolbar')
        ## self.saveResultsAction = QAction(QIcon.fromTheme("document-save", QIcon(":/document-save")), self.tr("Save results"), self)
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

        self.cw = QFrame()
        self.pw = dropFrame(None)
        self.cw.setFrameStyle(QFrame.Shape.StyledPanel|QFrame.Shadow.Sunken)
        self.pw.setFrameStyle(QFrame.Shape.StyledPanel|QFrame.Shadow.Sunken)
        #self.splitter = QSplitter(QtCore.Qt.Horizontal)
        self.splitter = QSplitter(QtCore.Qt.Orientation.Horizontal)
        self.pw.drpd.connect(self.onDropPrmFile)


        self.onWhatsThisAction = QAction(QIcon.fromTheme("help-contextual", QIcon(":/help-contextual")), self.tr('?'), self)
        self.menubar.addAction(self.onWhatsThisAction)
        self.onWhatsThisAction.triggered.connect(self.onWhatsThis)
        #STATUS BAR
        if "resultsFile" not in self.prm:
            self.statusBar().showMessage(self.tr('No results file selected, saving to file: test.txt'))
        else:
            self.statusBar().showMessage(self.tr('Saving results to file: ') + self.prm["resultsFile"])
       

        self.cw_sizer = QVBoxLayout()
        self.def_widg_sizer = QGridLayout()
        n = 0

        #LISTENER
        self.listenerLabel = QLabel(self.tr('Listener:'), self)
        self.def_widg_sizer.addWidget(self.listenerLabel,n, 0)
        self.listenerTF = QLineEdit("")
        if 'listener' in self.prm:
            self.listenerTF.setText(self.prm['listener'])
        self.listenerTF.editingFinished.connect(self.onListenerChange)
        self.listenerTF.setWhatsThis(self.tr("Set a label (e.g. initials, or full name) for the listener being tested."))
        self.def_widg_sizer.addWidget(self.listenerTF, n, 1)

        #min_pw_butt_size = 22
        #min_pw_icon_size = 20
        
        #self.def_widg_sizer.setRowMinimumHeight(0, min_pw_butt_size)
        self.soundCheckButton = QPushButton(self.tr("Sound check"), self)
        self.soundCheckButton.clicked.connect(self.onClickSoundCheckButton)
        self.soundCheckButton.setIcon(QIcon.fromTheme("media-playback-start", QIcon(":/media-playback-start")))
        #self.soundCheckButton.setIconSize(QtCore.QSize(min_pw_icon_size, min_pw_icon_size))
        self.soundCheckButton.setToolTip(self.tr("Play test sounds"))
        self.soundCheckButton.setWhatsThis(self.tr("Play some test sounds to check that audio output is working OK."))
        self.def_widg_sizer.addWidget(self.soundCheckButton, n, 3)
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
        self.sessionLabelTF.editingFinished.connect(self.onSessionLabelChange)
        #CONDITION LABEL
        n = n+1
        self.conditionLabelLabel = QLabel(self.tr('Condition Label:'), self)
        self.def_widg_sizer.addWidget(self.conditionLabelLabel, n, 0)
        self.conditionLabelTF = QLineEdit("")
        self.conditionLabelTF.setWhatsThis(self.tr("Set a label for the current experimental condition. This label applies only to the current experimental block."))
        self.def_widg_sizer.addWidget(self.conditionLabelTF, n, 1, 1, 1)
        #TASK LABEL
        self.taskLabelLabel = QLabel(self.tr('Task Label:'), self)
        self.def_widg_sizer.addWidget(self.taskLabelLabel, n, 2)
        self.taskLabelTF = QLineEdit("")
        self.taskLabelTF.setWhatsThis(self.tr("This label will be shown in the response box to tell the listener which task s/he's doing."))
        self.def_widg_sizer.addWidget(self.taskLabelTF, n, 3, 1, 1)
        #INSTRUCTIONS
        n = n+1
        self.instructionsLabel = QLabel(self.tr('Instructions:'), self)
        self.def_widg_sizer.addWidget(self.instructionsLabel, n, 0)
        self.instructionsTF = QTextEdit()
        self.instructionsTF.setWhatsThis(self.tr("Set the instructions to be shown to the participant for the current block."))
        self.instructionsTF.setMaximumHeight(60)
        self.def_widg_sizer.addWidget(self.instructionsTF, n, 1, 1, 3)
        #SHOW INSTRUCTIONS AT
        n = n+1
        self.instructionsAtLabel = QLabel(self.tr('Show Instructions At BP:'), self)
        self.def_widg_sizer.addWidget(self.instructionsAtLabel, n, 0)
        self.instructionsAtTF = QLineEdit()
        self.instructionsAtTF.setWhatsThis(self.tr("Indicate at which block positions the task instructions will be shown, e.g. '1,5,10'."))
        self.instructionsAtTF.editingFinished.connect(self.validateInstructionsAtTF)
        self.def_widg_sizer.addWidget(self.instructionsAtTF, n, 1, 1, 3)
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
        self.procResCheckBox = QCheckBox(self.tr('Proc. Res.'))
        self.procResCheckBox.setWhatsThis(self.tr("If checked, and if the procedure supports it the plain text results will be automatically processed at the end of the session. Does not work if different procedures are mixed within a session"))
        self.def_widg_sizer.addWidget(self.procResCheckBox, n, 0)
        #PROC RES TABLE
        self.procResTableCheckBox = QCheckBox(self.tr('Proc. Res. Table'))
        self.procResTableCheckBox.setWhatsThis(self.tr("If checked, and if the procedure supports it the tabular results will be automatically processed at the end of the session. Does not work if different procedures are mixed within a session"))
        self.procResTableCheckBox.stateChanged[int].connect(self.toggleResTableCheckBox)
        self.def_widg_sizer.addWidget(self.procResTableCheckBox, n, 1)
        n = n+1
        #PLOT
        self.winPlotCheckBox = QCheckBox(self.tr('Plot'))
        self.winPlotCheckBox.setWhatsThis(self.tr("If checked, and if the procedure supports it the results will be automatically plotted in a window at the end of the session. Does not work if different procedures are mixed within a session"))
        self.winPlotCheckBox.stateChanged[int].connect(self.toggleWinPlotCheckBox)
        self.def_widg_sizer.addWidget(self.winPlotCheckBox, n, 0)
        if self.prm['appData']['plotting_available'] == False:
            self.winPlotCheckBox.hide()
        #PDF PLOT
        self.pdfPlotCheckBox = QCheckBox(self.tr('PDF Plot'))
        self.pdfPlotCheckBox.setWhatsThis(self.tr("If checked, and if the procedure supports it the results will be automatically plotted in a pdf file at the end of the session. Does not work if different procedures are mixed within a session"))
        self.pdfPlotCheckBox.stateChanged[int].connect(self.togglePdfPlotCheckBox)
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
        self.experimentChooser.setWhatsThis(self.tr("Choose the experiment for the current block."))
        self.experimentChooser.addItems(self.prm["experimentsChoices"])
        self.def_widg_sizer.addWidget(self.experimentChooser, n, 1)
        self.experimentChooser.textActivated[str].connect(self.onExperimentChange)
        #PARADIGM
        n = n+1
        self.paradigmLabel = QLabel(self.tr("Paradigm:"), self)
        self.def_widg_sizer.addWidget(self.paradigmLabel, n, 0)
        self.paradigmChooser = QComboBox()
        self.paradigmChooser.addItems(self.prm[self.tr('Audiogram')]['paradigmChoices'])
        self.paradigmChooser.setCurrentIndex(1)
        self.paradigmChooser.setWhatsThis(self.tr("Choose the paradigm for the current block."))
        self.def_widg_sizer.addWidget(self.paradigmChooser, n, 1)
        self.paradigmChooser.textActivated[str].connect(self.onParadigmChange)
        #PHONES
        n = n+1
        self.phonesLabel = QLabel(self.tr("Phones:"), self)
        self.def_widg_sizer.addWidget(self.phonesLabel, n, 0)
        self.phonesChooser = QComboBox()
        self.phonesChooser.addItems(self.prm['phones']['phonesChoices'])
        self.phonesChooser.setCurrentIndex(self.prm['phones']['defaultPhones'].index("\u2713"))
        self.phonesChooser.setWhatsThis(self.tr("Choose the phones used in the current session. This calibrates sound levels if the phones have been registered in the phones database (see manual)."))
        self.def_widg_sizer.addWidget(self.phonesChooser, n, 1)
        #SAMPLING RATE
        n = n+1
        self.sampRateLabel = QLabel(self.tr("Sample Rate (Hz):"), self)
        self.def_widg_sizer.addWidget(self.sampRateLabel, n, 0)
        self.sampRateTF = QLineEdit()
        self.sampRateTF.setText(self.prm["pref"]["sound"]["defaultSampleRate"])
        self.sampRateTF.setValidator(QIntValidator(self))
        self.sampRateTF.setWhatsThis(self.tr("Set the sample rate for the current session. Sample rate chosen must be supported by your soundcard"))
        self.def_widg_sizer.addWidget(self.sampRateTF, n, 1)
        self.prm['sampRate'] =  self.currLocale.toInt(self.sampRateTF.text())[0]
        self.sampRateTF.editingFinished.connect(self.audioManager.initializeAudio)
        #BITS
        n = n+1
        self.nBitsLabel = QLabel(self.tr("Bits:"))
        self.def_widg_sizer.addWidget(self.nBitsLabel, n, 0)
        self.nBitsChooser = QComboBox()
        self.nBitsChooser.addItems(self.prm["nBitsChoices"])
        self.nBitsChooser.setWhatsThis(self.tr("Choose the bit depth for the current session. The bit depth chosen must be supported by your soundcard and the playing method chosen in the sound preferences (see manual)"))
        self.nBitsChooser.setCurrentIndex(self.prm["nBitsChoices"].index(self.prm["pref"]["sound"]["defaultNBits"])) 
        self.def_widg_sizer.addWidget(self.nBitsChooser, n, 1)
        self.nBitsChooser.textActivated[str].connect(self.audioManager.initializeAudio)
        #self.def_widg_sizer.addItem(QSpacerItem(10,10,QSizePolicy.Expanding), 0, 2)
        #self.def_widg_sizer.addItem(QSpacerItem(10,10,QSizePolicy.Expanding), 0, 3)
        #REPETITIONS
        n = n+1
        self.repetitionsLabel = QLabel(self.tr("No. Repetitions:"), self)
        self.def_widg_sizer.addWidget(self.repetitionsLabel, n, 0)
        self.repetitionsTF = QLineEdit()
        self.repetitionsTF.setText('1')
        self.repetitionsTF.setValidator(QIntValidator(self))
        self.repetitionsTF.setWhatsThis(self.tr("Sets the number of times the series of blocks will be repeated."))
        self.def_widg_sizer.addWidget(self.repetitionsTF, n, 1)
        #PRE-TRIAL Silence
        n = n+1
        self.preTrialSilenceLabel = QLabel(self.tr("Pre-Trial Silence (ms):"), self)
        self.def_widg_sizer.addWidget(self.preTrialSilenceLabel, n, 0)
        self.preTrialSilenceTF = QLineEdit()
        self.preTrialSilenceTF.setText(self.prm["pref"]["general"]["preTrialSilence"])
        self.preTrialSilenceTF.setValidator(QIntValidator(self))
        self.preTrialSilenceTF.setWhatsThis(self.tr("Sets the duration of a silent pause between the moment the listener has given the response and the start of the next trial"))
        self.def_widg_sizer.addWidget(self.preTrialSilenceTF, n, 1)
        #Warning Interval
        n = n+1
        self.warningIntervalLabel =  QLabel(self.tr("Warning Interval:"), self)
        self.warningIntervalChooser = QComboBox()
        self.warningIntervalChooser.addItems([self.tr("Yes"), self.tr("No")])
        self.warningIntervalChooser.setCurrentIndex(self.warningIntervalChooser.findText(self.tr("No")))
        self.warningIntervalChooser.textActivated[str].connect(self.onWarningIntervalChange)
        self.warningIntervalChooser.setWhatsThis(self.tr("Should a warning interval be presented at the beginning of each trial?"))
        self.def_widg_sizer.addWidget(self.warningIntervalLabel, n, 0)
        self.def_widg_sizer.addWidget(self.warningIntervalChooser, n, 1)
        n = n+1
        self.warningIntervalDurLabel = QLabel(self.tr("Warning Interval Duration (ms):"), self)
        self.def_widg_sizer.addWidget(self.warningIntervalDurLabel, n, 0)
        self.warningIntervalDurLabel.hide()
        self.warningIntervalDurTF = QLineEdit()
        self.warningIntervalDurTF.setText("500")
        self.warningIntervalDurTF.setValidator(QIntValidator(self))
        self.warningIntervalDurTF.setWhatsThis(self.tr("Sets the duration of the warning interval light"))
        self.warningIntervalDurTF.hide()
        self.def_widg_sizer.addWidget(self.warningIntervalDurTF, n, 1)
        n = n+1
        self.warningIntervalISILabel = QLabel(self.tr("Warning Interval ISI (ms):"), self)
        self.def_widg_sizer.addWidget(self.warningIntervalISILabel, n, 0)
        self.warningIntervalISILabel.hide()
        self.warningIntervalISITF = QLineEdit()
        self.warningIntervalISITF.setText("500")
        self.warningIntervalISITF.setValidator(QIntValidator(self))
        self.warningIntervalISITF.setWhatsThis(self.tr("Sets the duration of the silent interval between the warning interval and the first observation interval"))
        self.warningIntervalISITF.hide()
        self.def_widg_sizer.addWidget(self.warningIntervalISITF, n, 1)
        #INTERVAL LIGHTS
        n = n+1
        self.intervalLightsLabel = QLabel(self.tr("Interval Lights:"))
        self.def_widg_sizer.addWidget(self.intervalLightsLabel, n, 0)
        self.intervalLightsChooser = QComboBox()
        self.intervalLightsChooser.addItems([self.tr("Yes"), self.tr("No")])
        self.intervalLightsChooser.setWhatsThis(self.tr("Should interval lights be shown in the response box for the current block?"))
        self.intervalLightsChooser.setCurrentIndex(self.intervalLightsChooser.findText(self.prm['intervalLights']))
        self.def_widg_sizer.addWidget(self.intervalLightsChooser, n, 1)
        self.intervalLightsChooser.textActivated[str].connect(self.onIntervalLightsChange)
        #RESULTS FILE
        n = n+1
        self.saveResultsLabel =  QLabel(self.tr("Results File:"), self)
        self.def_widg_sizer.addWidget(self.saveResultsLabel, n, 0)
        min_pw_butt_size = 22
        min_pw_icon_size = 20
        
        self.def_widg_sizer.setRowMinimumHeight(0, min_pw_butt_size)
        self.saveResultsButton = QPushButton(self.tr("Choose Results File"), self)
        self.saveResultsButton.clicked.connect(self.onClickSaveResultsButton)
        self.saveResultsButton.setIcon(QIcon.fromTheme("document-save", QIcon(":/document-save")))
        self.saveResultsButton.setIconSize(QtCore.QSize(min_pw_icon_size, min_pw_icon_size))
        self.saveResultsButton.setToolTip(self.tr("Choose file to save results"))
        self.saveResultsButton.setWhatsThis(self.tr("Choose where to save the result files"))
        self.def_widg_sizer.addWidget(self.saveResultsButton, n, 1, 1, 1)
        #Additional Widgets
        self.add_widg_sizer = QGridLayout()
        self.add_widg_sizer.addItem(QSpacerItem(10,10, QSizePolicy.Policy.Expanding), 0, 2)
        self.add_widg_sizer.addItem(QSpacerItem(10,10, QSizePolicy.Policy.Expanding), 0, 3)
        #self.setAdditionalWidgets(self.currExp, self.prevExp) later

        #def widgets 2
        self.def_widg_sizer2 = QGridLayout()
      
        # SHUFFLE MODE
        self.shuffleLabel = QLabel(self.tr("Shuffle Mode:"))
        self.def_widg_sizer2.addWidget(self.shuffleLabel, 1, 0)
        self.shuffleChooser = QComboBox()
        self.shuffleChooser.addItems(self.prm['shuffleChoices'])
        self.shuffleChooser.setCurrentIndex(self.prm['shuffleChoices'].index(QApplication.translate("",self.prm['pref']['general']['defaultShuffle'],"")))   
        self.def_widg_sizer2.addWidget(self.shuffleChooser, 1, 1)
        self.def_widg_sizer2.addItem(QSpacerItem(10, 10, QSizePolicy.Policy.Expanding), 0, 4)

        #ONOFF Trigger
        self.triggerCheckBox = QCheckBox(self.tr('EEG ON/OFF Trigger'))
        self.def_widg_sizer2.addWidget(self.triggerCheckBox, 1, 2)

        #RESPONSE MODE
        self.responseModeLabel = QLabel(self.tr("Response Mode:"))
        self.def_widg_sizer2.addWidget(self.responseModeLabel, 2, 0)
        self.responseModeChooser = QComboBox()
        self.responseModeChooser.addItems(self.prm['responseModeChoices'])
        self.responseModeChooser.setCurrentIndex(self.prm['responseModeChoices'].index(QApplication.translate("",self.prm['pref']['general']['defaultResponseMode'],"")))
        self.responseModeChooser.textActivated[str].connect(self.onResponseModeChange)
        self.def_widg_sizer2.addWidget(self.responseModeChooser, 2, 1)
        
        #AUTO Percent Correct
        self.autoPCorrLabel = QLabel(self.tr("Percent Correct (%):"), self)
        self.def_widg_sizer2.addWidget(self.autoPCorrLabel, 2, 2)
        self.autoPCorrTF = QLineEdit()
        self.autoPCorrTF.setText('75')
        self.autoPCorrTF.setValidator(QDoubleValidator(0, 100, 6, self))
        self.def_widg_sizer2.addWidget(self.autoPCorrTF, 2, 3)
        self.autoPCorrLabel.hide()
        self.autoPCorrTF.hide()

        self.psyListSaveButton = QPushButton(self.tr("Save psychometric listener data"), self)
        self.psyListSaveButton.clicked.connect(self.onClickPsyListSaveButton)
        self.psyListSaveButton.setIcon(QIcon.fromTheme("document-save", QIcon(":/document-save")))
        self.psyListSaveButton.setIconSize(QtCore.QSize(min_pw_icon_size, min_pw_icon_size))
        self.psyListSaveButton.setToolTip(self.tr("Choose file to save results"))
        self.def_widg_sizer2.addWidget(self.psyListSaveButton, 2, 2)
        self.psyListSaveButton.hide()

        self.psyListPlotButton = QPushButton(self.tr("Plot psychometric listener function"), self)
        self.psyListPlotButton.clicked.connect(self.onClickPsyListPlotButton)
        self.psyListPlotButton.setIcon(QIcon.fromTheme("office-chart-line-stacked", QIcon(":/office-chart-line_stacked")))
        self.psyListPlotButton.setIconSize(QtCore.QSize(min_pw_icon_size, min_pw_icon_size))
        self.psyListPlotButton.setToolTip(self.tr("Plot psychometric listener function"))
        self.def_widg_sizer2.addWidget(self.psyListPlotButton, 2, 3)
        self.psyListPlotButton.hide()

        #For psychometric listener
        n = 2+1
        self.psyListFunChooserLabel = QLabel(self.tr("Psychometric Listener Function:"))
        self.def_widg_sizer2.addWidget(self.psyListFunChooserLabel, n, 0)
        self.psyListFunChooser = QComboBox()
        self.psyListFunChooser.addItems(self.prm['psyListFunChoices'])
        #self.psyListFunChooser.setCurrentIndex(self.prm['psyListFunChoices'].index(QApplication.translate("",self.prm['pref']['general']['defaultResponseMode'],"")))
        #self.psyListFunChooser.textActivated[str].connect(self.onResponseModeChange)
        self.def_widg_sizer2.addWidget(self.psyListFunChooser, n, 1)
        self.psyListFunChooserLabel.hide()
        self.psyListFunChooser.hide()
        #n = n+1
        self.psyListFunFitChooserLabel = QLabel(self.tr("Psychometric Listener Function Fit:"))
        self.def_widg_sizer2.addWidget(self.psyListFunFitChooserLabel, n, 2)
        self.psyListFunFitChooser = QComboBox()
        self.psyListFunFitChooser.addItems(["Linear", "Logarithmic"])
        self.def_widg_sizer2.addWidget(self.psyListFunFitChooser, n, 3)
        self.psyListFunFitChooserLabel.hide()
        self.psyListFunFitChooser.hide()
        n = n+1
        self.psyListMidpointLabel = QLabel(self.tr("Psychometric Listener Midpoint:"), self)
        self.def_widg_sizer2.addWidget(self.psyListMidpointLabel, n, 0)
        self.psyListMidpoint = QLineEdit()
        self.psyListMidpoint.setText('0')
        self.psyListMidpoint.setValidator(QDoubleValidator(self))
        self.def_widg_sizer2.addWidget(self.psyListMidpoint, n, 1)
        self.psyListMidpointLabel.hide()
        self.psyListMidpoint.hide()
        
        self.psyListSlopeLabel = QLabel(self.tr("Psychometric Listener Slope:"), self)
        self.def_widg_sizer2.addWidget(self.psyListSlopeLabel, n, 2)
        self.psyListSlope = QLineEdit()
        self.psyListSlope.setText('1')
        self.psyListSlope.setValidator(QDoubleValidator(self))
        self.def_widg_sizer2.addWidget(self.psyListSlope, n, 3)
        self.psyListSlopeLabel.hide()
        self.psyListSlope.hide()
        n = n+1
        self.psyListLapseLabel = QLabel(self.tr("Psychometric Listener Lapse:"), self)
        self.def_widg_sizer2.addWidget(self.psyListLapseLabel, n, 0)
        self.psyListLapse = QLineEdit()
        self.psyListLapse.setText('0')
        self.psyListLapse.setValidator(QDoubleValidator(self))
        self.def_widg_sizer2.addWidget(self.psyListLapse, n, 1)
        self.psyListLapseLabel.hide()
        self.psyListLapse.hide()

  
        
        #PARADIGM WIDGETS SIZER
        self.paradigm_widg_sizer = QGridLayout()


        #PARAMETERS WINDOW
        self.pw_sizer = QVBoxLayout()
        self.pw_buttons_sizer = QGridLayout()
        min_pw_butt_size = 22
        min_pw_icon_size = 20
        self.pw_buttons_sizer.setRowMinimumHeight(0, min_pw_butt_size)
        self.pw_buttons_sizer.setRowMinimumHeight(1, min_pw_butt_size)
        self.pw_buttons_sizer.setRowMinimumHeight(2, min_pw_butt_size)
    
        #---- FIRST ROW
        n = 0
        #LOAD PARAMETERS BUTTON
        self.loadParametersButton = QPushButton(self.tr("Load Prm"), self)
        self.loadParametersButton.setIcon(QIcon.fromTheme("document-open", QIcon(":/document-open")))
        self.loadParametersButton.setIconSize(QtCore.QSize(min_pw_icon_size, min_pw_icon_size))
        self.loadParametersButton.clicked.connect(self.onClickLoadParametersButton)
        self.loadParametersButton.setToolTip(self.tr("Load a parameters file"))
        self.loadParametersButton.setWhatsThis(self.tr("Load a file containing the parameters for an experimental session"))
        self.loadParametersButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.pw_buttons_sizer.addWidget(self.loadParametersButton, n, 0)

        #SAVE PARAMETERS BUTTON
        self.saveParametersButton = QPushButton(self.tr("Save Prm"), self)
        self.saveParametersButton.setIcon(QIcon.fromTheme("document-save", QIcon(":/document-save")))
        self.saveParametersButton.setIconSize(QtCore.QSize(min_pw_icon_size, min_pw_icon_size))
        self.saveParametersButton.clicked.connect(self.onClickSaveParametersButton)
        self.saveParametersButton.setToolTip(self.tr("Save a parameters file"))
        self.saveParametersButton.setWhatsThis(self.tr("Save the current experimental parameters to a file"))
        self.saveParametersButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.pw_buttons_sizer.addWidget(self.saveParametersButton, n, 1)

        #DELETE PARAMETERS BUTTON
        self.deleteParametersButton = QPushButton(self.tr("Delete"), self)
        self.deleteParametersButton.clicked.connect(self.onClickDeleteParametersButton)
        self.deleteParametersButton.setIcon(QIcon.fromTheme("edit-delete", QIcon(":/edit-delete")))
        self.deleteParametersButton.setIconSize(QtCore.QSize(min_pw_icon_size, min_pw_icon_size))
        self.deleteParametersButton.setToolTip(self.tr("Delete current block"))
        self.deleteParametersButton.setWhatsThis(self.tr("Delete the current block of trials."))
        self.deleteParametersButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.pw_buttons_sizer.addWidget(self.deleteParametersButton, n, 2)

     
        self.undoUnsavedButton = QPushButton(self.tr("Undo Unsaved"), self)
        self.undoUnsavedButton.clicked.connect(self.onClickUndoUnsavedButton)
        self.undoUnsavedButton.setIcon(QIcon.fromTheme("edit-undo", QIcon(":/edit-undo")))
        self.undoUnsavedButton.setIconSize(QtCore.QSize(min_pw_icon_size, min_pw_icon_size))
        self.undoUnsavedButton.setToolTip(self.tr("Undo unsaved changes"))
        self.undoUnsavedButton.setWhatsThis(self.tr("Undo changes in the current block that have not yet been stored in memory."))
        self.undoUnsavedButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.pw_buttons_sizer.addWidget(self.undoUnsavedButton, n, 3)

        #---- SECOND ROW
        n = n+1
        self.storeParametersButton = QPushButton(self.tr("Store"), self)
        self.storeParametersButton.clicked.connect(self.onClickStoreParametersButton)
        self.storeParametersButton.setIcon(QIcon.fromTheme("media-flash-memory-stick", QIcon(":/media-flash-memory-stick")))
        self.storeParametersButton.setIconSize(QtCore.QSize(min_pw_icon_size, min_pw_icon_size))
        self.storeParametersButton.setToolTip(self.tr("Store parameters in memory"))
        self.storeParametersButton.setWhatsThis(self.tr("Store parameters in memory."))
        self.storeParametersButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.pw_buttons_sizer.addWidget(self.storeParametersButton, n, 0)

        self.storeandaddParametersButton = QPushButton(self.tr("Store 'n' add!"), self)
        self.storeandaddParametersButton.clicked.connect(self.onClickStoreandaddParametersButton)
        self.storeandaddParametersButton.setToolTip(self.tr("Store parameters in memory and add a new block"))
        self.storeandaddParametersButton.setWhatsThis(self.tr("Store parameters in memory and add a new block."))
        self.storeandaddParametersButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.pw_buttons_sizer.addWidget(self.storeandaddParametersButton, n, 1)
        
        self.storeandgoParametersButton = QPushButton(self.tr("Store 'n' go!"), self)
        self.storeandgoParametersButton.clicked.connect(self.onClickStoreandgoParametersButton)
        self.storeandgoParametersButton.setToolTip(self.tr("Store parameters and go to the next block"))
        self.storeandgoParametersButton.setWhatsThis(self.tr("Store parameters and go to the next block"))
        self.storeandgoParametersButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.pw_buttons_sizer.addWidget(self.storeandgoParametersButton, n, 2)

        self.newBlockButton = QPushButton(self.tr("New Block"), self)
        self.newBlockButton.clicked.connect(self.onClickNewBlockButton)
        self.newBlockButton.setIcon(QIcon.fromTheme("document-new", QIcon(":/document-new")))
        self.newBlockButton.setIconSize(QtCore.QSize(min_pw_icon_size, min_pw_icon_size))
        self.newBlockButton.setToolTip(self.tr("Append a new block"))
        self.newBlockButton.setWhatsThis(self.tr("Append a new block."))
        self.newBlockButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.pw_buttons_sizer.addWidget(self.newBlockButton, n, 3)

      
      

        #---- THIRD ROW
        n = n+1
        self.prevBlockButton = QPushButton(self.tr("Previous"), self)
        self.prevBlockButton.clicked.connect(self.onClickPrevBlockButton)
        self.prevBlockButton.setIcon(QIcon.fromTheme("go-previous", QIcon(":/go-previous")))
        self.prevBlockButton.setIconSize(QtCore.QSize(min_pw_icon_size, min_pw_icon_size))
        self.prevBlockButton.setToolTip(self.tr("Move to previous block"))
        self.prevBlockButton.setWhatsThis(self.tr("Move to previous block."))
        self.prevBlockButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.pw_buttons_sizer.addWidget(self.prevBlockButton, n, 0)

        self.nextBlockButton = QPushButton(self.tr("Next"), self)
        self.nextBlockButton.clicked.connect(self.onClickNextBlockButton)
        self.nextBlockButton.setIcon(QIcon.fromTheme("go-next", QIcon(":/go-next")))
        self.nextBlockButton.setIconSize(QtCore.QSize(min_pw_icon_size, min_pw_icon_size))
        self.nextBlockButton.setToolTip(self.tr("Move to next block"))
        self.nextBlockButton.setWhatsThis(self.tr("Move to next block."))
        self.nextBlockButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.pw_buttons_sizer.addWidget(self.nextBlockButton, n, 1)

        self.shuffleBlocksButton = QPushButton(self.tr("Shuffle"), self)
        self.shuffleBlocksButton.clicked.connect(self.onClickShuffleBlocksButton)
        self.shuffleBlocksButton.setIcon(QIcon.fromTheme("media-playlist-shuffle", QIcon(":/media-playlist-shuffle")))
        self.shuffleBlocksButton.setIconSize(QtCore.QSize(min_pw_icon_size, min_pw_icon_size))
        self.shuffleBlocksButton.setToolTip(self.tr("Shuffle blocks"))
        self.shuffleBlocksButton.setWhatsThis(self.tr("Shuffle the blocks."))
        self.shuffleBlocksButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.pw_buttons_sizer.addWidget(self.shuffleBlocksButton, n, 2)

        self.resetParametersButton = QPushButton(self.tr("Reset"), self)
        self.resetParametersButton.clicked.connect(self.onClickResetParametersButton)
        self.resetParametersButton.setIcon(QIcon.fromTheme("go-home", QIcon(":/go-home")))
        self.resetParametersButton.setIconSize(QtCore.QSize(min_pw_icon_size, min_pw_icon_size))
        self.resetParametersButton.setToolTip(self.tr("Reset parameters"))
        self.resetParametersButton.setWhatsThis(self.tr("Reset the parameters."))
        self.resetParametersButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.pw_buttons_sizer.addWidget(self.resetParametersButton, n, 3)
        n = n+1
        self.pw_buttons_sizer.addItem(QSpacerItem(10,10,QSizePolicy.Policy.Expanding), n, 0, 1, 4)


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
        self.jumpToBlockChooser.textActivated[str].connect(self.onJumpToBlockChange)
        self.jumpToBlockChooser.setToolTip(self.tr("Jump to a given block"))
        self.jumpToBlockChooser.setWhatsThis(self.tr("Jump to a given block."))
        self.pw_buttons_sizer.addWidget(self.jumpToBlockLabel, n, 2)
        self.pw_buttons_sizer.addWidget(self.jumpToBlockChooser, n, 3)
        # SIXTH ROW
        n = n+1
        self.prevBlockPositionButton = QPushButton(self.tr("Previous Position"), self)
        self.prevBlockPositionButton.clicked.connect(self.onClickPrevBlockPositionButton)
        self.prevBlockPositionButton.setIcon(QIcon.fromTheme("go-previous", QIcon(":/go-previous")))
        self.prevBlockPositionButton.setToolTip(self.tr("Move to previous block position"))
        self.prevBlockPositionButton.setWhatsThis(self.tr("Move to previous block position."))
        self.pw_buttons_sizer.addWidget(self.prevBlockPositionButton, n, 0)

        self.nextBlockPositionButton = QPushButton(self.tr("Next Position"), self)
        self.nextBlockPositionButton.clicked.connect(self.onClickNextBlockPositionButton)
        self.nextBlockPositionButton.setIcon(QIcon.fromTheme("go-next", QIcon(":/go-next")))
        self.nextBlockPositionButton.setToolTip(self.tr("Move to next block position"))
        self.nextBlockPositionButton.setWhatsThis(self.tr("Move to next block position."))
        self.pw_buttons_sizer.addWidget(self.nextBlockPositionButton, n, 1)

        self.jumpToPositionLabel = QLabel(self.tr("Jump to Position:"))
        self.jumpToPositionChooser = QComboBox()
        self.jumpToPositionChooser.textActivated[str].connect(self.onJumpToPositionChange)
        self.jumpToPositionChooser.setToolTip(self.tr("Jump to a given block position."))
        self.jumpToPositionChooser.setWhatsThis(self.tr("Jump to a given block position."))
        self.pw_buttons_sizer.addWidget(self.jumpToPositionLabel, n, 2)
        self.pw_buttons_sizer.addWidget(self.jumpToPositionChooser, n, 3)

        # SEVENTH ROW
        n = n+1

        self.showExpDocButton = QPushButton(self.tr("Experiment Doc"), self)
        self.showExpDocButton.setIcon(QIcon.fromTheme("help-contents", QIcon(":/help-contents")))
        self.showExpDocButton.clicked.connect(self.onClickShowExpDocButton)
        self.showExpDocButton.setToolTip(self.tr("Show doc for current experiment"))
        self.showExpDocButton.setWhatsThis(self.tr("Show the documentation for the current experiment."))
        self.pw_buttons_sizer.addWidget(self.showExpDocButton, n, 0)

        self.shiftBlockDownButton = QPushButton(self.tr("< Shift Blk. Down"), self)
        self.shiftBlockDownButton.clicked.connect(self.onClickShiftBlockDownButton)
        self.shiftBlockDownButton.setToolTip(self.tr("Shift Block Down"))
        self.shiftBlockDownButton.setWhatsThis(self.tr("Shift block down."))
        self.pw_buttons_sizer.addWidget(self.shiftBlockDownButton, n, 2)

        self.shiftBlockUpButton = QPushButton(self.tr("Shift Blk. Up >"), self)
        self.shiftBlockUpButton.clicked.connect(self.onClickShiftBlockUpButton)
        self.shiftBlockUpButton.setToolTip(self.tr("Shift Block Up"))
        self.shiftBlockUpButton.setWhatsThis(self.tr("Shift block up."))
        self.pw_buttons_sizer.addWidget(self.shiftBlockUpButton, n, 3)
        
        
        n = n+1
        #spacer
        self.pw_buttons_sizer.addItem(QSpacerItem(10,10,QSizePolicy.Policy.Expanding), n, 5)

        #PARAMETERS AREA
        self.pw_prm_sizer = QHBoxLayout()
        self.pw_prm_sizer_0 = QGridLayout()
        self.pw_prm_sizer_1 = QGridLayout()
        #self.pw_prm_sizer_0.setVerticalSpacing(-20)
        #self.pw_prm_sizer_1.setVerticalSpacing(-20)
        self.pw_prm_sizer_0.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.pw_prm_sizer_1.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.cw_sizer.addLayout(self.def_widg_sizer)
        self.cw_sizer.addLayout(self.add_widg_sizer)
        self.cw_sizer.addLayout(self.def_widg_sizer2)
        self.cw_sizer.addLayout(self.paradigm_widg_sizer)
        self.cw.setLayout(self.cw_sizer)

        #self.pw.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.setDefaultParameters(self.tr("Audiogram"), self.tr("Transformed Up-Down"), self.par)
        self.cw_scrollarea = QScrollArea()
        self.cw_scrollarea.setWidget(self.cw)
        self.splitter.addWidget(self.cw_scrollarea)
        self.pw_sizer.addLayout(self.pw_buttons_sizer)
        self.pw_sizer.addSpacing(20)
        self.pw_prm_sizer.addLayout(self.pw_prm_sizer_0)
        self.pw_prm_sizer.addLayout(self.pw_prm_sizer_1)
        self.pw_sizer.addLayout(self.pw_prm_sizer)
        self.pw.setLayout(self.pw_sizer)
        self.pw.layout().setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.cw.layout().setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.pw_scrollarea = QScrollArea()
        self.pw_scrollarea.setWidget(self.pw)
        self.splitter.addWidget(self.pw_scrollarea)
        self.splitter.setSizes([int((2/6)*screen.width()), int((2/6)*screen.width())])
        #self.splitter.setStretchFactor(1, 1.5)
        #self.splitter.setStretchFactor(2, 1.5)
        self.setCentralWidget(self.splitter)
        
        if self.prm['startMinimized'] == True:
            self.showMinimized()
        else:
            self.show()

        self.responseBox = responseBox(self)
        self.responseBox.resize(int((1/4)*screen.width()), int((1.1/3)*screen.height()))
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
                #self.additionalWidgetsIntFieldLabelList[i].setParent(None)
                self.additionalWidgetsIntFieldLabelList[i].deleteLater()
                self.add_widg_sizer.removeWidget(self.additionalWidgetsIntFieldList[i])
                #self.additionalWidgetsIntFieldList[i].setParent(None)
                self.additionalWidgetsIntFieldList[i].deleteLater()
                self.add_widg_sizer.removeWidget(self.additionalWidgetsIntFieldCheckBoxList[i])
                #self.additionalWidgetsIntFieldCheckBoxList[i].setParent(None)
                self.additionalWidgetsIntFieldCheckBoxList[i].deleteLater()
            for i in range(len(self.additionalWidgetsChooserList)):
                self.add_widg_sizer.removeWidget(self.additionalWidgetsChooserLabelList[i])
                #self.additionalWidgetsChooserLabelList[i].setParent(None)
                self.additionalWidgetsChooserLabelList[i].deleteLater()
                self.add_widg_sizer.removeWidget(self.additionalWidgetsChooserList[i])
                #self.additionalWidgetsChooserList[i].setParent(None)
                self.additionalWidgetsChooserList[i].deleteLater()
                self.add_widg_sizer.removeWidget(self.additionalWidgetsChooserCheckBoxList[i])
                #self.additionalWidgetsChooserCheckBoxList[i].setParent(None)
                self.additionalWidgetsChooserCheckBoxList[i].deleteLater()


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
            self.ISIBox.setValidator(QIntValidator(self))
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
            self.nIntervalsChooser.textActivated[str].connect(self.onNIntervalsChange)
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
            self.nAlternativesChooser.textActivated[str].connect(self.onNAlternativesChange)
            self.nAlternativesCheckBox = QCheckBox()
            self.add_widg_sizer.addWidget(self.nAlternativesCheckBox, n, 0)
            self.additionalWidgetsChooserList.append(self.nAlternativesChooser)
            self.additionalWidgetsChooserLabelList.append(self.nAlternativesLabel)
            self.additionalWidgetsChooserCheckBoxList.append(self.nAlternativesCheckBox)
            n = n+1
        if self.prm[self.currExp]["hasAltReps"] == True:
            self.altRepsLabel = QLabel(self.tr("Alternated (AB) Reps.:"), self)
            self.add_widg_sizer.addWidget(self.altRepsLabel, n, 1)
            self.altRepsBox = QLineEdit()
            self.altRepsBox.setText('0')
            self.altRepsBox.setValidator(QIntValidator(self))
            self.add_widg_sizer.addWidget(self.altRepsBox, n, 2)
            self.altRepsBoxCheckBox = QCheckBox()
            self.add_widg_sizer.addWidget(self.altRepsBoxCheckBox, n, 0)
            self.additionalWidgetsIntFieldList.append(self.altRepsBox)
            self.additionalWidgetsIntFieldLabelList.append(self.altRepsLabel)
            self.additionalWidgetsIntFieldCheckBoxList.append(self.altRepsBoxCheckBox)
            n = n+1
            self.altRepsISILabel = QLabel(self.tr("Alternated (AB) Reps. ISI (ms):"), self)
            self.add_widg_sizer.addWidget(self.altRepsISILabel, n, 1)
            self.altRepsISIBox = QLineEdit()
            self.altRepsISIBox.setText('0')
            self.altRepsISIBox.setValidator(QIntValidator(self))
            self.add_widg_sizer.addWidget(self.altRepsISIBox, n, 2)
            self.altRepsISIBoxCheckBox = QCheckBox()
            self.add_widg_sizer.addWidget(self.altRepsISIBoxCheckBox, n, 0)
            self.additionalWidgetsIntFieldList.append(self.altRepsISIBox)
            self.additionalWidgetsIntFieldLabelList.append(self.altRepsISILabel)
            self.additionalWidgetsIntFieldCheckBoxList.append(self.altRepsISIBoxCheckBox)
            n = n+1

        #Pre-Trial Interval
        if self.prm[self.currExp]["hasPreTrialInterval"] == True:
            self.preTrialIntervalChooserLabel = QLabel(self.tr("Pre-Trial Interval:"), self)
            self.add_widg_sizer.addWidget(self.preTrialIntervalChooserLabel, n, 1)
            self.preTrialIntervalChooser = QComboBox()
            self.preTrialIntervalChooser.addItems([self.tr("Yes"), self.tr("No")])
            self.preTrialIntervalChooser.setCurrentIndex(1)
            self.preTrialIntervalChooser.textActivated[str].connect(self.onPreTrialIntervalChange)
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
            self.preTrialIntervalISITF.setValidator(QIntValidator(self))
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
            self.precursorIntervalChooser.textActivated[str].connect(self.onPrecursorIntervalChange)
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
            self.precursorIntervalISITF.setValidator(QIntValidator(self))
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
            self.postcursorIntervalChooser.textActivated[str].connect(self.onPostcursorIntervalChange)
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
            self.postcursorIntervalISITF.setValidator(QIntValidator(self))
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

            self.responseLightTypeLabel =  QLabel(self.tr("Response Light Type:"), self)
            self.responseLightTypeChooser = QComboBox()
            self.responseLightTypeChooser.addItems([self.tr("Light"), self.tr("Text"),
                                                    self.tr("Smiley"), self.tr("Light & Text"),
                                                    self.tr("Light & Smiley"), self.tr("Text & Smiley"),
                                                    self.tr("Light & Text & Smiley")])
            self.add_widg_sizer.addWidget(self.responseLightTypeLabel, n, 1)
            self.add_widg_sizer.addWidget(self.responseLightTypeChooser, n, 2)
            self.responseLightTypeCheckBox = QCheckBox()
            self.add_widg_sizer.addWidget(self.responseLightTypeCheckBox, n, 0)
            self.additionalWidgetsChooserList.append(self.responseLightTypeChooser)
            self.additionalWidgetsChooserLabelList.append(self.responseLightTypeLabel)
            self.additionalWidgetsChooserCheckBoxList.append(self.responseLightTypeCheckBox)
            
            n = n+1
            self.responseLightDurationLabel = QLabel(self.tr("Response Light Duration (ms):"), self)
            self.add_widg_sizer.addWidget(self.responseLightDurationLabel, n, 1)
            self.responseLightDurationTF = QLineEdit()
            self.responseLightDurationTF.setText(self.prm["pref"]["general"]["responseLightDuration"])
            self.responseLightDurationTF.setValidator(QIntValidator(self))

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
            self.responseLightTypeLabel =  QLabel(self.tr("Response Light Type:"), self)
            self.responseLightTypeChooser = QComboBox()
            self.responseLightTypeChooser.addItems([self.tr("Light"), self.tr("Text"),
                                                    self.tr("Smiley"), self.tr("Light & Text"),
                                                    self.tr("Light & Smiley"), self.tr("Text & Smiley"),
                                                    self.tr("Light & Text & Smiley")])
            self.add_widg_sizer.addWidget(self.responseLightTypeLabel, n, 1)
            self.add_widg_sizer.addWidget(self.responseLightTypeChooser, n, 2)
            self.responseLightTypeCheckBox = QCheckBox()
            self.add_widg_sizer.addWidget(self.responseLightTypeCheckBox, n, 0)
            self.additionalWidgetsChooserList.append(self.responseLightTypeChooser)
            self.additionalWidgetsChooserLabelList.append(self.responseLightTypeLabel)
            self.additionalWidgetsChooserCheckBoxList.append(self.responseLightTypeCheckBox)
            n = n+1
            self.responseLightDurationLabel = QLabel(self.tr("Response Light Duration (ms):"), self)
            self.add_widg_sizer.addWidget(self.responseLightDurationLabel, n, 1)
            self.responseLightDurationTF = QLineEdit()
            self.responseLightDurationTF.setText(self.prm["pref"]["general"]["responseLightDuration"])
            self.responseLightDurationTF.setValidator(QIntValidator(self))
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
                #self.paradigmChooserList[i].setParent(None)
                self.paradigmChooserList[i].deleteLater()
                self.paradigm_widg_sizer.removeWidget(self.paradigmChooserLabelList[i])
                #self.paradigmChooserLabelList[i].setParent(None)
                self.paradigmChooserLabelList[i].deleteLater()
                self.paradigm_widg_sizer.removeWidget(self.paradigmChooserCheckBoxList[i])
                #self.paradigmChooserCheckBoxList[i].setParent(None)
                self.paradigmChooserCheckBoxList[i].deleteLater()
            for i in range(len(self.paradigmFieldList)):
                self.paradigm_widg_sizer.removeWidget(self.paradigmFieldList[i])
                #self.paradigmFieldList[i].setParent(None)
                self.paradigmFieldList[i].deleteLater()
                self.paradigm_widg_sizer.removeWidget(self.paradigmFieldLabelList[i])
                #self.paradigmFieldLabelList[i].setParent(None)
                self.paradigmFieldLabelList[i].deleteLater()
                self.paradigm_widg_sizer.removeWidget(self.paradigmFieldCheckBoxList[i])
                #self.paradigmFieldCheckBoxList[i].setParent(None)
                self.paradigmFieldCheckBoxList[i].deleteLater()
            if prevParadigm in ["UML", "PSI", "UML - Est. Guess Rate", "PSI - Est. Guess Rate"]:
                for i in range(len(self.paradigmButtonList)):
                    self.paradigm_widg_sizer.removeWidget(self.paradigmButtonList[i])
                    #self.paradigmButtonList[i].setParent(None)
                    self.paradigmButtonList[i].deleteLater()

         
        #------------------------------------
        #TRANSFORMED UP-DOWN PARADIGM WIDGETS
        if self.currParadigm in [self.tr("Transformed Up-Down"), self.tr("Transformed Up-Down Limited")]:
            n = 0
            self.adaptiveTypeChooserLabel = QLabel(self.tr("Procedure:"), self)
            self.paradigm_widg_sizer.addWidget(self.adaptiveTypeChooserLabel, n, 1)
            self.adaptiveTypeChooser = QComboBox()
            self.adaptiveTypeChooser.addItems(self.prm["adaptiveTypeChoices"])
            try:
                self.adaptiveTypeChooser.setCurrentIndex(self.prm["adaptiveTypeChoices"].index(self.prm[self.currExp]['defaultAdaptiveType']))
            except:
                self.adaptiveTypeChooser.setCurrentIndex(0)
            self.paradigm_widg_sizer.addWidget(self.adaptiveTypeChooser, n, 2)
            self.adaptiveTypeCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.adaptiveTypeCheckBox, n, 0)

            n = n+1
            self.corrTrackDirChooserLabel = QLabel(self.tr("Corr. Resp. Move Track:"), self)
            self.paradigm_widg_sizer.addWidget(self.corrTrackDirChooserLabel, n, 1)
            self.corrTrackDirChooser = QComboBox()
            self.corrTrackDirChooser.addItems([self.tr("Up"), self.tr("Down")])
            self.corrTrackDirChooser.setCurrentIndex(1)
            self.paradigm_widg_sizer.addWidget(self.corrTrackDirChooser, n, 2)
            self.corrTrackDirCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.corrTrackDirCheckBox, n, 0)

            n = n+1
            self.ruleDownLabel = QLabel(self.tr("Rule Down"), self)
            self.paradigm_widg_sizer.addWidget(self.ruleDownLabel, n, 1)
            self.ruleDownTF = QLineEdit()
            self.ruleDownTF.setText('2')
            self.ruleDownTF.setValidator(QIntValidator(self))
            self.paradigm_widg_sizer.addWidget(self.ruleDownTF, n, 2)
            self.ruleDownCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.ruleDownCheckBox, n, 0)

            self.ruleUpLabel = QLabel(self.tr("Rule Up"), self)
            self.paradigm_widg_sizer.addWidget(self.ruleUpLabel, n, 4)
            self.ruleUpTF = QLineEdit()
            self.ruleUpTF.setText('1')
            self.ruleUpTF.setValidator(QIntValidator(self))
            self.paradigm_widg_sizer.addWidget(self.ruleUpTF, n, 5)
            self.ruleUpCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.ruleUpCheckBox, n, 3)
            n = n+1
            self.initialTurnpointsLabel = QLabel(self.tr("Initial Turnpoints"), self)
            self.paradigm_widg_sizer.addWidget(self.initialTurnpointsLabel, n, 1)
            self.initialTurnpointsTF = QLineEdit()
            self.initialTurnpointsTF.setText('4')
            self.initialTurnpointsTF.setValidator(QIntValidator(self))
            self.paradigm_widg_sizer.addWidget(self.initialTurnpointsTF, n, 2)
            self.initialTurnpointsCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.initialTurnpointsCheckBox, n, 0)

            self.totalTurnpointsLabel = QLabel(self.tr("Total Turnpoints"), self)
            self.paradigm_widg_sizer.addWidget(self.totalTurnpointsLabel, n, 4)
            self.totalTurnpointsTF = QLineEdit()
            self.totalTurnpointsTF.setText('16')
            self.totalTurnpointsTF.setValidator(QIntValidator(self))
            self.paradigm_widg_sizer.addWidget(self.totalTurnpointsTF, n, 5)
            self.totalTurnpointsCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.totalTurnpointsCheckBox, n, 3)
            n = n+1
            self.stepSize1Label = QLabel(self.tr("Step Size 1"), self)
            self.paradigm_widg_sizer.addWidget(self.stepSize1Label, n, 1)
            self.stepSize1TF = QLineEdit()
            self.stepSize1TF.setText('4')
            self.stepSize1TF.setValidator(QDoubleValidator(self))
            self.stepSize1TF.setWhatsThis(self.tr("Step size for the initial turnpoints"))
            self.paradigm_widg_sizer.addWidget(self.stepSize1TF, n, 2)
            self.stepSize1CheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.stepSize1CheckBox, n, 0)

            self.stepSize2Label = QLabel(self.tr("Step Size 2"), self)
            self.paradigm_widg_sizer.addWidget(self.stepSize2Label, n, 4)
            self.stepSize2TF = QLineEdit()
            self.stepSize2TF.setText('2')
            self.stepSize2TF.setValidator(QDoubleValidator(self))
            self.stepSize2TF.setWhatsThis(self.tr("Step size for the final turnpoints"))
            self.paradigm_widg_sizer.addWidget(self.stepSize2TF, n, 5)
            self.stepSize2CheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.stepSize2CheckBox, n, 3)

            self.paradigmChooserList = [self.adaptiveTypeChooser, self.corrTrackDirChooser]
            self.paradigmChooserLabelList = [self.adaptiveTypeChooserLabel, self.corrTrackDirChooserLabel]
            self.paradigmChooserOptionsList = [self.prm["adaptiveTypeChoices"], [self.tr("Up"), self.tr("Down")]]
            self.paradigmChooserCheckBoxList = [self.adaptiveTypeCheckBox, self.corrTrackDirCheckBox]

            self.paradigmFieldList = [self.ruleDownTF, self.ruleUpTF, self.initialTurnpointsTF, self.totalTurnpointsTF, self.stepSize1TF, self.stepSize2TF]
            self.paradigmFieldLabelList = [self.ruleDownLabel, self.ruleUpLabel, self.initialTurnpointsLabel, self.totalTurnpointsLabel, self.stepSize1Label, self.stepSize2Label]
            self.paradigmFieldCheckBoxList = [self.ruleDownCheckBox, self.ruleUpCheckBox, self.initialTurnpointsCheckBox, self.totalTurnpointsCheckBox, self.stepSize1CheckBox, self.stepSize2CheckBox]

        #------------------------------------
        #WEIGHTED UP/DOWN PARADIGM WIDGETS
        if self.currParadigm in [self.tr("Weighted Up-Down"), self.tr("Weighted Up-Down Limited")]:
            n = 0
            self.adaptiveTypeChooserLabel = QLabel(self.tr("Procedure:"), self)
            self.paradigm_widg_sizer.addWidget(self.adaptiveTypeChooserLabel, n, 1)
            self.adaptiveTypeChooser = QComboBox()
            self.adaptiveTypeChooser.addItems(self.prm["adaptiveTypeChoices"])
            try:
                self.adaptiveTypeChooser.setCurrentIndex(self.prm["adaptiveTypeChoices"].index(self.prm[self.currExp]['defaultAdaptiveType']))
            except:
                self.adaptiveTypeChooser.setCurrentIndex(0)
            self.paradigm_widg_sizer.addWidget(self.adaptiveTypeChooser, n, 2)
            self.adaptiveTypeCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.adaptiveTypeCheckBox, n, 0)

            n = n+1
            self.corrTrackDirChooserLabel = QLabel(self.tr("Corr. Resp. Move Track:"), self)
            self.paradigm_widg_sizer.addWidget(self.corrTrackDirChooserLabel, n, 1)
            self.corrTrackDirChooser = QComboBox()
            self.corrTrackDirChooser.addItems([self.tr("Up"), self.tr("Down")])
            self.corrTrackDirChooser.setCurrentIndex(1)
            self.paradigm_widg_sizer.addWidget(self.corrTrackDirChooser, n, 2)
            self.corrTrackDirCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.corrTrackDirCheckBox, n, 0)
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
            
            self.paradigmChooserList = [self.adaptiveTypeChooser, self.corrTrackDirChooser]
            self.paradigmChooserLabelList = [self.adaptiveTypeChooserLabel, self.corrTrackDirChooserLabel]
            self.paradigmChooserOptionsList = [self.prm["adaptiveTypeChoices"], [self.tr("Up"), self.tr("Down")]]
            self.paradigmChooserCheckBoxList = [self.adaptiveTypeCheckBox, self.corrTrackDirCheckBox]

            self.paradigmFieldList = [self.pcTrackedTF, self.initialTurnpointsTF, self.totalTurnpointsTF, self.stepSize1TF, self.stepSize2TF]
            self.paradigmFieldLabelList = [self.pcTrackedLabel, self.initialTurnpointsLabel, self.totalTurnpointsLabel, self.stepSize1Label, self.stepSize2Label]
            self.paradigmFieldCheckBoxList = [self.pcTrackedCheckBox, self.initialTurnpointsCheckBox, self.totalTurnpointsCheckBox, self.stepSize1CheckBox, self.stepSize2CheckBox]

        #------------------------------------
        #ADAPTIVE INTERLEAVED2 PARADIGM WIDGETS
        if self.currParadigm == self.tr("Transformed Up-Down Interleaved"):
            n = 0
            self.adaptiveTypeChooserLabel = QLabel(self.tr("Procedure:"), self)
            self.paradigm_widg_sizer.addWidget(self.adaptiveTypeChooserLabel, n, 1)
            self.adaptiveTypeChooser = QComboBox()
            self.adaptiveTypeChooser.addItems(self.prm["adaptiveTypeChoices"])
            try:
                self.adaptiveTypeChooser.setCurrentIndex(self.prm["adaptiveTypeChoices"].index(self.prm[self.currExp]['defaultAdaptiveType']))
            except:
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
            self.nTracksChooser.textActivated[str].connect(self.onChangeNTracks)
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
            self.corrTrackDirChooserLabel = []
            self.corrTrackDirChooser = []
            self.corrTrackDirOptionsList = []
            self.corrTrackDirCheckBox = []
            
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
                self.corrTrackDirChooserLabel.append(QLabel(self.tr("Corr. Resp. Move Track {0}:".format(str(i+1))), self))
                self.paradigm_widg_sizer.addWidget(self.corrTrackDirChooserLabel[i], n, 1)
                self.corrTrackDirChooser.append(QComboBox())
                self.corrTrackDirChooser[i].addItems([self.tr("Up"), self.tr("Down")])
                self.corrTrackDirChooser[i].setCurrentIndex(1)
                self.paradigm_widg_sizer.addWidget(self.corrTrackDirChooser[i], n, 2)
                self.corrTrackDirOptionsList.append([self.tr("Up"), self.tr("Down")])
                self.corrTrackDirCheckBox.append(QCheckBox())
                self.paradigm_widg_sizer.addWidget(self.corrTrackDirCheckBox[i], n, 0)
                n = n+1
                self.ruleDownLabel.append(QLabel(self.tr("Rule Down Track " + str(i+1)), self))
                self.paradigm_widg_sizer.addWidget(self.ruleDownLabel[i], n, 1)
                self.ruleDownTF.append(QLineEdit())
                self.ruleDownTF[i].setText('2')
                self.ruleDownTF[i].setValidator(QIntValidator(self))
                self.paradigm_widg_sizer.addWidget(self.ruleDownTF[i], n, 2)
                self.ruleDownCheckBox.append(QCheckBox())
                self.paradigm_widg_sizer.addWidget(self.ruleDownCheckBox[i], n, 0)

                self.ruleUpLabel.append(QLabel(self.tr("Rule Up Track " + str(i+1)), self))
                self.paradigm_widg_sizer.addWidget(self.ruleUpLabel[i], n, 4)
                self.ruleUpTF.append(QLineEdit())
                self.ruleUpTF[i].setText('1')
                self.ruleUpTF[i].setValidator(QIntValidator(self))
                self.paradigm_widg_sizer.addWidget(self.ruleUpTF[i], n, 5)
                self.ruleUpCheckBox.append(QCheckBox())
                self.paradigm_widg_sizer.addWidget(self.ruleUpCheckBox[i], n, 3)

                n = n+1
              
                self.initialTurnpointsLabel.append(QLabel(self.tr("Initial Turnpoints Track " + str(i+1)), self))
                self.paradigm_widg_sizer.addWidget(self.initialTurnpointsLabel[i], n, 1)
                self.initialTurnpointsTF.append(QLineEdit())
                self.initialTurnpointsTF[i].setText('4')
                self.initialTurnpointsTF[i].setValidator(QIntValidator(self))
                self.paradigm_widg_sizer.addWidget(self.initialTurnpointsTF[i], n, 2)
                self.initialTurnpointsCheckBox.append(QCheckBox())
                self.paradigm_widg_sizer.addWidget(self.initialTurnpointsCheckBox[i], n, 0)

                self.totalTurnpointsLabel.append(QLabel(self.tr("Total Turnpoints Track " + str(i+1)), self))
                self.paradigm_widg_sizer.addWidget(self.totalTurnpointsLabel[i], n, 4)
                self.totalTurnpointsTF.append(QLineEdit())
                self.totalTurnpointsTF[i].setText('16')
                self.totalTurnpointsTF[i].setValidator(QIntValidator(self))
                self.paradigm_widg_sizer.addWidget(self.totalTurnpointsTF[i], n, 5)
                self.totalTurnpointsCheckBox.append(QCheckBox())
                self.paradigm_widg_sizer.addWidget(self.totalTurnpointsCheckBox[i], n, 3)
                
                n = n+1
                self.stepSize1Label.append(QLabel(self.tr("Step Size 1 Track " + str(i+1)), self))
                self.paradigm_widg_sizer.addWidget(self.stepSize1Label[i], n, 1)
                self.stepSize1TF.append(QLineEdit())
                self.stepSize1TF[i].setText('4')
                self.stepSize1TF[i].setValidator(QDoubleValidator(self))
                self.paradigm_widg_sizer.addWidget(self.stepSize1TF[i], n, 2)
                self.stepSize1CheckBox.append(QCheckBox())
                self.paradigm_widg_sizer.addWidget(self.stepSize1CheckBox[i], n, 0)
                
                self.stepSize2Label.append(QLabel(self.tr("Step Size 2 Track " + str(i+1)), self))
                self.paradigm_widg_sizer.addWidget(self.stepSize2Label[i], n, 4)
                self.stepSize2TF.append(QLineEdit())
                self.stepSize2TF[i].setText('2')
                self.stepSize2TF[i].setValidator(QDoubleValidator(self))
                self.paradigm_widg_sizer.addWidget(self.stepSize2TF[i], n, 5)
                self.stepSize2CheckBox.append(QCheckBox())
                self.paradigm_widg_sizer.addWidget(self.stepSize2CheckBox[i], n, 3)
                n = n+1
           
                
            self.paradigmChooserList = [self.adaptiveTypeChooser, self.nTracksChooser, self.maxConsecutiveTrials, self.tnpToAverageChooser]
            self.paradigmChooserLabelList = [self.adaptiveTypeChooserLabel, self.nTracksLabel, self.maxConsecutiveTrialsLabel, self.tnpToAverageLabel]
            self.paradigmChooserOptionsList = [self.prm["adaptiveTypeChoices"], self.nTracksOptionsList, self.maxConsecutiveTrialsOptionsList, self.prm["tnpToAverageChoices"]]
            self.paradigmChooserCheckBoxList = [self.adaptiveTypeCheckBox, self.nTracksCheckBox, self.maxConsecutiveTrialsCheckBox, self.tnpToAverageCheckBox]
            self.paradigmChooserList.extend(self.corrTrackDirChooser)
            self.paradigmChooserLabelList.extend(self.corrTrackDirChooserLabel)
            self.paradigmChooserOptionsList.extend(self.corrTrackDirOptionsList)
            self.paradigmChooserCheckBoxList.extend(self.corrTrackDirCheckBox)

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
        if self.currParadigm == self.tr("Weighted Up-Down Interleaved"):
            n = 0
            self.adaptiveTypeChooserLabel = QLabel(self.tr("Procedure:"), self)
            self.paradigm_widg_sizer.addWidget(self.adaptiveTypeChooserLabel, n, 1)
            self.adaptiveTypeChooser = QComboBox()
            self.adaptiveTypeChooser.addItems(self.prm["adaptiveTypeChoices"])
            try:
                self.adaptiveTypeChooser.setCurrentIndex(self.prm["adaptiveTypeChoices"].index(self.prm[self.currExp]['defaultAdaptiveType']))
            except:
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
            self.nTracksChooser.textActivated[str].connect(self.onChangeNTracks)
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
            self.corrTrackDirChooserLabel = []
            self.corrTrackDirChooser = []
            self.corrTrackDirOptionsList = []
            self.corrTrackDirCheckBox = []
             
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
                self.corrTrackDirChooserLabel.append(QLabel(self.tr("Corr. Resp. Move Track {0}:".format(str(i+1))), self))
                self.paradigm_widg_sizer.addWidget(self.corrTrackDirChooserLabel[i], n, 1)
                self.corrTrackDirChooser.append(QComboBox())
                self.corrTrackDirChooser[i].addItems([self.tr("Up"), self.tr("Down")])
                self.corrTrackDirChooser[i].setCurrentIndex(1)
                self.paradigm_widg_sizer.addWidget(self.corrTrackDirChooser[i], n, 2)
                self.corrTrackDirOptionsList.append([self.tr("Up"), self.tr("Down")])
                self.corrTrackDirCheckBox.append(QCheckBox())
                self.paradigm_widg_sizer.addWidget(self.corrTrackDirCheckBox[i], n, 0)
                n = n+1
                self.pcTrackedLabel.append(QLabel(self.tr("Percent Correct Tracked Track " + str(i+1)), self))
                self.paradigm_widg_sizer.addWidget(self.pcTrackedLabel[i], n, 1)
                self.pcTrackedTF.append(QLineEdit())
                self.pcTrackedTF[i].setText('75')
                self.pcTrackedTF[i].setValidator(QDoubleValidator(self))
                self.paradigm_widg_sizer.addWidget(self.pcTrackedTF[i], n, 2)
                self.pcTrackedCheckBox.append(QCheckBox())
                self.paradigm_widg_sizer.addWidget(self.pcTrackedCheckBox[i], n, 0)

                n = n+1
                self.initialTurnpointsLabel.append(QLabel(self.tr("Initial Turnpoints Track " + str(i+1)), self))
                self.paradigm_widg_sizer.addWidget(self.initialTurnpointsLabel[i], n, 1)
                self.initialTurnpointsTF.append(QLineEdit())
                self.initialTurnpointsTF[i].setText('4')
                self.initialTurnpointsTF[i].setValidator(QIntValidator(self))
                self.paradigm_widg_sizer.addWidget(self.initialTurnpointsTF[i], n, 2)
                self.initialTurnpointsCheckBox.append(QCheckBox())
                self.paradigm_widg_sizer.addWidget(self.initialTurnpointsCheckBox[i], n, 0)

                self.totalTurnpointsLabel.append(QLabel(self.tr("Total Turnpoints Track " + str(i+1)), self))
                self.paradigm_widg_sizer.addWidget(self.totalTurnpointsLabel[i], n, 4)
                self.totalTurnpointsTF.append(QLineEdit())
                self.totalTurnpointsTF[i].setText('16')
                self.totalTurnpointsTF[i].setValidator(QIntValidator(self))
                self.paradigm_widg_sizer.addWidget(self.totalTurnpointsTF[i], n, 5)
                self.totalTurnpointsCheckBox.append(QCheckBox())
                self.paradigm_widg_sizer.addWidget(self.totalTurnpointsCheckBox[i], n, 3)
                
                n = n+1
                self.stepSize1Label.append(QLabel(self.tr("Step Size 1 Track " + str(i+1)), self))
                self.paradigm_widg_sizer.addWidget(self.stepSize1Label[i], n, 1)
                self.stepSize1TF.append(QLineEdit())
                self.stepSize1TF[i].setText('4')
                self.stepSize1TF[i].setValidator(QDoubleValidator(self))
                self.paradigm_widg_sizer.addWidget(self.stepSize1TF[i], n, 2)
                self.stepSize1CheckBox.append(QCheckBox())
                self.paradigm_widg_sizer.addWidget(self.stepSize1CheckBox[i], n, 0)
                
                self.stepSize2Label.append(QLabel(self.tr("Step Size 2 Track " + str(i+1)), self))
                self.paradigm_widg_sizer.addWidget(self.stepSize2Label[i], n, 4)
                self.stepSize2TF.append(QLineEdit())
                self.stepSize2TF[i].setText('2')
                self.stepSize2TF[i].setValidator(QDoubleValidator(self))
                self.paradigm_widg_sizer.addWidget(self.stepSize2TF[i], n, 5)
                self.stepSize2CheckBox.append(QCheckBox())
                self.paradigm_widg_sizer.addWidget(self.stepSize2CheckBox[i], n, 3)
                n = n+1
           
                
            self.paradigmChooserList = [self.adaptiveTypeChooser, self.nTracksChooser, self.maxConsecutiveTrials, self.tnpToAverageChooser]
            self.paradigmChooserLabelList = [self.adaptiveTypeChooserLabel, self.nTracksLabel, self.maxConsecutiveTrialsLabel, self.tnpToAverageLabel]
            self.paradigmChooserOptionsList = [self.prm["adaptiveTypeChoices"], self.nTracksOptionsList, self.maxConsecutiveTrialsOptionsList, self.prm["tnpToAverageChoices"]]
            self.paradigmChooserCheckBoxList = [self.adaptiveTypeCheckBox, self.nTracksCheckBox, self.maxConsecutiveTrialsCheckBox, self.tnpToAverageCheckBox]
            self.paradigmChooserList.extend(self.corrTrackDirChooser)
            self.paradigmChooserLabelList.extend(self.corrTrackDirChooserLabel)
            self.paradigmChooserOptionsList.extend(self.corrTrackDirOptionsList)
            self.paradigmChooserCheckBoxList.extend(self.corrTrackDirCheckBox)

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

        #-------------------------------------------------------
        #Transformed Up-Down Hybrid Paradigm Widgets
        if self.currParadigm in [self.tr("Transformed Up-Down Hybrid")]:
            n = 0
            self.adaptiveTypeChooserLabel = QLabel(self.tr("Procedure:"), self)
            self.paradigm_widg_sizer.addWidget(self.adaptiveTypeChooserLabel, n, 1)
            self.adaptiveTypeChooser = QComboBox()
            self.adaptiveTypeChooser.addItems(self.prm["adaptiveTypeChoices"])
            try:
                self.adaptiveTypeChooser.setCurrentIndex(self.prm["adaptiveTypeChoices"].index(self.prm[self.currExp]['defaultAdaptiveType']))
            except:
                self.adaptiveTypeChooser.setCurrentIndex(0)
            self.paradigm_widg_sizer.addWidget(self.adaptiveTypeChooser, n, 2)
            self.adaptiveTypeCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.adaptiveTypeCheckBox, n, 0)

            n = n+1
            self.corrTrackDirChooserLabel = QLabel(self.tr("Corr. Resp. Move Track:"), self)
            self.paradigm_widg_sizer.addWidget(self.corrTrackDirChooserLabel, n, 1)
            self.corrTrackDirChooser = QComboBox()
            self.corrTrackDirChooser.addItems([self.tr("Up"), self.tr("Down")])
            self.corrTrackDirChooser.setCurrentIndex(1)
            self.paradigm_widg_sizer.addWidget(self.corrTrackDirChooser, n, 2)
            self.corrTrackDirCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.corrTrackDirCheckBox, n, 0)

            n = n+1
            self.ruleDownLabel = QLabel(self.tr("Rule Down"), self)
            self.paradigm_widg_sizer.addWidget(self.ruleDownLabel, n, 1)
            self.ruleDownTF = QLineEdit()
            self.ruleDownTF.setText('2')
            self.ruleDownTF.setValidator(QIntValidator(self))
            self.paradigm_widg_sizer.addWidget(self.ruleDownTF, n, 2)
            self.ruleDownCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.ruleDownCheckBox, n, 0)

            self.ruleUpLabel = QLabel(self.tr("Rule Up"), self)
            self.paradigm_widg_sizer.addWidget(self.ruleUpLabel, n, 4)
            self.ruleUpTF = QLineEdit()
            self.ruleUpTF.setText('1')
            self.ruleUpTF.setValidator(QIntValidator(self))
            self.paradigm_widg_sizer.addWidget(self.ruleUpTF, n, 5)
            self.ruleUpCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.ruleUpCheckBox, n, 3)
            n = n+1
            self.initialTurnpointsLabel = QLabel(self.tr("Initial Turnpoints"), self)
            self.paradigm_widg_sizer.addWidget(self.initialTurnpointsLabel, n, 1)
            self.initialTurnpointsTF = QLineEdit()
            self.initialTurnpointsTF.setText('4')
            self.initialTurnpointsTF.setValidator(QIntValidator(self))
            self.paradigm_widg_sizer.addWidget(self.initialTurnpointsTF, n, 2)
            self.initialTurnpointsCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.initialTurnpointsCheckBox, n, 0)

            self.totalTurnpointsLabel = QLabel(self.tr("Total Turnpoints"), self)
            self.paradigm_widg_sizer.addWidget(self.totalTurnpointsLabel, n, 4)
            self.totalTurnpointsTF = QLineEdit()
            self.totalTurnpointsTF.setText('16')
            self.totalTurnpointsTF.setValidator(QIntValidator(self))
            self.paradigm_widg_sizer.addWidget(self.totalTurnpointsTF, n, 5)
            self.totalTurnpointsCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.totalTurnpointsCheckBox, n, 3)
            n = n+1
            self.stepSize1Label = QLabel(self.tr("Step Size 1"), self)
            self.paradigm_widg_sizer.addWidget(self.stepSize1Label, n, 1)
            self.stepSize1TF = QLineEdit()
            self.stepSize1TF.setText('4')
            self.stepSize1TF.setValidator(QDoubleValidator(self))
            self.stepSize1TF.setWhatsThis(self.tr("Step size for the initial turnpoints"))
            self.paradigm_widg_sizer.addWidget(self.stepSize1TF, n, 2)
            self.stepSize1CheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.stepSize1CheckBox, n, 0)

            self.stepSize2Label = QLabel(self.tr("Step Size 2"), self)
            self.paradigm_widg_sizer.addWidget(self.stepSize2Label, n, 4)
            self.stepSize2TF = QLineEdit()
            self.stepSize2TF.setText('2')
            self.stepSize2TF.setValidator(QDoubleValidator(self))
            self.stepSize2TF.setWhatsThis(self.tr("Step size for the final turnpoints"))
            self.paradigm_widg_sizer.addWidget(self.stepSize2TF, n, 5)
            self.stepSize2CheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.stepSize2CheckBox, n, 3)

            n = n+1
            self.constantNTrialsLabel = QLabel(self.tr("Constant No. Trials"), self)
            self.paradigm_widg_sizer.addWidget(self.constantNTrialsLabel, n, 1)
            self.constantNTrialsTF = QLineEdit()
            self.constantNTrialsTF.setText('50')
            self.constantNTrialsTF.setValidator(QIntValidator(self))
            self.paradigm_widg_sizer.addWidget(self.constantNTrialsTF, n, 2)
            self.constantNTrialsCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.constantNTrialsCheckBox, n, 0)

            n = n+1
            self.switchAfterInitialTurnpointsChooserLabel = QLabel(self.tr("Switch only after initial turnpoints:"), self)
            self.paradigm_widg_sizer.addWidget(self.switchAfterInitialTurnpointsChooserLabel, n, 1)
            self.switchAfterInitialTurnpointsChooser = QComboBox()
            self.switchAfterInitialTurnpointsChooser.addItems([self.tr("Yes"), self.tr("No")])
            self.switchAfterInitialTurnpointsChooser.setCurrentIndex(0)
            self.paradigm_widg_sizer.addWidget(self.switchAfterInitialTurnpointsChooser, n, 2)
            self.switchAfterInitialTurnpointsCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.switchAfterInitialTurnpointsCheckBox, n, 0)
            # self.adaptParamLimLabel = QLabel(self.tr("Adapt. Param. Limit"), self)
            # self.paradigm_widg_sizer.addWidget(self.adaptParamLimLabel, n, 4)
            # self.adaptParamLimTF = QLineEdit()
            # self.adaptParamLimTF.setText('10')
            # self.adaptParamLimTF.setValidator(QIntValidator(self))
            # self.paradigm_widg_sizer.addWidget(self.adaptParamLimTF, n, 5)
            # self.adaptParamLimCheckBox = QCheckBox()
            # self.paradigm_widg_sizer.addWidget(self.adaptParamLimCheckBox, n, 3)

            self.paradigmChooserList = [self.adaptiveTypeChooser, self.corrTrackDirChooser, self.switchAfterInitialTurnpointsChooser]
            self.paradigmChooserLabelList = [self.adaptiveTypeChooserLabel, self.corrTrackDirChooserLabel, self.switchAfterInitialTurnpointsChooserLabel]
            self.paradigmChooserOptionsList = [self.prm["adaptiveTypeChoices"], [self.tr("Up"), self.tr("Down")], [self.tr("Yes"), self.tr("No")]]
            self.paradigmChooserCheckBoxList = [self.adaptiveTypeCheckBox, self.corrTrackDirCheckBox, self.switchAfterInitialTurnpointsCheckBox]

            self.paradigmFieldList = [self.ruleDownTF, self.ruleUpTF, self.initialTurnpointsTF, self.totalTurnpointsTF, self.stepSize1TF, self.stepSize2TF, self.constantNTrialsTF]#, self.adaptParamLimTF]
            self.paradigmFieldLabelList = [self.ruleDownLabel, self.ruleUpLabel, self.initialTurnpointsLabel, self.totalTurnpointsLabel, self.stepSize1Label, self.stepSize2Label,  self.constantNTrialsLabel]#, self.adaptParamLimLabel]
            self.paradigmFieldCheckBoxList = [self.ruleDownCheckBox, self.ruleUpCheckBox, self.initialTurnpointsCheckBox, self.totalTurnpointsCheckBox, self.stepSize1CheckBox, self.stepSize2CheckBox, self.constantNTrialsCheckBox]#, self.adaptParamLimCheckBox]

        #------------------------------------
        #WEIGHTED UP/DOWN Hybrid PARADIGM WIDGETS
        if self.currParadigm in [self.tr("Weighted Up-Down Hybrid")]:
            n = 0
            self.adaptiveTypeChooserLabel = QLabel(self.tr("Procedure:"), self)
            self.paradigm_widg_sizer.addWidget(self.adaptiveTypeChooserLabel, n, 1)
            self.adaptiveTypeChooser = QComboBox()
            self.adaptiveTypeChooser.addItems(self.prm["adaptiveTypeChoices"])
            try:
                self.adaptiveTypeChooser.setCurrentIndex(self.prm["adaptiveTypeChoices"].index(self.prm[self.currExp]['defaultAdaptiveType']))
            except:
                self.adaptiveTypeChooser.setCurrentIndex(0)
            self.paradigm_widg_sizer.addWidget(self.adaptiveTypeChooser, n, 2)
            self.adaptiveTypeCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.adaptiveTypeCheckBox, n, 0)

            n = n+1
            self.corrTrackDirChooserLabel = QLabel(self.tr("Corr. Resp. Move Track:"), self)
            self.paradigm_widg_sizer.addWidget(self.corrTrackDirChooserLabel, n, 1)
            self.corrTrackDirChooser = QComboBox()
            self.corrTrackDirChooser.addItems([self.tr("Up"), self.tr("Down")])
            self.corrTrackDirChooser.setCurrentIndex(1)
            self.paradigm_widg_sizer.addWidget(self.corrTrackDirChooser, n, 2)
            self.corrTrackDirCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.corrTrackDirCheckBox, n, 0)
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

            self.constantNTrialsLabel = QLabel(self.tr("Constant No. Trials"), self)
            self.paradigm_widg_sizer.addWidget(self.constantNTrialsLabel, n, 1)
            self.constantNTrialsTF = QLineEdit()
            self.constantNTrialsTF.setText('50')
            self.constantNTrialsTF.setValidator(QIntValidator(self))
            self.paradigm_widg_sizer.addWidget(self.constantNTrialsTF, n, 2)
            self.constantNTrialsCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.constantNTrialsCheckBox, n, 0)

            # self.adaptParamLimLabel = QLabel(self.tr("Adapt. Param. Limit"), self)
            # self.paradigm_widg_sizer.addWidget(self.adaptParamLimLabel, n, 4)
            # self.adaptParamLimTF = QLineEdit()
            # self.adaptParamLimTF.setText('10')
            # self.adaptParamLimTF.setValidator(QIntValidator(self))
            # self.paradigm_widg_sizer.addWidget(self.adaptParamLimTF, n, 5)
            # self.adaptParamLimCheckBox = QCheckBox()
            # self.paradigm_widg_sizer.addWidget(self.adaptParamLimCheckBox, n, 3)

            n = n+1
            self.switchAfterInitialTurnpointsChooserLabel = QLabel(self.tr("Switch only after initial turnpoints:"), self)
            self.paradigm_widg_sizer.addWidget(self.switchAfterInitialTurnpointsChooserLabel, n, 1)
            self.switchAfterInitialTurnpointsChooser = QComboBox()
            self.switchAfterInitialTurnpointsChooser.addItems([self.tr("Yes"), self.tr("No")])
            self.switchAfterInitialTurnpointsChooser.setCurrentIndex(0)
            self.paradigm_widg_sizer.addWidget(self.switchAfterInitialTurnpointsChooser, n, 2)
            self.switchAfterInitialTurnpointsCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.switchAfterInitialTurnpointsCheckBox, n, 0)
            
            self.paradigmChooserList = [self.adaptiveTypeChooser, self.corrTrackDirChooser, self.switchAfterInitialTurnpointsChooser]
            self.paradigmChooserLabelList = [self.adaptiveTypeChooserLabel, self.corrTrackDirChooserLabel, self.switchAfterInitialTurnpointsChooserLabel]
            self.paradigmChooserOptionsList = [self.prm["adaptiveTypeChoices"], [self.tr("Up"), self.tr("Down")], [self.tr("Yes"), self.tr("No")]]
            self.paradigmChooserCheckBoxList = [self.adaptiveTypeCheckBox, self.corrTrackDirCheckBox, self.switchAfterInitialTurnpointsCheckBox]

            self.paradigmFieldList = [self.pcTrackedTF, self.initialTurnpointsTF, self.totalTurnpointsTF, self.stepSize1TF, self.stepSize2TF, self.constantNTrialsTF]#, self.adaptParamLimTF]
            self.paradigmFieldLabelList = [self.pcTrackedLabel, self.initialTurnpointsLabel, self.totalTurnpointsLabel, self.stepSize1Label, self.stepSize2Label, self.constantNTrialsLabel]#, self.adaptParamLimLabel]
            self.paradigmFieldCheckBoxList = [self.pcTrackedCheckBox, self.initialTurnpointsCheckBox, self.totalTurnpointsCheckBox, self.stepSize1CheckBox, self.stepSize2CheckBox, self.constantNTrialsCheckBox]#, self.adaptParamLimCheckBox]

        #------------------------
        #ONE CONSTANT PARADIGM WIDGETS
        if self.currParadigm in [self.tr("Constant 1-Interval 2-Alternatives"), self.tr("Constant 1-Pair Same/Different"), self.tr("Constant m-Intervals n-Alternatives")]:
            n = 0
            self.nTrialsLabel = QLabel(self.tr("No. Trials"), self)
            self.paradigm_widg_sizer.addWidget(self.nTrialsLabel, n, 1)
            self.nTrialsTF = QLineEdit()
            self.nTrialsTF.setText('25')
            self.nTrialsTF.setValidator(QIntValidator(self))
            self.paradigm_widg_sizer.addWidget(self.nTrialsTF, n, 2)
            self.nTrialsCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.nTrialsCheckBox, n, 0)

            n = n+1
            self.nPracticeTrialsLabel = QLabel(self.tr("No. Practice Trials"), self)
            self.paradigm_widg_sizer.addWidget(self.nPracticeTrialsLabel, n, 1)
            self.nPracticeTrialsTF = QLineEdit()
            self.nPracticeTrialsTF.setText('0')
            self.nPracticeTrialsTF.setValidator(QIntValidator(self))
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
        if self.currParadigm in [self.tr("Multiple Constants 1-Interval 2-Alternatives"),
                                 self.tr("Multiple Constants m-Intervals n-Alternatives"),
                                 self.tr("Multiple Constants 1-Pair Same/Different"),
                                 self.tr("Multiple Constants ABX"),
                                 self.tr("Multiple Constants Odd One Out"),
                                 self.tr("Multiple Constants Sound Comparison")]:
            n = 0
            self.nTrialsLabel = QLabel(self.tr("No. Trials"), self)
            self.paradigm_widg_sizer.addWidget(self.nTrialsLabel, n, 1)
            self.nTrialsTF = QLineEdit()
            self.nTrialsTF.setText('25')
            self.nTrialsTF.setValidator(QIntValidator(self))
            self.paradigm_widg_sizer.addWidget(self.nTrialsTF, n, 2)
            self.nTrialsCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.nTrialsCheckBox, n, 0)

            n = n+1
            self.nPracticeTrialsLabel = QLabel(self.tr("No. Practice Trials"), self)
            self.paradigm_widg_sizer.addWidget(self.nPracticeTrialsLabel, n, 1)
            self.nPracticeTrialsTF = QLineEdit()
            self.nPracticeTrialsTF.setText('0')
            self.nPracticeTrialsTF.setValidator(QIntValidator(self))
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
            self.nDifferencesChooser.textActivated[str].connect(self.onChangeNDifferences)

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

        #------------------------------------
        #PEST PARADIGM WIDGETS
        if self.currParadigm == self.tr("PEST"):
            n = 0
            self.adaptiveTypeChooserLabel = QLabel(self.tr("Procedure:"), self)
            self.paradigm_widg_sizer.addWidget(self.adaptiveTypeChooserLabel, n, 1)
            self.adaptiveTypeChooser = QComboBox()
            self.adaptiveTypeChooser.addItems(self.prm["adaptiveTypeChoices"])
            try:
                self.adaptiveTypeChooser.setCurrentIndex(self.prm["adaptiveTypeChoices"].index(self.prm[self.currExp]['defaultAdaptiveType']))
            except:
                self.adaptiveTypeChooser.setCurrentIndex(0)
            self.paradigm_widg_sizer.addWidget(self.adaptiveTypeChooser, n, 2)
            self.adaptiveTypeCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.adaptiveTypeCheckBox, n, 0)

            n = n+1
            self.trackDirChooserLabel = QLabel(self.tr("Corr. Resp. Move Track:"), self)
            self.paradigm_widg_sizer.addWidget(self.trackDirChooserLabel, n, 1)
            self.trackDirChooser = QComboBox()
            self.trackDirChooser.addItems([self.tr("Up"), self.tr("Down")])
            self.trackDirChooser.setCurrentIndex(1)
            self.paradigm_widg_sizer.addWidget(self.trackDirChooser, n, 2)
            self.trackDirCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.trackDirCheckBox, n, 0)

            n = n+1
            self.pcTrackedLabel = QLabel(self.tr("Percent Correct Tracked"), self)
            self.paradigm_widg_sizer.addWidget(self.pcTrackedLabel, n, 1)
            self.pcTrackedTF = QLineEdit()
            self.pcTrackedTF.setText('75')
            self.pcTrackedTF.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.pcTrackedTF, n, 2)
            self.pcTrackedCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.pcTrackedCheckBox, n, 0)

            #n = n+1
            self.initialStepSizeLabel = QLabel(self.tr("Initial Step Size"), self)
            self.paradigm_widg_sizer.addWidget(self.initialStepSizeLabel, n, 4)
            self.initialStepSizeTF = QLineEdit()
            self.initialStepSizeTF.setText('5')
            self.initialStepSizeTF.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.initialStepSizeTF, n, 5)
            self.initialStepSizeCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.initialStepSizeCheckBox, n, 3)

            n = n+1
            self.minStepSizeLabel = QLabel(self.tr("Minimum Step Size"), self)
            self.paradigm_widg_sizer.addWidget(self.minStepSizeLabel, n, 1)
            self.minStepSizeTF = QLineEdit()
            self.minStepSizeTF.setText('1')
            self.minStepSizeTF.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.minStepSizeTF, n, 2)
            self.minStepSizeCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.minStepSizeCheckBox, n, 0)

            #n = n+1
            self.maxStepSizeLabel = QLabel(self.tr("Maximum Step Size"), self)
            self.paradigm_widg_sizer.addWidget(self.maxStepSizeLabel, n, 4)
            self.maxStepSizeTF = QLineEdit()
            self.maxStepSizeTF.setText('10')
            self.maxStepSizeTF.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.maxStepSizeTF, n, 5)
            self.maxStepSizeCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.maxStepSizeCheckBox, n, 3)

            n = n+1
            self.WLabel = QLabel(self.tr("W"), self)
            self.paradigm_widg_sizer.addWidget(self.WLabel, n, 1)
            self.WTF = QLineEdit()
            self.WTF.setText('1.5')
            self.WTF.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.WTF, n, 2)
            self.WCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.WCheckBox, n, 0)

            self.paradigmChooserList = [self.adaptiveTypeChooser, self.trackDirChooser]
            self.paradigmChooserLabelList = [self.adaptiveTypeChooserLabel, self.trackDirChooserLabel]
            self.paradigmChooserOptionsList = [self.prm["adaptiveTypeChoices"], [self.tr("Up"), self.tr("Down")]]
            self.paradigmChooserCheckBoxList = [self.adaptiveTypeCheckBox, self.trackDirCheckBox]

            self.paradigmFieldList = [self.initialStepSizeTF, self.minStepSizeTF, self.maxStepSizeTF,
                                      self.WTF, self.pcTrackedTF]
            self.paradigmFieldLabelList = [self.initialStepSizeLabel, self.minStepSizeLabel,
                                           self.maxStepSizeLabel, self.WLabel, self.pcTrackedLabel]
            self.paradigmFieldCheckBoxList = [self.initialStepSizeCheckBox, self.minStepSizeCheckBox,
                                              self.maxStepSizeCheckBox, self.WCheckBox, self.pcTrackedCheckBox]

        #Maximum Likelihood
        if self.currParadigm in [self.tr("Maximum Likelihood")]:
            n = 0
            psyFunOptions = ["Logistic"]
            # n = n+1
            self.psyFunChooserLabel = QLabel(self.tr("Psychometric Function:"), self)
            self.paradigm_widg_sizer.addWidget(self.psyFunChooserLabel, n, 1)
            self.psyFunChooser = QComboBox()
            self.psyFunChooser.addItems(psyFunOptions)
            self.paradigm_widg_sizer.addWidget(self.psyFunChooser, n, 2)
            self.psyFunCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.psyFunCheckBox, n, 0)
            n = n+1
 
            #min thresh
            self.loMidPointLabel = QLabel(self.tr("Mid Point Minimum"), self)
            self.paradigm_widg_sizer.addWidget(self.loMidPointLabel, n, 1)
            self.loMidPoint = QLineEdit()
            self.loMidPoint.setText('0.001')
            self.loMidPoint.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.loMidPoint, n, 2)
            self.loMidPointCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.loMidPointCheckBox, n, 0)
            #n = n+1
            #max thresh
            self.hiMidPointLabel = QLabel(self.tr("Mid Point Maximum"), self)
            self.paradigm_widg_sizer.addWidget(self.hiMidPointLabel, n, 4)
            self.hiMidPoint = QLineEdit()
            self.hiMidPoint.setText('200')
            self.hiMidPoint.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.hiMidPoint, n, 5)
            self.hiMidPointCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.hiMidPointCheckBox, n, 3)
            n = n+1
            #step
            self.threshGridStepLabel = QLabel(self.tr("Mid Point Step"), self)
            self.paradigm_widg_sizer.addWidget(self.threshGridStepLabel, n, 1)
            self.threshGridStep = QLineEdit()
            self.threshGridStep.setText('0.001')
            self.threshGridStep.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.threshGridStep, n, 2)
            self.threshGridStepCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.threshGridStepCheckBox, n, 0)
            #n = n+1
            #percent tracked
            self.percCorrTrackedLabel = QLabel(self.tr("Percent Correct Tracked"), self)
            self.paradigm_widg_sizer.addWidget(self.percCorrTrackedLabel, n, 4)
            self.percCorrTracked = QLineEdit()
            self.percCorrTracked.setText('75')
            self.percCorrTracked.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.percCorrTracked, n, 5)
            self.percCorrTrackedCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.percCorrTrackedCheckBox, n, 3)
            n = n+1
            #psyfunslope
            self.psyFunSlopeLabel = QLabel(self.tr("Psychometric Function Slope"), self)
            self.paradigm_widg_sizer.addWidget(self.psyFunSlopeLabel, n, 1)
            self.psyFunSlope = QLineEdit()
            self.psyFunSlope.setText('1')
            self.psyFunSlope.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.psyFunSlope, n, 2)
            self.psyFunSlopeCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.psyFunSlopeCheckBox, n, 0)
            #n = n+1
            self.lapseRateLabel = QLabel(self.tr("Lapse Rate"), self)
            self.paradigm_widg_sizer.addWidget(self.lapseRateLabel, n, 4)
            self.lapseRate = QLineEdit()
            self.lapseRate.setText('0.001')
            self.lapseRate.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.lapseRate, n, 5)
            self.lapseRateCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.lapseRateCheckBox, n, 3)
            # #mode, median, mean
            # self.centTendChooserLabel = QLabel(self.tr("Central Tendency:"), self)
            # self.paradigm_widg_sizer.addWidget(self.centTendChooserLabel, n, 1)
            # self.centTendChooser = QComboBox()
            # self.centTendChooser.addItems(centTendOptions)
            # self.centTendCheckBox = QCheckBox()
            # self.paradigm_widg_sizer.addWidget(self.centTendCheckBox, n, 0)
            n = n+1

            self.logSpaceStimChooserLabel = QLabel(self.tr("Log scale:"), self)
            self.paradigm_widg_sizer.addWidget(self.logSpaceStimChooserLabel, n, 1)
            self.logSpaceStimChooser = QComboBox()
            self.logSpaceStimChooser.addItems(["No", "Yes"])
            self.paradigm_widg_sizer.addWidget(self.logSpaceStimChooser, n, 2)
            self.logSpaceStimCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.logSpaceStimCheckBox, n, 0)

            n = n+1
            
            self.nTrialsLabel = QLabel(self.tr("No. Trials"), self)
            self.paradigm_widg_sizer.addWidget(self.nTrialsLabel, n, 1)
            self.nTrialsTF = QLineEdit()
            self.nTrialsTF.setText("30")
            self.nTrialsTF.setValidator(QIntValidator(self))
            self.paradigm_widg_sizer.addWidget(self.nTrialsTF, n, 2)
            self.nTrialsCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.nTrialsCheckBox, n, 0)

 
         

            self.paradigmChooserList = [self.psyFunChooser, self.logSpaceStimChooser]
            self.paradigmChooserLabelList = [self.psyFunChooserLabel, self.logSpaceStimChooserLabel]
            self.paradigmChooserOptionsList = [psyFunOptions, ["No", "Yes"]]
            self.paradigmChooserCheckBoxList = [self.psyFunCheckBox, self.logSpaceStimCheckBox]

            self.paradigmFieldList = [self.psyFunSlope, self.loMidPoint, self.hiMidPoint, self.threshGridStep, self.percCorrTracked, self.lapseRate, self.nTrialsTF]
            self.paradigmFieldLabelList = [self.psyFunSlopeLabel, self.loMidPointLabel, self.hiMidPointLabel, self.threshGridStepLabel, self.percCorrTrackedLabel, self.lapseRateLabel, self.nTrialsLabel]
            self.paradigmFieldCheckBoxList = [self.psyFunSlopeCheckBox, self.loMidPointCheckBox, self.hiMidPointCheckBox, self.threshGridStepCheckBox, self.percCorrTrackedCheckBox, self.lapseRateCheckBox, self.nTrialsCheckBox]


        if self.currParadigm in [self.tr("PSI")]:
            n = 0
            priorOptions = ["Uniform", "Normal", "Gamma"]
            psyFunOptions = ["Logistic", "Gaussian", "Gumbel", "Weibull"]
            # n = n+1
            self.psyFunChooserLabel = QLabel(self.tr("Psychometric Function:"), self)
            self.paradigm_widg_sizer.addWidget(self.psyFunChooserLabel, n, 1)
            self.psyFunChooser = QComboBox()
            self.psyFunChooser.addItems(psyFunOptions)
            self.paradigm_widg_sizer.addWidget(self.psyFunChooser, n, 2)
            self.psyFunCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.psyFunCheckBox, n, 0)

            self.stimScalingChooserLabel = QLabel(self.tr("Stim. Scaling:"), self)
            self.paradigm_widg_sizer.addWidget(self.stimScalingChooserLabel, n, 4)
            self.stimScalingChooser = QComboBox()
            self.stimScalingChooser.addItems(["Linear", "Logarithmic"])
            self.paradigm_widg_sizer.addWidget(self.stimScalingChooser, n, 5)
            self.stimScalingCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.stimScalingCheckBox, n, 3)
            self.stimScalingChooser.textActivated[str].connect(self.onStimScalingChooserChange)

            self.nTrialsLabel = QLabel(self.tr("No. Trials"), self)
            self.paradigm_widg_sizer.addWidget(self.nTrialsLabel, n, 7)
            self.nTrialsTF = QLineEdit()
            self.nTrialsTF.setText("100")
            self.nTrialsTF.setValidator(QIntValidator(self))
            self.paradigm_widg_sizer.addWidget(self.nTrialsTF, n, 8)
            self.nTrialsCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.nTrialsCheckBox, n, 6)

            n = n+1

            #min midpoint
            self.loStimLabel = QLabel(self.tr("Stim. Min"), self)
            self.paradigm_widg_sizer.addWidget(self.loStimLabel, n, 1)
            self.loStim = QLineEdit()
            self.loStim.setText('0.5')
            self.loStim.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.loStim, n, 2)
            self.loStimCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.loStimCheckBox, n, 0)
            #n = n+1
            #max midpoint
            self.hiStimLabel = QLabel(self.tr("Stim. Max"), self)
            self.paradigm_widg_sizer.addWidget(self.hiStimLabel, n, 4)
            self.hiStim = QLineEdit()
            self.hiStim.setText('40')
            self.hiStim.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.hiStim, n, 5)
            self.hiStimCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.hiStimCheckBox, n, 3)
            # midpoint step
            self.stimGridStepLabel = QLabel(self.tr("Stim. Step"), self)
            self.paradigm_widg_sizer.addWidget(self.stimGridStepLabel, n, 7)
            self.stimGridStep = QLineEdit()
            self.stimGridStep.setText('0.5')
            self.stimGridStep.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.stimGridStep, n, 8)
            self.stimGridStepCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.stimGridStepCheckBox, n, 6)
            n = n+1
            #min midpoint
            self.loMidPointLabel = QLabel(self.tr("Mid Point Min"), self)
            self.paradigm_widg_sizer.addWidget(self.loMidPointLabel, n, 1)
            self.loMidPoint = QLineEdit()
            self.loMidPoint.setText('2')
            self.loMidPoint.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.loMidPoint, n, 2)
            self.loMidPointCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.loMidPointCheckBox, n, 0)
            #n = n+1
            #max midpoint
            self.hiMidPointLabel = QLabel(self.tr("Mid Point Max"), self)
            self.paradigm_widg_sizer.addWidget(self.hiMidPointLabel, n, 4)
            self.hiMidPoint = QLineEdit()
            self.hiMidPoint.setText('20')
            self.hiMidPoint.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.hiMidPoint, n, 5)
            self.hiMidPointCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.hiMidPointCheckBox, n, 3)
            # midpoint step
            self.threshGridStepLabel = QLabel(self.tr("Mid Point Step"), self)
            self.paradigm_widg_sizer.addWidget(self.threshGridStepLabel, n, 7)
            self.threshGridStep = QLineEdit()
            self.threshGridStep.setText('0.5')
            self.threshGridStep.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.threshGridStep, n, 8)
            self.threshGridStepCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.threshGridStepCheckBox, n, 6)
            n = n+1
            # thresh prior
            self.threshPriorChooserLabel = QLabel(self.tr("Mid Point Prior:"), self)
            self.paradigm_widg_sizer.addWidget(self.threshPriorChooserLabel, n, 1)
            self.threshPriorChooser = QComboBox()
            self.threshPriorChooser.addItems(priorOptions)
            self.paradigm_widg_sizer.addWidget(self.threshPriorChooser, n, 2)
            self.threshPriorChooser.textActivated[str].connect(self.onChangeThreshPrior)
            self.threshPriorChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.threshPriorChooserCheckBox, n, 0)
            # thres priro mu
            self.threshPriorMuLabel = QLabel(self.tr("Mid Point mu"), self)
            self.paradigm_widg_sizer.addWidget(self.threshPriorMuLabel, n, 4)
            self.threshPriorMu = QLineEdit()
            self.threshPriorMu.setText('0.001')
            self.threshPriorMu.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.threshPriorMu, n, 5)
            self.threshPriorMuCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.threshPriorMuCheckBox, n, 3)
            # thresh prior sd
            self.threshPriorSTDLabel = QLabel(self.tr("Mid Point STD"), self)
            self.paradigm_widg_sizer.addWidget(self.threshPriorSTDLabel, n, 7)
            self.threshPriorSTD = QLineEdit()
            self.threshPriorSTD.setText('1.1')
            self.threshPriorSTD.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.threshPriorSTD, n, 8)
            self.threshPriorSTDCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.threshPriorSTDCheckBox, n, 6)
            n = n+1
            
            #min slope
            self.loSlopeLabel = QLabel(self.tr("Slope Min"), self)
            self.paradigm_widg_sizer.addWidget(self.loSlopeLabel, n, 1)
            self.loSlope = QLineEdit()
            self.loSlope.setText('0.1')
            self.loSlope.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.loSlope, n, 2)
            self.loSlopeCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.loSlopeCheckBox, n, 0)
            #slope max
            self.hiSlopeLabel = QLabel(self.tr("Slope Max"), self)
            self.paradigm_widg_sizer.addWidget(self.hiSlopeLabel, n, 4)
            self.hiSlope = QLineEdit()
            self.hiSlope.setText('10')
            self.hiSlope.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.hiSlope, n, 5)
            self.hiSlopeCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.hiSlopeCheckBox, n, 3)
            #slope step
            self.slopeGridStepLabel = QLabel(self.tr("Slope Step"), self)
            self.paradigm_widg_sizer.addWidget(self.slopeGridStepLabel, n, 7)
            self.slopeGridStep = QLineEdit()
            self.slopeGridStep.setText('0.1')
            self.slopeGridStep.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.slopeGridStep, n, 8)
            self.slopeGridStepCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.slopeGridStepCheckBox, n, 6)
            n = n+1
            self.slopeSpacingChooserLabel = QLabel(self.tr("Slope Spacing:"), self)
            self.paradigm_widg_sizer.addWidget(self.slopeSpacingChooserLabel, n, 1)
            self.slopeSpacingChooser = QComboBox()
            self.slopeSpacingChooser.addItems(["Linear", "Logarithmic"])
            self.paradigm_widg_sizer.addWidget(self.slopeSpacingChooser, n, 2)
            self.slopeSpacingChooser.textActivated[str].connect(self.onSlopeSpacingChooserChange)
            self.slopeSpacingChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.slopeSpacingChooserCheckBox, n, 0)

            n = n+1
            # slope prior
            self.slopePriorChooserLabel = QLabel(self.tr("Slope Prior:"), self)
            self.paradigm_widg_sizer.addWidget(self.slopePriorChooserLabel, n, 1)
            self.slopePriorChooser = QComboBox()
            self.slopePriorChooser.addItems(priorOptions)
            self.paradigm_widg_sizer.addWidget(self.slopePriorChooser, n, 2)
            self.slopePriorChooser.textActivated[str].connect(self.onChangeSlopePrior)
            self.slopePriorChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.slopePriorChooserCheckBox, n, 0)
            # thres priro mu
            self.slopePriorMuLabel = QLabel(self.tr("Slope mu"), self)
            self.paradigm_widg_sizer.addWidget(self.slopePriorMuLabel, n, 4)
            self.slopePriorMu = QLineEdit()
            self.slopePriorMu.setText('1.1')
            self.slopePriorMu.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.slopePriorMu, n, 5)
            self.slopePriorMuCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.slopePriorMuCheckBox, n, 3)
            # slope prior sd
            self.slopePriorSTDLabel = QLabel(self.tr("Slope STD"), self)
            self.paradigm_widg_sizer.addWidget(self.slopePriorSTDLabel, n, 7)
            self.slopePriorSTD = QLineEdit()
            self.slopePriorSTD.setText('1.1')
            self.slopePriorSTD.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.slopePriorSTD, n, 8)
            self.slopePriorSTDCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.slopePriorSTDCheckBox, n, 6)
            n = n+1

            #min lapse
            self.loLapseLabel = QLabel(self.tr("Lapse Min"), self)
            self.paradigm_widg_sizer.addWidget(self.loLapseLabel, n, 1)
            self.loLapse = QLineEdit()
            self.loLapse.setText('0')
            self.loLapse.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.loLapse, n, 2)
            self.loLapseCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.loLapseCheckBox, n, 0)
            #max lapse
            self.hiLapseLabel = QLabel(self.tr("Lapse Max"), self)
            self.paradigm_widg_sizer.addWidget(self.hiLapseLabel, n, 4)
            self.hiLapse = QLineEdit()
            self.hiLapse.setText('0.2')
            self.hiLapse.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.hiLapse, n, 5)
            self.hiLapseCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.hiLapseCheckBox, n, 3)
            #lapse step
            self.lapseGridStepLabel = QLabel(self.tr("Lapse Step"), self)
            self.paradigm_widg_sizer.addWidget(self.lapseGridStepLabel, n, 7)
            self.lapseGridStep = QLineEdit()
            self.lapseGridStep.setText('0.01')
            self.lapseGridStep.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.lapseGridStep, n, 8)
            self.lapseGridStepCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.lapseGridStepCheckBox, n, 6)
            n = n+1
            self.lapseSpacingChooserLabel = QLabel(self.tr("Lapse Spacing:"), self)
            self.paradigm_widg_sizer.addWidget(self.lapseSpacingChooserLabel, n, 1)
            self.lapseSpacingChooser = QComboBox()
            self.lapseSpacingChooser.addItems(["Linear", "Logarithmic"])
            self.paradigm_widg_sizer.addWidget(self.lapseSpacingChooser, n, 2)
            self.lapseSpacingChooser.textActivated[str].connect(self.onLapseSpacingChooserChange)
            self.lapseSpacingChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.lapseSpacingChooserCheckBox, n, 0)
            n = n+1
            # lapse prior
            self.lapsePriorChooserLabel = QLabel(self.tr("Lapse Prior:"), self)
            self.paradigm_widg_sizer.addWidget(self.lapsePriorChooserLabel, n, 1)
            self.lapsePriorChooser = QComboBox()
            self.lapsePriorChooser.addItems(priorOptions)
            self.paradigm_widg_sizer.addWidget(self.lapsePriorChooser, n, 2)
            self.lapsePriorChooser.textActivated[str].connect(self.onChangeLapsePrior)
            self.lapsePriorChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.lapsePriorChooserCheckBox, n, 0)
            # lapse priro mu
            self.lapsePriorMuLabel = QLabel(self.tr("Lapse mu"), self)
            self.paradigm_widg_sizer.addWidget(self.lapsePriorMuLabel, n, 4)
            self.lapsePriorMu = QLineEdit()
            self.lapsePriorMu.setText('0.01')
            self.lapsePriorMu.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.lapsePriorMu, n, 5)
            self.lapsePriorMuCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.lapsePriorMuCheckBox, n, 3)
            # lapse prior sd
            self.lapsePriorSTDLabel = QLabel(self.tr("Lapse STD"), self)
            self.paradigm_widg_sizer.addWidget(self.lapsePriorSTDLabel, n, 7)
            self.lapsePriorSTD = QLineEdit()
            self.lapsePriorSTD.setText('1.1')
            self.lapsePriorSTD.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.lapsePriorSTD, n, 8)
            self.lapsePriorSTDCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.lapsePriorSTDCheckBox, n, 6)
            n = n+1
         

            self.margLapseChooserLabel = QLabel(self.tr("Marginalize Lapse:"), self)
            self.paradigm_widg_sizer.addWidget(self.margLapseChooserLabel, n, 1)
            self.margLapseChooser = QComboBox()
            self.margLapseChooser.addItems(["No", "Yes"])
            self.paradigm_widg_sizer.addWidget(self.margLapseChooser, n, 2)
            self.margLapseChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.margLapseChooserCheckBox, n, 0)

            self.startLevelChooserLabel = QLabel(self.tr("Start Level:"), self)
            self.paradigm_widg_sizer.addWidget(self.startLevelChooserLabel, n, 4)
            self.startLevelChooser = QComboBox()
            self.startLevelChooser.addItems(["Auto", "Suggested"])
            self.paradigm_widg_sizer.addWidget(self.startLevelChooser, n, 5)
            self.startLevelChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.startLevelChooserCheckBox, n, 3)
            self.startLevelChooserLabel.hide()
            self.startLevelChooser.hide()
            self.startLevelChooserCheckBox.hide()

            self.PSIParSpacePlotButton = QPushButton(self.tr("Plot PSI Par. Space"))
            self.PSIParSpacePlotButton.clicked.connect(self.onClickPSIParSpacePlotButton)
            self.PSIParSpacePlotButton.setIcon(QIcon.fromTheme("office-chart-line-stacked", QIcon(":/office-chart-line_stacked")))
            #self.PSIParSpacePlotButton.setIconSize(QtCore.QSize(min_pw_icon_size, min_pw_icon_size))
            self.PSIParSpacePlotButton.setToolTip(self.tr("Plot PSI parameter space"))
            self.paradigm_widg_sizer.addWidget(self.PSIParSpacePlotButton, n, 8)
            if matplotlib_available == False:
                self.PSIParSpacePlotButton.hide()
            
            n = n+1
            self.margSlopeChooserLabel = QLabel(self.tr("Marginalize Slope:"), self)
            self.paradigm_widg_sizer.addWidget(self.margSlopeChooserLabel, n, 1)
            self.margSlopeChooser = QComboBox()
            self.margSlopeChooser.addItems(["No", "Yes"])
            self.paradigm_widg_sizer.addWidget(self.margSlopeChooser, n, 2)
            self.margSlopeChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.margSlopeChooserCheckBox, n, 0)
            n = n+1
            self.margThreshChooserLabel = QLabel(self.tr("Marginalize Mid Point:"), self)
            self.paradigm_widg_sizer.addWidget(self.margThreshChooserLabel, n, 1)
            self.margThreshChooser = QComboBox()
            self.margThreshChooser.addItems(["No", "Yes"])
            self.paradigm_widg_sizer.addWidget(self.margThreshChooser, n, 2)
            self.margThreshChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.margThreshChooserCheckBox, n, 0)
            n = n+1
            
          

 
         

            self.paradigmChooserList = [self.threshPriorChooser,
                                        self.slopePriorChooser,
                                        self.lapsePriorChooser,
                                        self.psyFunChooser,
                                        self.stimScalingChooser,
                                        self.margLapseChooser,
                                        self.margSlopeChooser,
                                        self.margThreshChooser,
                                        self.startLevelChooser,
                                        self.slopeSpacingChooser,
                                        self.lapseSpacingChooser]
            self.paradigmChooserLabelList = [self.threshPriorChooserLabel,
                                             self.slopePriorChooserLabel,
                                             self.lapsePriorChooserLabel,
                                             self.psyFunChooserLabel,
                                             self.stimScalingChooserLabel,
                                             self.margLapseChooserLabel,
                                             self.margSlopeChooserLabel,
                                             self.margThreshChooserLabel,
                                             self.startLevelChooserLabel,
                                             self.slopeSpacingChooserLabel,
                                             self.lapseSpacingChooserLabel]
            self.paradigmChooserOptionsList = [priorOptions,
                                               priorOptions,
                                               priorOptions,
                                               psyFunOptions,
                                               ["Linear", "Logarithmic"],
                                               ["No", "Yes"],
                                               ["No", "Yes"],
                                               ["No", "Yes"],
                                               ["Auto", "Suggested"],
                                               ["Linear", "Logarithmic"],
                                               ["Linear", "Logarithmic"]]
            self.paradigmChooserCheckBoxList = [self.threshPriorChooserCheckBox,
                                                self.slopePriorChooserCheckBox,
                                                self.lapsePriorChooserCheckBox,
                                                self.psyFunCheckBox,
                                                self.stimScalingCheckBox,
                                                self.margLapseChooserCheckBox,
                                                self.margSlopeChooserCheckBox,
                                                self.margThreshChooserCheckBox,
                                                self.startLevelChooserCheckBox,
                                                self.slopeSpacingChooserCheckBox,
                                                self.lapseSpacingChooserCheckBox]

            self.paradigmFieldList = [self.loStim, self.hiStim, self.stimGridStep,
                                      self.loMidPoint, self.hiMidPoint, self.threshGridStep,
                                      self.loSlope, self.hiSlope, self.slopeGridStep,
                                      self.loLapse, self.hiLapse, self.lapseGridStep,
                                      self.threshPriorMu, self.threshPriorSTD,
                                      self.slopePriorMu, self.slopePriorSTD,
                                      self.lapsePriorMu, self.lapsePriorSTD,
                                      self.nTrialsTF]
            self.paradigmFieldLabelList = [self.loStimLabel, self.hiStimLabel, self.stimGridStepLabel,
                                           self.loMidPointLabel, self.hiMidPointLabel, self.threshGridStepLabel,
                                           self.loSlopeLabel, self.hiSlopeLabel, self.slopeGridStepLabel,
                                           self.loLapseLabel, self.hiLapseLabel, self.lapseGridStepLabel,
                                           self.threshPriorMuLabel, self.threshPriorSTDLabel,
                                           self.slopePriorMuLabel, self.slopePriorSTDLabel,
                                           self.lapsePriorMuLabel, self.lapsePriorSTDLabel,
                                           self.nTrialsLabel]
            self.paradigmFieldCheckBoxList = [self.loStimCheckBox, self.hiStimCheckBox, self.stimGridStepCheckBox,
                                              self.loMidPointCheckBox, self.hiMidPointCheckBox, self.threshGridStepCheckBox,
                                              self.loSlopeCheckBox, self.hiSlopeCheckBox, self.slopeGridStepCheckBox,
                                              self.loLapseCheckBox, self.hiLapseCheckBox, self.lapseGridStepCheckBox,
                                              self.threshPriorMuCheckBox, self.threshPriorSTDCheckBox,
                                              self.slopePriorMuCheckBox, self.slopePriorSTDCheckBox,
                                              self.lapsePriorMuCheckBox, self.lapsePriorSTDCheckBox,
                                              self.nTrialsCheckBox]
            self.paradigmButtonList = [self.PSIParSpacePlotButton]
            
            self.onChangeThreshPrior()
            self.onChangeSlopePrior()
            self.onChangeLapsePrior()

        # for i in range(self.responseModeChooser.count()):
        #     self.responseModeChooser.removeItem(0)
        # if self.currParadigm in [self.tr("Transformed Up-Down"), self.tr("Weighted Up-Down"),
        #                          self.tr("Transformed Up-Down Limited"), self.tr("Weighted Up-Down Limited"),
        #                          self.tr("Transformed Up-Down Interleaved"), self.tr("Weighted Up-Down Interleaved"),
        #                          self.tr("PEST"), self.tr("Maximum Likelihood"), self.tr("PSI")]:
        #     self.prm['responseModeChoices'] = ["Real Listener", "Automatic", "Simulated Listener", "Psychometric"]
        # else:
        #     self.prm['responseModeChoices'] = ["Real Listener", "Automatic", "Simulated Listener"]
        # self.responseModeChooser.addItems(self.prm['responseModeChoices'])
        if self.currParadigm in [self.tr("UML")]:
            n = 0
            priorOptions = [self.tr("Uniform"), self.tr("Normal"), self.tr("Gamma")]
            lambdaPriorOptions = [self.tr("Uniform"), self.tr("Normal"), self.tr("Gamma"), self.tr("Beta"), self.tr("Generalized Beta")]
            psyFunOptions = [self.tr("Logistic"), self.tr("Gaussian"), self.tr("Weibull")]
            # n = n+1
            self.psyFunChooserLabel = QLabel(self.tr("Psychometric Function:"), self)
            self.paradigm_widg_sizer.addWidget(self.psyFunChooserLabel, n, 1)
            self.psyFunChooser = QComboBox()
            self.psyFunChooser.addItems(psyFunOptions)
            self.paradigm_widg_sizer.addWidget(self.psyFunChooser, n, 2)
            self.psyFunCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.psyFunCheckBox, n, 0)

            self.psyFunPostSummChooserLabel = QLabel(self.tr("Posterior Summary:"), self)
            self.paradigm_widg_sizer.addWidget(self.psyFunPostSummChooserLabel, n, 4)
            self.psyFunPostSummChooser = QComboBox()
            self.psyFunPostSummChooser.addItems(["Mean", "Mode"])
            self.paradigm_widg_sizer.addWidget(self.psyFunPostSummChooser, n, 5)
            self.psyFunPostSummCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.psyFunPostSummCheckBox, n, 3)

            self.UMLParSpacePlotButton = QPushButton(self.tr("Plot UML Par. Space"))
            self.UMLParSpacePlotButton.clicked.connect(self.onClickUMLParSpacePlotButton)
            self.UMLParSpacePlotButton.setIcon(QIcon.fromTheme("office-chart-line-stacked", QIcon(":/office-chart-line_stacked")))
            #self.UMLParSpacePlotButton.setIconSize(QtCore.QSize(min_pw_icon_size, min_pw_icon_size))
            self.UMLParSpacePlotButton.setToolTip(self.tr("Plot UML parameter space"))
            self.paradigm_widg_sizer.addWidget(self.UMLParSpacePlotButton, n, 8)
            if matplotlib_available == False:
                self.UMLParSpacePlotButton.hide()

            n = n+1

            self.nTrialsLabel = QLabel(self.tr("No. Trials"), self)
            self.paradigm_widg_sizer.addWidget(self.nTrialsLabel, n, 1)
            self.nTrialsTF = QLineEdit()
            self.nTrialsTF.setText("100")
            self.nTrialsTF.setValidator(QIntValidator(self))
            self.paradigm_widg_sizer.addWidget(self.nTrialsTF, n, 2)
            self.nTrialsCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.nTrialsCheckBox, n, 0)

            self.swptRuleChooserLabel = QLabel(self.tr("Swpt. Rule:"), self)
            self.paradigm_widg_sizer.addWidget(self.swptRuleChooserLabel, n, 4)
            self.swptRuleChooser = QComboBox()
            self.swptRuleChooser.addItems(["Up-Down", "Random"])
            self.paradigm_widg_sizer.addWidget(self.swptRuleChooser, n, 5)
            self.swptRuleChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.swptRuleChooserCheckBox, n, 3)
            self.swptRuleChooser.textActivated[str].connect(self.onChangeSwptRule)
            
            self.ruleDownLabel = QLabel(self.tr("Rule Down"), self)
            self.paradigm_widg_sizer.addWidget(self.ruleDownLabel, n, 7)
            self.ruleDownTF = QLineEdit()
            self.ruleDownTF.setText('2')
            self.ruleDownTF.setValidator(QIntValidator(self))
            self.paradigm_widg_sizer.addWidget(self.ruleDownTF, n, 8)
            self.ruleDownCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.ruleDownCheckBox, n, 6)

            
            n = n+1

            #min stim
            self.loStimLabel = QLabel(self.tr("Stim. Min"), self)
            self.paradigm_widg_sizer.addWidget(self.loStimLabel, n, 1)
            self.loStim = QLineEdit()
            self.loStim.setText('0.5')
            self.loStim.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.loStim, n, 2)
            self.loStimCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.loStimCheckBox, n, 0)
            #n = n+1
            #max stim
            self.hiStimLabel = QLabel(self.tr("Stim. Max"), self)
            self.paradigm_widg_sizer.addWidget(self.hiStimLabel, n, 4)
            self.hiStim = QLineEdit()
            self.hiStim.setText('40')
            self.hiStim.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.hiStim, n, 5)
            self.hiStimCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.hiStimCheckBox, n, 3)

            self.stimScalingChooserLabel = QLabel(self.tr("Stim. Scaling:"), self)
            self.paradigm_widg_sizer.addWidget(self.stimScalingChooserLabel, n, 7)
            self.stimScalingChooser = QComboBox()
            self.stimScalingChooser.addItems(["Linear", "Logarithmic"])
            self.paradigm_widg_sizer.addWidget(self.stimScalingChooser, n, 8)
            self.stimScalingCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.stimScalingCheckBox, n, 6)
            self.stimScalingChooser.textActivated[str].connect(self.onStimScalingChooserChange)
            n = n+1
            self.suggestedLambdaSwptLabel = QLabel(self.tr("Suggested Lapse Swpt."))
            self.suggestedLambdaSwpt = QLineEdit("40")
            self.suggestedLambdaSwptCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.suggestedLambdaSwptLabel, n, 1)
            self.paradigm_widg_sizer.addWidget(self.suggestedLambdaSwpt, n, 2)
            self.paradigm_widg_sizer.addWidget(self.suggestedLambdaSwptCheckBox, n, 0)
            n = n+1
            self.lambdaSwptPCLabel = QLabel(self.tr("Pr. Corr. at Est. Lapse Swpt."))
            self.lambdaSwptPC = QLineEdit("0.99")
            self.lambdaSwptPCCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.lambdaSwptPCLabel, n, 1)
            self.paradigm_widg_sizer.addWidget(self.lambdaSwptPC, n, 2)
            self.paradigm_widg_sizer.addWidget(self.lambdaSwptPCCheckBox, n, 0)
            n = n+1
            #min midpoint
            self.loMidPointLabel = QLabel(self.tr("Mid Point Min"), self)
            self.paradigm_widg_sizer.addWidget(self.loMidPointLabel, n, 1)
            self.loMidPoint = QLineEdit()
            self.loMidPoint.setText('2')
            self.loMidPoint.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.loMidPoint, n, 2)
            self.loMidPointCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.loMidPointCheckBox, n, 0)
            #n = n+1
            #max midpoint
            self.hiMidPointLabel = QLabel(self.tr("Mid Point Max"), self)
            self.paradigm_widg_sizer.addWidget(self.hiMidPointLabel, n, 4)
            self.hiMidPoint = QLineEdit()
            self.hiMidPoint.setText('20')
            self.hiMidPoint.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.hiMidPoint, n, 5)
            self.hiMidPointCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.hiMidPointCheckBox, n, 3)
            # midpoint step
            self.threshGridStepLabel = QLabel(self.tr("Mid Point Step"), self)
            self.paradigm_widg_sizer.addWidget(self.threshGridStepLabel, n, 7)
            self.threshGridStep = QLineEdit()
            self.threshGridStep.setText('0.5')
            self.threshGridStep.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.threshGridStep, n, 8)
            self.threshGridStepCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.threshGridStepCheckBox, n, 6)
            n = n+1
            # thresh prior
            self.threshPriorChooserLabel = QLabel(self.tr("Mid Point Prior:"), self)
            self.paradigm_widg_sizer.addWidget(self.threshPriorChooserLabel, n, 1)
            self.threshPriorChooser = QComboBox()
            self.threshPriorChooser.addItems(priorOptions)
            self.paradigm_widg_sizer.addWidget(self.threshPriorChooser, n, 2)
            self.threshPriorChooser.textActivated[str].connect(self.onChangeThreshPrior)
            self.threshPriorChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.threshPriorChooserCheckBox, n, 0)
            # thres priro mu
            self.threshPriorMuLabel = QLabel(self.tr("Mid Point mu"), self)
            self.paradigm_widg_sizer.addWidget(self.threshPriorMuLabel, n, 4)
            self.threshPriorMu = QLineEdit()
            self.threshPriorMu.setText('0.001')
            self.threshPriorMu.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.threshPriorMu, n, 5)
            self.threshPriorMuCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.threshPriorMuCheckBox, n, 3)
            # thresh prior sd
            self.threshPriorSTDLabel = QLabel(self.tr("Mid Point STD"), self)
            self.paradigm_widg_sizer.addWidget(self.threshPriorSTDLabel, n, 7)
            self.threshPriorSTD = QLineEdit()
            self.threshPriorSTD.setText('1.1')
            self.threshPriorSTD.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.threshPriorSTD, n, 8)
            self.threshPriorSTDCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.threshPriorSTDCheckBox, n, 6)
            n = n+1
            
            #min slope
            self.loSlopeLabel = QLabel(self.tr("Slope Min"), self)
            self.paradigm_widg_sizer.addWidget(self.loSlopeLabel, n, 1)
            self.loSlope = QLineEdit()
            self.loSlope.setText('0.1')
            self.loSlope.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.loSlope, n, 2)
            self.loSlopeCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.loSlopeCheckBox, n, 0)
            #slope max
            self.hiSlopeLabel = QLabel(self.tr("Slope Max"), self)
            self.paradigm_widg_sizer.addWidget(self.hiSlopeLabel, n, 4)
            self.hiSlope = QLineEdit()
            self.hiSlope.setText('10')
            self.hiSlope.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.hiSlope, n, 5)
            self.hiSlopeCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.hiSlopeCheckBox, n, 3)
            #slope step
            self.slopeGridStepLabel = QLabel(self.tr("Slope Step"), self)
            self.paradigm_widg_sizer.addWidget(self.slopeGridStepLabel, n, 7)
            self.slopeGridStep = QLineEdit()
            self.slopeGridStep.setText('0.1')
            self.slopeGridStep.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.slopeGridStep, n, 8)
            self.slopeGridStepCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.slopeGridStepCheckBox, n, 6)
            n = n+1
            self.slopeSpacingChooserLabel = QLabel(self.tr("Slope Spacing:"), self)
            self.paradigm_widg_sizer.addWidget(self.slopeSpacingChooserLabel, n, 1)
            self.slopeSpacingChooser = QComboBox()
            self.slopeSpacingChooser.addItems(["Linear", "Logarithmic"])
            self.paradigm_widg_sizer.addWidget(self.slopeSpacingChooser, n, 2)
            self.slopeSpacingChooser.textActivated[str].connect(self.onSlopeSpacingChooserChange)
            self.slopeSpacingChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.slopeSpacingChooserCheckBox, n, 0)
            n = n+1
            # slope prior
            self.slopePriorChooserLabel = QLabel(self.tr("Slope Prior:"), self)
            self.paradigm_widg_sizer.addWidget(self.slopePriorChooserLabel, n, 1)
            self.slopePriorChooser = QComboBox()
            self.slopePriorChooser.addItems(priorOptions)
            self.paradigm_widg_sizer.addWidget(self.slopePriorChooser, n, 2)
            self.slopePriorChooser.textActivated[str].connect(self.onChangeSlopePrior)
            self.slopePriorChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.slopePriorChooserCheckBox, n, 0)
            # thres priro mu
            self.slopePriorMuLabel = QLabel(self.tr("Slope mu"), self)
            self.paradigm_widg_sizer.addWidget(self.slopePriorMuLabel, n, 4)
            self.slopePriorMu = QLineEdit()
            self.slopePriorMu.setText('1.1')
            self.slopePriorMu.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.slopePriorMu, n, 5)
            self.slopePriorMuCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.slopePriorMuCheckBox, n, 3)
            # slope prior sd
            self.slopePriorSTDLabel = QLabel(self.tr("Slope STD"), self)
            self.paradigm_widg_sizer.addWidget(self.slopePriorSTDLabel, n, 7)
            self.slopePriorSTD = QLineEdit()
            self.slopePriorSTD.setText('1.1')
            self.slopePriorSTD.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.slopePriorSTD, n, 8)
            self.slopePriorSTDCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.slopePriorSTDCheckBox, n, 6)
            n = n+1

            #min lapse
            self.loLapseLabel = QLabel(self.tr("Lapse Min"), self)
            self.paradigm_widg_sizer.addWidget(self.loLapseLabel, n, 1)
            self.loLapse = QLineEdit()
            self.loLapse.setText('0')
            self.loLapse.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.loLapse, n, 2)
            self.loLapseCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.loLapseCheckBox, n, 0)
            #max lapse
            self.hiLapseLabel = QLabel(self.tr("Lapse Max"), self)
            self.paradigm_widg_sizer.addWidget(self.hiLapseLabel, n, 4)
            self.hiLapse = QLineEdit()
            self.hiLapse.setText('0.2')
            self.hiLapse.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.hiLapse, n, 5)
            self.hiLapseCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.hiLapseCheckBox, n, 3)
            #lapse step
            self.lapseGridStepLabel = QLabel(self.tr("Lapse Step"), self)
            self.paradigm_widg_sizer.addWidget(self.lapseGridStepLabel, n, 7)
            self.lapseGridStep = QLineEdit()
            self.lapseGridStep.setText('0.01')
            self.lapseGridStep.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.lapseGridStep, n, 8)
            self.lapseGridStepCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.lapseGridStepCheckBox, n, 6)
            n = n+1
            self.lapseSpacingChooserLabel = QLabel(self.tr("Lapse Spacing:"), self)
            self.paradigm_widg_sizer.addWidget(self.lapseSpacingChooserLabel, n, 1)
            self.lapseSpacingChooser = QComboBox()
            self.lapseSpacingChooser.addItems(["Linear", "Logarithmic"])
            self.paradigm_widg_sizer.addWidget(self.lapseSpacingChooser, n, 2)
            self.lapseSpacingChooser.textActivated[str].connect(self.onLapseSpacingChooserChange)
            self.lapseSpacingChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.lapseSpacingChooserCheckBox, n, 0)
            n = n+1
            # lapse prior
            self.lapsePriorChooserLabel = QLabel(self.tr("Lapse Prior:"), self)
            self.paradigm_widg_sizer.addWidget(self.lapsePriorChooserLabel, n, 1)
            self.lapsePriorChooser = QComboBox()
            self.lapsePriorChooser.addItems(lambdaPriorOptions)
            self.paradigm_widg_sizer.addWidget(self.lapsePriorChooser, n, 2)
            self.lapsePriorChooser.textActivated[str].connect(self.onChangeLapsePrior)
            self.lapsePriorChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.lapsePriorChooserCheckBox, n, 0)
            # lapse priro mu
            self.lapsePriorMuLabel = QLabel(self.tr("Lapse mu"), self)
            self.paradigm_widg_sizer.addWidget(self.lapsePriorMuLabel, n, 4)
            self.lapsePriorMu = QLineEdit()
            self.lapsePriorMu.setText('0.01')
            self.lapsePriorMu.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.lapsePriorMu, n, 5)
            self.lapsePriorMuCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.lapsePriorMuCheckBox, n, 3)
            # lapse prior sd
            self.lapsePriorSTDLabel = QLabel(self.tr("Lapse STD"), self)
            self.paradigm_widg_sizer.addWidget(self.lapsePriorSTDLabel, n, 7)
            self.lapsePriorSTD = QLineEdit()
            self.lapsePriorSTD.setText('1.1')
            self.lapsePriorSTD.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.lapsePriorSTD, n, 8)
            self.lapsePriorSTDCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.lapsePriorSTDCheckBox, n, 6)
            n = n+1
            # load state
            self.loadStateChooserLabel = QLabel(self.tr("Load UML state from prev. blocks:"), self)
            self.paradigm_widg_sizer.addWidget(self.loadStateChooserLabel, n, 1)
            self.loadStateChooser = QComboBox()
            self.loadStateChooser.setCurrentIndex(1)
            self.loadStateChooser.addItems(["Yes", "No"])
            self.paradigm_widg_sizer.addWidget(self.loadStateChooser, n, 2)
            self.loadStateChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.loadStateChooserCheckBox, n, 0)
            
            self.paradigmChooserList = [self.threshPriorChooser,
                                        self.slopePriorChooser,
                                        self.lapsePriorChooser,
                                        self.psyFunChooser,
                                        self.psyFunPostSummChooser,
                                        self.swptRuleChooser,
                                        self.stimScalingChooser,
                                        self.slopeSpacingChooser,
                                        self.lapseSpacingChooser,
                                        self.loadStateChooser]
            self.paradigmChooserLabelList = [self.threshPriorChooserLabel,
                                             self.slopePriorChooserLabel,
                                             self.lapsePriorChooserLabel,
                                             self.psyFunChooserLabel,
                                             self.psyFunPostSummChooserLabel,
                                             self.swptRuleChooserLabel,
                                             self.stimScalingChooserLabel,
                                             self.slopeSpacingChooserLabel,
                                             self.lapseSpacingChooserLabel,
                                             self.loadStateChooserLabel]
            self.paradigmChooserOptionsList = [priorOptions,
                                               priorOptions,
                                               lambdaPriorOptions,
                                               psyFunOptions,
                                               [self.tr("Mean"), self.tr("Mode")],
                                               [self.tr("Up-Down"), self.tr("Random")],
                                               [self.tr("Linear"), self.tr("Logarithmic")],
                                               [self.tr("Linear"), self.tr("Logarithmic")],
                                               [self.tr("Linear"), self.tr("Logarithmic")],
                                               ["Yes", "No"]]
            self.paradigmChooserCheckBoxList = [self.threshPriorChooserCheckBox,
                                                self.slopePriorChooserCheckBox,
                                                self.lapsePriorChooserCheckBox,
                                                self.psyFunCheckBox,
                                                self.psyFunPostSummCheckBox,
                                                self.swptRuleChooserCheckBox,
                                                self.stimScalingCheckBox,
                                                self.slopeSpacingChooserCheckBox,
                                                self.lapseSpacingChooserCheckBox,
                                                self.loadStateChooserCheckBox]

            self.paradigmFieldList = [self.loStim, self.hiStim, self.suggestedLambdaSwpt,
                                      self.lambdaSwptPC, self.ruleDownTF,
                                      self.loMidPoint, self.hiMidPoint, self.threshGridStep,
                                      self.loSlope, self.hiSlope, self.slopeGridStep,
                                      self.loLapse, self.hiLapse, self.lapseGridStep,
                                      self.threshPriorMu, self.threshPriorSTD,
                                      self.slopePriorMu, self.slopePriorSTD,
                                      self.lapsePriorMu, self.lapsePriorSTD,
                                      self.nTrialsTF]
            self.paradigmFieldLabelList = [self.loStimLabel, self.hiStimLabel, self.suggestedLambdaSwptLabel,
                                           self.lambdaSwptPCLabel, self.ruleDownLabel,
                                           self.loMidPointLabel, self.hiMidPointLabel, self.threshGridStepLabel,
                                           self.loSlopeLabel, self.hiSlopeLabel, self.slopeGridStepLabel,
                                           self.loLapseLabel, self.hiLapseLabel, self.lapseGridStepLabel,
                                           self.threshPriorMuLabel, self.threshPriorSTDLabel,
                                           self.slopePriorMuLabel, self.slopePriorSTDLabel,
                                           self.lapsePriorMuLabel, self.lapsePriorSTDLabel,
                                           self.nTrialsLabel]
            self.paradigmFieldCheckBoxList = [self.loStimCheckBox, self.hiStimCheckBox, self.suggestedLambdaSwptCheckBox,
                                              self.lambdaSwptPCCheckBox, self.ruleDownCheckBox,
                                              self.loMidPointCheckBox, self.hiMidPointCheckBox, self.threshGridStepCheckBox,
                                              self.loSlopeCheckBox, self.hiSlopeCheckBox, self.slopeGridStepCheckBox,
                                              self.loLapseCheckBox, self.hiLapseCheckBox, self.lapseGridStepCheckBox,
                                              self.threshPriorMuCheckBox, self.threshPriorSTDCheckBox,
                                              self.slopePriorMuCheckBox, self.slopePriorSTDCheckBox,
                                              self.lapsePriorMuCheckBox, self.lapsePriorSTDCheckBox,
                                              self.nTrialsCheckBox]
            self.paradigmButtonList = [self.UMLParSpacePlotButton]
            self.onChangeThreshPrior()
            self.onChangeSlopePrior()
            self.onChangeLapsePrior()
            self.onChangeSwptRule()

        #PSI guess
        if self.currParadigm in [self.tr("PSI - Est. Guess Rate")]:
            n = 0
            priorOptions = ["Uniform", "Normal", "Gamma"]
            psyFunOptions = ["Logistic", "Gaussian", "Gumbel", "Weibull"]
            # n = n+1
            self.psyFunChooserLabel = QLabel(self.tr("Psychometric Function:"), self)
            self.paradigm_widg_sizer.addWidget(self.psyFunChooserLabel, n, 1)
            self.psyFunChooser = QComboBox()
            self.psyFunChooser.addItems(psyFunOptions)
            self.paradigm_widg_sizer.addWidget(self.psyFunChooser, n, 2)
            self.psyFunCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.psyFunCheckBox, n, 0)

            self.stimScalingChooserLabel = QLabel(self.tr("Stim. Scaling:"), self)
            self.paradigm_widg_sizer.addWidget(self.stimScalingChooserLabel, n, 4)
            self.stimScalingChooser = QComboBox()
            self.stimScalingChooser.addItems(["Linear", "Logarithmic"])
            self.paradigm_widg_sizer.addWidget(self.stimScalingChooser, n, 5)
            self.stimScalingCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.stimScalingCheckBox, n, 3)
            self.stimScalingChooser.textActivated[str].connect(self.onStimScalingChooserChange)

            self.nTrialsLabel = QLabel(self.tr("No. Trials"), self)
            self.paradigm_widg_sizer.addWidget(self.nTrialsLabel, n, 7)
            self.nTrialsTF = QLineEdit()
            self.nTrialsTF.setText("100")
            self.nTrialsTF.setValidator(QIntValidator(self))
            self.paradigm_widg_sizer.addWidget(self.nTrialsTF, n, 8)
            self.nTrialsCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.nTrialsCheckBox, n, 6)

            n = n+1

            #min midpoint
            self.loStimLabel = QLabel(self.tr("Stim. Min"), self)
            self.paradigm_widg_sizer.addWidget(self.loStimLabel, n, 1)
            self.loStim = QLineEdit()
            self.loStim.setText('0.5')
            self.loStim.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.loStim, n, 2)
            self.loStimCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.loStimCheckBox, n, 0)
            #n = n+1
            #max midpoint
            self.hiStimLabel = QLabel(self.tr("Stim. Max"), self)
            self.paradigm_widg_sizer.addWidget(self.hiStimLabel, n, 4)
            self.hiStim = QLineEdit()
            self.hiStim.setText('40')
            self.hiStim.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.hiStim, n, 5)
            self.hiStimCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.hiStimCheckBox, n, 3)
            # midpoint step
            self.stimGridStepLabel = QLabel(self.tr("Stim. Step"), self)
            self.paradigm_widg_sizer.addWidget(self.stimGridStepLabel, n, 7)
            self.stimGridStep = QLineEdit()
            self.stimGridStep.setText('0.5')
            self.stimGridStep.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.stimGridStep, n, 8)
            self.stimGridStepCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.stimGridStepCheckBox, n, 6)
            n = n+1
            #min midpoint
            self.loMidPointLabel = QLabel(self.tr("Mid Point Min"), self)
            self.paradigm_widg_sizer.addWidget(self.loMidPointLabel, n, 1)
            self.loMidPoint = QLineEdit()
            self.loMidPoint.setText('2')
            self.loMidPoint.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.loMidPoint, n, 2)
            self.loMidPointCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.loMidPointCheckBox, n, 0)
            #n = n+1
            #max midpoint
            self.hiMidPointLabel = QLabel(self.tr("Mid Point Max"), self)
            self.paradigm_widg_sizer.addWidget(self.hiMidPointLabel, n, 4)
            self.hiMidPoint = QLineEdit()
            self.hiMidPoint.setText('20')
            self.hiMidPoint.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.hiMidPoint, n, 5)
            self.hiMidPointCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.hiMidPointCheckBox, n, 3)
            # midpoint step
            self.threshGridStepLabel = QLabel(self.tr("Mid Point Step"), self)
            self.paradigm_widg_sizer.addWidget(self.threshGridStepLabel, n, 7)
            self.threshGridStep = QLineEdit()
            self.threshGridStep.setText('0.5')
            self.threshGridStep.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.threshGridStep, n, 8)
            self.threshGridStepCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.threshGridStepCheckBox, n, 6)
            n = n+1
            # thresh prior
            self.threshPriorChooserLabel = QLabel(self.tr("Mid Point Prior:"), self)
            self.paradigm_widg_sizer.addWidget(self.threshPriorChooserLabel, n, 1)
            self.threshPriorChooser = QComboBox()
            self.threshPriorChooser.addItems(priorOptions)
            self.paradigm_widg_sizer.addWidget(self.threshPriorChooser, n, 2)
            self.threshPriorChooser.textActivated[str].connect(self.onChangeThreshPrior)
            self.threshPriorChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.threshPriorChooserCheckBox, n, 0)
            # thres priro mu
            self.threshPriorMuLabel = QLabel(self.tr("Mid Point mu"), self)
            self.paradigm_widg_sizer.addWidget(self.threshPriorMuLabel, n, 4)
            self.threshPriorMu = QLineEdit()
            self.threshPriorMu.setText('0.001')
            self.threshPriorMu.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.threshPriorMu, n, 5)
            self.threshPriorMuCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.threshPriorMuCheckBox, n, 3)
            # thresh prior sd
            self.threshPriorSTDLabel = QLabel(self.tr("Mid Point STD"), self)
            self.paradigm_widg_sizer.addWidget(self.threshPriorSTDLabel, n, 7)
            self.threshPriorSTD = QLineEdit()
            self.threshPriorSTD.setText('1.1')
            self.threshPriorSTD.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.threshPriorSTD, n, 8)
            self.threshPriorSTDCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.threshPriorSTDCheckBox, n, 6)
            n = n+1

            #start guess
            #min guess
            self.loGuessLabel = QLabel(self.tr("Guess Min"), self)
            self.paradigm_widg_sizer.addWidget(self.loGuessLabel, n, 1)
            self.loGuess = QLineEdit()
            self.loGuess.setText('0.0')
            self.loGuess.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.loGuess, n, 2)
            self.loGuessCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.loGuessCheckBox, n, 0)
            #guess max
            self.hiGuessLabel = QLabel(self.tr("Guess Max"), self)
            self.paradigm_widg_sizer.addWidget(self.hiGuessLabel, n, 4)
            self.hiGuess = QLineEdit()
            self.hiGuess.setText('0.4')
            self.hiGuess.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.hiGuess, n, 5)
            self.hiGuessCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.hiGuessCheckBox, n, 3)
            #guess step
            self.guessGridStepLabel = QLabel(self.tr("Guess Step"), self)
            self.paradigm_widg_sizer.addWidget(self.guessGridStepLabel, n, 7)
            self.guessGridStep = QLineEdit()
            self.guessGridStep.setText('0.01')
            self.guessGridStep.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.guessGridStep, n, 8)
            self.guessGridStepCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.guessGridStepCheckBox, n, 6)
            n = n+1
            self.guessSpacingChooserLabel = QLabel(self.tr("Guess Spacing:"), self)
            self.paradigm_widg_sizer.addWidget(self.guessSpacingChooserLabel, n, 1)
            self.guessSpacingChooser = QComboBox()
            self.guessSpacingChooser.addItems(["Linear", "Logarithmic"])
            self.paradigm_widg_sizer.addWidget(self.guessSpacingChooser, n, 2)
            self.guessSpacingChooser.textActivated[str].connect(self.onGuessSpacingChooserChange)
            self.guessSpacingChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.guessSpacingChooserCheckBox, n, 0)

            n = n+1
            # guess prior
            self.guessPriorChooserLabel = QLabel(self.tr("Guess Prior:"), self)
            self.paradigm_widg_sizer.addWidget(self.guessPriorChooserLabel, n, 1)
            self.guessPriorChooser = QComboBox()
            self.guessPriorChooser.addItems(priorOptions)
            self.paradigm_widg_sizer.addWidget(self.guessPriorChooser, n, 2)
            self.guessPriorChooser.textActivated[str].connect(self.onChangeGuessPrior)
            self.guessPriorChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.guessPriorChooserCheckBox, n, 0)
            # guess prior mu
            self.guessPriorMuLabel = QLabel(self.tr("Guess mu"), self)
            self.paradigm_widg_sizer.addWidget(self.guessPriorMuLabel, n, 4)
            self.guessPriorMu = QLineEdit()
            self.guessPriorMu.setText('1.1')
            self.guessPriorMu.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.guessPriorMu, n, 5)
            self.guessPriorMuCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.guessPriorMuCheckBox, n, 3)
            # guess prior sd
            self.guessPriorSTDLabel = QLabel(self.tr("Guess STD"), self)
            self.paradigm_widg_sizer.addWidget(self.guessPriorSTDLabel, n, 7)
            self.guessPriorSTD = QLineEdit()
            self.guessPriorSTD.setText('1.1')
            self.guessPriorSTD.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.guessPriorSTD, n, 8)
            self.guessPriorSTDCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.guessPriorSTDCheckBox, n, 6)
            n = n+1
            #end guess
            
            #min slope
            self.loSlopeLabel = QLabel(self.tr("Slope Min"), self)
            self.paradigm_widg_sizer.addWidget(self.loSlopeLabel, n, 1)
            self.loSlope = QLineEdit()
            self.loSlope.setText('0.1')
            self.loSlope.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.loSlope, n, 2)
            self.loSlopeCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.loSlopeCheckBox, n, 0)
            #slope max
            self.hiSlopeLabel = QLabel(self.tr("Slope Max"), self)
            self.paradigm_widg_sizer.addWidget(self.hiSlopeLabel, n, 4)
            self.hiSlope = QLineEdit()
            self.hiSlope.setText('10')
            self.hiSlope.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.hiSlope, n, 5)
            self.hiSlopeCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.hiSlopeCheckBox, n, 3)
            #slope step
            self.slopeGridStepLabel = QLabel(self.tr("Slope Step"), self)
            self.paradigm_widg_sizer.addWidget(self.slopeGridStepLabel, n, 7)
            self.slopeGridStep = QLineEdit()
            self.slopeGridStep.setText('0.1')
            self.slopeGridStep.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.slopeGridStep, n, 8)
            self.slopeGridStepCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.slopeGridStepCheckBox, n, 6)
            n = n+1
            self.slopeSpacingChooserLabel = QLabel(self.tr("Slope Spacing:"), self)
            self.paradigm_widg_sizer.addWidget(self.slopeSpacingChooserLabel, n, 1)
            self.slopeSpacingChooser = QComboBox()
            self.slopeSpacingChooser.addItems(["Linear", "Logarithmic"])
            self.paradigm_widg_sizer.addWidget(self.slopeSpacingChooser, n, 2)
            self.slopeSpacingChooser.textActivated[str].connect(self.onSlopeSpacingChooserChange)
            self.slopeSpacingChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.slopeSpacingChooserCheckBox, n, 0)

            n = n+1
            # slope prior
            self.slopePriorChooserLabel = QLabel(self.tr("Slope Prior:"), self)
            self.paradigm_widg_sizer.addWidget(self.slopePriorChooserLabel, n, 1)
            self.slopePriorChooser = QComboBox()
            self.slopePriorChooser.addItems(priorOptions)
            self.paradigm_widg_sizer.addWidget(self.slopePriorChooser, n, 2)
            self.slopePriorChooser.textActivated[str].connect(self.onChangeSlopePrior)
            self.slopePriorChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.slopePriorChooserCheckBox, n, 0)
            # thres priro mu
            self.slopePriorMuLabel = QLabel(self.tr("Slope mu"), self)
            self.paradigm_widg_sizer.addWidget(self.slopePriorMuLabel, n, 4)
            self.slopePriorMu = QLineEdit()
            self.slopePriorMu.setText('1.1')
            self.slopePriorMu.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.slopePriorMu, n, 5)
            self.slopePriorMuCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.slopePriorMuCheckBox, n, 3)
            # slope prior sd
            self.slopePriorSTDLabel = QLabel(self.tr("Slope STD"), self)
            self.paradigm_widg_sizer.addWidget(self.slopePriorSTDLabel, n, 7)
            self.slopePriorSTD = QLineEdit()
            self.slopePriorSTD.setText('1.1')
            self.slopePriorSTD.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.slopePriorSTD, n, 8)
            self.slopePriorSTDCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.slopePriorSTDCheckBox, n, 6)
            n = n+1

            #min lapse
            self.loLapseLabel = QLabel(self.tr("Lapse Min"), self)
            self.paradigm_widg_sizer.addWidget(self.loLapseLabel, n, 1)
            self.loLapse = QLineEdit()
            self.loLapse.setText('0')
            self.loLapse.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.loLapse, n, 2)
            self.loLapseCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.loLapseCheckBox, n, 0)
            #max lapse
            self.hiLapseLabel = QLabel(self.tr("Lapse Max"), self)
            self.paradigm_widg_sizer.addWidget(self.hiLapseLabel, n, 4)
            self.hiLapse = QLineEdit()
            self.hiLapse.setText('0.2')
            self.hiLapse.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.hiLapse, n, 5)
            self.hiLapseCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.hiLapseCheckBox, n, 3)
            #lapse step
            self.lapseGridStepLabel = QLabel(self.tr("Lapse Step"), self)
            self.paradigm_widg_sizer.addWidget(self.lapseGridStepLabel, n, 7)
            self.lapseGridStep = QLineEdit()
            self.lapseGridStep.setText('0.01')
            self.lapseGridStep.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.lapseGridStep, n, 8)
            self.lapseGridStepCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.lapseGridStepCheckBox, n, 6)
            n = n+1
            self.lapseSpacingChooserLabel = QLabel(self.tr("Lapse Spacing:"), self)
            self.paradigm_widg_sizer.addWidget(self.lapseSpacingChooserLabel, n, 1)
            self.lapseSpacingChooser = QComboBox()
            self.lapseSpacingChooser.addItems(["Linear", "Logarithmic"])
            self.paradigm_widg_sizer.addWidget(self.lapseSpacingChooser, n, 2)
            self.lapseSpacingChooser.textActivated[str].connect(self.onLapseSpacingChooserChange)
            self.lapseSpacingChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.lapseSpacingChooserCheckBox, n, 0)
            n = n+1
            # lapse prior
            self.lapsePriorChooserLabel = QLabel(self.tr("Lapse Prior:"), self)
            self.paradigm_widg_sizer.addWidget(self.lapsePriorChooserLabel, n, 1)
            self.lapsePriorChooser = QComboBox()
            self.lapsePriorChooser.addItems(priorOptions)
            self.paradigm_widg_sizer.addWidget(self.lapsePriorChooser, n, 2)
            self.lapsePriorChooser.textActivated[str].connect(self.onChangeLapsePrior)
            self.lapsePriorChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.lapsePriorChooserCheckBox, n, 0)
            # lapse priro mu
            self.lapsePriorMuLabel = QLabel(self.tr("Lapse mu"), self)
            self.paradigm_widg_sizer.addWidget(self.lapsePriorMuLabel, n, 4)
            self.lapsePriorMu = QLineEdit()
            self.lapsePriorMu.setText('0.01')
            self.lapsePriorMu.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.lapsePriorMu, n, 5)
            self.lapsePriorMuCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.lapsePriorMuCheckBox, n, 3)
            # lapse prior sd
            self.lapsePriorSTDLabel = QLabel(self.tr("Lapse STD"), self)
            self.paradigm_widg_sizer.addWidget(self.lapsePriorSTDLabel, n, 7)
            self.lapsePriorSTD = QLineEdit()
            self.lapsePriorSTD.setText('1.1')
            self.lapsePriorSTD.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.lapsePriorSTD, n, 8)
            self.lapsePriorSTDCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.lapsePriorSTDCheckBox, n, 6)
            n = n+1
         

            self.margLapseChooserLabel = QLabel(self.tr("Marginalize Lapse:"), self)
            self.paradigm_widg_sizer.addWidget(self.margLapseChooserLabel, n, 1)
            self.margLapseChooser = QComboBox()
            self.margLapseChooser.addItems(["No", "Yes"])
            self.paradigm_widg_sizer.addWidget(self.margLapseChooser, n, 2)
            self.margLapseChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.margLapseChooserCheckBox, n, 0)

            self.startLevelChooserLabel = QLabel(self.tr("Start Level:"), self)
            self.paradigm_widg_sizer.addWidget(self.startLevelChooserLabel, n, 4)
            self.startLevelChooser = QComboBox()
            self.startLevelChooser.addItems(["Auto", "Suggested"])
            self.paradigm_widg_sizer.addWidget(self.startLevelChooser, n, 5)
            self.startLevelChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.startLevelChooserCheckBox, n, 3)
            self.startLevelChooserLabel.hide()
            self.startLevelChooser.hide()
            self.startLevelChooserCheckBox.hide()

            self.PSIParSpacePlotButton = QPushButton(self.tr("Plot PSI Par. Space"))
            self.PSIParSpacePlotButton.clicked.connect(self.onClickPSIEstGuessRateParSpacePlotButton)
            self.PSIParSpacePlotButton.setIcon(QIcon.fromTheme("office-chart-line-stacked", QIcon(":/office-chart-line_stacked")))
            #self.PSIParSpacePlotButton.setIconSize(QtCore.QSize(min_pw_icon_size, min_pw_icon_size))
            self.PSIParSpacePlotButton.setToolTip(self.tr("Plot PSI parameter space"))
            self.paradigm_widg_sizer.addWidget(self.PSIParSpacePlotButton, n, 8)
            if matplotlib_available == False:
                self.PSIParSpacePlotButton.hide()

            n = n+1
            self.margGuessChooserLabel = QLabel(self.tr("Marginalize Guess:"), self)
            self.paradigm_widg_sizer.addWidget(self.margGuessChooserLabel, n, 1)
            self.margGuessChooser = QComboBox()
            self.margGuessChooser.addItems(["No", "Yes"])
            self.paradigm_widg_sizer.addWidget(self.margGuessChooser, n, 2)
            self.margGuessChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.margGuessChooserCheckBox, n, 0)
            n = n+1
            self.margSlopeChooserLabel = QLabel(self.tr("Marginalize Slope:"), self)
            self.paradigm_widg_sizer.addWidget(self.margSlopeChooserLabel, n, 1)
            self.margSlopeChooser = QComboBox()
            self.margSlopeChooser.addItems(["No", "Yes"])
            self.paradigm_widg_sizer.addWidget(self.margSlopeChooser, n, 2)
            self.margSlopeChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.margSlopeChooserCheckBox, n, 0)
            n = n+1
            self.margThreshChooserLabel = QLabel(self.tr("Marginalize Mid Point:"), self)
            self.paradigm_widg_sizer.addWidget(self.margThreshChooserLabel, n, 1)
            self.margThreshChooser = QComboBox()
            self.margThreshChooser.addItems(["No", "Yes"])
            self.paradigm_widg_sizer.addWidget(self.margThreshChooser, n, 2)
            self.margThreshChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.margThreshChooserCheckBox, n, 0)
            n = n+1
            
          
            self.paradigmChooserList = [self.threshPriorChooser,
                                        self.guessPriorChooser,
                                        self.slopePriorChooser,
                                        self.lapsePriorChooser,
                                        self.psyFunChooser,
                                        self.stimScalingChooser,
                                        self.margLapseChooser,
                                        self.margGuessChooser,
                                        self.margSlopeChooser,
                                        self.margThreshChooser,
                                        self.startLevelChooser,
                                        self.guessSpacingChooser,
                                        self.slopeSpacingChooser,
                                        self.lapseSpacingChooser]
            self.paradigmChooserLabelList = [self.threshPriorChooserLabel,
                                             self.guessPriorChooserLabel,
                                             self.slopePriorChooserLabel,
                                             self.lapsePriorChooserLabel,
                                             self.psyFunChooserLabel,
                                             self.stimScalingChooserLabel,
                                             self.margLapseChooserLabel,
                                             self.margGuessChooserLabel,
                                             self.margSlopeChooserLabel,
                                             self.margThreshChooserLabel,
                                             self.startLevelChooserLabel,
                                             self.guessSpacingChooserLabel,
                                             self.slopeSpacingChooserLabel,
                                             self.lapseSpacingChooserLabel]
            self.paradigmChooserOptionsList = [priorOptions,
                                               priorOptions,
                                               priorOptions,
                                               priorOptions,
                                               psyFunOptions,
                                               ["Linear", "Logarithmic"],
                                               ["No", "Yes"],
                                               ["No", "Yes"],
                                               ["No", "Yes"],
                                               ["No", "Yes"],
                                               ["Auto", "Suggested"],
                                               ["Linear", "Logarithmic"],
                                               ["Linear", "Logarithmic"],
                                               ["Linear", "Logarithmic"]]
            self.paradigmChooserCheckBoxList = [self.threshPriorChooserCheckBox,
                                                self.guessPriorChooserCheckBox,
                                                self.slopePriorChooserCheckBox,
                                                self.lapsePriorChooserCheckBox,
                                                self.psyFunCheckBox,
                                                self.stimScalingCheckBox,
                                                self.margLapseChooserCheckBox,
                                                self.margGuessChooserCheckBox,
                                                self.margSlopeChooserCheckBox,
                                                self.margThreshChooserCheckBox,
                                                self.startLevelChooserCheckBox,
                                                self.guessSpacingChooserCheckBox,
                                                self.slopeSpacingChooserCheckBox,
                                                self.lapseSpacingChooserCheckBox]

            self.paradigmFieldList = [self.loStim, self.hiStim, self.stimGridStep,
                                      self.loMidPoint, self.hiMidPoint, self.threshGridStep,
                                      self.loGuess, self.hiGuess, self.guessGridStep,
                                      self.loSlope, self.hiSlope, self.slopeGridStep,
                                      self.loLapse, self.hiLapse, self.lapseGridStep,
                                      self.threshPriorMu, self.threshPriorSTD,
                                      self.guessPriorMu, self.guessPriorSTD,
                                      self.slopePriorMu, self.slopePriorSTD,
                                      self.lapsePriorMu, self.lapsePriorSTD,
                                      self.nTrialsTF]
            self.paradigmFieldLabelList = [self.loStimLabel, self.hiStimLabel, self.stimGridStepLabel,
                                           self.loMidPointLabel, self.hiMidPointLabel, self.threshGridStepLabel,
                                           self.loGuessLabel, self.hiGuessLabel, self.guessGridStepLabel,
                                           self.loSlopeLabel, self.hiSlopeLabel, self.slopeGridStepLabel,
                                           self.loLapseLabel, self.hiLapseLabel, self.lapseGridStepLabel,
                                           self.threshPriorMuLabel, self.threshPriorSTDLabel,
                                           self.guessPriorMuLabel, self.guessPriorSTDLabel,
                                           self.slopePriorMuLabel, self.slopePriorSTDLabel,
                                           self.lapsePriorMuLabel, self.lapsePriorSTDLabel,
                                           self.nTrialsLabel]
            self.paradigmFieldCheckBoxList = [self.loStimCheckBox, self.hiStimCheckBox, self.stimGridStepCheckBox,
                                              self.loMidPointCheckBox, self.hiMidPointCheckBox, self.threshGridStepCheckBox,
                                              self.loGuessCheckBox, self.hiGuessCheckBox, self.guessGridStepCheckBox,
                                              self.loSlopeCheckBox, self.hiSlopeCheckBox, self.slopeGridStepCheckBox,
                                              self.loLapseCheckBox, self.hiLapseCheckBox, self.lapseGridStepCheckBox,
                                              self.threshPriorMuCheckBox, self.threshPriorSTDCheckBox,
                                              self.guessPriorMuCheckBox, self.guessPriorSTDCheckBox,
                                              self.slopePriorMuCheckBox, self.slopePriorSTDCheckBox,
                                              self.lapsePriorMuCheckBox, self.lapsePriorSTDCheckBox,
                                              self.nTrialsCheckBox]
            self.paradigmButtonList = [self.PSIParSpacePlotButton]
            
            self.onChangeThreshPrior()
            self.onChangeGuessPrior()
            self.onChangeSlopePrior()
            self.onChangeLapsePrior()

        #######
        #UML - Est. Guess Rate
        if self.currParadigm in [self.tr("UML - Est. Guess Rate")]:
            n = 0
            priorOptions = [self.tr("Uniform"), self.tr("Normal"), self.tr("Gamma")]
            psyFunOptions = [self.tr("Logistic"), self.tr("Gaussian"), self.tr("Weibull")]
            # n = n+1
            self.psyFunChooserLabel = QLabel(self.tr("Psychometric Function:"), self)
            self.paradigm_widg_sizer.addWidget(self.psyFunChooserLabel, n, 1)
            self.psyFunChooser = QComboBox()
            self.psyFunChooser.addItems(psyFunOptions)
            self.paradigm_widg_sizer.addWidget(self.psyFunChooser, n, 2)
            self.psyFunCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.psyFunCheckBox, n, 0)

            self.psyFunPostSummChooserLabel = QLabel(self.tr("Posterior Summary:"), self)
            self.paradigm_widg_sizer.addWidget(self.psyFunPostSummChooserLabel, n, 4)
            self.psyFunPostSummChooser = QComboBox()
            self.psyFunPostSummChooser.addItems(["Mean", "Mode"])
            self.paradigm_widg_sizer.addWidget(self.psyFunPostSummChooser, n, 5)
            self.psyFunPostSummCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.psyFunPostSummCheckBox, n, 3)

            self.UMLParSpacePlotButton = QPushButton(self.tr("Plot UML Par. Space"))
            self.UMLParSpacePlotButton.clicked.connect(self.onClickUMLEstGuessRateParSpacePlotButton)
            self.UMLParSpacePlotButton.setIcon(QIcon.fromTheme("office-chart-line-stacked", QIcon(":/office-chart-line_stacked")))
            #self.UMLParSpacePlotButton.setIconSize(QtCore.QSize(min_pw_icon_size, min_pw_icon_size))
            self.UMLParSpacePlotButton.setToolTip(self.tr("Plot UML parameter space"))
            self.paradigm_widg_sizer.addWidget(self.UMLParSpacePlotButton, n, 8)
            if matplotlib_available == False:
                self.UMLParSpacePlotButton.hide()

            n = n+1

            self.nTrialsLabel = QLabel(self.tr("No. Trials"), self)
            self.paradigm_widg_sizer.addWidget(self.nTrialsLabel, n, 1)
            self.nTrialsTF = QLineEdit()
            self.nTrialsTF.setText("100")
            self.nTrialsTF.setValidator(QIntValidator(self))
            self.paradigm_widg_sizer.addWidget(self.nTrialsTF, n, 2)
            self.nTrialsCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.nTrialsCheckBox, n, 0)

            self.swptRuleChooserLabel = QLabel(self.tr("Swpt. Rule:"), self)
            self.paradigm_widg_sizer.addWidget(self.swptRuleChooserLabel, n, 4)
            self.swptRuleChooser = QComboBox()
            self.swptRuleChooser.addItems(["Up-Down", "Random"])
            self.paradigm_widg_sizer.addWidget(self.swptRuleChooser, n, 5)
            self.swptRuleChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.swptRuleChooserCheckBox, n, 3)
            self.swptRuleChooser.textActivated[str].connect(self.onChangeSwptRule)
            
            self.ruleDownLabel = QLabel(self.tr("Rule Down"), self)
            self.paradigm_widg_sizer.addWidget(self.ruleDownLabel, n, 7)
            self.ruleDownTF = QLineEdit()
            self.ruleDownTF.setText('2')
            self.ruleDownTF.setValidator(QIntValidator(self))
            self.paradigm_widg_sizer.addWidget(self.ruleDownTF, n, 8)
            self.ruleDownCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.ruleDownCheckBox, n, 6)

            
            n = n+1

            #min stim
            self.loStimLabel = QLabel(self.tr("Stim. Min"), self)
            self.paradigm_widg_sizer.addWidget(self.loStimLabel, n, 1)
            self.loStim = QLineEdit()
            self.loStim.setText('0.5')
            self.loStim.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.loStim, n, 2)
            self.loStimCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.loStimCheckBox, n, 0)
            #n = n+1
            #max stim
            self.hiStimLabel = QLabel(self.tr("Stim. Max"), self)
            self.paradigm_widg_sizer.addWidget(self.hiStimLabel, n, 4)
            self.hiStim = QLineEdit()
            self.hiStim.setText('40')
            self.hiStim.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.hiStim, n, 5)
            self.hiStimCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.hiStimCheckBox, n, 3)

            self.stimScalingChooserLabel = QLabel(self.tr("Stim. Scaling:"), self)
            self.paradigm_widg_sizer.addWidget(self.stimScalingChooserLabel, n, 7)
            self.stimScalingChooser = QComboBox()
            self.stimScalingChooser.addItems(["Linear", "Logarithmic"])
            self.paradigm_widg_sizer.addWidget(self.stimScalingChooser, n, 8)
            self.stimScalingCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.stimScalingCheckBox, n, 6)
            self.stimScalingChooser.textActivated[str].connect(self.onStimScalingChooserChange)
            n = n+1
            self.suggestedLambdaSwptLabel = QLabel(self.tr("Suggested Lapse Swpt."))
            self.suggestedLambdaSwpt = QLineEdit("40")
            self.suggestedLambdaSwptCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.suggestedLambdaSwptLabel, n, 1)
            self.paradigm_widg_sizer.addWidget(self.suggestedLambdaSwpt, n, 2)
            self.paradigm_widg_sizer.addWidget(self.suggestedLambdaSwptCheckBox, n, 0)
            n = n+1
            self.lambdaSwptPCLabel = QLabel(self.tr("Pr. Corr. at Est. Lapse Swpt."))
            self.lambdaSwptPC = QLineEdit("0.99")
            self.lambdaSwptPCCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.lambdaSwptPCLabel, n, 1)
            self.paradigm_widg_sizer.addWidget(self.lambdaSwptPC, n, 2)
            self.paradigm_widg_sizer.addWidget(self.lambdaSwptPCCheckBox, n, 0)
            n = n+1
            #min midpoint
            self.loMidPointLabel = QLabel(self.tr("Mid Point Min"), self)
            self.paradigm_widg_sizer.addWidget(self.loMidPointLabel, n, 1)
            self.loMidPoint = QLineEdit()
            self.loMidPoint.setText('2')
            self.loMidPoint.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.loMidPoint, n, 2)
            self.loMidPointCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.loMidPointCheckBox, n, 0)
            #n = n+1
            #max midpoint
            self.hiMidPointLabel = QLabel(self.tr("Mid Point Max"), self)
            self.paradigm_widg_sizer.addWidget(self.hiMidPointLabel, n, 4)
            self.hiMidPoint = QLineEdit()
            self.hiMidPoint.setText('20')
            self.hiMidPoint.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.hiMidPoint, n, 5)
            self.hiMidPointCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.hiMidPointCheckBox, n, 3)
            # midpoint step
            self.threshGridStepLabel = QLabel(self.tr("Mid Point Step"), self)
            self.paradigm_widg_sizer.addWidget(self.threshGridStepLabel, n, 7)
            self.threshGridStep = QLineEdit()
            self.threshGridStep.setText('0.5')
            self.threshGridStep.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.threshGridStep, n, 8)
            self.threshGridStepCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.threshGridStepCheckBox, n, 6)
            n = n+1
            # thresh prior
            self.threshPriorChooserLabel = QLabel(self.tr("Mid Point Prior:"), self)
            self.paradigm_widg_sizer.addWidget(self.threshPriorChooserLabel, n, 1)
            self.threshPriorChooser = QComboBox()
            self.threshPriorChooser.addItems(priorOptions)
            self.paradigm_widg_sizer.addWidget(self.threshPriorChooser, n, 2)
            self.threshPriorChooser.textActivated[str].connect(self.onChangeThreshPrior)
            self.threshPriorChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.threshPriorChooserCheckBox, n, 0)
            # thresh prior mu
            self.threshPriorMuLabel = QLabel(self.tr("Mid Point mu"), self)
            self.paradigm_widg_sizer.addWidget(self.threshPriorMuLabel, n, 4)
            self.threshPriorMu = QLineEdit()
            self.threshPriorMu.setText('0.001')
            self.threshPriorMu.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.threshPriorMu, n, 5)
            self.threshPriorMuCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.threshPriorMuCheckBox, n, 3)
            # thresh prior sd
            self.threshPriorSTDLabel = QLabel(self.tr("Mid Point STD"), self)
            self.paradigm_widg_sizer.addWidget(self.threshPriorSTDLabel, n, 7)
            self.threshPriorSTD = QLineEdit()
            self.threshPriorSTD.setText('1.1')
            self.threshPriorSTD.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.threshPriorSTD, n, 8)
            self.threshPriorSTDCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.threshPriorSTDCheckBox, n, 6)
            n = n+1

            #min guess
            self.loGuessLabel = QLabel(self.tr("Guess Min"), self)
            self.paradigm_widg_sizer.addWidget(self.loGuessLabel, n, 1)
            self.loGuess = QLineEdit()
            self.loGuess.setText('0.0')
            self.loGuess.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.loGuess, n, 2)
            self.loGuessCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.loGuessCheckBox, n, 0)
            #guess max
            self.hiGuessLabel = QLabel(self.tr("Guess Max"), self)
            self.paradigm_widg_sizer.addWidget(self.hiGuessLabel, n, 4)
            self.hiGuess = QLineEdit()
            self.hiGuess.setText('0.4')
            self.hiGuess.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.hiGuess, n, 5)
            self.hiGuessCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.hiGuessCheckBox, n, 3)
            #guess step
            self.guessGridStepLabel = QLabel(self.tr("Guess Step"), self)
            self.paradigm_widg_sizer.addWidget(self.guessGridStepLabel, n, 7)
            self.guessGridStep = QLineEdit()
            self.guessGridStep.setText('0.01')
            self.guessGridStep.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.guessGridStep, n, 8)
            self.guessGridStepCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.guessGridStepCheckBox, n, 6)
            n = n+1
            self.guessSpacingChooserLabel = QLabel(self.tr("Guess Spacing:"), self)
            self.paradigm_widg_sizer.addWidget(self.guessSpacingChooserLabel, n, 1)
            self.guessSpacingChooser = QComboBox()
            self.guessSpacingChooser.addItems(["Linear", "Logarithmic"])
            self.paradigm_widg_sizer.addWidget(self.guessSpacingChooser, n, 2)
            self.guessSpacingChooser.textActivated[str].connect(self.onGuessSpacingChooserChange)
            self.guessSpacingChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.guessSpacingChooserCheckBox, n, 0)
            n = n+1
            # guess prior
            self.guessPriorChooserLabel = QLabel(self.tr("Guess Prior:"), self)
            self.paradigm_widg_sizer.addWidget(self.guessPriorChooserLabel, n, 1)
            self.guessPriorChooser = QComboBox()
            self.guessPriorChooser.addItems(priorOptions)
            self.paradigm_widg_sizer.addWidget(self.guessPriorChooser, n, 2)
            self.guessPriorChooser.textActivated[str].connect(self.onChangeGuessPrior)
            self.guessPriorChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.guessPriorChooserCheckBox, n, 0)
            # guess prior mu
            self.guessPriorMuLabel = QLabel(self.tr("Guess mu"), self)
            self.paradigm_widg_sizer.addWidget(self.guessPriorMuLabel, n, 4)
            self.guessPriorMu = QLineEdit()
            self.guessPriorMu.setText('1.1')
            self.guessPriorMu.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.guessPriorMu, n, 5)
            self.guessPriorMuCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.guessPriorMuCheckBox, n, 3)
            # guess prior sd
            self.guessPriorSTDLabel = QLabel(self.tr("Guess STD"), self)
            self.paradigm_widg_sizer.addWidget(self.guessPriorSTDLabel, n, 7)
            self.guessPriorSTD = QLineEdit()
            self.guessPriorSTD.setText('1.1')
            self.guessPriorSTD.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.guessPriorSTD, n, 8)
            self.guessPriorSTDCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.guessPriorSTDCheckBox, n, 6)
            n = n+1
            
            #min slope
            self.loSlopeLabel = QLabel(self.tr("Slope Min"), self)
            self.paradigm_widg_sizer.addWidget(self.loSlopeLabel, n, 1)
            self.loSlope = QLineEdit()
            self.loSlope.setText('0.1')
            self.loSlope.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.loSlope, n, 2)
            self.loSlopeCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.loSlopeCheckBox, n, 0)
            #slope max
            self.hiSlopeLabel = QLabel(self.tr("Slope Max"), self)
            self.paradigm_widg_sizer.addWidget(self.hiSlopeLabel, n, 4)
            self.hiSlope = QLineEdit()
            self.hiSlope.setText('10')
            self.hiSlope.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.hiSlope, n, 5)
            self.hiSlopeCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.hiSlopeCheckBox, n, 3)
            #slope step
            self.slopeGridStepLabel = QLabel(self.tr("Slope Step"), self)
            self.paradigm_widg_sizer.addWidget(self.slopeGridStepLabel, n, 7)
            self.slopeGridStep = QLineEdit()
            self.slopeGridStep.setText('0.1')
            self.slopeGridStep.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.slopeGridStep, n, 8)
            self.slopeGridStepCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.slopeGridStepCheckBox, n, 6)
            n = n+1
            self.slopeSpacingChooserLabel = QLabel(self.tr("Slope Spacing:"), self)
            self.paradigm_widg_sizer.addWidget(self.slopeSpacingChooserLabel, n, 1)
            self.slopeSpacingChooser = QComboBox()
            self.slopeSpacingChooser.addItems(["Linear", "Logarithmic"])
            self.paradigm_widg_sizer.addWidget(self.slopeSpacingChooser, n, 2)
            self.slopeSpacingChooser.textActivated[str].connect(self.onSlopeSpacingChooserChange)
            self.slopeSpacingChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.slopeSpacingChooserCheckBox, n, 0)
            n = n+1
            # slope prior
            self.slopePriorChooserLabel = QLabel(self.tr("Slope Prior:"), self)
            self.paradigm_widg_sizer.addWidget(self.slopePriorChooserLabel, n, 1)
            self.slopePriorChooser = QComboBox()
            self.slopePriorChooser.addItems(priorOptions)
            self.paradigm_widg_sizer.addWidget(self.slopePriorChooser, n, 2)
            self.slopePriorChooser.textActivated[str].connect(self.onChangeSlopePrior)
            self.slopePriorChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.slopePriorChooserCheckBox, n, 0)
            # thres priro mu
            self.slopePriorMuLabel = QLabel(self.tr("Slope mu"), self)
            self.paradigm_widg_sizer.addWidget(self.slopePriorMuLabel, n, 4)
            self.slopePriorMu = QLineEdit()
            self.slopePriorMu.setText('1.1')
            self.slopePriorMu.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.slopePriorMu, n, 5)
            self.slopePriorMuCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.slopePriorMuCheckBox, n, 3)
            # slope prior sd
            self.slopePriorSTDLabel = QLabel(self.tr("Slope STD"), self)
            self.paradigm_widg_sizer.addWidget(self.slopePriorSTDLabel, n, 7)
            self.slopePriorSTD = QLineEdit()
            self.slopePriorSTD.setText('1.1')
            self.slopePriorSTD.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.slopePriorSTD, n, 8)
            self.slopePriorSTDCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.slopePriorSTDCheckBox, n, 6)
            n = n+1

            #min lapse
            self.loLapseLabel = QLabel(self.tr("Lapse Min"), self)
            self.paradigm_widg_sizer.addWidget(self.loLapseLabel, n, 1)
            self.loLapse = QLineEdit()
            self.loLapse.setText('0')
            self.loLapse.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.loLapse, n, 2)
            self.loLapseCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.loLapseCheckBox, n, 0)
            #max lapse
            self.hiLapseLabel = QLabel(self.tr("Lapse Max"), self)
            self.paradigm_widg_sizer.addWidget(self.hiLapseLabel, n, 4)
            self.hiLapse = QLineEdit()
            self.hiLapse.setText('0.2')
            self.hiLapse.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.hiLapse, n, 5)
            self.hiLapseCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.hiLapseCheckBox, n, 3)
            #lapse step
            self.lapseGridStepLabel = QLabel(self.tr("Lapse Step"), self)
            self.paradigm_widg_sizer.addWidget(self.lapseGridStepLabel, n, 7)
            self.lapseGridStep = QLineEdit()
            self.lapseGridStep.setText('0.01')
            self.lapseGridStep.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.lapseGridStep, n, 8)
            self.lapseGridStepCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.lapseGridStepCheckBox, n, 6)
            n = n+1
            self.lapseSpacingChooserLabel = QLabel(self.tr("Lapse Spacing:"), self)
            self.paradigm_widg_sizer.addWidget(self.lapseSpacingChooserLabel, n, 1)
            self.lapseSpacingChooser = QComboBox()
            self.lapseSpacingChooser.addItems(["Linear", "Logarithmic"])
            self.paradigm_widg_sizer.addWidget(self.lapseSpacingChooser, n, 2)
            self.lapseSpacingChooser.textActivated[str].connect(self.onLapseSpacingChooserChange)
            self.lapseSpacingChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.lapseSpacingChooserCheckBox, n, 0)
            n = n+1
            # lapse prior
            self.lapsePriorChooserLabel = QLabel(self.tr("Lapse Prior:"), self)
            self.paradigm_widg_sizer.addWidget(self.lapsePriorChooserLabel, n, 1)
            self.lapsePriorChooser = QComboBox()
            self.lapsePriorChooser.addItems(priorOptions)
            self.paradigm_widg_sizer.addWidget(self.lapsePriorChooser, n, 2)
            self.lapsePriorChooser.textActivated[str].connect(self.onChangeLapsePrior)
            self.lapsePriorChooserCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.lapsePriorChooserCheckBox, n, 0)
            # lapse priro mu
            self.lapsePriorMuLabel = QLabel(self.tr("Lapse mu"), self)
            self.paradigm_widg_sizer.addWidget(self.lapsePriorMuLabel, n, 4)
            self.lapsePriorMu = QLineEdit()
            self.lapsePriorMu.setText('0.01')
            self.lapsePriorMu.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.lapsePriorMu, n, 5)
            self.lapsePriorMuCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.lapsePriorMuCheckBox, n, 3)
            # lapse prior sd
            self.lapsePriorSTDLabel = QLabel(self.tr("Lapse STD"), self)
            self.paradigm_widg_sizer.addWidget(self.lapsePriorSTDLabel, n, 7)
            self.lapsePriorSTD = QLineEdit()
            self.lapsePriorSTD.setText('1.1')
            self.lapsePriorSTD.setValidator(QDoubleValidator(self))
            self.paradigm_widg_sizer.addWidget(self.lapsePriorSTD, n, 8)
            self.lapsePriorSTDCheckBox = QCheckBox()
            self.paradigm_widg_sizer.addWidget(self.lapsePriorSTDCheckBox, n, 6)
            #n = n+1

            self.paradigmChooserList = [self.threshPriorChooser,
                                        self.guessPriorChooser,
                                        self.slopePriorChooser,
                                        self.lapsePriorChooser,
                                        self.psyFunChooser,
                                        self.psyFunPostSummChooser,
                                        self.swptRuleChooser,
                                        self.stimScalingChooser,
                                        self.guessSpacingChooser,
                                        self.slopeSpacingChooser,
                                        self.lapseSpacingChooser]
            self.paradigmChooserLabelList = [self.threshPriorChooserLabel,
                                             self.guessPriorChooserLabel,
                                             self.slopePriorChooserLabel,
                                             self.lapsePriorChooserLabel,
                                             self.psyFunChooserLabel,
                                             self.psyFunPostSummChooserLabel,
                                             self.swptRuleChooserLabel,
                                             self.stimScalingChooserLabel,
                                             self.guessSpacingChooserLabel,
                                             self.slopeSpacingChooserLabel,
                                             self.lapseSpacingChooserLabel]
            self.paradigmChooserOptionsList = [priorOptions,
                                               priorOptions,
                                               priorOptions,
                                               priorOptions,
                                               psyFunOptions,
                                               [self.tr("Mean"), self.tr("Mode")],
                                               [self.tr("Up-Down"), self.tr("Random")],
                                               [self.tr("Linear"), self.tr("Logarithmic")],
                                               [self.tr("Linear"), self.tr("Logarithmic")],
                                               [self.tr("Linear"), self.tr("Logarithmic")],
                                               [self.tr("Linear"), self.tr("Logarithmic")]]
            self.paradigmChooserCheckBoxList = [self.threshPriorChooserCheckBox,
                                                self.guessPriorChooserCheckBox,
                                                self.slopePriorChooserCheckBox,
                                                self.lapsePriorChooserCheckBox,
                                                self.psyFunCheckBox,
                                                self.psyFunPostSummCheckBox,
                                                self.swptRuleChooserCheckBox,
                                                self.stimScalingCheckBox,
                                                self.guessSpacingChooserCheckBox,
                                                self.slopeSpacingChooserCheckBox,
                                                self.lapseSpacingChooserCheckBox]

            self.paradigmFieldList = [self.loStim, self.hiStim, self.suggestedLambdaSwpt,
                                      self.lambdaSwptPC, self.ruleDownTF,
                                      self.loMidPoint, self.hiMidPoint, self.threshGridStep,
                                      self.loGuess, self.hiGuess, self.guessGridStep,
                                      self.loSlope, self.hiSlope, self.slopeGridStep,
                                      self.loLapse, self.hiLapse, self.lapseGridStep,
                                      self.threshPriorMu, self.threshPriorSTD,
                                      self.guessPriorMu, self.guessPriorSTD,
                                      self.slopePriorMu, self.slopePriorSTD,
                                      self.lapsePriorMu, self.lapsePriorSTD,
                                      self.nTrialsTF]
            self.paradigmFieldLabelList = [self.loStimLabel, self.hiStimLabel, self.suggestedLambdaSwptLabel,
                                           self.lambdaSwptPCLabel, self.ruleDownLabel,
                                           self.loMidPointLabel, self.hiMidPointLabel, self.threshGridStepLabel,
                                           self.loGuessLabel, self.hiGuessLabel, self.guessGridStepLabel,
                                           self.loSlopeLabel, self.hiSlopeLabel, self.slopeGridStepLabel,
                                           self.loLapseLabel, self.hiLapseLabel, self.lapseGridStepLabel,
                                           self.threshPriorMuLabel, self.threshPriorSTDLabel,
                                           self.guessPriorMuLabel, self.guessPriorSTDLabel,
                                           self.slopePriorMuLabel, self.slopePriorSTDLabel,
                                           self.lapsePriorMuLabel, self.lapsePriorSTDLabel,
                                           self.nTrialsLabel]
            self.paradigmFieldCheckBoxList = [self.loStimCheckBox, self.hiStimCheckBox, self.suggestedLambdaSwptCheckBox,
                                              self.lambdaSwptPCCheckBox, self.ruleDownCheckBox,
                                              self.loMidPointCheckBox, self.hiMidPointCheckBox, self.threshGridStepCheckBox,
                                              self.loGuessCheckBox, self.hiGuessCheckBox, self.guessGridStepCheckBox,
                                              self.loSlopeCheckBox, self.hiSlopeCheckBox, self.slopeGridStepCheckBox,
                                              self.loLapseCheckBox, self.hiLapseCheckBox, self.lapseGridStepCheckBox,
                                              self.threshPriorMuCheckBox, self.threshPriorSTDCheckBox,
                                              self.guessPriorMuCheckBox, self.guessPriorSTDCheckBox,
                                              self.slopePriorMuCheckBox, self.slopePriorSTDCheckBox,
                                              self.lapsePriorMuCheckBox, self.lapsePriorSTDCheckBox,
                                              self.nTrialsCheckBox]
            self.paradigmButtonList = [self.UMLParSpacePlotButton]
            self.onChangeThreshPrior()
            self.onChangeSlopePrior()
            self.onChangeLapsePrior()
            self.onChangeSwptRule()

        if self.currParadigm in [self.tr("Adaptive Digit Span")]:
            self.paradigmChooserList = []
            self.paradigmChooserLabelList = []
            self.paradigmChooserOptionsList = []
            self.paradigmChooserCheckBoxList = []
            self.paradigmFieldList = []
            self.paradigmFieldLabelList = []
            self.paradigmFieldCheckBoxList = []

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
        # if self.currParadigm in [self.tr("Transformed Up-Down"), self.tr("Weighted Up-Down"),
        #                           self.tr("Transformed Up-Down Limited"), self.tr("Weighted Up-Down Limited"),
        #                           self.tr("Transformed Up-Down Interleaved"), self.tr("Weighted Up-Down Interleaved"),
        #                           self.tr("PEST"), self.tr("Maximum Likelihood"), self.tr("PSI")]:
        #     self.prm['responseModeChoices'] = ["Real Listener", "Automatic", "Simulated Listener", "Psychometric"]
        # else:
        #     self.prm['responseModeChoices'] = ["Real Listener", "Automatic", "Simulated Listener"]
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
        if selectedMode != self.tr("Psychometric"):
            self.psyListFunChooser.hide()
            self.psyListFunChooserLabel.hide()
            self.psyListFunFitChooser.hide()
            self.psyListFunFitChooserLabel.hide()
            self.psyListMidpoint.hide()
            self.psyListMidpointLabel.hide()
            self.psyListSlope.hide()
            self.psyListSlopeLabel.hide()
            self.psyListLapse.hide()
            self.psyListLapseLabel.hide()
            self.psyListSaveButton.hide()
            self.psyListPlotButton.hide()
        else:
            self.psyListFunChooser.show()
            self.psyListFunChooserLabel.show()
            self.psyListFunFitChooser.show()
            self.psyListFunFitChooserLabel.show()
            self.psyListMidpoint.show()
            self.psyListMidpointLabel.show()
            self.psyListSlope.show()
            self.psyListSlopeLabel.show()
            self.psyListLapse.show()
            self.psyListLapseLabel.show()
            self.psyListSaveButton.show()
            if matplotlib_available:
                self.psyListPlotButton.show()

    def validateInstructionsAtTF(self):
        text = self.instructionsAtTF.text()
        if len(text) > 1:
            try:
                [int(x) for x in text.split(",")]
            except:
                chars = text.split(",")
                nChars = len(chars)
                newChars = []
                flag = 0
                for i in range(nChars):
                    try:
                        int(chars[i])
                        newChars.append(chars[i])
                    except:
                        flag = 1
                self.instructionsAtTF.setText(', '.join(map(str, newChars)))#tmp[2:len(tmp)-2])
                if flag == 1:
                    ret = QMessageBox.warning(self, self.tr("Warning"),
                                              self.tr("Invalid character removed from 'Show Instructions At' text field."),
                                              QMessageBox.StandardButton.Ok)
            
    def onDropPrmFile(self, l):
        lastFileDropped = l #l[len(l)-1]
        if os.path.exists(lastFileDropped):
            reply = QMessageBox.question(self, self.tr('Message'), self.tr("Do you want to load the parameters file {0} ?").format(lastFileDropped), QMessageBox.StandardButton.Yes | 
                                               QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)
            if reply == QMessageBox.StandardButton.Yes:
                self.loadParameters(lastFileDropped)
            else:
                pass
                
    def setDefaultParameters(self, experiment, paradigm, par):
        self.prevExp = self.currExp
        self.currExp = experiment
        self.removePrmWidgets()
        
        if paradigm in [self.tr("Transformed Up-Down Interleaved"), self.tr("Weighted Up-Down Interleaved")]:
            if self.prm[self.currExp]['hasNTracksChooser'] == False:
                self.par['nDifferences'] = self.prm[self.currExp]['defaultNTracks']
            else:
                if 'nDifferences' not in par:
                    if 'defaultNTracks' in self.prm[self.currExp]:
                        self.par['nDifferences'] = self.prm[self.currExp]['defaultNTracks']
                    else:
                        self.par['nDifferences'] = 2

        if paradigm in [self.tr("Multiple Constants 1-Interval 2-Alternatives"), 
                        self.tr("Multiple Constants m-Intervals n-Alternatives"), 
                        self.tr("Multiple Constants 1-Pair Same/Different"),
                        self.tr("Multiple Constants ABX"), 
                        self.tr("Multiple Constants Odd One Out"),
                        self.tr("Multiple Constants Sound Comparison")]:
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

        if 'dirChooser' in tmp:
            self.prm['dirChooser'] = tmp['dirChooser']
            self.prm['dirChooserButton'] = tmp['dirChooserButton']
        else:
            self.prm['dirChooser'] = []
            self.prm['dirChooserButton'] = []
        self.prm['nDirChoosers'] = len(self.prm['dirChooser'])
        
        # SET UP TEXT FIELDS
        self.field = list(range(self.prm['nFields']))
        self.fieldLabel = list(range(self.prm['nFields']))
        self.fieldCheckBox = list(range(self.prm['nFields']))
        for f in range(self.prm['nFields']):
            self.fieldLabel[f] = QLabel(self.tr(self.prm['fieldLabel'][f]))
            self.pw_prm_sizer_0.addWidget(self.fieldLabel[f], f, 1)
            self.field[f] = QLineEdit()
            self.field[f].setText(str(self.prm['field'][f]))
            self.field[f].setValidator(QDoubleValidator(self))
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
            self.chooser[c].textActivated[str].connect(self.onChooserChange)
 
        #SET UP FILE CHOOSERS
        self.fileChooser = list(range(self.prm['nFileChoosers']))
        self.fileChooserButton = list(range(self.prm['nFileChoosers']))
        self.fileChooserCheckBox = list(range(self.prm['nFileChoosers']))
        for f in range(self.prm['nFileChoosers']):
            self.fileChooser[f] = QLineEdit()
            self.fileChooser[f].setText(str(self.prm['fileChooser'][f]))
            self.pw_prm_sizer_0.addWidget(self.fileChooser[f], self.prm['nFields']+f, 2)
            self.fileChooserButton[f] =  QPushButton(self.tr(self.prm['fileChooserButton'][f]), self)
            self.fileChooserButton[f].clicked.connect(self.fileChooserButtonClicked)
            self.pw_prm_sizer_0.addWidget(self.fileChooserButton[f], self.prm['nFields']+f, 1)
            self.fileChooserCheckBox[f] = QCheckBox()
            self.pw_prm_sizer_0.addWidget(self.fileChooserCheckBox[f], self.prm['nFields']+f, 0)

        #SET UP DIR CHOOSERS
        self.dirChooser = list(range(self.prm['nDirChoosers']))
        self.dirChooserButton = list(range(self.prm['nDirChoosers']))
        self.dirChooserCheckBox = list(range(self.prm['nDirChoosers']))
        for f in range(self.prm['nDirChoosers']):
            self.dirChooser[f] = QLineEdit()
            self.dirChooser[f].setText(str(self.prm['dirChooser'][f]))
            self.pw_prm_sizer_0.addWidget(self.dirChooser[f], self.prm['nFields']+self.prm['nFileChoosers']+f, 2)
            self.dirChooserButton[f] =  QPushButton(self.tr(self.prm['dirChooserButton'][f]), self)
            self.dirChooserButton[f].clicked.connect(self.dirChooserButtonClicked)
            self.pw_prm_sizer_0.addWidget(self.dirChooserButton[f], self.prm['nFields']+self.prm['nFileChoosers']+f, 1)
            self.dirChooserCheckBox[f] = QCheckBox()
            self.pw_prm_sizer_0.addWidget(self.dirChooserCheckBox[f], self.prm['nFields']+self.prm['nFileChoosers']+f, 0)
        
        self.prevParadigm = self.currParadigm
        self.currParadigm = paradigm 
        self.paradigmChooser.setCurrentIndex(self.prm[self.currExp]["paradigmChoices"].index(self.currParadigm))
        self.preTrialSilenceTF.setText(self.prm["pref"]["general"]["preTrialSilence"])

        self.setParadigmWidgets(self.currParadigm, self.prevParadigm)
        if self.currParadigm in [self.tr("Transformed Up-Down"), self.tr("Weighted Up-Down"),
                                 self.tr("Transformed Up-Down Limited"), self.tr("Weighted Up-Down Limited"),
                                 self.tr("Transformed Up-Down Hybrid"), self.tr("Weighted Up-Down Hybrid"),
                                 self.tr("Transformed Up-Down Interleaved"), self.tr("Weighted Up-Down Interleaved"),
                                 self.tr("PEST")]:
            try: #set to the default adaptive type is specified
                self.adaptiveTypeChooser.setCurrentIndex(self.prm["adaptiveTypeChoices"].index(self.prm[self.currExp]['defaultAdaptiveType']))
            except:
                self.adaptiveTypeChooser.setCurrentIndex(0)

        self.prm['nIntervals'] = self.prm[self.currExp]['defaultNIntervals']  
        self.prm['nAlternatives'] = self.prm[self.currExp]['defaultNAlternatives']
        self.setAdditionalWidgets(self.currExp, self.prevExp)
        
        self.onChooserChange(None)
        
    def removePrmWidgets(self):
        if self.prevExp != None:
            for f in range(len(self.field)):
                self.pw_prm_sizer_0.removeWidget(self.fieldLabel[f])
                #self.fieldLabel[f].setParent(None)
                self.fieldLabel[f].deleteLater()
                self.pw_prm_sizer_0.removeWidget(self.field[f])
                #self.field[f].setParent(None)
                self.field[f].deleteLater()
                self.pw_prm_sizer_0.removeWidget(self.fieldCheckBox[f])
                #self.fieldCheckBox[f].setParent(None)
                self.fieldCheckBox[f].deleteLater()
            for c in range(len(self.chooser)):
                self.pw_prm_sizer_1.removeWidget(self.chooserLabel[c])
                #self.chooserLabel[c].setParent(None)
                self.chooserLabel[c].deleteLater()
                self.pw_prm_sizer_1.removeWidget(self.chooser[c])
                #self.chooser[c].setParent(None)
                self.chooser[c].deleteLater()
                self.pw_prm_sizer_1.removeWidget(self.chooserCheckBox[c])
                #self.chooserCheckBox[c].setParent(None)
                self.chooserCheckBox[c].deleteLater()
            for f in range(len(self.fileChooser)):
                self.pw_prm_sizer_0.removeWidget(self.fileChooser[f])
                #self.fileChooser[f].setParent(None)
                self.fileChooser[f].deleteLater()
                self.pw_prm_sizer_0.removeWidget(self.fileChooserButton[f])
                #self.fileChooserButton[f].setParent(None)
                self.fileChooserButton[f].deleteLater()
                self.pw_prm_sizer_0.removeWidget(self.fileChooserCheckBox[f])
                #self.fileChooserCheckBox[f].setParent(None)
                self.fileChooserCheckBox[f].deleteLater()
            for f in range(len(self.dirChooser)):
                self.pw_prm_sizer_0.removeWidget(self.dirChooser[f])
                #self.dirChooser[f].setParent(None)
                self.dirChooser[f].deleteLater()
                self.pw_prm_sizer_0.removeWidget(self.dirChooserButton[f])
                #self.dirChooserButton[f].setParent(None)
                self.dirChooserButton[f].deleteLater()
                self.pw_prm_sizer_0.removeWidget(self.dirChooserCheckBox[f])
                #self.dirChooserCheckBox[f].setParent(None)
                self.dirChooserCheckBox[f].deleteLater()
            
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
        self.taskLabelTF.setText(self.prm[block]['taskLabel'])
        self.instructionsTF.setText(self.prm[block]['instructions'])

        currExp = self.tr(self.prm[block]['experiment'])
        paradigm = self.tr(self.prm[block]['paradigm'])
        self.experimentChooser.setCurrentIndex(self.prm['experimentsChoices'].index(currExp))
        for i in range(self.paradigmChooser.count()):
            self.paradigmChooser.removeItem(0)
        self.paradigmChooser.addItems(self.prm[currExp]['paradigmChoices'])
        self.paradigmChooser.setCurrentIndex(self.prm[currExp]["paradigmChoices"].index(paradigm))

        if paradigm in [self.tr("Multiple Constants 1-Interval 2-Alternatives"),
                        self.tr("Multiple Constants m-Intervals n-Alternatives"), 
                        self.tr("Multiple Constants 1-Pair Same/Different"),
                        self.tr("Multiple Constants ABX"),
                        self.tr("Multiple Constants Odd One Out"),
                        self.tr("Multiple Constants Sound Comparison")]:
            self.par['nDifferences'] = int(self.prm[block]['paradigmChooser'][self.prm[block]['paradigmChooserLabel'].index(self.tr("No. Differences:"))])
        if paradigm in [self.tr("Transformed Up-Down Interleaved"), self.tr("Weighted Up-Down Interleaved")]:
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
        for f in range(len(self.dirChooser)):
            self.dirChooser[f].setText(self.prm[block]['dirChooser'][f])
            self.dirChooserCheckBox[f].setChecked(self.prm[block]['dirChooserCheckBox'][f])

        for f in range(len(self.paradigmFieldList)):
            self.paradigmFieldList[f].setText(self.currLocale.toString(self.prm[block]['paradigmField'][f], precision=self.prm["pref"]["general"]["precision"]))
            self.paradigmFieldCheckBoxList[f].setChecked(self.prm[block]['paradigmFieldCheckBox'][f])
        for c in range(len(self.paradigmChooserList)):
            self.paradigmChooserList[c].setCurrentIndex(self.paradigmChooserList[c].findText(self.prm[block]['paradigmChooser'][c]))
            self.paradigmChooserCheckBoxList[c].setChecked(self.prm[block]['paradigmChooserCheckBox'][c])

        if paradigm in ["UML", "PSI"]:
            self.onChangeThreshPrior()
            self.onChangeSlopePrior()
            self.onChangeLapsePrior()
        elif paradigm in ["UML - Est. Guess Rate", "PSI - Est. Guess Rate"]:
            self.onChangeThreshPrior()
            self.onChangeSlopePrior()
            self.onChangeLapsePrior()    
            self.onChangeSwptRule()

        self.preTrialSilenceTF.setText(self.currLocale.toString(self.prm[block]['preTrialSilence']))
        self.warningIntervalChooser.setCurrentIndex(self.warningIntervalChooser.findText(self.prm[block]['warningInterval']))
        self.onWarningIntervalChange()
        self.warningIntervalDurTF.setText(self.currLocale.toString(self.prm[block]['warningIntervalDur']))
        self.warningIntervalISITF.setText(self.currLocale.toString(self.prm[block]['warningIntervalISI']))
        self.intervalLightsChooser.setCurrentIndex(self.intervalLightsChooser.findText(self.prm[block]['intervalLights']))

        self.psyListFunChooser.setCurrentIndex( self.psyListFunChooser.findText(self.prm[block]['psyListFun']))
        self.psyListFunFitChooser.setCurrentIndex( self.psyListFunFitChooser.findText(self.prm[block]['psyListFunFit']))
        self.psyListMidpoint.setText(self.currLocale.toString(self.prm[block]['psyListMidpoint']))
        self.psyListSlope.setText(self.currLocale.toString(self.prm[block]['psyListSlope']))
        self.psyListLapse.setText(self.currLocale.toString(self.prm[block]['psyListLapse']))
        
        
        
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
        if self.prm[currExp]["hasAltReps"] == True:
            self.altRepsBox.setText(self.currLocale.toString(self.prm[block]['altReps']))
            self.altRepsBoxCheckBox.setChecked(self.prm[block]['altRepsCheckBox'])
            self.altRepsISIBox.setText(self.currLocale.toString(self.prm[block]['altRepsISI']))
            self.altRepsISIBoxCheckBox.setChecked(self.prm[block]['altRepsISICheckBox'])
     
        self.responseLightChooser.setCurrentIndex(self.responseLightChooser.findText(self.prm[block]['responseLight']))
        self.responseLightCheckBox.setChecked(self.prm[block]['responseLightCheckBox'])
        self.responseLightTypeChooser.setCurrentIndex(self.responseLightTypeChooser.findText(self.prm[block]['responseLightType']))
        self.responseLightTypeCheckBox.setChecked(self.prm[block]['responseLightTypeCheckBox'])
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
            self.chooser[c].textActivated[str].connect(self.onChooserChange)
        self.onChooserChange(None)
        self.responseBox.setupLights()

    def onClickSaveResultsButton(self):
        ftow = QFileDialog.getSaveFileName(self, self.tr('Choose file to write results'), "", self.tr('All Files (*)'), "", QFileDialog.Option.DontConfirmOverwrite)[0]
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
        if len(self.instructionsAtTF.text())>0:
            self.prm['allBlocks']['instructionsAt'] = [int(x) for x in self.instructionsAtTF.text().split(",")]
        else:
            self.prm['allBlocks']['instructionsAt'] = []
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
        self.prm[currBlock]['taskLabel'] = self.taskLabelTF.text()
        self.prm[currBlock]['instructions'] = self.instructionsTF.toPlainText()
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
        self.prm[currBlock]['dirChooser'] = list(range(self.prm['nDirChoosers']))
        self.prm[currBlock]['dirChooserButton'] = list(range(self.prm['nDirChoosers']))
        self.prm[currBlock]['dirChooserCheckBox'] = list(range(self.prm['nDirChoosers']))
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

        self.prm[currBlock]['psyListFun'] = self.psyListFunChooser.currentText()
        self.prm[currBlock]['psyListFunFit'] = self.psyListFunFitChooser.currentText()
        self.prm[currBlock]['psyListMidpoint'] = self.currLocale.toDouble(self.psyListMidpoint.text())[0]
        self.prm[currBlock]['psyListSlope'] = self.currLocale.toDouble(self.psyListSlope.text())[0]
        self.prm[currBlock]['psyListLapse'] = self.currLocale.toDouble(self.psyListLapse.text())[0]
        
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
        if self.prm[currExp]["hasAltReps"] == True:
            self.prm[currBlock]['altReps'] = self.currLocale.toInt(self.altRepsBox.text())[0]
            self.prm[currBlock]['altRepsCheckBox'] = self.altRepsBoxCheckBox.isChecked()
            self.prm[currBlock]['altRepsISI'] = self.currLocale.toInt(self.altRepsISIBox.text())[0]
            self.prm[currBlock]['altRepsISICheckBox'] = self.altRepsISIBoxCheckBox.isChecked()
        
        self.prm[currBlock]['responseLight'] = self.responseLightChooser.currentText()
        self.prm[currBlock]['responseLightCheckBox'] = self.responseLightCheckBox.isChecked()
        self.prm[currBlock]['responseLightType'] = self.responseLightTypeChooser.currentText()
        self.prm[currBlock]['responseLightTypeCheckBox'] = self.responseLightTypeCheckBox.isChecked()
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

        for f in range(self.prm['nDirChoosers']):
            self.prm[currBlock]['dirChooser'][f] = self.dirChooser[f].text()
            self.prm[currBlock]['dirChooserButton'][f] =  self.dirChooserButton[f].text()
            self.prm[currBlock]['dirChooserCheckBox'][f] =  self.dirChooserCheckBox[f].isChecked()

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
        #print(self.prm['rbTrans'].translate("rb", "Start"))
        #print(self.responseBox.statusButton.text())
        self.responseBox.RBTaskLabel.setText(self.taskLabelTF.text())
        self.saveParametersToFile(self.prm["tmpParametersFile"])
        self.autoSetGaugeValue()
        
    def onClickStoreandgoParametersButton(self):
        self.onClickStoreParametersButton()
        self.moveNextBlock()
        
    def onClickStoreandaddParametersButton(self):
        self.onClickStoreParametersButton()
        self.onClickNewBlockButton()

    def onClickPsyListPlotButton(self):
        psychListenerPlot(self)

    def onClickPsyListSaveButton(self):
        ftow = QFileDialog.getSaveFileName(self, self.tr('Choose file to write results'), "psy_list.txt", self.tr('All Files (*)'), "")[0]
        if len(ftow) > 0:
            if fnmatch.fnmatch(ftow, '*.txt') == False:
                ftow = ftow + '.txt'
            #self.prm['resultsFile'] = ftow
            psyFun = self.psyListFunChooser.currentText()
            psyFunFit = self.psyListFunFitChooser.currentText()
            alphax = self.currLocale.toDouble(self.psyListMidpoint.text())[0]
            betax = self.currLocale.toDouble(self.psyListSlope.text())[0]
            lambdax = self.currLocale.toDouble(self.psyListLapse.text())[0]
            gammax = 1/self.currLocale.toDouble(self.nAlternativesChooser.currentText())[0]
            pcCorr = numpy.round(numpy.arange(numpy.round(gammax, 3), 1.001, 0.001), 3)
            if psyFun == "Logistic":
                if psyFunFit == "Linear":
                    stim = invLogisticPsy(pcCorr, alphax, betax, gammax, lambdax)
                elif psyFunFit == "Logarithmic":
                    stim = invLogisticPsy(pcCorr, log(alphax), betax, gammax, lambdax)
                    stim = numpy.exp(stim)
            elif psyFun == "Gaussian":
                if psyFunFit == "Linear":
                    stim = invGaussianPsy(pcCorr, alphax, betax, gammax, lambdax)
                elif psyFunFit == "Logarithmic":
                    stim = invGaussianPsy(pcCorr, log(alphax), betax, gammax, lambdax)
                    stim = numpy.exp(stim)
            elif psyFun == "Gumbel":
                if psyFunFit == "Linear":
                    stim = invGumbelPsy(pcCorr, alphax, betax, gammax, lambdax)
                elif psyFunFit == "Logarithmic":
                    stim = invGumbelPsy(pcCorr, log(alphax), betax, gammax, lambdax)
                    stim = numpy.exp(stim)
            elif psyFun == "Weibull":
                if psyFunFit == "Linear":
                    stim = invWeibullPsy(pcCorr, alphax, betax, gammax, lambdax)
                elif psyFunFit == "Logarithmic":
                    stim = invWeibullPsy(pcCorr, log(alphax), betax, gammax, lambdax)
                    stim = numpy.exp(stim)
            else:
                print("sorry only available for logistic function")
            #if os.path.exists(ftow) == False:
            fName = open(ftow, 'w')
            for i in range(len(pcCorr)):
                fName.write(str(pcCorr[i]) + ' ' + str(stim[i]) + '\n')
            fName.close()

            self.statusBar().showMessage(self.tr('Saved psychometric listener data to: ') + ftow)

    def onClickUMLParSpacePlotButton(self):
        UMLParSpacePlot(self)

    def onClickPSIParSpacePlotButton(self):
        PSIParSpacePlot(self)

    def onClickUMLEstGuessRateParSpacePlotButton(self):
        UMLEstGuessRateParSpacePlot(self)

    def onClickPSIEstGuessRateParSpacePlotButton(self):
        PSIEstGuessRateParSpacePlot(self)
        
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
            if len(self.instructionsAtTF.text())>0:
                tmpPrm['allBlocks']['instructionsAt'] = [int(x) for x in self.instructionsAtTF.text().split(",")]
            else:
                tmpPrm['allBlocks']['instructionsAt'] = []
            #tmpPrm['allBlocks']['instructionsAt'] = [int(x) for x in self.instructionsAtTF.text().split(",")]
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
            tmpPrm[currBlock]['taskLabel'] = self.taskLabelTF.text()
            tmpPrm[currBlock]['instructions'] = self.instructionsTF.toPlainText()
            tmpPrm[currBlock]['experiment'] = currExp
            tmpPrm[currBlock]['paradigm'] = currParadigm
            tmpPrm[currBlock]['field'] = list(range(tmpPrm['nFields']))
            tmpPrm[currBlock]['fieldCheckBox'] = list(range(tmpPrm['nFields']))
            tmpPrm[currBlock]['chooser'] = list(range(tmpPrm['nChoosers']))
            tmpPrm[currBlock]['chooserCheckBox'] = list(range(tmpPrm['nChoosers']))
            tmpPrm[currBlock]['fileChooser'] = list(range(tmpPrm['nFileChoosers']))
            tmpPrm[currBlock]['fileChooserCheckBox'] = list(range(tmpPrm['nFileChoosers']))
            tmpPrm[currBlock]['dirChooser'] = list(range(tmpPrm['nDirChoosers']))
            tmpPrm[currBlock]['dirChooserCheckBox'] = list(range(tmpPrm['nDirChoosers']))
            tmpPrm[currBlock]['paradigmChooser'] = []
            tmpPrm[currBlock]['paradigmField'] = []
            tmpPrm[currBlock]['paradigmChooserCheckBox'] = []
            tmpPrm[currBlock]['paradigmFieldCheckBox'] = []
         

            otherKeysToCompare = ['preTrialSilence', 'intervalLights', 'responseLight', 'responseLightType', 'responseLightDuration',
                                  'conditionLabel', 'taskLabel', 'instructions', 'warningInterval', 'warningIntervalDur', 'warningIntervalISI',
                                  'psyListFun', 'psyListFunFit', 'psyListMidpoint', 'psyListSlope', 'psyListLapse']
        
            tmpPrm[currBlock]['preTrialSilence'] = self.currLocale.toInt(self.preTrialSilenceTF.text())[0]
            tmpPrm[currBlock]['intervalLights'] = self.intervalLightsChooser.currentText()
            tmpPrm[currBlock]['warningInterval'] = self.warningIntervalChooser.currentText()
            tmpPrm[currBlock]['warningIntervalDur'] = self.currLocale.toInt(self.warningIntervalDurTF.text())[0]
            tmpPrm[currBlock]['warningIntervalISI'] = self.currLocale.toInt(self.warningIntervalISITF.text())[0]
            tmpPrm[currBlock]['responseLight'] = self.responseLightChooser.currentText()
            tmpPrm[currBlock]['responseLightCheckBox'] = self.responseLightCheckBox.isChecked()
            tmpPrm[currBlock]['responseLightType'] = self.responseLightTypeChooser.currentText()
            tmpPrm[currBlock]['responseLightTypeCheckBox'] = self.responseLightTypeCheckBox.isChecked()
            tmpPrm[currBlock]['responseLightDuration'] = self.currLocale.toInt(self.responseLightDurationTF.text())[0]
            tmpPrm[currBlock]['responseLightDurationCheckBox'] = self.responseLightDurationCheckBox.isChecked()
            tmpPrm[currBlock]['psyListFun'] = self.psyListFunChooser.currentText()
            tmpPrm[currBlock]['psyListFunFit'] = self.psyListFunFitChooser.currentText()
            tmpPrm[currBlock]['psyListMidpoint'] = self.currLocale.toDouble(self.psyListMidpoint.text())[0]
            tmpPrm[currBlock]['psyListSlope'] = self.currLocale.toDouble(self.psyListSlope.text())[0]
            tmpPrm[currBlock]['psyListLapse'] = self.currLocale.toDouble(self.psyListLapse.text())[0]
        
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
            if tmpPrm[currExp]["hasAltReps"] == True:
                tmpPrm[currBlock]['altReps'] = self.currLocale.toInt(self.altRepsBox.text())[0]
                tmpPrm[currBlock]['altRepsCheckBox'] = self.altRepsBoxCheckBox.isChecked()
                tmpPrm[currBlock]['altRepsISI'] = self.currLocale.toInt(self.altRepsISIBox.text())[0]
                tmpPrm[currBlock]['altRepsISICheckBox'] = self.altRepsISIBoxCheckBox.isChecked()
          

            for f in range(tmpPrm['nFields']):
                tmpPrm[currBlock]['field'][f] = self.currLocale.toDouble(self.field[f].text())[0]
                tmpPrm[currBlock]['fieldCheckBox'][f] = self.fieldCheckBox[f].isChecked()
            
            for c in range(tmpPrm['nChoosers']):
                tmpPrm[currBlock]['chooser'][c] =  self.chooserOptions[c][self.chooser[c].currentIndex()]
                tmpPrm[currBlock]['chooserCheckBox'][c] =  self.chooserCheckBox[c].isChecked()

            for f in range(tmpPrm['nFileChoosers']):
                tmpPrm[currBlock]['fileChooser'][f] = self.fileChooser[f].text()
                tmpPrm[currBlock]['fileChooserCheckBox'][f] = self.fileChooserCheckBox[f].isChecked()

            for f in range(tmpPrm['nDirChoosers']):
                tmpPrm[currBlock]['dirChooser'][f] = self.dirChooser[f].text()
                tmpPrm[currBlock]['dirChooserCheckBox'][f] = self.dirChooserCheckBox[f].isChecked()
            
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
            if tmpPrm['b'+str(i+1)]['dirChooser'] != self.prm['b'+str(i+1)]['dirChooser']:
                prmChanged = True
            if tmpPrm['b'+str(i+1)]['fieldCheckBox'] != self.prm['b'+str(i+1)]['fieldCheckBox']:
                prmChanged = True
            if tmpPrm['b'+str(i+1)]['chooserCheckBox'] != self.prm['b'+str(i+1)]['chooserCheckBox']:
                prmChanged = True
            if tmpPrm['b'+str(i+1)]['fileChooserCheckBox'] != self.prm['b'+str(i+1)]['fileChooserCheckBox']:
                prmChanged = True
            if tmpPrm['b'+str(i+1)]['dirChooserCheckBox'] != self.prm['b'+str(i+1)]['dirChooserCheckBox']:
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
                if thisKey not in ['conditionLabel', 'taskLabel', 'instructions', 'preTrialSilence', 'warningInterval', #these ones don't have check boxes
                                   'warningIntervalDur', 'warningIntervalISI', 'intervalLights', 'psyListFun',
                                   'psyListFunFit', 'psyListMidpoint', 'psyListSlope', 'psyListLapse']:
                    if tmpPrm['b'+str(i+1)][otherKeysToCompare[j]+'CheckBox'] != self.prm['b'+str(i+1)][thisKey+'CheckBox']:
                        prmChanged = True

            for key in tmpPrm['allBlocks']:
                if tmpPrm['allBlocks'][key] != self.prm['allBlocks'][key]:
                    prmChanged = True

                
        if nStoredDifferent == True:
            ret = QMessageBox.warning(self, self.tr("Warning"),
                                            self.tr("Last block has not been stored. Do you want to store it?"),
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if ret == QMessageBox.StandardButton.Yes:
                self.onClickStoreParametersButton()
        elif prmChanged == True:
            ret = QMessageBox.warning(self, self.tr("Warning"),
                                            self.tr("Some parameters have been modified but not stored. Do you want to store them?"),
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if ret == QMessageBox.StandardButton.Yes:
                self.onClickStoreParametersButton()
                
    def onClickNewBlockButton(self):
        if self.prm["storedBlocks"] >= self.prm["currentBlock"]:
            self.compareGuiStoredParameters()
            block =  currBlock = 'b' + str(self.prm["currentBlock"])
            self.prm["currentBlock"] = self.prm["storedBlocks"] + 1
            self.prm["tmpBlockPosition"] = self.prm["storedBlocks"] + 1
            self.setNewBlock(block)
        else:
            ret = QMessageBox.warning(self, self.tr("Warning"),
                                            self.tr("You need to store the current block before adding a new one."),
                                            QMessageBox.StandardButton.Ok)
          
        
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
            self.responseBox.RBTaskLabel.setText(self.taskLabelTF.text())
    def onClickUndoUnsavedButton(self):
        if self.prm["currentBlock"] > self.prm["storedBlocks"]:
            self.onExperimentChange(self.experimentChooser.currentText())
        else:
            self.updateParametersWin()
   
    def onClickLoadParametersButton(self):
        fName = QFileDialog.getOpenFileName(self, self.tr("Choose parameters file to load"), '', self.tr("prm files (*.prm *PRM *Prm);;All Files (*)"))[0]
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
                    QMessageBox.warning(self, self.tr("Warning"), errMsg)
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
                experimentLabelToSet = allLines[i].split(':', 1)[1].strip()
                self.experimentLabelTF.setText(experimentLabelToSet)
            elif allLines[i].split(':')[0] == 'End Command':
                endExpCommandToSet = allLines[i].split(':', 1)[1].strip()
                self.endExpCommandTF.setText(endExpCommandToSet)
            elif allLines[i].split(':')[0] == 'Instructions At BP':
                instructionsAtToSet = allLines[i].split(':')[1].strip()
                self.instructionsAtTF.setText(instructionsAtToSet)
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
                tmp['b'+str(blockNumber)]['taskLabel'] = ""
                tmp['b'+str(blockNumber)]['instructions'] = ""
                tmp['b'+str(blockNumber)]['instructionsAt'] = ""
                tmp['b'+str(blockNumber)]['responseLightType'] = self.tr("Light")
                tmp['b'+str(blockNumber)]['responseLightTypeCheckBox'] = False
                
            if allLines[i].split(':')[0] == 'Block Position':
                tmp['b'+str(blockNumber)]['blockPosition'] = allLines[i].split(':')[1].strip()
            if allLines[i].split(':')[0] == 'Condition Label':
                tmp['b'+str(blockNumber)]['conditionLabel'] = allLines[i].split(':', 1)[1].strip()
            if allLines[i].split(':')[0] == 'Task Label':
                tmp['b'+str(blockNumber)]['taskLabel'] = allLines[i].split(':', 1)[1].strip()#':'.join(allLines[i].split(':')[1:len(allLines[i].split(':'))]).strip()
            if allLines[i].split(':')[0] == 'Instructions':
                tmp['b'+str(blockNumber)]['instructions'] = allLines[i].split(':', 1)[1].strip().replace("nwln", "\n")
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
            if allLines[i].split(':')[0] == 'Alternated (AB) Reps.':
                tmp['b'+str(blockNumber)]['altReps'] = self.currLocale.toInt(allLines[i].split(':')[1].strip())[0]
                tmp['b'+str(blockNumber)]['altRepsCheckBox'] = strToBoolean(allLines[i].split(':')[2].strip())
            if allLines[i].split(':')[0] == 'Alternated (AB) Reps. ISI (ms)':
                tmp['b'+str(blockNumber)]['altRepsISI'] = self.currLocale.toInt(allLines[i].split(':')[1].strip())[0]
                tmp['b'+str(blockNumber)]['altRepsISICheckBox'] = strToBoolean(allLines[i].split(':')[2].strip())
            if allLines[i].split(':')[0] == 'Response Light':
                tmp['b'+str(blockNumber)]['responseLight'] = allLines[i].split(':')[1].strip()
                tmp['b'+str(blockNumber)]['responseLightCheckBox'] = strToBoolean(allLines[i].split(':')[2].strip())
            if allLines[i].split(':')[0] == 'Response Light Type':
                tmp['b'+str(blockNumber)]['responseLightType'] = allLines[i].split(':')[1].strip()
                tmp['b'+str(blockNumber)]['responseLightTypeCheckBox'] = strToBoolean(allLines[i].split(':')[2].strip())
            if allLines[i].split(':')[0] == 'Response Light Duration (ms)':
                tmp['b'+str(blockNumber)]['responseLightDuration'] = self.currLocale.toInt(allLines[i].split(':')[1].strip())[0]
                tmp['b'+str(blockNumber)]['responseLightDurationCheckBox'] = strToBoolean(allLines[i].split(':')[2].strip())
            if allLines[i].split(':')[0] == 'Psychometric Listener Function':
                tmp['b'+str(blockNumber)]['psyListFun'] = allLines[i].split(':')[1].strip()
                #tmp['b'+str(blockNumber)]['responseLightDurationCheckBox'] = strToBoolean(allLines[i].split(':')[2].strip())
            if allLines[i].split(':')[0] == 'Psychometric Listener Function Fit':
                tmp['b'+str(blockNumber)]['psyListFunFit'] = allLines[i].split(':')[1].strip()
                #tmp['b'+str(blockNumber)]['responseLightDurationCheckBox'] = strToBoolean(allLines[i].split(':')[2].strip())
            if allLines[i].split(':')[0] == 'Psychometric Listener Midpoint':
                tmp['b'+str(blockNumber)]['psyListMidpoint'] = self.currLocale.toDouble(allLines[i].split(':')[1].strip())[0]
                #tmp['b'+str(blockNumber)]['responseLightDurationCheckBox'] = strToBoolean(allLines[i].split(':')[2].strip())
            if allLines[i].split(':')[0] == 'Psychometric Listener Slope':
                tmp['b'+str(blockNumber)]['psyListSlope'] = self.currLocale.toDouble(allLines[i].split(':')[1].strip())[0]
                #tmp['b'+str(blockNumber)]['responseLightDurationCheckBox'] = strToBoolean(allLines[i].split(':')[2].strip())
            if allLines[i].split(':')[0] == 'Psychometric Listener Lapse':
                tmp['b'+str(blockNumber)]['psyListLapse'] = self.currLocale.toDouble(allLines[i].split(':')[1].strip())[0]
                #tmp['b'+str(blockNumber)]['responseLightDurationCheckBox'] = strToBoolean(allLines[i].split(':')[2].strip())
            if allLines[i].strip() == '.':
                foo['b'+str(blockNumber)]['startParadigmChooser'] = i+1
            if allLines[i].strip() == '..':
                foo['b'+str(blockNumber)]['startParadigmField'] = i+1
            if allLines[i].strip() == '...':
                foo['b'+str(blockNumber)]['startChooser'] = i+1
            if allLines[i].strip() == '....':
                foo['b'+str(blockNumber)]['startFileChooser'] = i+1
            if allLines[i].strip() == '.....':
                foo['b'+str(blockNumber)]['startDirChooser'] = i+1
            if allLines[i].strip() == '......':
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
            tmp['b'+str(blockNumber)]['dirChooser'] = []
            tmp['b'+str(blockNumber)]['dirChooserCheckBox'] = []
            tmp['b'+str(blockNumber)]['dirChooserButton'] = []
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

            for i in range(foo['b'+str(blockNumber)]['startDirChooser'] - foo['b'+str(blockNumber)]['startFileChooser'] -1):
                tmp['b'+str(blockNumber)]['fileChooser'].append(allLines[foo['b'+str(blockNumber)]['startFileChooser']+i].split(': ')[1].strip())
                tmp['b'+str(blockNumber)]['fileChooserButton'].append(allLines[foo['b'+str(blockNumber)]['startFileChooser']+i].split(': ')[0].strip())#+':')
                tmp['b'+str(blockNumber)]['fileChooserCheckBox'].append(strToBoolean(allLines[foo['b'+str(blockNumber)]['startFileChooser']+i].split(': ')[2].strip()))

            for i in range(foo['b'+str(blockNumber)]['startField'] - foo['b'+str(blockNumber)]['startDirChooser'] -1):
                tmp['b'+str(blockNumber)]['dirChooser'].append(allLines[foo['b'+str(blockNumber)]['startDirChooser']+i].split(': ')[1].strip())
                tmp['b'+str(blockNumber)]['dirChooserButton'].append(allLines[foo['b'+str(blockNumber)]['startDirChooser']+i].split(': ')[0].strip())#+':')
                tmp['b'+str(blockNumber)]['dirChooserCheckBox'].append(strToBoolean(allLines[foo['b'+str(blockNumber)]['startDirChooser']+i].split(': ')[2].strip()))

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
        if len(self.instructionsAtTF.text())>0:
            self.prm['allBlocks']['instructionsAt'] = [int(x) for x in self.instructionsAtTF.text().split(",")]
        else:
            self.prm['allBlocks']['instructionsAt'] = []
        #self.prm['allBlocks']['instructionsAt'] = [int(x) for x in self.instructionsAtTF.text().split(",")]
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
        self.responseBox.RBTaskLabel.setText(self.taskLabelTF.text())
        self.saveParametersToFile(self.prm["tmpParametersFile"])
        self.audioManager.initializeAudio()
      
    def onClickSaveParametersButton(self):
        if self.prm["storedBlocks"] < 1:
            ret = QMessageBox.warning(self, self.tr("Warning"),
                                      self.tr("There are no stored parameters to save."),
                                      QMessageBox.StandardButton.Ok)
        else:
            if self.parametersFile == None:
                ftow = QFileDialog.getSaveFileName(self, self.tr('Choose file to write prm'), ".prm", self.tr('All Files (*)'))[0]
            else:
                ftow = QFileDialog.getSaveFileName(self, self.tr('Choose file to write prm'), self.parametersFile, self.tr('All Files (*)'))[0]

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
        fName.write('Instructions At BP: ' + self.instructionsAtTF.text() + '\n')
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
            fName.write(self.tr('Task Label: ') + self.prm[currBlock]['taskLabel']+ '\n')
            fName.write(self.tr('Instructions: ') + self.prm[currBlock]['instructions'].replace("\n", "nwln") + '\n')
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
            fName.write(self.tr('Psychometric Listener Function: ') + self.prm[currBlock]['psyListFun']+ '\n')
            fName.write(self.tr('Psychometric Listener Function Fit: ') + self.prm[currBlock]['psyListFunFit']+ '\n')
            fName.write(self.tr('Psychometric Listener Midpoint: ') + self.currLocale.toString(self.prm[currBlock]['psyListMidpoint']) + '\n')
            fName.write(self.tr('Psychometric Listener Slope: ') + self.currLocale.toString(self.prm[currBlock]['psyListSlope']) + '\n')
            fName.write(self.tr('Psychometric Listener Lapse: ') + self.currLocale.toString(self.prm[currBlock]['psyListLapse']) + '\n')
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
            if self.prm[currExp]["hasAltReps"] == True:
                fName.write(self.tr('Alternated (AB) Reps.: ') + self.currLocale.toString(self.prm[currBlock]['altReps']) + ' :' + str(self.prm[currBlock]['altRepsCheckBox']) + '\n')
                fName.write(self.tr('Alternated (AB) Reps. ISI (ms): ') + self.currLocale.toString(self.prm[currBlock]['altRepsISI']) + ' :' + str(self.prm[currBlock]['altRepsISICheckBox']) + '\n')
             

            fName.write(self.tr('Response Light: ') + str(self.prm[currBlock]['responseLight']) + ' :' + str(self.prm[currBlock]['responseLightCheckBox']) + '\n')
            fName.write(self.tr('Response Light Type: ') + str(self.prm[currBlock]['responseLightType']) + ' :' + str(self.prm[currBlock]['responseLightTypeCheckBox']) + '\n')
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
                fName.write(self.prm[currBlock]['fileChooserButton'][k] +': ' + self.prm[currBlock]['fileChooser'][k] + ' : ' + str(self.prm[currBlock]['fileChooserCheckBox'][k]) + '\n')
            fName.write('.....\n')
            for k in range(len(self.prm[currBlock]['dirChooser'])):
                fName.write(self.prm[currBlock]['dirChooserButton'][k] +': ' + self.prm[currBlock]['dirChooser'][k] + ' : ' + str(self.prm[currBlock]['dirChooserCheckBox'][k]) + '\n')
            fName.write('......\n')
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
            self.responseBox.RBTaskLabel.setText(self.taskLabelTF.text())
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
            self.responseBox.RBTaskLabel.setText(self.taskLabelTF.text())
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
            self.responseBox.RBTaskLabel.setText(self.taskLabelTF.text())
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
            self.responseBox.RBTaskLabel.setText(self.taskLabelTF.text())
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
                    ret = QMessageBox.warning(self, self.tr("Warning"),
                                                    self.tr("Shuffling failed :-( Something may be wrong with your shuffling scheme."),
                                                    QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                    return
                if len(numpy.unique(blockPositions)) != self.prm['storedBlocks']:
                    ret = QMessageBox.warning(self, self.tr("Warning"),
                                                    self.tr("Shuffling failed :-( The length of the shuffling sequence seems to be different than the number of stored blocks. Maybe you recently added of deleted a block."),
                                                    QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                    return
                    
                for k in range(self.prm["storedBlocks"]):
                    self.prm['b'+str(k+1)]['blockPosition'] = str(blockPositions[k])

            self.moveToBlockPosition(1)
            self.prm['shuffled'] = True
            self.saveParametersToFile(self.prm["tmpParametersFile"])
            self.updateParametersWin()
            #QApplication.processEvents()
            self.responseBox.statusButton.setText(self.prm['rbTrans'].translate("rb", "Start"))
            self.responseBox.RBTaskLabel.setText(self.taskLabelTF.text())
            self.autoSetGaugeValue()
            
    def autoSetGaugeValue(self):
        bp = int(self.prm['b'+str(self.prm["currentBlock"])]["blockPosition"])
        pcThisRep = (bp-1)/self.prm["storedBlocks"]*100
        pcTot = (self.prm['currentRepetition'] - 1) / self.prm['allBlocks']['repetitions']*100 + 1 / self.prm['allBlocks']['repetitions']*pcThisRep
        self.responseBox.gauge.setValue(int(pcTot))
        self.responseBox.blockGauge.setRange(0, self.prm['storedBlocks']*self.prm['allBlocks']['repetitions'])

        cb = (self.prm['currentRepetition']-1)*self.prm["storedBlocks"]+bp
        self.responseBox.blockGauge.setValue(cb-1)
        self.responseBox.blockGauge.setFormat(self.prm['rbTrans'].translate('rb', "Completed") +  ' ' + str(cb-1) + '/' + str(self.prm['storedBlocks']*self.prm['allBlocks']['repetitions']) + ' ' + self.prm['rbTrans'].translate('rb', "Blocks"))
        
    def swapBlocks(self, b1, b2):
        self.compareGuiStoredParameters()
        if self.prm["storedBlocks"] < 1:
            return
        if b1 > self.prm["storedBlocks"] or b2 > self.prm["storedBlocks"]:
            ret = QMessageBox.warning(self, self.tr("Warning"),
                                            self.tr("You're trying to swap the position of a block that has not been stored yet. Please, store the block first."),
                                            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
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

    def onClickShowExpDocButton(self):
        
        thisDoc = eval(self.prm[self.currExp]['execString']+".__doc__")
        winTitle = self.currExp
        dialog = showExpDocDialog(self, thisDoc, winTitle)

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

    def onChangeThreshPrior(self):
        prior = self.threshPriorChooser.currentText()
        if prior == "Uniform":
            self.threshPriorMu.hide()
            self.threshPriorMuLabel.hide()
            self.threshPriorMuCheckBox.hide()
            self.threshPriorSTD.hide()
            self.threshPriorSTDLabel.hide()
            self.threshPriorSTDCheckBox.hide()
        else:
            self.threshPriorMu.show()
            self.threshPriorMuLabel.show()
            self.threshPriorMuCheckBox.show()
            self.threshPriorSTD.show()
            self.threshPriorSTDLabel.show()
            self.threshPriorSTDCheckBox.show()
            
    def onChangeSlopePrior(self):
        prior = self.slopePriorChooser.currentText()
        if prior == "Uniform":
            self.slopePriorMu.hide()
            self.slopePriorMuLabel.hide()
            self.slopePriorMuCheckBox.hide()
            self.slopePriorSTD.hide()
            self.slopePriorSTDLabel.hide()
            self.slopePriorSTDCheckBox.hide()
        else:
            self.slopePriorMu.show()
            self.slopePriorMuLabel.show()
            self.slopePriorMuCheckBox.show()
            self.slopePriorSTD.show()
            self.slopePriorSTDLabel.show()
            self.slopePriorSTDCheckBox.show()

    def onChangeGuessPrior(self):
        prior = self.guessPriorChooser.currentText()
        if prior == "Uniform":
            self.guessPriorMu.hide()
            self.guessPriorMuLabel.hide()
            self.guessPriorMuCheckBox.hide()
            self.guessPriorSTD.hide()
            self.guessPriorSTDLabel.hide()
            self.guessPriorSTDCheckBox.hide()
        else:
            self.guessPriorMu.show()
            self.guessPriorMuLabel.show()
            self.guessPriorMuCheckBox.show()
            self.guessPriorSTD.show()
            self.guessPriorSTDLabel.show()
            self.guessPriorSTDCheckBox.show()

    def onChangeLapsePrior(self):
        prior = self.lapsePriorChooser.currentText()
        if prior == "Uniform":
            self.lapsePriorMu.hide()
            self.lapsePriorMuLabel.hide()
            self.lapsePriorMuCheckBox.hide()
            self.lapsePriorSTD.hide()
            self.lapsePriorSTDLabel.hide()
            self.lapsePriorSTDCheckBox.hide()
        else:
            self.lapsePriorMu.show()
            self.lapsePriorMuLabel.show()
            self.lapsePriorMuCheckBox.show()
            self.lapsePriorSTD.show()
            self.lapsePriorSTDLabel.show()
            self.lapsePriorSTDCheckBox.show()
    def onStimScalingChooserChange(self):
        currScaling = self.stimScalingChooser.currentText()
        if currScaling == "Linear":
            pass
        elif currScaling == "Logarithmic":
            if self.currLocale.toDouble(self.threshGridStep.text())[0] <= 1:
                self.threshGridStep.setText('1.1')
                try: #stimGridStep is only for PSI not UML
                    self.stimGridStep.setText('1.1')
                except:
                    pass

    def onGuessSpacingChooserChange(self):
        currSpacing = self.guessSpacingChooser.currentText()
        if currSpacing == "Linear":
            pass
        elif currSpacing == "Logarithmic":
            if self.currLocale.toDouble(self.guessGridStep.text())[0] <= 1:
                self.guessGridStep.setText('1.1')

    def onSlopeSpacingChooserChange(self):
        currSpacing = self.slopeSpacingChooser.currentText()
        if currSpacing == "Linear":
            pass
        elif currSpacing == "Logarithmic":
            if self.currLocale.toDouble(self.slopeGridStep.text())[0] <= 1:
                self.slopeGridStep.setText('1.1')

    def onLapseSpacingChooserChange(self):
        currSpacing = self.lapseSpacingChooser.currentText()
        if currSpacing == "Linear":
            pass
        elif currSpacing == "Logarithmic":
            if self.currLocale.toDouble(self.lapseGridStep.text())[0] <= 1:
                self.lapseGridStep.setText('1.1')

    def onChangeSwptRule(self):
        swptRule = self.swptRuleChooser.currentText()
        if swptRule == "Random":
            self.ruleDownLabel.hide()
            self.ruleDownTF.hide()
            self.ruleDownCheckBox.hide()
        else:
            self.ruleDownLabel.show()
            self.ruleDownTF.show()
            self.ruleDownCheckBox.show()

    def onChooserChange(self, selectedOption):
        self.fieldsToHide = []; self.fieldsToShow = []
        self.choosersToHide = []; self.choosersToShow = [];
        self.fileChoosersToHide = []; self.fileChoosersToShow = [];
        self.dirChoosersToHide = []; self.dirChoosersToShow = [];

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
                self.fileChooser[self.fileChoosersToShow[i]].show()
                self.fileChooserButton[self.fileChoosersToShow[i]].show()
                self.fileChooserCheckBox[self.fileChoosersToShow[i]].show()
            for i in range(len(self.dirChoosersToHide)):
                self.dirChooser[self.dirChoosersToHide[i]].hide()
                self.dirChooserButton[self.dirChoosersToHide[i]].hide()
                self.dirChooserCheckBox[self.dirChoosersToHide[i]].hide()
            for i in range(len(self.dirChoosersToShow)):
                self.dirChooser[self.dirChoosersToShow[i]].show()
                self.dirChooserButton[self.dirChoosersToShow[i]].show()
                self.dirChooserCheckBox[self.dirChoosersToShow[i]].show()

    def fileChooserButtonClicked(self):
        sender = self.sender()
        fName = QFileDialog.getOpenFileName(self, self.tr("Choose file"), '', self.tr("All Files (*);; WAV (*.wav *WAV)"))[0]
        lbls = []
 
        if len(fName) > 0: #if the user didn't press cancel
            for i in range(self.prm['nFileChoosers']):
                lbls.append(self.fileChooserButton[i].text())
            self.fileChooser[lbls.index(sender.text())].setText(fName)
        #print(sender.text())
    def dirChooserButtonClicked(self):
        sender = self.sender()
        fName = QFileDialog.getExistingDirectory()#QFileDialog.getOpenFileName(self, self.tr("Choose directory"), '')[0]
        lbls = []
 
        if len(fName) > 0: #if the user didn't press cancel
            for i in range(self.prm['nDirChoosers']):
                lbls.append(self.dirChooserButton[i].text())
            self.dirChooser[lbls.index(sender.text())].setText(fName)
        
    def onEditPref(self):
        dialog = preferencesDialog(self)
        if dialog.exec():
            dialog.permanentApply()
            self.audioManager.initializeAudio()
    def onEditPhones(self):
        currIdx = self.phonesChooser.currentIndex()
        dialog = phonesDialog(self)
        if dialog.exec():
            dialog.permanentApply()
     
        self.phonesChooser.setCurrentIndex(currIdx)
        if self.phonesChooser.currentIndex() == -1:
            self.phonesChooser.setCurrentIndex(0)

    def onEditExperimenters(self):
        dialog = experimentersDialog(self)
        if dialog.exec():
            dialog.onClickApplyButton()

    def processResultsLinearDialog(self):
        fList = QFileDialog.getOpenFileNames(self, self.tr("Choose results file to load"), '', self.tr("All Files (*)"))[0]
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
        fList = QFileDialog.getOpenFileNames(self, self.tr("Choose results file to load"), '', self.tr("All Files (*)"))[0]
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
                sep, ok = QInputDialog.getText(self, self.tr('Input Dialog'), "CSV separator")
                if ok == False:
                    return

            paradigm = thisLines[1].split(sep)[prdgCol]
                
            dialog = processResultsDialog(self, fList, resformat, paradigm, sep)
   

    def onClickOpenResultsButton(self):
        if "resultsFile" in self.prm:
            fileToOpen = self.prm["resultsFile"]
            QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(fileToOpen))
        else:
            ret = QMessageBox.information(self, self.tr("message"),
                                                self.tr("No results file has been selected"),
                                                QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            
    def onAbout(self):
        if pyqtversion in [4,5,6]:
            qt_compiled_ver = QtCore.QT_VERSION_STR
            qt_runtime_ver = QtCore.qVersion()
            qt_pybackend_ver = QtCore.PYQT_VERSION_STR
            qt_pybackend = "PyQt"
        # elif pyqtversion == -4:
        #     qt_compiled_ver = QtCore.__version__
        #     qt_runtime_ver = QtCore.qVersion()
        #     qt_pybackend_ver = PySide.__version__
        #     qt_pybackend = "PySide"

        QMessageBox.about(self, self.tr("About pychoacoustics"),
                              self.tr("""<b>pychoacoustics - Python app for psychoacoustics</b> <br>
                              - version: {0}; <br>
                              - build date: {1} <br>
                              <p> Copyright &copy; 2008-2023 Samuele Carcagno. <a href="mailto:sam.carcagno@gmail.com">sam.carcagno@gmail.com</a> 
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
                              <p>Python {2} - {3} {4} compiled against Qt {5}, and running with Qt {6} on {7}""").format(__version__, self.prm['builddate'], platform.python_version(), qt_pybackend, qt_pybackend_ver, qt_compiled_ver, qt_runtime_ver, platform.system()))
        
    def closeEvent(self, event):
        self.exitFlag = True
        #here we need to check if parameters file and temporary parameters file are the same or not
        self.compareGuiStoredParameters()
        if self.prm['storedBlocks'] > 0:
            if self.parametersFile == None:
                ret = QMessageBox.warning(self, self.tr("Warning"),
                                                self.tr("The parameters have not been saved to a file. \n Do you want to save them before exiting?"),
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
                if ret == QMessageBox.StandardButton.Yes:
                    self.onClickSaveParametersButton()
                elif ret == QMessageBox.StandardButton.Cancel:
                    self.exitFlag = False
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
                    pardiff = difflib.unified_diff(l1,l2, n=0)
                    pardiff = '\n'.join(list(pardiff))
                    dialog = dialogMemoryFileParametersDiffer(self, "The parameters in memory differ from the parameters on file. \nDo you want to save the parameters stored in memory them before exiting?", pardiff)
                    if dialog.exec() and self.exitFlag == True:
                        self.onClickSaveParametersButton()

        if self.exitFlag == True:
            event.accept()
        else:
            event.ignore()

    def onWhatsThis(self):
        if QWhatsThis.inWhatsThisMode() == True:
            QWhatsThis.leaveWhatsThisMode()
        else:
            QWhatsThis.enterWhatsThisMode()

    def onShowFortune(self):
        dialog = showFortuneDialog(self)
        
    def onShowManualPdf(self):
        fileToOpen = os.path.abspath(os.path.dirname(__file__)) + '/doc/_build/latex/pychoacoustics.pdf'
        QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(fileToOpen))
        
    def onShowModulesDoc(self):
        fileToOpen = os.path.abspath(os.path.dirname(__file__)) + '/doc/_build/html/index.html'
        QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(fileToOpen))
        
    def onSwapBlocksAction(self):
        dialog = swapBlocksDialog(self)
        if dialog.exec():
            blockA = self.currLocale.toInt(dialog.blockAWidget.text())[0]
            blockB = self.currLocale.toInt(dialog.blockBWidget.text())[0]
            if self.prm['storedBlocks'] < 1:
                ret = QMessageBox.warning(self, self.tr("Warning"),
                                                self.tr("There are no stored blocks to swap."),
                                                QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                return
            if blockA < 1 or blockB < 1 or blockA > self.prm['storedBlocks'] or blockB > self.prm['storedBlocks']:
                ret = QMessageBox.warning(self, self.tr("Warning"),
                                                self.tr("Block numbers specified out of range."),
                                                QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
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
                ret = QMessageBox.warning(self, self.tr("Warning"),
                                                self.tr("Shuffling scheme contains non-allowed characters."),
                                                QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
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

    def onClickSoundCheckButton(self):
        # G= 196
        # Eb= 155.56
        # F= 174.61
        # D = 146.83
        # tUnit = 250
        # ramp = 25
        # level = 65
        # channel = "Both"
        # lowHarm = 2
        # highHarm = 2
        
        # for i in range(3):
        #     thisSnd = complexTone(G, "Sine", lowHarm, highHarm, 0, level, tUnit, ramp, channel, self.prm['sampRate'], float(self.prm['phones']['phonesMaxLevel'][self.phonesChooser.currentIndex()]))
        #     self.audioManager.playSound(thisSnd, self.prm['sampRate'], self.currLocale.toInt(self.nBitsChooser.currentText())[0], False, 'foo.wav')

        # thisSnd = complexTone(Eb, "Sine", lowHarm, highHarm, 0, level, tUnit*4, ramp, channel, self.prm['sampRate'], float(self.prm['phones']['phonesMaxLevel'][self.phonesChooser.currentIndex()]))
        # self.audioManager.playSound(thisSnd, self.prm['sampRate'], self.currLocale.toInt(self.nBitsChooser.currentText())[0], False, 'foo.wav')
        # time.sleep(tUnit/1000+ramp/1000*2)
        # for i in range(3):
        #     thisSnd = complexTone(F, "Sine", lowHarm, highHarm, 0, level, tUnit, ramp, channel, self.prm['sampRate'], float(self.prm['phones']['phonesMaxLevel'][self.phonesChooser.currentIndex()]))
        #     self.audioManager.playSound(thisSnd, self.prm['sampRate'], self.currLocale.toInt(self.nBitsChooser.currentText())[0], False, 'foo.wav')

        # thisSnd = complexTone(D, "Sine", lowHarm, highHarm, 0, level, tUnit*4, ramp, channel, self.prm['sampRate'], float(self.prm['phones']['phonesMaxLevel'][self.phonesChooser.currentIndex()]))
        # self.audioManager.playSound(thisSnd, self.prm['sampRate'], self.currLocale.toInt(self.nBitsChooser.currentText())[0], False, 'foo.wav')

        thisSnd, thisFs, thisNBits = self.audioManager.loadWavFile(os.path.abspath(os.path.dirname(__file__)) + '/sounds/left_right_tone_test_48000Hz.wav', 75, float(self.prm['phones']['phonesMaxLevel'][self.phonesChooser.currentIndex()]), "Both", desiredSampleRate=self.currLocale.toInt(self.sampRateTF.text())[0])
        self.audioManager.playSound(thisSnd, self.currLocale.toInt(self.sampRateTF.text())[0], self.currLocale.toInt(self.nBitsChooser.currentText())[0], False, 'foo.wav')

class dropFrame(QFrame):
    drpd = QtCore.Signal(str) 
    def __init__(self, parent):
        QFrame.__init__(self, parent)
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
                self.drpd.emit(l[len(l)-1])
        else:
            event.ignore()


  
class commandExecuter1(QThread):
    def __init__(self, parent):
        QThread.__init__(self, parent)
    def executeCommand(self, cmd):
        self.cmd = cmd
        self.start()
    def run(self):
        for i in range(len(self.cmd)):
            os.system(self.cmd[i])
