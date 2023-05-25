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
    from PyQt5.QtCore import Qt, QEvent, QThread, QDate, QRegularExpression, QTime, QDateTime, QRect
    from PyQt5.QtWidgets import QAction, QApplication, QComboBox, QDesktopWidget, QFileDialog, QFrame, QGridLayout, QInputDialog, QLabel, QLineEdit, QMainWindow, QMessageBox, QProgressBar, QPushButton, QScrollArea, QShortcut, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget, QWidgetItem
    from PyQt5.QtGui import QColor, QDoubleValidator, QIcon, QIntValidator, QPainter, QRegularExpressionValidator, QValidator
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
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtCore import Qt, QEvent, QThread, QDate, QRegularExpression, QTime, QDateTime, QRect
    from PyQt6.QtWidgets import QApplication, QComboBox, QFileDialog, QFrame, QGridLayout, QInputDialog, QLabel, QLineEdit, QMainWindow, QMessageBox, QProgressBar, QPushButton, QScrollArea, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget, QWidgetItem
    from PyQt6.QtGui import QAction, QColor, QDoubleValidator, QIcon, QIntValidator, QPainter, QRegularExpressionValidator, QValidator, QShortcut
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

    
from numpy.fft import rfft, irfft, fft, ifft
import base64, fnmatch, copy, numpy, os, platform, random, string, smtplib, sys, time     
from numpy import abs, array, concatenate, exp, float64, log, log10, nan, mean, repeat, std
from .utils_general import*
from .stats_utils import*
from .pysdt import*
from scipy.stats.distributions import norm

from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders

from .audio_manager import*
from .dialog_show_instructions import*
from .stats_utils import*
from .sndlib import*
from .utils_general import*
from .utils_process_results import*
from .PSI_method import*
from .PSI_method_est_guess import setupPSIEstGuessRate, PSIEstGuessRate_update
from .UML_method import*
from .UML_method_est_guess import setupUMLEstGuessRate, UMLEstGuessRate_update


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
        self.setWindowFlags(QtCore.Qt.WindowType.Window | QtCore.Qt.WindowType.CustomizeWindowHint | QtCore.Qt.WindowType.WindowMinimizeButtonHint | QtCore.Qt.WindowType.WindowMaximizeButtonHint)
        #self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowSystemMenuHint) 
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.prm = parent.prm
        self.audioManager = parent.audioManager
        self.currLocale = self.parent().prm['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.NumberOption.OmitGroupSeparator | self.currLocale.NumberOption.RejectGroupSeparator)
        self.setWindowTitle(self.tr('Response Box'))
        self.responseBoxButtonFont = QFont()
        self.responseBoxButtonFont.fromString(self.prm["pref"]["resp_box"]["responseBoxButtonFont"])
        #self.setStyleSheet("QPushButton[responseBoxButton='true'] {font-weight:bold; font-size: %spx;} " % self.prm['pref']['interface']['responseButtonSize'])
        self.menubar = self.menuBar()
        #FILE MENU
        self.fileMenu = self.menubar.addMenu(self.tr('-'))

        ## for some reason couldn't get these into translation files in any other way
        foo = self.prm['rbTrans'].translate('rb', "CORRECT")
        foo = self.prm['rbTrans'].translate('rb', "INCORRECT")
        foo = self.prm['rbTrans'].translate('rb', "DONE")
        foo = self.prm['rbTrans'].translate('rb', "")
        ##
       
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
        #self.toggleBlockGauge.setChecked(True)

        #self.statusBar()
        self.fileMenu.addAction(self.toggleControlWin)
        self.fileMenu.addAction(self.toggleGauge)
        self.fileMenu.addAction(self.toggleBlockGauge)

        #HELP MENU
        self.helpMenu = self.menubar.addMenu(self.tr('&Help'))

        self.showInstructions = QAction(self.tr('Show Task Instructions'), self)
        self.showInstructions.triggered.connect(self.onClickShowInstructions)
        self.helpMenu.addAction(self.showInstructions)
        
        self.rb = QFrame()
        self.rb.setFrameStyle(QFrame.Shape.StyledPanel|QFrame.Shadow.Sunken)
        self.rb_sizer = QVBoxLayout()
        self.intervalSizer = QGridLayout()
        self.responseButtonSizer = QGridLayout()

        self.RBTaskLabel = QLabel(self.parent().taskLabelTF.text())
        self.RBTaskLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
       
        self.statusButton = QPushButton(self.prm['rbTrans'].translate('rb', "Wait"), self)
        self.statusButton.clicked.connect(self.onClickStatusButton)
        self.statusButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        #self.statusButton.setProperty("responseBoxButton", True)
        self.statusButton.setFont(self.responseBoxButtonFont)
        self.statBtnShortcut = QShortcut("Ctrl+R", self, activated = self.onClickStatusButton)
        self.statusButton.setToolTip(self.tr("Press Ctrl+R to activate"))
        
        self.responseLight = responseLight(self)

        self.gauge = QProgressBar(self)
        self.gauge.setRange(0, 100)
        self.blockGauge = QProgressBar(self)
 
        self.rb_sizer.addWidget(self.RBTaskLabel)
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

        if self.prm["pref"]["general"]["showBlockProgBar"] == True:
            self.toggleBlockGauge.setChecked(True)
            self.onToggleBlockGauge()
        else:
           self.toggleBlockGauge.setChecked(False)
           self.onToggleBlockGauge()
        if self.prm['blockProgbar'] == True:
            self.toggleBlockGauge.setChecked(True)
            self.onToggleBlockGauge()

        self.rb.setLayout(self.rb_sizer)
        self.setCentralWidget(self.rb)
        if self.prm['startMinimized'] == True:
            self.showMinimized()
        else:
            self.show()

        self.prm['listener'] = self.parent().listenerTF.text()
        self.prm['sessionLabel'] = self.parent().sessionLabelTF.text()
        if self.prm['hideWins'] == True:
            self.parent().hide()
   
    # def clearLayout(self, layout):
    #     #http://stackoverflow.com/questions/9374063/pyqt4-remove-widgets-and-layout-as-well
    #     for i in reversed(range(layout.count())):
    #         item = layout.itemAt(i)
    #         layout.removeItem(item)
    #         if isinstance(item, QWidgetItem):
    #             #item.widget().close()
    #             # or
    #             item.widget().setParent(None)
    #         elif isinstance(item, QSpacerItem):
    #             pass
    #             # no need to do extra stuff
    #         else:
    #             self.clearLayout(item.layout())

    #         # remove the item from layout
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())
             
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

        if pyqtversion == 5:
            screen = QDesktopWidget().screenGeometry()
        elif pyqtversion == 6:
            screen = self.screen().geometry()
            
        if self.parent().currExp == self.tr("Coordinate Response Measure"):
            self.statusButton.setMaximumSize(screen.width(), int(screen.height()/15))
            self.responseLight.setMaximumSize(screen.width(), int(screen.height()/10))
            self.statusButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
            self.responseLight.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

            cols = ["cornflowerblue", "red", "white", "green"]
            cnt = 0
            for cl in range(len(cols)):
                for rw in range(4):
                    self.responseButton.append(QPushButton(str(rw+1), self))
                    self.responseButtonSizer.addWidget(self.responseButton[cnt], rw, cl)
                    sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                    self.responseButton[cnt].setSizePolicy(sizePolicy)
                    #self.responseButton[cnt].setProperty("responseBoxButton", True)
                    self.responseButton[cnt].setFont(self.responseBoxButtonFont)
                    self.responseButton[cnt].clicked.connect(self.sortResponseButton)
                    self.responseButton[cnt].setFocusPolicy(Qt.FocusPolicy.NoFocus)
                    self.responseButton[cnt].setStyleSheet("background-color: " + cols[cl])
                    cnt = cnt+1
        elif self.parent().currExp in [self.tr("Digit Triplets Test"), self.tr("Digit Span")]:
            self.statusButton.setMaximumSize(screen.width(), int(screen.height()/15))
            self.responseLight.setMaximumSize(screen.width(), int(screen.height()/10))
            self.statusButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
            self.responseLight.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
            cnt = 0

            self.responseButton.append(QPushButton("0", self))
            self.responseButtonSizer.addWidget(self.responseButton[cnt], 3, 1)
            sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.responseButton[cnt].setSizePolicy(sizePolicy)
            self.responseButton[cnt].setFont(self.responseBoxButtonFont)
            self.responseButton[cnt].clicked.connect(self.dialerButtonClicked)
            self.responseButton[cnt].setFocusPolicy(Qt.FocusPolicy.NoFocus)
            cnt = cnt+1
            
            for rw in range(3):
                for cl in range(3):
                    self.responseButton.append(QPushButton(str(cnt), self))
                    self.responseButtonSizer.addWidget(self.responseButton[cnt], rw, cl)
                    sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                    self.responseButton[cnt].setSizePolicy(sizePolicy)
                    self.responseButton[cnt].setFont(self.responseBoxButtonFont)
                    self.responseButton[cnt].clicked.connect(self.dialerButtonClicked)
                    self.responseButton[cnt].setFocusPolicy(Qt.FocusPolicy.NoFocus)
                    cnt = cnt+1

            self.responseButton.append(QPushButton(self.tr("Backspace"), self))
            self.responseButtonSizer.addWidget(self.responseButton[cnt], 3, 0)
            sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.responseButton[cnt].setSizePolicy(sizePolicy)
            self.responseButton[cnt].setFont(self.responseBoxButtonFont)
            self.responseButton[cnt].clicked.connect(self.backspaceButtonPressed)
            self.responseButton[cnt].setFocusPolicy(Qt.FocusPolicy.NoFocus)
            cnt = cnt+1


            
            self.responseButton.append(QPushButton(self.tr("Enter"), self))
            self.responseButtonSizer.addWidget(self.responseButton[cnt], 3, 2)
            sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.responseButton[cnt].setSizePolicy(sizePolicy)
            self.responseButton[cnt].setFont(self.responseBoxButtonFont)
            self.responseButton[cnt].clicked.connect(self.enterButtonPressed)
            self.responseButton[cnt].setFocusPolicy(Qt.FocusPolicy.NoFocus)

            self.dialerResponseField = QLineEdit("")
            if self.parent().currExp == self.tr("Digit Triplets Test"): #only three max digits
                self.dialerResponseField.setValidator(QIntValidator(0, 999, self))
            else:
                thisValidator = QRegularExpressionValidator(self)
                thisValidator.setRegularExpression(QRegularExpression("[0-9]+"))
                self.dialerResponseField.setValidator(thisValidator)
                    
                #self.dialerResponseField.setValidator(ValidDigitSequence(self)) #QIntValidator doesn't accept digit sequences greater than 2^31 or something like that so we have to use a custom validator


            self.responseButtonSizer.addWidget(self.dialerResponseField, 4, 0, 1, 3)
            self.dialerResponseField.returnPressed.connect(self.enterButtonPressed)
            self.dialerResponseField.setSizePolicy(sizePolicy)
            self.dialerResponseField.setStyleSheet("font-size: 40px")
           

        else:
            self.statusButton.setMaximumSize(screen.width(), screen.height())
            self.responseLight.setMaximumSize(screen.width(), screen.height())
            if self.parent().currParadigm in ["Transformed Up-Down", #add translation
                                              "Transformed Up-Down Limited",
                                              "Transformed Up-Down Hybrid",
                                              "Weighted Up-Down",
                                              "Weighted Up-Down Limited",
                                              "Weighted Up-Down Hybrid",
                                              "Constant m-Intervals n-Alternatives",
                                              "Transformed Up-Down Interleaved",
                                              "Weighted Up-Down Interleaved",
                                              "Multiple Constants m-Intervals n-Alternatives",
                                              "PEST",
                                              "Maximum Likelihood",
                                              "PSI",
                                              "UML"]:

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
                    self.responseButtonSizer.addItem(QSpacerItem(-1, -1, QSizePolicy.Policy.Expanding), 0, r)
                    r = r+1
                if self.prm["preTrialInterval"] == True:
                    self.responseButtonSizer.addItem(QSpacerItem(-1, -1, QSizePolicy.Policy.Expanding), 0, r)
                    r = r+1
                if nAlternatives == nIntervals:
                    for i in range(nAlternatives):
                        if self.prm["precursorInterval"] == True:
                            self.responseButtonSizer.addItem(QSpacerItem(-1, -1, QSizePolicy.Policy.Expanding), 0, r)
                            r = r+1
                        self.responseButton.append(QPushButton(str(i+1), self))
                        self.responseButtonSizer.addWidget(self.responseButton[i], 1, r)
                        self.responseButton[i].setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
                        #self.responseButton[i].setProperty("responseBoxButton", True)
                        self.responseButton[i].setFont(self.responseBoxButtonFont)
                        r = r+1
                        if self.prm[self.parent().currExp]["hasPostcursorInterval"] == True:
                            self.responseButtonSizer.addItem(QSpacerItem(-1, -1, QSizePolicy.Policy.Expanding), 0, r)
                            r = r+1
                        self.responseButton[i].clicked.connect(self.sortResponseButton)
                        self.responseButton[i].setFocusPolicy(Qt.FocusPolicy.NoFocus)

                elif nAlternatives == nIntervals-1:
                    for i in range(nAlternatives):
                        if self.prm[self.parent().currExp]["hasPrecursorInterval"] == True:
                            self.responseButtonSizer.addItem(QSpacerItem(-1, -1, QSizePolicy.Policy.Expanding), 0, r)
                            r = r+1
                        if i == 0:
                            self.responseButtonSizer.addItem(QSpacerItem(-1, -1, QSizePolicy.Policy.Expanding), 0, r)
                            r = r+1

                        self.responseButton.append(QPushButton(str(i+1), self))
                        self.responseButtonSizer.addWidget(self.responseButton[i], 1, r)
                        self.responseButton[i].setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
                        #self.responseButton[i].setProperty("responseBoxButton", True)
                        self.responseButton[i].setFont(self.responseBoxButtonFont)
                        r = r+1
                        self.responseButton[i].clicked.connect(self.sortResponseButton)
                        self.responseButton[i].setFocusPolicy(Qt.FocusPolicy.NoFocus)
                        if self.prm[self.parent().currExp]["hasPostcursorInterval"] == True:
                            self.responseButtonSizer.addItem(QSpacerItem(-1, -1, QSizePolicy.Policy.Expanding), 0, r)
                            r = r+1

            elif self.parent().currParadigm in ["Constant 1-Interval 2-Alternatives",
                                                "Multiple Constants 1-Interval 2-Alternatives",
                                                "Constant 1-Pair Same/Different",
                                                "Multiple Constants 1-Pair Same/Different",
                                                "Constant ABX",
                                                "Multiple Constants ABX",
                                                "UML - Est. Guess Rate",
                                                "PSI - Est. Guess Rate"]:
                for i in range(nIntervals):
                    self.intervalLight.append(intervalLight(self))
                    self.intervalSizer.addWidget(self.intervalLight[n], 0, n)
                    n = n+1

                for i in range(self.prm['nAlternatives']):
                    self.responseButton.append(QPushButton(self.prm[self.tr(self.parent().experimentChooser.currentText())]['buttonLabels'][i], self))

                    self.responseButtonSizer.addWidget(self.responseButton[i], 1, i)
                    self.responseButton[i].setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
                    #self.responseButton[i].setProperty("responseBoxButton", True)
                    self.responseButton[i].setFont(self.responseBoxButtonFont)
                    self.responseButton[i].clicked.connect(self.sortResponseButton)
                    self.responseButton[i].setFocusPolicy(Qt.FocusPolicy.NoFocus)
            elif self.parent().currParadigm in ["Constant ABX", "Multiple Constants ABX"]:
                for i in range(3):
                    self.intervalLight.append(intervalLight(self))
                    self.intervalSizer.addWidget(self.intervalLight[n], 0, n)
                    n = n+1

                for i in range(2):
                    self.responseButton.append(QPushButton(self.prm[self.tr(self.parent().experimentChooser.currentText())]['buttonLabels'][i], self))

                    self.responseButtonSizer.addWidget(self.responseButton[i], 1, i)
                    self.responseButton[i].setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
                    #self.responseButton[i].setProperty("responseBoxButton", True)
                    self.responseButton[i].setFont(self.responseBoxButtonFont)
                    self.responseButton[i].clicked.connect(self.sortResponseButton)
                    self.responseButton[i].setFocusPolicy(Qt.FocusPolicy.NoFocus)
            elif self.parent().currParadigm in ["Multiple Constants Odd One Out", "Multiple Constants Sound Comparison"]:
                for i in range(nIntervals):
                    self.intervalLight.append(intervalLight(self))
                    self.intervalSizer.addWidget(self.intervalLight[n], 0, n)
                    n = n+1

                r = 0
                if self.prm["warningInterval"] == True:
                    self.responseButtonSizer.addItem(QSpacerItem(-1, -1, QSizePolicy.Policy.Expanding), 0, r)
                    r = r+1
                for i in range(self.prm['nAlternatives']):
                    self.responseButton.append(QPushButton(str(i+1), self))
                    self.responseButtonSizer.addWidget(self.responseButton[i], 1, i+r)
                    self.responseButton[i].setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
                    #self.responseButton[i].setProperty("responseBoxButton", True)
                    self.responseButton[i].setFont(self.responseBoxButtonFont)
                    self.responseButton[i].clicked.connect(self.sortResponseButton)
                    self.responseButton[i].setFocusPolicy(Qt.FocusPolicy.NoFocus)


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

    def onClickShowInstructions(self):
        dialog = showInstructionsDialog(self)

    def onAskSaveResultsButton(self):
        ftow = QFileDialog.getSaveFileName(self, self.tr('Choose file to write results'), "", self.tr('All Files (*)'), "", QFileDialog.DontConfirmOverwrite)[0]
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
        #print(self.statusButton.text())
        if self.prm['storedBlocks'] == 0 or self.statusButton.text() in [self.prm['rbTrans'].translate("rb", "Running"), "&"+self.prm['rbTrans'].translate("rb", "Running")] or self.statusButton.text() in [self.prm['rbTrans'].translate("rb", "Finished"), "&" + self.prm['rbTrans'].translate("rb", "Finished")]:
            return
        self.parent().compareGuiStoredParameters()
        
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
                                               self.prm['rbTrans'].translate('rb', "Do you want to shuffle the blocks?"), QMessageBox.StandardButton.Yes | 
                                               QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.parent().onClickShuffleBlocksButton()
                self.prm["shuffled"] = True
        elif int(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition']) == 1 and self.prm["shuffled"] == False and self.prm['allBlocks']['shuffleMode'] == self.tr("Auto") and self.prm['storedBlocks'] > 1 :
         
            self.parent().onClickShuffleBlocksButton()

            self.prm["shuffled"] = True
        #self.prm[currBlock]['blockPosition']
        if int(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition']) in self.prm["allBlocks"]["instructionsAt"]:
            instrClosed = False
            while instrClosed == False:
                dialog = showInstructionsDialog(self)
                if dialog.exec_():
                    instrClosed = True
                else:
                    instrClosed = True
                time.sleep(1.5)
        self.prm['startOfBlock'] = True
        self.statusButton.setText(self.prm['rbTrans'].translate("rb", "Running"))
        self.prm['trialRunning'] = True
        QApplication.processEvents()

        if self.prm['allBlocks']['sendTriggers'] == True:
            thisSnd = pureTone(440, 0, -200, 980, 10, "Both", self.prm['allBlocks']['sampRate'], 100)
            #playCmd = self.prm['pref']['sound']['playCommand']
            self.audioManager.playSoundWithTrigger(thisSnd, self.prm['allBlocks']['sampRate'], self.prm['allBlocks']['nBits'], False, 'ONTrigger.wav', self.prm["pref"]["general"]["ONTrigger"])
            print("SENDING START TRIGGER", self.prm["pref"]["general"]["ONTrigger"])
        if self.prm['currentBlock'] > self.prm['storedBlocks']:
            self.parent().onClickNextBlockPositionButton()

        self.doTrial()

    def playRandomisedIntervals(self, stimulusCorrect, stimulusIncorrect, preTrialStim=None, precursorStim=None, postCursorStim=None):
        # this randint function comes from numpy and has different behaviour than in the python 'random' module
        # Return random integers x such that low <= x < high
        currBlock = 'b'+ str(self.prm['currentBlock'])
        try:
            nAlternatives = self.prm[currBlock]['nAlternatives']
            nIntervals = self.prm[currBlock]['nIntervals']
        except: #this should work for paradigms that don't have the alternatives chooser, hence have a fixed number of response alternatives
             nIntervals = self.prm[self.parent().currExp]['defaultNIntervals'] 
             nAlternatives = self.prm[self.parent().currExp]['defaultNAlternatives'] 
        #cmd = self.prm['pref']['sound']['playCommand']
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
            self.audioManager.playSound(preTrialStim, self.prm['allBlocks']['sampRate'], self.prm['allBlocks']['nBits'], self.prm['pref']['sound']['writewav'], 'pre-trial_interval' +'.wav')
            self.intervalLight[nLight].setStatus('off')
            nLight = nLight+1
            time.sleep(self.prm[currBlock]['preTrialIntervalISI']/1000)

        for i in range(nIntervals):
            if self.prm["precursorInterval"] == True:
                self.intervalLight[nLight].setStatus('on')
                self.audioManager.playSound(precursorStim, self.prm['allBlocks']['sampRate'], self.prm['allBlocks']['nBits'], self.prm['pref']['sound']['writewav'], 'precursor_interval'+str(i+1) +'.wav')
                self.intervalLight[nLight].setStatus('off')
                nLight = nLight+1
                time.sleep(self.prm[currBlock]['precursorIntervalISI']/1000)
            self.intervalLight[nLight].setStatus('on')
            self.audioManager.playSound(soundList[i], self.prm['allBlocks']['sampRate'], self.prm['allBlocks']['nBits'], self.prm['pref']['sound']['writewav'], 'interval'+str(i+1) +'.wav')
            self.intervalLight[nLight].setStatus('off')
            nLight = nLight+1
            if self.prm["postcursorInterval"] == True:
                self.intervalLight[nLight].setStatus('on')
                self.audioManager.playSound(postcursorStim, self.prm['allBlocks']['sampRate'], self.prm['allBlocks']['nBits'], self.prm['pref']['sound']['writewav'], 'postcursor_interval'+str(i+1) +'.wav')
                self.intervalLight[nLight].setStatus('off')
                nLight = nLight+1
                time.sleep(self.prm[currBlock]['postcursorIntervalISI']/1000)
            if i < nIntervals-1:
                time.sleep(self.prm['isi']/1000.)

    def playSequentialIntervals(self, sndList, ISIList=[], trigNum=None):
        currBlock = 'b'+ str(self.prm['currentBlock'])
        #cmd = self.prm['pref']['sound']['playCommand']
        for i in range(len(sndList)):
            if self.prm['pref']['sound']['writeSndSeqSegments'] == True:
                #self.audioManager.scipy_wavwrite("sndSeq%i.wav"%(i+1), self.prm['allBlocks']['sampRate'], self.prm['allBlocks']['nBits'], sndList[i])
                self.audioManager.wavwrite(sndList[i], self.prm['allBlocks']['sampRate'], self.prm['allBlocks']['nBits'], "sndSeq%i.wav"%(i+1))
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
                self.audioManager.playSoundWithTrigger(sndList[i], self.prm['allBlocks']['sampRate'], self.prm['allBlocks']['nBits'], self.prm['pref']['sound']['writewav'], 'soundSequence.wav', trigNum)
            else:
                self.audioManager.playSound(sndList[i], self.prm['allBlocks']['sampRate'], self.prm['allBlocks']['nBits'], self.prm['pref']['sound']['writewav'], 'soundSequence.wav')
            self.intervalLight[nLight].setStatus('off')
            nLight = nLight+1

            if i < (len(sndList) - 1):
                time.sleep(ISIList[i]/1000)

        return

    def playSequentialIntervalsNoLights(self, sndList, ISIList=[], trigNum=None):
        currBlock = 'b'+ str(self.prm['currentBlock'])
        #self.dialerResponseField.setReadOnly(True)
        
        for i in range(len(sndList)):
            if self.prm['pref']['sound']['writeSndSeqSegments'] == True:
                self.audioManager.wavwrite(sndList[i], self.prm['allBlocks']['sampRate'], self.prm['allBlocks']['nBits'], "sndSeq%i.wav"%(i+1))
        for i in range(len(sndList)):
            if trigNum != None:
                self.audioManager.playSoundWithTrigger(sndList[i], self.prm['allBlocks']['sampRate'], self.prm['allBlocks']['nBits'], self.prm['pref']['sound']['writewav'], 'soundSequence.wav', trigNum)
            else:
                self.audioManager.playSound(sndList[i], self.prm['allBlocks']['sampRate'], self.prm['allBlocks']['nBits'], self.prm['pref']['sound']['writewav'], 'soundSequence.wav')

            if i < (len(sndList) - 1):
                time.sleep(ISIList[i]/1000)
        #self.dialerResponseField.setReadOnly(False)
        #self.dialerResponseField.setText("")
        #QApplication.processEvents()

        return
    

    def playSoundsWavComp(self, soundList):
        currBlock = 'b'+ str(self.prm['currentBlock'])
        nIntervals = self.prm['nIntervals']

        # numpy.random.shuffle(parent.prm['currStimOrder'])
        # parent.correctButton = parent.prm['currStimOrder'].index(2)+1

        nLight = 0
        if self.prm["warningInterval"] == True:
            self.intervalLight[nLight].setStatus('on')
            time.sleep(self.prm[currBlock]['warningIntervalDur']/1000)
            self.intervalLight[nLight].setStatus('off')
            nLight = nLight+1
            time.sleep(self.prm[currBlock]['warningIntervalISI']/1000)
            
        for i in range(nIntervals):
            self.intervalLight[nLight].setStatus('on')
            self.audioManager.playSound(soundList[i], self.prm['allBlocks']['sampRate'], self.prm['allBlocks']['nBits'], self.prm['pref']['sound']['writewav'], 'interval'+str(i+1) +'.wav')
            self.intervalLight[nLight].setStatus('off')
            nLight = nLight+1
            if i < nIntervals-1:
                time.sleep(self.prm['isi']/1000)

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
        if self.prm[self.parent().currExp]["hasAltReps"] == True:
            self.prm['altReps'] = self.prm[currBlock]['altReps']
            self.prm['altRepsISI'] = self.prm[currBlock]['altRepsISI']
        else:
            self.prm['altReps'] = 0
        self.prm["responseLight"] = self.prm[currBlock]['responseLight']
        self.prm["responseLightType"] = self.prm[currBlock]['responseLightType']

        if self.prm['startOfBlock'] == True:
            self.getStartTime()
            #clear these variables
            self.prm['additional_parameters_to_write'] = {}
            self.prm['additional_parameters_to_write_labels'] = []

            if self.prm['paradigm'] in [self.tr("Transformed Up-Down Interleaved"),
                                        self.tr("Weighted Up-Down Interleaved")]:
                self.prm['nDifferences'] = int(self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("No. Tracks:"))])
                if self.prm['nDifferences'] == 1:
                    self.prm['maxConsecutiveTrials'] = self.tr('unlimited')
                else:
                    self.prm['maxConsecutiveTrials'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Max. Consecutive Trials x Track:"))]
           
            if self.prm['paradigm'] in [self.tr("Transformed Up-Down"), self.tr("Transformed Up-Down Limited")]:
                self.prm['numberCorrectNeeded'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Rule Down"))])
                self.prm['numberIncorrectNeeded'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Rule Up"))])
                self.prm['initialTurnpoints'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Initial Turnpoints"))])
                self.prm['totalTurnpoints'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Total Turnpoints"))])
                self.prm['adaptiveStepSize1'] = self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Step Size 1"))]
                self.prm['adaptiveStepSize2'] = self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Step Size 2"))]
                self.prm['adaptiveType'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Procedure:"))]
                self.prm['corrTrackDir'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Corr. Resp. Move Track:"))]

            elif self.prm['paradigm'] == self.tr("Transformed Up-Down Interleaved"):
                self.prm['adaptiveType'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Procedure:"))]
                self.prm['turnpointsToAverage'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Turnpoints to average:"))]
                
                self.prm['numberCorrectNeeded'] = []
                self.prm['numberIncorrectNeeded'] = []
                self.prm['initialTurnpoints'] = []
                self.prm['totalTurnpoints'] = []
                self.prm['adaptiveStepSize1'] = []
                self.prm['adaptiveStepSize2'] = []
                self.prm['consecutiveTrialsCounter'] = []
                self.prm['corrTrackDir'] = []
                for i in range(self.prm['nDifferences']):
                    self.prm['numberCorrectNeeded'].append(int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Rule Down Track " + str(i+1)))]))
                    self.prm['numberIncorrectNeeded'].append(int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Rule Up Track " + str(i+1)))]))
                    self.prm['initialTurnpoints'].append(int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Initial Turnpoints Track " + str(i+1)))]))
                    self.prm['totalTurnpoints'].append(int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Total Turnpoints Track " + str(i+1)))]))
                    self.prm['adaptiveStepSize1'].append(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Step Size 1 Track " + str(i+1)))])
                    self.prm['adaptiveStepSize2'].append(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Step Size 2 Track " + str(i+1)))])
                    self.prm['consecutiveTrialsCounter'].append(0)
                    self.prm['corrTrackDir'].append(self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Corr. Resp. Move Track {0}:".format(str(i+1))))])
            elif self.prm['paradigm'] in [self.tr("Transformed Up-Down Hybrid")]:
                self.prm['numberCorrectNeeded'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Rule Down"))])
                self.prm['numberIncorrectNeeded'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Rule Up"))])
                self.prm['initialTurnpoints'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Initial Turnpoints"))])
                self.prm['totalTurnpoints'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Total Turnpoints"))])
                self.prm['adaptiveStepSize1'] = self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Step Size 1"))]
                self.prm['adaptiveStepSize2'] = self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Step Size 2"))]
                self.prm['adaptiveType'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Procedure:"))]
                self.prm['corrTrackDir'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Corr. Resp. Move Track:"))]
                self.prm['nTrialsRequiredAtMaxLimit'] = self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Constant No. Trials"))]
                #self.prm['minSwitchTrials'] = self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Min. No. trials before switch"))]
                #self.prm['adaptiveMaxLimit'] = self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Adapt. Param. Limit"))]
                self.prm['switchAfterInitialTurnpoints'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Switch only after initial turnpoints:"))]

            elif self.prm['paradigm'] in [self.tr("Weighted Up-Down"), self.tr("Weighted Up-Down Limited")]:
                self.prm['percentCorrectTracked'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Percent Correct Tracked"))])

                self.prm['initialTurnpoints'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Initial Turnpoints"))])
                self.prm['totalTurnpoints'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Total Turnpoints"))])
                self.prm['adaptiveStepSize1'] = self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Step Size 1"))]
                self.prm['adaptiveStepSize2'] = self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Step Size 2"))]
                self.prm['adaptiveType'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Procedure:"))]
                self.prm['corrTrackDir'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Corr. Resp. Move Track:"))]
                self.prm['numberCorrectNeeded'] = 1
                self.prm['numberIncorrectNeeded'] = 1

            elif self.prm['paradigm'] == self.tr("Weighted Up-Down Interleaved"):
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
                self.prm['corrTrackDir'] = []
                for i in range(self.prm['nDifferences']):
                    self.prm['numberCorrectNeeded'].append(1)
                    self.prm['numberIncorrectNeeded'].append(1)
                    self.prm['percentCorrectTracked'].append(float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Percent Correct Tracked Track " + str(i+1)))]))
                    self.prm['initialTurnpoints'].append(int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Initial Turnpoints Track " + str(i+1)))]))
                    self.prm['totalTurnpoints'].append(int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Total Turnpoints Track " + str(i+1)))]))
                    self.prm['adaptiveStepSize1'].append(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Step Size 1 Track " + str(i+1)))])
                    self.prm['adaptiveStepSize2'].append(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Step Size 2 Track " + str(i+1)))])
                    self.prm['consecutiveTrialsCounter'].append(0)
                    self.prm['corrTrackDir'].append(self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Corr. Resp. Move Track {0}:".format(str(i+1))))])

            elif self.prm['paradigm'] in [self.tr("Weighted Up-Down Hybrid")]:
                self.prm['percentCorrectTracked'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Percent Correct Tracked"))])

                self.prm['initialTurnpoints'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Initial Turnpoints"))])
                self.prm['totalTurnpoints'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Total Turnpoints"))])
                self.prm['adaptiveStepSize1'] = self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Step Size 1"))]
                self.prm['adaptiveStepSize2'] = self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Step Size 2"))]
                self.prm['adaptiveType'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Procedure:"))]
                self.prm['corrTrackDir'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Corr. Resp. Move Track:"))]
                self.prm['numberCorrectNeeded'] = 1
                self.prm['numberIncorrectNeeded'] = 1
                self.prm['nTrialsRequiredAtMaxLimit'] = self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Constant No. Trials"))]
                #self.prm['minSwitchTrials'] = self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Min. No. trials before switch"))]
                self.prm['switchAfterInitialTurnpoints'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Switch only after initial turnpoints:"))]
                
            elif self.prm['paradigm'] in [self.tr("Constant m-Intervals n-Alternatives"),
                                          self.tr("Constant 1-Interval 2-Alternatives"),
                                          self.tr("Constant 1-Pair Same/Different")]:
                self.prm['nTrials'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("No. Trials"))])
                self.prm['nPracticeTrials'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("No. Practice Trials"))])
            elif self.prm['paradigm'] in [self.tr("Multiple Constants 1-Interval 2-Alternatives"),
                                          self.tr("Multiple Constants m-Intervals n-Alternatives"),
                                          self.tr("Multiple Constants 1-Pair Same/Different"),
                                          self.tr("Multiple Constants ABX"),
                                          self.tr("Multiple Constants Odd One Out"),
                                          self.tr("Multiple Constants Sound Comparison")]:
                self.prm['nTrials'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("No. Trials"))])
                self.prm['nPracticeTrials'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("No. Practice Trials"))])
                self.prm['nDifferences'] = int(self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("No. Differences:"))])
                if self.prm['startOfBlock'] == True:
                    self.prm['currentDifference'] = numpy.random.randint(self.prm['nDifferences'])
            elif self.prm['paradigm'] == self.tr("PEST"):
                self.prm['corrTrackDir'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Corr. Resp. Move Track:"))]
                self.prm['adaptiveType'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Procedure:"))]
                self.prm['initialStepSize'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Initial Step Size"))])
                self.prm['minStepSize'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Minimum Step Size"))])
                self.prm['maxStepSize'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Maximum Step Size"))])
                self.prm['percentCorrectTracked'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Percent Correct Tracked"))])
                self.prm['W'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("W"))])
            elif self.prm["paradigm"] == self.tr("Maximum Likelihood"):
                self.prm['psyFunType'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Psychometric Function:"))]
                self.prm['psyFunLogScale'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Log scale:"))]
                self.prm['psyFunLoMidPoint'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Mid Point Minimum"))])
                self.prm['psyFunHiMidPoint'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Mid Point Maximum"))])
                self.prm['psyFunMidPointStep'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Mid Point Step"))])
                self.prm['percentCorrectTracked'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Percent Correct Tracked"))])
                self.prm['psyFunSlope'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Psychometric Function Slope"))])
                self.prm['psyFunLapseRate'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Lapse Rate"))])
                self.prm['nTrials'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("No. Trials"))])
            elif self.prm["paradigm"] == self.tr("PSI"):
                self.prm['psyFunType'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Psychometric Function:"))]
                self.prm['nTrials'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("No. Trials"))])
                self.prm['stimScale'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Stim. Scaling:"))]

                self.prm['stimLo'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Stim. Min"))])
                self.prm['stimHi'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Stim. Max"))])
                self.prm['stimStep'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Stim. Step"))])

                self.prm['loMidPoint'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Mid Point Min"))])
                self.prm['hiMidPoint'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Mid Point Max"))])
                self.prm['midPointStep'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Mid Point Step"))])
                self.prm['midPointPrior'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Mid Point Prior:"))]
                self.prm['midPointPriorMu'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Mid Point mu"))])
                self.prm['midPointPriorSTD'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Mid Point STD"))])

                self.prm['loSlope'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Slope Min"))])
                self.prm['hiSlope'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Slope Max"))])
                self.prm['slopeStep'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Slope Step"))])
                self.prm['slopeSpacing'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Slope Spacing:"))]
                self.prm['slopePrior'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Slope Prior:"))]
                self.prm['slopePriorMu'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Slope mu"))])
                self.prm['slopePriorSTD'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Slope STD"))])

                self.prm['loLapse'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Lapse Min"))])
                self.prm['hiLapse'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Lapse Max"))])
                self.prm['lapseStep'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Lapse Step"))])
                self.prm['lapseSpacing'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Lapse Spacing:"))]
                self.prm['lapsePrior'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Lapse Prior:"))]
                self.prm['lapsePriorMu'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Lapse mu"))])
                self.prm['lapsePriorSTD'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Lapse STD"))])

                self.prm['margLapse'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Marginalize Lapse:"))]
                self.prm['margSlope'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Marginalize Slope:"))]
                self.prm['margThresh'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Marginalize Mid Point:"))]
                self.prm['startLevelType'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Start Level:"))]

            elif self.prm["paradigm"] == self.tr("PSI - Est. Guess Rate"):
                self.prm['psyFunType'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Psychometric Function:"))]
                self.prm['nTrials'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("No. Trials"))])
                self.prm['stimScale'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Stim. Scaling:"))]

                self.prm['stimLo'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Stim. Min"))])
                self.prm['stimHi'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Stim. Max"))])
                self.prm['stimStep'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Stim. Step"))])

                self.prm['loMidPoint'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Mid Point Min"))])
                self.prm['hiMidPoint'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Mid Point Max"))])
                self.prm['midPointStep'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Mid Point Step"))])
                self.prm['midPointPrior'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Mid Point Prior:"))]
                self.prm['midPointPriorMu'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Mid Point mu"))])
                self.prm['midPointPriorSTD'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Mid Point STD"))])

                self.prm['loGuess'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Guess Min"))])
                self.prm['hiGuess'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Guess Max"))])
                self.prm['guessStep'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Guess Step"))])
                self.prm['guessSpacing'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Guess Spacing:"))]
                self.prm['guessPrior'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Guess Prior:"))]
                self.prm['guessPriorMu'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Guess mu"))])
                self.prm['guessPriorSTD'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Guess STD"))])

                self.prm['loSlope'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Slope Min"))])
                self.prm['hiSlope'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Slope Max"))])
                self.prm['slopeStep'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Slope Step"))])
                self.prm['slopeSpacing'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Slope Spacing:"))]
                self.prm['slopePrior'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Slope Prior:"))]
                self.prm['slopePriorMu'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Slope mu"))])
                self.prm['slopePriorSTD'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Slope STD"))])

                self.prm['loLapse'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Lapse Min"))])
                self.prm['hiLapse'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Lapse Max"))])
                self.prm['lapseStep'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Lapse Step"))])
                self.prm['lapseSpacing'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Lapse Spacing:"))]
                self.prm['lapsePrior'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Lapse Prior:"))]
                self.prm['lapsePriorMu'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Lapse mu"))])
                self.prm['lapsePriorSTD'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Lapse STD"))])

                self.prm['margGuess'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Marginalize Guess:"))]
                self.prm['margLapse'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Marginalize Lapse:"))]
                self.prm['margSlope'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Marginalize Slope:"))]
                self.prm['margThresh'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Marginalize Mid Point:"))]
                self.prm['startLevelType'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Start Level:"))]

            elif self.prm["paradigm"] == self.tr("UML"):
                self.prm['psyFunType'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Psychometric Function:"))]
                self.prm['swptRule'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Swpt. Rule:"))]
                self.prm['psyFunPosteriorSummary'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Posterior Summary:"))]
                self.prm['nTrials'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("No. Trials"))])
                self.prm['numberCorrectNeeded'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Rule Down"))])
                
                self.prm['stimScale'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Stim. Scaling:"))]
                self.prm['stimLo'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Stim. Min"))])
                self.prm['stimHi'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Stim. Max"))])
                self.prm['suggestedLambdaSwpt'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Suggested Lapse Swpt."))])
                self.prm['lambdaSwptPC'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Pr. Corr. at Est. Lapse Swpt."))])

                self.prm['loMidPoint'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Mid Point Min"))])
                self.prm['hiMidPoint'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Mid Point Max"))])
                self.prm['midPointStep'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Mid Point Step"))])
                self.prm['midPointPrior'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Mid Point Prior:"))]
                self.prm['midPointPriorMu'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Mid Point mu"))])
                self.prm['midPointPriorSTD'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Mid Point STD"))])

                self.prm['loSlope'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Slope Min"))])
                self.prm['hiSlope'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Slope Max"))])
                self.prm['slopeStep'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Slope Step"))])
                self.prm['slopeSpacing'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Slope Spacing:"))]
                self.prm['slopePrior'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Slope Prior:"))]
                self.prm['slopePriorMu'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Slope mu"))])
                self.prm['slopePriorSTD'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Slope STD"))])

                self.prm['loLapse'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Lapse Min"))])
                self.prm['hiLapse'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Lapse Max"))])
                self.prm['lapseStep'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Lapse Step"))])
                self.prm['lapseSpacing'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Lapse Spacing:"))]
                self.prm['lapsePrior'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Lapse Prior:"))]
                self.prm['lapsePriorMu'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Lapse mu"))])
                self.prm['lapsePriorSTD'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Lapse STD"))])

                if self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Load UML state from prev. blocks:"))] == "Yes":
                    self.prm["saveUMLState"] = True
                else:
                    self.prm["saveUMLState"] = False

            elif self.prm["paradigm"] == self.tr("UML - Est. Guess Rate"):
                self.prm['psyFunType'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Psychometric Function:"))]
                self.prm['swptRule'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Swpt. Rule:"))]
                self.prm['psyFunPosteriorSummary'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Posterior Summary:"))]
                self.prm['nTrials'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("No. Trials"))])
                self.prm['numberCorrectNeeded'] = int(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Rule Down"))])
                
                self.prm['stimScale'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Stim. Scaling:"))]
                self.prm['stimLo'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Stim. Min"))])
                self.prm['stimHi'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Stim. Max"))])
                self.prm['suggestedLambdaSwpt'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Suggested Lapse Swpt."))])
                self.prm['lambdaSwptPC'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Pr. Corr. at Est. Lapse Swpt."))])

                self.prm['loMidPoint'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Mid Point Min"))])
                self.prm['hiMidPoint'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Mid Point Max"))])
                self.prm['midPointStep'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Mid Point Step"))])
                self.prm['midPointPrior'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Mid Point Prior:"))]
                self.prm['midPointPriorMu'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Mid Point mu"))])
                self.prm['midPointPriorSTD'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Mid Point STD"))])

                self.prm['loGuess'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Guess Min"))])
                self.prm['hiGuess'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Guess Max"))])
                self.prm['guessStep'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Guess Step"))])
                self.prm['guessSpacing'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Guess Spacing:"))]
                self.prm['guessPrior'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Guess Prior:"))]
                self.prm['guessPriorMu'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Guess mu"))])
                self.prm['guessPriorSTD'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Guess STD"))])

                self.prm['loSlope'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Slope Min"))])
                self.prm['hiSlope'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Slope Max"))])
                self.prm['slopeStep'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Slope Step"))])
                self.prm['slopeSpacing'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Slope Spacing:"))]
                self.prm['slopePrior'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Slope Prior:"))]
                self.prm['slopePriorMu'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Slope mu"))])
                self.prm['slopePriorSTD'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Slope STD"))])

                self.prm['loLapse'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Lapse Min"))])
                self.prm['hiLapse'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Lapse Max"))])
                self.prm['lapseStep'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Lapse Step"))])
                self.prm['lapseSpacing'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Lapse Spacing:"))]
                self.prm['lapsePrior'] = self.prm[currBlock]['paradigmChooser'][self.prm[currBlock]['paradigmChooserLabel'].index(self.tr("Lapse Prior:"))]
                self.prm['lapsePriorMu'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Lapse mu"))])
                self.prm['lapsePriorSTD'] = float(self.prm[currBlock]['paradigmField'][self.prm[currBlock]['paradigmFieldLabel'].index(self.tr("Lapse STD"))])


                
        if self.prm['startOfBlock'] == True and 'resultsFile' not in self.prm:
            if self.prm['pref']['general']['resFileFormat'] == 'fixed':
                self.prm['resultsFile'] = self.prm['pref']['general']['resFileFixedString']
                resFileToOpen = copy.copy(self.prm['pref']['general']['resFileFixedString'])

                fName = open(resFileToOpen, 'a')
                fName.write('')
                fName.close()
            elif self.prm['pref']['general']['resFileFormat'] == 'variable':
                self.prm['resultsFile'] = self.prm['listener'] + '_' + time.strftime("%y-%m-%d_%H-%M-%S", time.localtime())

        if self.prm['paradigm'] in [self.tr("Transformed Up-Down Interleaved"),
                                    self.tr("Weighted Up-Down Interleaved")]:
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
                                         "[resFileTrial]",
                                         "[resFileSess]",
                                         "[resTable]",
                                         "[resTableTrial]",
                                         "[resTableSess]",
                                         "[pdfPlot]",
                                         "[listener]",
                                         "[experimenter]"]
        self.pychovariablesSubstitute = [os.path.dirname(self.prm['resultsFile']),
                                         self.prm['resultsFile'],
                                         self.prm['resultsFile'].split('.txt')[0]+ self.prm["pref"]["general"]["fullFileSuffix"],
                                         self.prm['resultsFile'].split('.txt')[0]+ self.prm["pref"]["general"]["sessSummResFileSuffix"],
                                         self.prm['resultsFile'].split('.txt')[0]+'_table.csv',
                                         self.prm['resultsFile'].split('.txt')[0]+'_table' + self.prm["pref"]["general"]["fullFileSuffix"]+'.csv',
                                         self.prm['resultsFile'].split('.txt')[0]+'_table' + self.prm["pref"]["general"]["sessSummResFileSuffix"]+'.csv',
                                         self.prm['resultsFile'].split('.txt')[0]+'_table' + self.prm["pref"]["general"]["sessSummResFileSuffix"]+'.pdf',
                                         self.prm['listener'],
                                         self.prm['allBlocks']['currentExperimenter']]
      

        
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
            resp = np.random.binomial(1, self.prm['allBlocks']['autoPCCorr'], 1)[0]
            if resp == 1:
                self.sortResponse(self.correctButton)
            else:
                self.sortResponse(random.choice(numpy.delete(numpy.arange(self.prm['nAlternatives'])+1, self.correctButton-1)))

        if self.prm['allBlocks']['responseMode'] == self.tr("Psychometric"):
            if self.prm['paradigm'] not in [self.tr("Transformed Up-Down"),
                                            self.tr("Weighted Up-Down"),
                                            self.tr("Transformed Up-Down Limited"),
                                            self.tr("Transformed Up-Down Hybrid"),
                                            self.tr("Weighted Up-Down Limited"),
                                            self.tr("Weighted Up-Down Hybrid"),
                                            self.tr("Transformed Up-Down Interleaved"),
                                            self.tr("Weighted Up-Down Interleaved"),
                                            self.tr("PEST"), self.tr("Maximum Likelihood"),
                                            self.tr("PSI"),
                                            self.tr("UML"),
                                            self.tr("UML - Est. Guess Rate"),
                                            self.tr("PSI - Est. Guess Rate")]:
                ret = QMessageBox.warning(self, self.tr("Warning"),
                                          self.tr("Sorry, psychometric listener not supported by current paradigm. Please, choose another response mode."),
                                          QMessageBox.StandardButton.Ok)
                return
                
            self.prm['responseModeChoices'] = ["Real Listener", "Automatic", "Simulated Listener", "Psychometric"]
            if self.prm[currBlock]['psyListFun'] == "Logistic":
                if self.prm[currBlock]['psyListFunFit'] == "Linear":
                    probCorr = logisticPsy(self.prm['adaptiveParam'], self.prm[currBlock]['psyListMidpoint'],
                                           self.prm[currBlock]['psyListSlope'], 1/self.prm[currBlock]['nAlternatives'],
                                           self.prm[currBlock]['psyListLapse'])
                elif self.prm[currBlock]['psyListFunFit'] == "Logarithmic":
                    # print(self.prm['adaptiveParam'])
                    # print(self.prm[currBlock]['psyListMidpoint'])
                    # print(self.prm[currBlock]['psyListSlope'])
                    # print(1/self.prm[currBlock]['nAlternatives'])
                    # print(self.prm[currBlock]['psyListLapse'])
                    probCorr = logisticPsy(np.log(self.prm['adaptiveParam']), np.log(self.prm[currBlock]['psyListMidpoint']),
                                           self.prm[currBlock]['psyListSlope'], 1/self.prm[currBlock]['nAlternatives'],
                                           self.prm[currBlock]['psyListLapse'])
            elif self.prm[currBlock]['psyListFun'] == "Gaussian":
                if self.prm[currBlock]['psyListFunFit'] == "Linear":
                    probCorr = gaussianPsy(self.prm['adaptiveParam'], self.prm[currBlock]['psyListMidpoint'],
                                           self.prm[currBlock]['psyListSlope'], 1/self.prm[currBlock]['nAlternatives'],
                                           self.prm[currBlock]['psyListLapse'])
                elif self.prm[currBlock]['psyListFunFit'] == "Logarithmic":
                    probCorr = gaussianPsy(np.log(self.prm['adaptiveParam']), np.log(self.prm[currBlock]['psyListMidpoint']),
                                           self.prm[currBlock]['psyListSlope'], 1/self.prm[currBlock]['nAlternatives'],
                                           self.prm[currBlock]['psyListLapse'])
            elif self.prm[currBlock]['psyListFun'] == "Gumbel":
                if self.prm[currBlock]['psyListFunFit'] == "Linear":
                    probCorr = gumbelPsy(self.prm['adaptiveParam'], self.prm[currBlock]['psyListMidpoint'],
                                         self.prm[currBlock]['psyListSlope'], 1/self.prm[currBlock]['nAlternatives'],
                                         self.prm[currBlock]['psyListLapse'])
                elif self.prm[currBlock]['psyListFunFit'] == "Logarithmic":
                    probCorr = gumbelPsy(np.log(self.prm['adaptiveParam']), np.log(self.prm[currBlock]['psyListMidpoint']),
                                         self.prm[currBlock]['psyListSlope'], 1/self.prm[currBlock]['nAlternatives'],
                                         self.prm[currBlock]['psyListLapse'])
            elif self.prm[currBlock]['psyListFun'] == "Weibull":
                if self.prm[currBlock]['psyListFunFit'] == "Linear":
                    probCorr = weibullPsy(self.prm['adaptiveParam'], self.prm[currBlock]['psyListMidpoint'],
                                          self.prm[currBlock]['psyListSlope'], 1/self.prm[currBlock]['nAlternatives'],
                                          self.prm[currBlock]['psyListLapse'])
                elif self.prm[currBlock]['psyListFunFit'] == "Logarithmic":
                    probCorr = weibullPsy(np.log(self.prm['adaptiveParam']), np.log(self.prm[currBlock]['psyListMidpoint']),
                                          self.prm[currBlock]['psyListSlope'], 1/self.prm[currBlock]['nAlternatives'],
                                          self.prm[currBlock]['psyListLapse'])
            resp = np.random.binomial(1, probCorr, 1)[0]
            if resp == 1:
                self.sortResponse(self.correctButton)
            else:
                self.sortResponse(random.choice(numpy.delete(numpy.arange(self.prm['nAlternatives'])+1, self.correctButton-1)))
       #==================================================================

    def dialerButtonClicked(self):
        if self.parent().currExp == self.tr("Digit Span") and self.prm['trialRunning'] == True:
            return
        buttonClicked = self.responseButton.index(self.sender())
        currText = self.dialerResponseField.text()
        newText = currText + str(buttonClicked)
        if self.parent().currExp == self.tr("Digit Triplets Test"):
            nDigits = len(newText)
            if nDigits > 3:
                newText = newText[0:3]
        self.dialerResponseField.setText(newText)

    def backspaceButtonPressed(self):
        self.dialerResponseField.backspace()

    def enterButtonPressed(self):
        currText = self.dialerResponseField.text()
        if self.parent().currExp == self.tr("Digit Triplets Test"):
            if len(currText) < 3:
                return
            else:
                if currText[0] == currText[1] or currText[0] == currText[2] or currText[1] == currText[2]:
                    ret = QMessageBox.warning(self, self.tr("Warning"),
                                              self.tr("Repeated digits are not allowed. Please, edit your response."),
                                              QMessageBox.StandardButton.Ok)
                    return

        if self.parent().currExp == self.tr("Digit Span"):
            if len(currText) < len(str(self.correctButton)):
                ret = QMessageBox.warning(self, self.tr("Warning"),
                                          self.tr("Input sequence is shorter than correct sequence."),
                                          QMessageBox.StandardButton.Ok)
                return
        
        self.dialerResponseField.setText("   ")
        self.dialerResponseField.setText("")
        self.sortResponse(int(currText))

    def sortResponseButton(self):
        #the try-except is here because when the interface is updating between blocks
        #the sender may be missing (participants press multiple times response button when interface is changing)
        try:
            buttonClicked = self.responseButton.index(self.sender())+1
        except:
            buttonClicked = 0
        self.sortResponse(buttonClicked)
        
    def keyPressEvent(self, event):
        if (event.type() == QEvent.Type.KeyPress): 
            if event.key()==Qt.Key.Key_0:
                buttonClicked = 0
            elif event.key()==Qt.Key.Key_1:
                buttonClicked = 1
            elif event.key()==Qt.Key.Key_2:
                buttonClicked = 2
            elif event.key()==Qt.Key.Key_3:
                buttonClicked = 3
            elif event.key()==Qt.Key.Key_4:
                buttonClicked = 4
            elif event.key()==Qt.Key.Key_5:
                buttonClicked = 5
            elif event.key()==Qt.Key.Key_6:
                buttonClicked = 6
            elif event.key()==Qt.Key.Key_7:
                buttonClicked = 7
            elif event.key()==Qt.Key.Key_8:
                buttonClicked = 8
            elif event.key()==Qt.Key.Key_9:
                buttonClicked = 9
            else:
                buttonClicked = 0
            self.sortResponse(buttonClicked)
        return 
       
    def sortResponse(self, buttonClicked):
        currBlock = 'b'+ str(self.prm['currentBlock'])
        if buttonClicked == 0: #0 is not a response option
            return
        if self.parent().currExp == self.tr("Digit Triplets Test"):
            if buttonClicked < 10:
                return
            if self.statusButton.text() not in [self.prm['rbTrans'].translate("rb", "Running"), "&" + self.prm['rbTrans'].translate("rb", "Running")]:
                return
        elif self.parent().currExp == self.tr("Digit Span"):
            if self.statusButton.text() not in [self.prm['rbTrans'].translate("rb", "Running"), "&" + self.prm['rbTrans'].translate("rb", "Running")]:
                return
        else:
            if buttonClicked > self.prm['nAlternatives'] or self.statusButton.text() not in [self.prm['rbTrans'].translate("rb", "Running"), "&"+ self.prm['rbTrans'].translate("rb", "Running")]: #self.tr("Running"): #1) do not accept responses outside the possible alternatives and 2) if the block is not running (like wait or finished)
                return
        if buttonClicked < (self.prm['nAlternatives']+1) and self.prm['trialRunning'] == True: #1) can't remember why I put the first condition 2) do not accept responses while the trial is running
            return
        if self.prm['sortingResponse'] == True: #Do not accept other responses while processing the current one
            return
        self.prm['sortingResponse'] = True

        if self.prm['paradigm'] == self.tr("Transformed Up-Down"):
            self.sortResponseAdaptive(buttonClicked, 'transformedUpDown')
        elif self.prm['paradigm'] == self.tr("Transformed Up-Down Interleaved"):
            self.sortResponseAdaptiveInterleaved(buttonClicked, 'transformedUpDown')
        elif self.prm['paradigm'] == self.tr("Transformed Up-Down Limited"):
            self.sortResponseAdaptiveLimited(buttonClicked, 'transformedUpDown')
        elif self.prm['paradigm'] == self.tr("Transformed Up-Down Hybrid"):
            self.sortResponseAdaptiveHybrid(buttonClicked, 'transformedUpDown')
        elif self.prm['paradigm'] == self.tr("Weighted Up-Down"):
            self.sortResponseAdaptive(buttonClicked, 'weightedUpDown')
        elif self.prm['paradigm'] == self.tr("Weighted Up-Down Interleaved"):
            self.sortResponseAdaptiveInterleaved(buttonClicked, 'weightedUpDown')
        elif self.prm['paradigm'] == self.tr("Weighted Up-Down Limited"):
            self.sortResponseAdaptiveLimited(buttonClicked, 'weightedUpDown')
        elif self.prm['paradigm'] == self.tr("Weighted Up-Down Hybrid"):
            self.sortResponseAdaptiveHybrid(buttonClicked, 'weightedUpDown')
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
        elif self.prm['paradigm'] == self.tr("Multiple Constants 1-Pair Same/Different"):
            self.sortResponseMultipleConstants1PairSameDifferent(buttonClicked)
        elif self.prm['paradigm'] == self.tr("Multiple Constants ABX"):
            self.sortResponseMultipleConstantsABX(buttonClicked)
        elif self.prm['paradigm'] == self.tr("PEST"):
            self.sortResponsePEST(buttonClicked)
        elif self.prm['paradigm'] == self.tr("Maximum Likelihood"):
            self.sortResponseMaximumLikelihood(buttonClicked)
        elif self.prm['paradigm'] == self.tr("PSI"):
            self.sortResponsePSI(buttonClicked)
        elif self.prm['paradigm'] == self.tr("PSI - Est. Guess Rate"):
            self.sortResponsePSIEstGuessRate(buttonClicked)
        elif self.prm['paradigm'] == self.tr("UML"):
            self.sortResponseUML(buttonClicked)
        elif self.prm['paradigm'] == self.tr("UML - Est. Guess Rate"):
            self.sortResponseUMLEstGuessRate(buttonClicked)
        elif self.prm['paradigm'] == self.tr("Multiple Constants Odd One Out"):
            self.sortResponseMultipleConstantsOddOneOut(buttonClicked)
        elif self.prm['paradigm'] == self.tr("Multiple Constants Sound Comparison"):
            self.sortResponseMultipleConstantsSoundComparison(buttonClicked)
        elif self.prm['paradigm'] == self.tr("Adaptive Digit Span"):
            self.sortResponseAdaptiveDigitSpan(buttonClicked)
        self.prm['sortingResponse'] = False
            

    def sortResponseAdaptive(self, buttonClicked, method):
        if self.prm['startOfBlock'] == True:
            self.prm['correctCount'] = 0
            self.prm['incorrectCount'] = 0
            self.prm['nTurnpoints'] = 0
            self.prm['startOfBlock'] = False
            self.prm['turnpointVal'] = []
            self.prm['trackDir'] = copy.copy(self.prm['corrTrackDir'])
            if self.prm['corrTrackDir'] == self.tr("Down"):
                self.prm['corrTrackSign'] = -1
                self.prm['incorrTrackSign'] = 1
                self.prm['incorrTrackDir'] = self.tr("Up")
            else:
                self.prm['corrTrackSign'] = 1
                self.prm['incorrTrackSign'] = -1
                self.prm['incorrTrackDir'] = self.tr("Down")
            self.fullFileLines = []
            self.fullFileSummLines = []
            self.prm['buttonCounter'] = [0 for i in range(self.prm['nAlternatives'])]
        self.prm['buttonCounter'][buttonClicked-1] = self.prm['buttonCounter'][buttonClicked-1] + 1

        stepSize = {}
        if method == 'transformedUpDown':
            if self.prm['nTurnpoints'] < self.prm['initialTurnpoints']:
                stepSize[self.tr("Down")] = self.prm['adaptiveStepSize1']
                stepSize[self.tr("Up")]   = self.prm['adaptiveStepSize1']
            else:
                stepSize[self.tr("Down")] = self.prm['adaptiveStepSize2']
                stepSize[self.tr("Up")]   = self.prm['adaptiveStepSize2']
        elif method == 'weightedUpDown':
            if self.prm['nTurnpoints'] < self.prm['initialTurnpoints']:
                stepSize[self.prm['corrTrackDir']] = self.prm['adaptiveStepSize1']

                if self.prm['adaptiveType'] == self.tr("Arithmetic"):
                    stepSize[self.prm['incorrTrackDir']] = self.prm['adaptiveStepSize1'] * (self.prm['percentCorrectTracked'] / (100-self.prm['percentCorrectTracked']))
                elif self.prm['adaptiveType'] == self.tr("Geometric"):
                    stepSize[self.prm['incorrTrackDir']] = self.prm['adaptiveStepSize1'] ** (self.prm['percentCorrectTracked'] / (100-self.prm['percentCorrectTracked']))
            else:
                stepSize[self.prm['corrTrackDir']] = self.prm['adaptiveStepSize2']
                if self.prm['adaptiveType'] == self.tr("Arithmetic"):
                    stepSize[self.prm['incorrTrackDir']] = self.prm['adaptiveStepSize2'] * (self.prm['percentCorrectTracked'] / (100-self.prm['percentCorrectTracked']))
                elif self.prm['adaptiveType'] == self.tr("Geometric"):
                    stepSize[self.prm['incorrTrackDir']] = self.prm['adaptiveStepSize2'] ** (self.prm['percentCorrectTracked'] / (100-self.prm['percentCorrectTracked']))
            
        if buttonClicked == self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback("correct")
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback("neutral")
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback("off")
            
            self.fullFileLog.write(str(self.prm['adaptiveParam']) + '; ')
            self.fullFileLines.append(str(self.prm['adaptiveParam']) + '; ')
            self.fullFileSummLines.append([str(self.prm['adaptiveParam']) + self.prm["pref"]["general"]["csvSeparator"]])
            self.fullFileLog.write('1; ')
            self.fullFileLines.append('1; ')
            self.fullFileSummLines[len(self.fullFileSummLines)-1].append('1' + self.prm["pref"]["general"]["csvSeparator"])
            if 'additional_parameters_to_write' in self.prm:
                for p in range(len(self.prm['additional_parameters_to_write'])):
                    self.fullFileLog.write(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileLines.append(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileSummLines[len(self.fullFileSummLines)-1].append(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileLog.write(' ;')
                    self.fullFileLines.append(' ;')
                    self.fullFileSummLines[len(self.fullFileSummLines)-1].append(self.prm["pref"]["general"]["csvSeparator"])
            self.fullFileLog.write('\n')
            self.fullFileLines.append('\n')
            self.prm['correctCount'] = self.prm['correctCount'] + 1
            self.prm['incorrectCount'] = 0

            if self.prm['correctCount'] == self.prm['numberCorrectNeeded']:
                self.prm['correctCount'] = 0
                if self.prm['trackDir'] == self.prm['incorrTrackDir']:
                    self.prm['turnpointVal'].append(self.prm['adaptiveParam'])
                    self.prm['nTurnpoints'] = self.prm['nTurnpoints'] +1
                    self.prm['trackDir'] = copy.copy(self.prm['corrTrackDir'])
                        
                if self.prm['adaptiveType'] == self.tr("Arithmetic"):
                    self.prm['adaptiveParam'] = self.prm['adaptiveParam'] + (stepSize[self.prm['corrTrackDir']]*self.prm['corrTrackSign'])
                elif self.prm['adaptiveType'] == self.tr("Geometric"):
                    self.prm['adaptiveParam'] = self.prm['adaptiveParam'] * (stepSize[self.prm['corrTrackDir']]**self.prm['corrTrackSign'])
                
        elif buttonClicked != self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback("incorrect")
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback("neutral")
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback("off")
                
            self.fullFileLog.write(str(self.prm['adaptiveParam']) + '; ')
            self.fullFileLines.append(str(self.prm['adaptiveParam']) + '; ')
            self.fullFileSummLines.append([str(self.prm['adaptiveParam']) + self.prm["pref"]["general"]["csvSeparator"]])
            self.fullFileLog.write('0; ')
            self.fullFileLines.append('0; ')
            self.fullFileSummLines[len(self.fullFileSummLines)-1].append('0' + self.prm["pref"]["general"]["csvSeparator"])
            if 'additional_parameters_to_write' in self.prm:
                for p in range(len(self.prm['additional_parameters_to_write'])):
                    self.fullFileLog.write(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileLines.append(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileSummLines[len(self.fullFileSummLines)-1].append(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileLog.write('; ')
                    self.fullFileLines.append('; ')
                    self.fullFileSummLines[len(self.fullFileSummLines)-1].append(self.prm["pref"]["general"]["csvSeparator"])
            self.fullFileLog.write('\n')
            self.fullFileLines.append('\n')
            
            self.prm['incorrectCount'] = self.prm['incorrectCount'] + 1
            self.prm['correctCount'] = 0

            if self.prm['incorrectCount'] == self.prm['numberIncorrectNeeded']:
                self.prm['incorrectCount'] = 0
                if self.prm['trackDir'] == self.prm['corrTrackDir']:#self.tr('Down'):
                    self.prm['turnpointVal'].append(self.prm['adaptiveParam'])
                    self.prm['nTurnpoints'] = self.prm['nTurnpoints'] +1
                    self.prm['trackDir'] = copy.copy(self.prm['incorrTrackDir'])#self.tr('Up')
                    
                if self.prm['adaptiveType'] == self.tr("Arithmetic"):
                    self.prm['adaptiveParam'] = self.prm['adaptiveParam'] + (stepSize[self.prm['incorrTrackDir']]*self.prm['incorrTrackSign'])
                elif self.prm['adaptiveType'] == self.tr("Geometric"):
                    self.prm['adaptiveParam'] = self.prm['adaptiveParam'] * (stepSize[self.prm['incorrTrackDir']]**self.prm['incorrTrackSign'])
                                                     

        self.fullFileLog.flush()
        pcDone = (self.prm['nTurnpoints'] / self.prm['totalTurnpoints']) * 100
        bp = int(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'])
        pcThisRep = (bp-1) / self.prm['storedBlocks']*100 + 1 / self.prm['storedBlocks']*pcDone
        pcTot = (self.prm['currentRepetition'] - 1) / self.prm['allBlocks']['repetitions']*100 + 1 / self.prm['allBlocks']['repetitions']*pcThisRep
        self.gauge.setValue(int(pcTot))
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
                finalTurnpoints = array(self.prm['turnpointVal'][self.prm['initialTurnpoints'] : self.prm['totalTurnpoints']], dtype=float64)
                turnpointMean = mean(finalTurnpoints)
                turnpointSd = std(finalTurnpoints, ddof=1)
                self.resFile.write('\n\n')
                self.resFile.write('turnpointMean = %5.2f, s.d. = %5.2f \n' %(turnpointMean,turnpointSd))
                self.resFileLog.write('\n\n')
                self.resFileLog.write('turnpointMean = %5.2f, s.d. = %5.2f \n' %(turnpointMean,turnpointSd))
            elif self.prm['adaptiveType'] == self.tr("Geometric"):
                finalTurnpoints = abs(array(self.prm['turnpointVal'][self.prm['initialTurnpoints'] : self.prm['totalTurnpoints']], dtype=float64))
                turnpointMean = geoMean(finalTurnpoints)
                turnpointSd = geoSd(finalTurnpoints)
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
            resLineToWrite = '{0:5.3f}'.format(turnpointMean) + self.prm["pref"]["general"]["csvSeparator"] + \
                             '{0:5.3f}'.format(turnpointSd) + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm[currBlock]['conditionLabel'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['listener'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['sessionLabel'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['allBlocks']['experimentLabel'] + self.prm["pref"]["general"]["csvSeparator"] +\
                             self.prm['blockEndDateString'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['blockEndTimeString'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             durString + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm[currBlock]['blockPosition'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm[currBlock]['experiment'] + self.prm["pref"]["general"]["csvSeparator"] +\
                             self.prm[currBlock]['paradigm'] + self.prm["pref"]["general"]["csvSeparator"]
            resLineToWrite = self.getCommonTabFields(resLineToWrite)
            resLineToWrite = resLineToWrite + '\n'
            
            if method == 'transformedUpDown':
                self.writeResultsSummaryLine('Transformed Up-Down', resLineToWrite)
            elif method == 'weightedUpDown':
                self.writeResultsSummaryLine('Weighted Up-Down', resLineToWrite)

            resLineToWriteSummFull = ""
            for i in range(len(self.fullFileSummLines)):
              resLineToWriteSummFull = resLineToWriteSummFull + " ".join(self.fullFileSummLines[i]) + \
                             self.prm[currBlock]['conditionLabel'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['listener'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['sessionLabel'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['allBlocks']['experimentLabel'] + self.prm["pref"]["general"]["csvSeparator"] +\
                             self.prm['blockEndDateString'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['blockEndTimeString'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             durString + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm[currBlock]['blockPosition'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm[currBlock]['experiment'] + self.prm["pref"]["general"]["csvSeparator"] +\
                             self.prm[currBlock]['paradigm'] + self.prm["pref"]["general"]["csvSeparator"]
             
              resLineToWriteSummFull = self.getCommonTabFields(resLineToWriteSummFull)
              resLineToWriteSummFull = resLineToWriteSummFull + '\n'
            
            
            if method == 'transformedUpDown':
                self.writeResultsSummaryFullLine('Transformed Up-Down', resLineToWriteSummFull)
            elif method == 'weightedUpDown':
                self.writeResultsSummaryFullLine('Weighted Up-Down', resLineToWriteSummFull)

            self.atBlockEnd()
            
        else:
            self.doTrial()

    def sortResponseAdaptiveHybrid(self, buttonClicked, method):
        # procedure inspired by Hopkins, K., & Moore, B. C. J. (2010). Development of a fast method for measuring sensitivity to temporal fine structure information at low frequencies. International Journal of Audiology, 49(12), 940–6. http://doi.org/10.3109/14992027.2010.512613
        # see also:
        # King, A., Hopkins, K., & Plack, C. J. (2014). The effects of age and hearing loss on interaural phase difference discrimination. The Journal of the Acoustical Society of America, 135(1), 342–51. http://doi.org/10.1121/1.4838995
        # if the adaptive track reaches self.prm['adaptiveMaxLimit'], switch to a constant procedure
        # that measures percent correct at self.prm['adaptiveMaxLimit'] for self.prm['nTrialsRequiredAtMaxLimit']
        # note that the the value of parent.prm['adaptiveParam'] needs to be limited in the experiment file!
        if self.prm['startOfBlock'] == True:
            self.prm['blockHasEnded'] = False
            self.prm['correctCount'] = 0
            self.prm['incorrectCount'] = 0
            self.prm['nTurnpoints'] = 0
            self.prm['startOfBlock'] = False
            self.prm['turnpointVal'] = []
            self.prm['trackDir'] = copy.copy(self.prm['corrTrackDir'])
            self.prm['nCorrectAtMaxLimit'] = 0 ##
            self.prm['nTotalAtMaxLimit'] = 0 ##
            self.prm['percentCorrectAtMaxLimit'] = numpy.nan ##
            self.prm['switchedToConstant'] = False ##
            if method == 'transformedUpDown':
                self.prm['percentCorrectTracked'] = (0.5**(1/self.prm['numberCorrectNeeded']))*100
            if self.prm['corrTrackDir'] == self.tr("Down"):
                self.prm['corrTrackSign'] = -1
                self.prm['incorrTrackSign'] = 1
                self.prm['incorrTrackDir'] = self.tr("Up")
            else:
                self.prm['corrTrackSign'] = 1
                self.prm['incorrTrackSign'] = -1
                self.prm['incorrTrackDir'] = self.tr("Down")
            self.fullFileLines = []
            self.fullFileSummLines = []
            self.prm['buttonCounter'] = [0 for i in range(self.prm['nAlternatives'])]
        self.prm['buttonCounter'][buttonClicked-1] = self.prm['buttonCounter'][buttonClicked-1] + 1
        
        stepSize = {}
        if method == 'transformedUpDown':
            if self.prm['nTurnpoints'] < self.prm['initialTurnpoints']:
                stepSize[self.tr("Down")] = self.prm['adaptiveStepSize1']
                stepSize[self.tr("Up")]   = self.prm['adaptiveStepSize1']
            else:
                stepSize[self.tr("Down")] = self.prm['adaptiveStepSize2']
                stepSize[self.tr("Up")]   = self.prm['adaptiveStepSize2']
        elif method == 'weightedUpDown':
            if self.prm['nTurnpoints'] < self.prm['initialTurnpoints']:
                stepSize[self.prm['corrTrackDir']] = self.prm['adaptiveStepSize1']

                if self.prm['adaptiveType'] == self.tr("Arithmetic"):
                    stepSize[self.prm['incorrTrackDir']] = self.prm['adaptiveStepSize1'] * (self.prm['percentCorrectTracked'] / (100-self.prm['percentCorrectTracked']))
                elif self.prm['adaptiveType'] == self.tr("Geometric"):
                    stepSize[self.prm['incorrTrackDir']] = self.prm['adaptiveStepSize1'] ** (self.prm['percentCorrectTracked'] / (100-self.prm['percentCorrectTracked']))
            else:
                stepSize[self.prm['corrTrackDir']] = self.prm['adaptiveStepSize2']
                if self.prm['adaptiveType'] == self.tr("Arithmetic"):
                    stepSize[self.prm['incorrTrackDir']] = self.prm['adaptiveStepSize2'] * (self.prm['percentCorrectTracked'] / (100-self.prm['percentCorrectTracked']))
                elif self.prm['adaptiveType'] == self.tr("Geometric"):
                    stepSize[self.prm['incorrTrackDir']] = self.prm['adaptiveStepSize2'] ** (self.prm['percentCorrectTracked'] / (100-self.prm['percentCorrectTracked']))

        #--..--
        # if self.prm['adaptiveParam'] >= self.prm['adaptiveMaxLimit']:
        #     self.prm['nTotalAtMaxLimit'] = self.prm['nTotalAtMaxLimit']+1
        #     if buttonClicked == self.correctButton:
        #         self.prm['nCorrectAtMaxLimit'] = self.prm['nCorrectAtMaxLimit']+1
        #     self.prm['percentCorrectAtMaxLimit'] = (self.prm['nCorrectAtMaxLimit']/self.prm['nTotalAtMaxLimit'])*100
        # if  self.prm['nTotalAtMaxLimit'] > self.prm['minSwitchTrials']:
        #     if  self.prm['percentCorrectAtMaxLimit'] < self.prm['percentCorrectTracked']:
        #         self.prm['switchedToConstant'] = True
        if self.prm['switchAfterInitialTurnpoints'] == self.tr("Yes"):
            if self.prm['adaptiveParam'] >= self.prm['adaptiveMaxLimit'] and self.prm['nTurnpoints'] > self.prm['initialTurnpoints']: 
                self.prm['nTotalAtMaxLimit'] = self.prm['nTotalAtMaxLimit']+1
                if buttonClicked == self.correctButton:
                    self.prm['nCorrectAtMaxLimit'] = self.prm['nCorrectAtMaxLimit']+1
                self.prm['percentCorrectAtMaxLimit'] = (self.prm['nCorrectAtMaxLimit']/self.prm['nTotalAtMaxLimit'])*100
        else:
            if self.prm['adaptiveParam'] >= self.prm['adaptiveMaxLimit']: 
                self.prm['nTotalAtMaxLimit'] = self.prm['nTotalAtMaxLimit']+1
                if buttonClicked == self.correctButton:
                    self.prm['nCorrectAtMaxLimit'] = self.prm['nCorrectAtMaxLimit']+1
                self.prm['percentCorrectAtMaxLimit'] = (self.prm['nCorrectAtMaxLimit']/self.prm['nTotalAtMaxLimit'])*100
            
            
        if buttonClicked == self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback("correct")
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback("neutral")
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback("off")

            self.fullFileLog.write(str(self.prm['adaptiveParam']) + '; ')
            self.fullFileLines.append(str(self.prm['adaptiveParam']) + '; ')
            self.fullFileSummLines.append([str(self.prm['adaptiveParam']) + self.prm["pref"]["general"]["csvSeparator"]])
            self.fullFileLog.write('1; ')
            self.fullFileLines.append('1; ')
            self.fullFileSummLines[len(self.fullFileSummLines)-1].append('1' + self.prm["pref"]["general"]["csvSeparator"])
            if 'additional_parameters_to_write' in self.prm:
                for p in range(len(self.prm['additional_parameters_to_write'])):
                    self.fullFileLog.write(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileLines.append(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileSummLines[len(self.fullFileSummLines)-1].append(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileLog.write(' ;')
                    self.fullFileLines.append(' ;')
                    self.fullFileSummLines[len(self.fullFileSummLines)-1].append(self.prm["pref"]["general"]["csvSeparator"])
            self.fullFileLog.write('\n')
            self.fullFileLines.append('\n')

            if self.prm['switchedToConstant'] == False:
                self.prm['correctCount'] = self.prm['correctCount'] + 1
                self.prm['incorrectCount'] = 0

                if self.prm['correctCount'] == self.prm['numberCorrectNeeded']:
                    self.prm['correctCount'] = 0
                    if self.prm['trackDir'] == self.prm['incorrTrackDir']:
                        self.prm['turnpointVal'].append(self.prm['adaptiveParam'])
                        self.prm['nTurnpoints'] = self.prm['nTurnpoints'] +1
                        self.prm['trackDir'] = copy.copy(self.prm['corrTrackDir'])

                    if self.prm['adaptiveType'] == self.tr("Arithmetic"):
                        self.prm['adaptiveParam'] = self.prm['adaptiveParam'] + (stepSize[self.prm['corrTrackDir']]*self.prm['corrTrackSign'])
                    elif self.prm['adaptiveType'] == self.tr("Geometric"):
                        self.prm['adaptiveParam'] = self.prm['adaptiveParam'] * (stepSize[self.prm['corrTrackDir']]**self.prm['corrTrackSign'])

        elif buttonClicked != self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback("incorrect")
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback("neutral")
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback("off")

            self.fullFileLog.write(str(self.prm['adaptiveParam']) + '; ')
            self.fullFileLines.append(str(self.prm['adaptiveParam']) + '; ')
            self.fullFileSummLines.append([str(self.prm['adaptiveParam']) + self.prm["pref"]["general"]["csvSeparator"]])
            self.fullFileLog.write('0; ')
            self.fullFileLines.append('0; ')
            self.fullFileSummLines[len(self.fullFileSummLines)-1].append('0' + self.prm["pref"]["general"]["csvSeparator"])
            if 'additional_parameters_to_write' in self.prm:
                for p in range(len(self.prm['additional_parameters_to_write'])):
                    self.fullFileLog.write(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileLines.append(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileSummLines[len(self.fullFileSummLines)-1].append(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileLog.write('; ')
                    self.fullFileLines.append('; ')
                    self.fullFileSummLines[len(self.fullFileSummLines)-1].append(self.prm["pref"]["general"]["csvSeparator"])
            self.fullFileLog.write('\n')
            self.fullFileLines.append('\n')

            if self.prm['switchedToConstant'] == False:
                self.prm['incorrectCount'] = self.prm['incorrectCount'] + 1
                self.prm['correctCount'] = 0

                if self.prm['incorrectCount'] == self.prm['numberIncorrectNeeded']:
                    self.prm['incorrectCount'] = 0
                    if self.prm['trackDir'] == self.prm['corrTrackDir']:#self.tr('Down'):
                        self.prm['turnpointVal'].append(self.prm['adaptiveParam'])
                        self.prm['nTurnpoints'] = self.prm['nTurnpoints'] +1
                        self.prm['trackDir'] = copy.copy(self.prm['incorrTrackDir'])#self.tr('Up')

                    if self.prm['adaptiveType'] == self.tr("Arithmetic"):
                        self.prm['adaptiveParam'] = self.prm['adaptiveParam'] + (stepSize[self.prm['incorrTrackDir']]*self.prm['incorrTrackSign'])
                    elif self.prm['adaptiveType'] == self.tr("Geometric"):
                        self.prm['adaptiveParam'] = self.prm['adaptiveParam'] * (stepSize[self.prm['incorrTrackDir']]**self.prm['incorrTrackSign'])

        if self.prm['switchAfterInitialTurnpoints'] == self.tr("Yes"):
            if self.prm['adaptiveParam'] >= self.prm['adaptiveMaxLimit'] and self.prm['nTurnpoints'] >= self.prm['initialTurnpoints']:
                self.prm['switchedToConstant'] = True
        else:
            if self.prm['adaptiveParam'] >= self.prm['adaptiveMaxLimit']:
                self.prm['switchedToConstant'] = True
                

        #print("Adaptive param. :" + str(self.prm['adaptiveParam']))
        #print("PC tracked: " + str(self.prm['percentCorrectTracked']))
        print(self.prm['nTurnpoints'])
        print("Switched to constant: " + str(self.prm['switchedToConstant']))
        print("N corr. at max limit: " + str(self.prm['nCorrectAtMaxLimit']))
        print("N tot. at max limit: " + str(self.prm['nTotalAtMaxLimit']))
        print("PC at max limit: " + str(self.prm['percentCorrectAtMaxLimit']))

        self.fullFileLog.flush()
        if self.prm['switchedToConstant'] == False:
            pcDone = (self.prm['nTurnpoints'] / self.prm['totalTurnpoints']) * 100
        else:
            pcDone = (self.prm['nTotalAtMaxLimit'] / self.prm['nTrialsRequiredAtMaxLimit'])*100
        bp = int(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'])
        pcThisRep = (bp-1) / self.prm['storedBlocks']*100 + 1 / self.prm['storedBlocks']*pcDone
        pcTot = (self.prm['currentRepetition'] - 1) / self.prm['allBlocks']['repetitions']*100 + 1 / self.prm['allBlocks']['repetitions']*pcThisRep
        self.gauge.setValue(int(pcTot))

        if self.prm['switchedToConstant'] == False:
            if self.prm['nTurnpoints'] == self.prm['totalTurnpoints']:
                self.prm['blockHasEnded'] = True
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
                    finalTurnpoints = array(self.prm['turnpointVal'][self.prm['initialTurnpoints'] : self.prm['totalTurnpoints']], dtype=float64)
                    turnpointMean = mean(finalTurnpoints)
                    turnpointSd = std(finalTurnpoints, ddof=1)
                    self.resFile.write('\n\n')
                    self.resFile.write('turnpointMean = %5.2f, s.d. = %5.2f \n' %(turnpointMean,turnpointSd))
                    self.resFileLog.write('\n\n')
                    self.resFileLog.write('turnpointMean = %5.2f, s.d. = %5.2f \n' %(turnpointMean,turnpointSd))
                elif self.prm['adaptiveType'] == self.tr("Geometric"):
                    finalTurnpoints = abs(array(self.prm['turnpointVal'][self.prm['initialTurnpoints'] : self.prm['totalTurnpoints']], dtype=float64))
                    turnpointMean = geoMean(finalTurnpoints)
                    turnpointSd = geoSd(finalTurnpoints)
                    self.resFile.write('\n\n')
                    self.resFile.write('geometric turnpointMean = %5.2f, s.d. = %5.2f \n' %(turnpointMean,turnpointSd))
                    self.resFileLog.write('\n\n')
                    self.resFileLog.write('geometric turnpointMean = %5.2f, s.d. = %5.2f \n' %(turnpointMean,turnpointSd))
        else:
            if self.prm['nTotalAtMaxLimit'] >= self.prm['nTrialsRequiredAtMaxLimit']:
                self.prm['blockHasEnded'] = True
                self.writeResultsHeader('standard')
                #process results
                self.fullFileLog.write('\n')
                self.fullFileLines.append('\n')
                for i in range(len(self.fullFileLines)):
                    self.fullFile.write(self.fullFileLines[i])

                self.resFile.write('No. Correct at Max Level = %d \n' %(self.prm['nCorrectAtMaxLimit']))
                self.resFile.write('No. Total at Max Level = %d \n' %(self.prm['nTotalAtMaxLimit']))
                self.resFile.write('Percent Correct at Max Level = %5.2f \n' %(self.prm['percentCorrectAtMaxLimit']))
                self.resFile.write('\n\n')
                self.resFileLog.write('No. Correct at Max Level = %d \n' %(self.prm['nCorrectAtMaxLimit']))
                self.resFileLog.write('No. Total at Max Level = %d \n' %(self.prm['nTotalAtMaxLimit']))
                self.resFileLog.write('Percent Correct at Max Level = %5.2f \n' %(self.prm['percentCorrectAtMaxLimit']))
                self.resFileLog.write('\n\n')
                turnpointMean = numpy.nan
                turnpointSd = numpy.nan
                
        if self.prm['blockHasEnded'] == True:
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
            resLineToWrite = '{0:5.3f}'.format(turnpointMean) + self.prm["pref"]["general"]["csvSeparator"] + \
                             '{0:5.3f}'.format(turnpointSd) + self.prm["pref"]["general"]["csvSeparator"] + \
                             str(self.prm['nCorrectAtMaxLimit']) + self.prm["pref"]["general"]["csvSeparator"] + \
                             str(self.prm['nTotalAtMaxLimit']) + self.prm["pref"]["general"]["csvSeparator"] + \
                             '{0:5.2f}'.format(self.prm['percentCorrectAtMaxLimit']) + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm[currBlock]['conditionLabel'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['listener'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['sessionLabel'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['allBlocks']['experimentLabel'] + self.prm["pref"]["general"]["csvSeparator"] +\
                             self.prm['blockEndDateString'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['blockEndTimeString'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             durString + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm[currBlock]['blockPosition'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm[currBlock]['experiment'] + self.prm["pref"]["general"]["csvSeparator"] +\
                             self.prm[currBlock]['paradigm'] + self.prm["pref"]["general"]["csvSeparator"]
            resLineToWrite = self.getCommonTabFields(resLineToWrite)
            resLineToWrite = resLineToWrite + '\n'

            if method == 'transformedUpDown':
                self.writeResultsSummaryLine('Transformed Up-Down Hybrid', resLineToWrite)
            elif method == 'weightedUpDown':
                self.writeResultsSummaryLine('Weighted Up-Down Hybrid', resLineToWrite)

            resLineToWriteSummFull = ""
            for i in range(len(self.fullFileSummLines)):
              resLineToWriteSummFull = resLineToWriteSummFull + " ".join(self.fullFileSummLines[i]) + \
                             self.prm[currBlock]['conditionLabel'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['listener'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['sessionLabel'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['allBlocks']['experimentLabel'] + self.prm["pref"]["general"]["csvSeparator"] +\
                             self.prm['blockEndDateString'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['blockEndTimeString'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             durString + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm[currBlock]['blockPosition'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm[currBlock]['experiment'] + self.prm["pref"]["general"]["csvSeparator"] +\
                             self.prm[currBlock]['paradigm'] + self.prm["pref"]["general"]["csvSeparator"]

              resLineToWriteSummFull = self.getCommonTabFields(resLineToWriteSummFull)
              resLineToWriteSummFull = resLineToWriteSummFull + '\n'


            if method == 'transformedUpDown':
                self.writeResultsSummaryFullLine('Transformed Up-Down Hybrid', resLineToWriteSummFull)
            elif method == 'weightedUpDown':
                self.writeResultsSummaryFullLine('Weighted Up-Down Hybrid', resLineToWriteSummFull)

            self.atBlockEnd()

        else:
            self.doTrial()



    def sortResponseAdaptiveLimited(self, buttonClicked, method):
        #I used this procedure a long time ago for an experiment in which participants were stuck at the maximum
        #adaptive difference and the block took too long to complete. To speed up things this procedure will call
        #a turnpoint not only when the track is going from the "incorrect" direction to the "correct" direction,
        # but also when self.prm['adaptiveParam'] == self.prm['adaptiveMaxLimit'].
        #This was done only to speed things up, and in retrospect it was not the most elegant solution.
        #I do not recommend using this procedure in general. It is here mainly for historical purposes.
        if self.prm['startOfBlock'] == True:
            self.prm['correctCount'] = 0
            self.prm['incorrectCount'] = 0
            self.prm['nTurnpoints'] = 0
            self.prm['startOfBlock'] = False
            self.prm['turnpointVal'] = []
            self.prm['trackDir'] = copy.copy(self.prm['corrTrackDir'])
            if self.prm['corrTrackDir'] == self.tr("Down"):
                self.prm['corrTrackSign'] = -1
                self.prm['incorrTrackSign'] = 1
                self.prm['incorrTrackDir'] = self.tr("Up")
            else:
                self.prm['corrTrackSign'] = 1
                self.prm['incorrTrackSign'] = -1
                self.prm['incorrTrackDir'] = self.tr("Down")
            self.fullFileLines = []
            self.fullFileSummLines = []
            self.prm['buttonCounter'] = [0 for i in range(self.prm['nAlternatives'])]
        self.prm['buttonCounter'][buttonClicked-1] = self.prm['buttonCounter'][buttonClicked-1] + 1

        stepSize = {}
        if method == 'transformedUpDown':
            if self.prm['nTurnpoints'] < self.prm['initialTurnpoints']:
                stepSize[self.tr("Down")] = self.prm['adaptiveStepSize1']
                stepSize[self.tr("Up")]   = self.prm['adaptiveStepSize1']
            else:
                stepSize[self.tr("Down")] = self.prm['adaptiveStepSize2']
                stepSize[self.tr("Up")]   = self.prm['adaptiveStepSize2']
        elif method == 'weightedUpDown':
            if self.prm['nTurnpoints'] < self.prm['initialTurnpoints']:
                stepSize[self.prm['corrTrackDir']] = self.prm['adaptiveStepSize1']

                if self.prm['adaptiveType'] == self.tr("Arithmetic"):
                    stepSize[self.prm['incorrTrackDir']] = self.prm['adaptiveStepSize1'] * (self.prm['percentCorrectTracked'] / (100-self.prm['percentCorrectTracked']))
                elif self.prm['adaptiveType'] == self.tr("Geometric"):
                    stepSize[self.prm['incorrTrackDir']] = self.prm['adaptiveStepSize1'] ** (self.prm['percentCorrectTracked'] / (100-self.prm['percentCorrectTracked']))
            else:
                stepSize[self.prm['corrTrackDir']] = self.prm['adaptiveStepSize2']
                if self.prm['adaptiveType'] == self.tr("Arithmetic"):
                    stepSize[self.prm['incorrTrackDir']] = self.prm['adaptiveStepSize2'] * (self.prm['percentCorrectTracked'] / (100-self.prm['percentCorrectTracked']))
                elif self.prm['adaptiveType'] == self.tr("Geometric"):
                    stepSize[self.prm['incorrTrackDir']] = self.prm['adaptiveStepSize2'] ** (self.prm['percentCorrectTracked'] / (100-self.prm['percentCorrectTracked']))
            
        if buttonClicked == self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback("correct")
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback("neutral")
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback("off")
            
            self.fullFileLog.write(str(self.prm['adaptiveParam']) + '; ')
            self.fullFileLines.append(str(self.prm['adaptiveParam']) + '; ')
            self.fullFileSummLines.append([str(self.prm['adaptiveParam']) + self.prm["pref"]["general"]["csvSeparator"]])
            self.fullFileLog.write('1; ')
            self.fullFileLines.append('1; ')
            self.fullFileSummLines[len(self.fullFileSummLines)-1].append('1' + self.prm["pref"]["general"]["csvSeparator"])
            if 'additional_parameters_to_write' in self.prm:
                for p in range(len(self.prm['additional_parameters_to_write'])):
                    self.fullFileLog.write(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileLines.append(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileSummLines[len(self.fullFileSummLines)-1].append(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileLog.write(' ;')
                    self.fullFileLines.append(' ;')
                    self.fullFileSummLines[len(self.fullFileSummLines)-1].append(self.prm["pref"]["general"]["csvSeparator"])
            self.fullFileLog.write('\n')
            self.fullFileLines.append('\n')
            self.prm['correctCount'] = self.prm['correctCount'] + 1
            self.prm['incorrectCount'] = 0

            if self.prm['correctCount'] == self.prm['numberCorrectNeeded']:
                self.prm['correctCount'] = 0
                if self.prm['trackDir'] == self.prm['incorrTrackDir']:
                    self.prm['turnpointVal'].append(self.prm['adaptiveParam'])
                    self.prm['nTurnpoints'] = self.prm['nTurnpoints'] +1
                    self.prm['trackDir'] = copy.copy(self.prm['corrTrackDir'])
                        
                if self.prm['adaptiveType'] == self.tr("Arithmetic"):
                    self.prm['adaptiveParam'] = self.prm['adaptiveParam'] + (stepSize[self.prm['corrTrackDir']]*self.prm['corrTrackSign'])
                elif self.prm['adaptiveType'] == self.tr("Geometric"):
                    self.prm['adaptiveParam'] = self.prm['adaptiveParam'] * (stepSize[self.prm['corrTrackDir']]**self.prm['corrTrackSign'])
                
        elif buttonClicked != self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback("incorrect")
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback("neutral")
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback("off")
                
            self.fullFileLog.write(str(self.prm['adaptiveParam']) + '; ')
            self.fullFileLines.append(str(self.prm['adaptiveParam']) + '; ')
            self.fullFileSummLines.append([str(self.prm['adaptiveParam']) + self.prm["pref"]["general"]["csvSeparator"]])
            self.fullFileLog.write('0; ')
            self.fullFileLines.append('0; ')
            self.fullFileSummLines[len(self.fullFileSummLines)-1].append('0' + self.prm["pref"]["general"]["csvSeparator"])
            if 'additional_parameters_to_write' in self.prm:
                for p in range(len(self.prm['additional_parameters_to_write'])):
                    self.fullFileLog.write(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileLines.append(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileSummLines[len(self.fullFileSummLines)-1].append(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileLog.write('; ')
                    self.fullFileLines.append('; ')
                    self.fullFileSummLines[len(self.fullFileSummLines)-1].append(self.prm["pref"]["general"]["csvSeparator"])
            self.fullFileLog.write('\n')
            self.fullFileLines.append('\n')
            
            self.prm['incorrectCount'] = self.prm['incorrectCount'] + 1
            self.prm['correctCount'] = 0

            if self.prm['incorrectCount'] == self.prm['numberIncorrectNeeded']:
                self.prm['incorrectCount'] = 0
                if self.prm['trackDir'] == self.prm['corrTrackDir'] or self.prm['adaptiveParam'] == self.prm['adaptiveMaxLimit']:
                    self.prm['turnpointVal'].append(self.prm['adaptiveParam'])
                    self.prm['nTurnpoints'] = self.prm['nTurnpoints'] +1
                    self.prm['trackDir'] = copy.copy(self.prm['incorrTrackDir'])
                    
                if self.prm['adaptiveType'] == self.tr("Arithmetic"):
                    self.prm['adaptiveParam'] = self.prm['adaptiveParam'] + (stepSize[self.prm['incorrTrackDir']]*self.prm['incorrTrackSign'])
                elif self.prm['adaptiveType'] == self.tr("Geometric"):
                    self.prm['adaptiveParam'] = self.prm['adaptiveParam'] * (stepSize[self.prm['incorrTrackDir']]**self.prm['incorrTrackSign'])
                                                     

        self.fullFileLog.flush()
        pcDone = (self.prm['nTurnpoints'] / self.prm['totalTurnpoints']) * 100
        bp = int(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'])
        pcThisRep = (bp-1) / self.prm['storedBlocks']*100 + 1 / self.prm['storedBlocks']*pcDone
        pcTot = (self.prm['currentRepetition'] - 1) / self.prm['allBlocks']['repetitions']*100 + 1 / self.prm['allBlocks']['repetitions']*pcThisRep
        self.gauge.setValue(int(pcTot))
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
                finalTurnpoints = array(self.prm['turnpointVal'][self.prm['initialTurnpoints'] : self.prm['totalTurnpoints']], dtype=float64)
                turnpointMean = mean(finalTurnpoints)
                turnpointSd = std(finalTurnpoints, ddof=1)
                self.resFile.write('\n\n')
                self.resFile.write('turnpointMean = %5.2f, s.d. = %5.2f \n' %(turnpointMean,turnpointSd))
                self.resFileLog.write('\n\n')
                self.resFileLog.write('turnpointMean = %5.2f, s.d. = %5.2f \n' %(turnpointMean,turnpointSd))
            elif self.prm['adaptiveType'] == self.tr("Geometric"):
                finalTurnpoints = abs(array(self.prm['turnpointVal'][self.prm['initialTurnpoints'] : self.prm['totalTurnpoints']], dtype=float64))
                turnpointMean = geoMean(finalTurnpoints)
                turnpointSd = geoSd(finalTurnpoints)
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
            resLineToWrite = '{0:5.3f}'.format(turnpointMean) + self.prm["pref"]["general"]["csvSeparator"] + \
                             '{0:5.3f}'.format(turnpointSd) + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm[currBlock]['conditionLabel'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['listener'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['sessionLabel'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['allBlocks']['experimentLabel'] + self.prm["pref"]["general"]["csvSeparator"] +\
                             self.prm['blockEndDateString'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['blockEndTimeString'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             durString + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm[currBlock]['blockPosition'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm[currBlock]['experiment'] + self.prm["pref"]["general"]["csvSeparator"] +\
                             self.prm[currBlock]['paradigm'] + self.prm["pref"]["general"]["csvSeparator"]
            resLineToWrite = self.getCommonTabFields(resLineToWrite)
            resLineToWrite = resLineToWrite + '\n'
            
            if method == 'transformedUpDown':
                self.writeResultsSummaryLine('Transformed Up-Down Limited', resLineToWrite)
            elif method == 'weightedUpDown':
                self.writeResultsSummaryLine('Weighted Up-Down Limited', resLineToWrite)

            resLineToWriteSummFull = ""
            for i in range(len(self.fullFileSummLines)):
              resLineToWriteSummFull = resLineToWriteSummFull + " ".join(self.fullFileSummLines[i]) + \
                             self.prm[currBlock]['conditionLabel'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['listener'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['sessionLabel'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['allBlocks']['experimentLabel'] + self.prm["pref"]["general"]["csvSeparator"] +\
                             self.prm['blockEndDateString'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['blockEndTimeString'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             durString + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm[currBlock]['blockPosition'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm[currBlock]['experiment'] + self.prm["pref"]["general"]["csvSeparator"] +\
                             self.prm[currBlock]['paradigm'] + self.prm["pref"]["general"]["csvSeparator"]
             
              resLineToWriteSummFull = self.getCommonTabFields(resLineToWriteSummFull)
              resLineToWriteSummFull = resLineToWriteSummFull + '\n'
            
            
            if method == 'transformedUpDown':
                self.writeResultsSummaryFullLine('Transformed Up-Down Limited', resLineToWriteSummFull)
            elif method == 'weightedUpDown':
                self.writeResultsSummaryFullLine('Weighted Up-Down Limited', resLineToWriteSummFull)

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

            self.prm['trackDir'] = []
            self.prm['incorrTrackDir'] = []
            self.prm['corrTrackSign'] = []
            self.prm['incorrTrackSign'] = []
            for i in range(self.prm['nDifferences']):
                self.prm['trackDir'].append(copy.copy(self.prm['corrTrackDir'][i]))
                if self.prm['corrTrackDir'][i] == self.tr("Down"):
                    self.prm['corrTrackSign'].append(-1)
                    self.prm['incorrTrackSign'].append(1)
                    self.prm['incorrTrackDir'].append(self.tr("Up"))
                else:
                    self.prm['corrTrackSign'].append(1)
                    self.prm['incorrTrackSign'].append(-1)
                    self.prm['incorrTrackDir'].append(self.tr("Down"))
                    
        if buttonClicked == self.correctButton:
            print("Correct Button Clicked")
        else:
            print("Incorrect Button Clicked")
        trackNumber = self.prm['currentDifference']
        self.prm['buttonCounter'][trackNumber][buttonClicked-1] = self.prm['buttonCounter'][trackNumber][buttonClicked-1] + 1
        stepSize = {}
        if method == 'weightedUpDown':
            if self.prm['nTurnpoints'][trackNumber] < self.prm['initialTurnpoints'][trackNumber]:
                stepSize[self.prm['corrTrackDir'][trackNumber]] = self.prm['adaptiveStepSize1'][trackNumber]
                if self.prm['adaptiveType'] == self.tr("Arithmetic"):
                    stepSize[self.prm['incorrTrackDir'][trackNumber]]   = self.prm['adaptiveStepSize1'][trackNumber] * (self.prm['percentCorrectTracked'][trackNumber] / (100-self.prm['percentCorrectTracked'][trackNumber]))
                elif self.prm['adaptiveType'] == self.tr("Geometric"):
                    stepSize[self.prm['incorrTrackDir'][trackNumber]]   = self.prm['adaptiveStepSize1'][trackNumber] ** (self.prm['percentCorrectTracked'][trackNumber] / (100-self.prm['percentCorrectTracked'][trackNumber]))
            else:
                stepSize[self.prm['corrTrackDir'][trackNumber]] = self.prm['adaptiveStepSize2'][trackNumber]
                if self.prm['adaptiveType'] == self.tr("Arithmetic"):
                    stepSize[self.prm['incorrTrackDir'][trackNumber]]   = self.prm['adaptiveStepSize2'][trackNumber] * (self.prm['percentCorrectTracked'][trackNumber] / (100-self.prm['percentCorrectTracked'][trackNumber]))
                elif self.prm['adaptiveType'] == self.tr("Geometric"):
                    stepSize[self.prm['incorrTrackDir'][trackNumber]]   = self.prm['adaptiveStepSize2'][trackNumber] ** (self.prm['percentCorrectTracked'][trackNumber] / (100-self.prm['percentCorrectTracked'][trackNumber]))
        elif method == 'transformedUpDown':
            if self.prm['nTurnpoints'][trackNumber] < self.prm['initialTurnpoints'][trackNumber]:
                stepSize[self.prm['corrTrackDir'][trackNumber]] = self.prm['adaptiveStepSize1'][trackNumber]
                stepSize[self.prm['incorrTrackDir'][trackNumber]]   = self.prm['adaptiveStepSize1'][trackNumber]
            else:
                stepSize[self.prm['corrTrackDir'][trackNumber]] = self.prm['adaptiveStepSize2'][trackNumber]
                stepSize[self.prm['incorrTrackDir'][trackNumber]]   = self.prm['adaptiveStepSize2'][trackNumber]
            
        if buttonClicked == self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback('correct')
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback('neutral')
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback('off')
            
            self.fullFileLog.write(str(self.prm['adaptiveParam'][trackNumber]) + '; ')
            self.fullFileLines.append(str(self.prm['adaptiveParam'][trackNumber]) + '; ')
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
                if self.prm['trackDir'][trackNumber] == self.prm['incorrTrackDir'][trackNumber]:
                    self.prm['turnpointVal'][trackNumber].append(self.prm['adaptiveParam'][trackNumber])
                    self.prm['nTurnpoints'][trackNumber] = self.prm['nTurnpoints'][trackNumber] +1
                    self.prm['trackDir'][trackNumber] = copy.copy(self.prm['corrTrackDir'][trackNumber])

                if self.prm['adaptiveType'] == self.tr("Arithmetic"):
                    self.prm['adaptiveParam'][trackNumber] = self.prm['adaptiveParam'][trackNumber] + (stepSize[self.prm['corrTrackDir'][trackNumber]]*self.prm['corrTrackSign'][trackNumber])
                elif self.prm['adaptiveType'] == self.tr("Geometric"):
                    self.prm['adaptiveParam'][trackNumber] = self.prm['adaptiveParam'][trackNumber] * (stepSize[self.prm['corrTrackDir'][trackNumber]]**self.prm['corrTrackSign'][trackNumber])
                
        elif buttonClicked != self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback('incorrect')
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback('neutral')
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback('off')
                
            self.fullFileLog.write(str(self.prm['adaptiveParam'][trackNumber]) + '; ')
            self.fullFileLines.append(str(self.prm['adaptiveParam'][trackNumber]) + '; ')
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
                if self.prm['trackDir'][trackNumber] == self.prm['corrTrackDir'][trackNumber]:
                    self.prm['turnpointVal'][trackNumber].append(self.prm['adaptiveParam'][trackNumber])
                    self.prm['nTurnpoints'][trackNumber] = self.prm['nTurnpoints'][trackNumber] +1
                    self.prm['trackDir'][trackNumber] = copy.copy(self.prm['incorrTrackDir'][trackNumber])

                if self.prm['adaptiveType'] == self.tr("Arithmetic"):
                    self.prm['adaptiveParam'][trackNumber] = self.prm['adaptiveParam'][trackNumber] + (stepSize[self.prm['incorrTrackDir'][trackNumber]]*self.prm['incorrTrackSign'][trackNumber])
                elif self.prm['adaptiveType'] == self.tr("Geometric"):
                    self.prm['adaptiveParam'][trackNumber] = self.prm['adaptiveParam'][trackNumber] * (stepSize[self.prm['incorrTrackDir'][trackNumber]]**self.prm['incorrTrackSign'][trackNumber])
      
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
        self.gauge.setValue(int(pcTot))

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
                    turnpointMean = mean(array(self.prm['turnpointVal'][j][tnpStart : tnpEnd], dtype=float64))
                    turnpointSd = std(array(self.prm['turnpointVal'][j][tnpStart : tnpEnd], dtype=float64), ddof=1)
                    self.resFile.write('\n\n')
                    self.resFile.write('turnpointMean = %5.2f, s.d. = %5.2f \n' %(turnpointMean, turnpointSd))
                    self.resFileLog.write('\n\n')
                    self.resFileLog.write('turnpointMean = %5.2f, s.d. = %5.2f \n' %(turnpointMean, turnpointSd))
                    turnpointMeanList.append(turnpointMean)
                    turnpointSdList.append(turnpointSd)
                elif self.prm['adaptiveType'] == self.tr("Geometric"):
                    turnpointMean = geoMean(abs(array(self.prm['turnpointVal'][j][tnpStart : tnpEnd], dtype=float64)))
                    turnpointSd = geoSd(abs(array(self.prm['turnpointVal'][j][tnpStart : tnpEnd], dtype=float64)))
                    self.resFile.write('\n\n')
                    self.resFile.write('geometric turnpointMean = %5.2f, s.d. = %5.2f \n' %(turnpointMean, turnpointSd))
                    self.resFileLog.write('\n\n')
                    self.resFileLog.write('geometric turnpointMean = %5.2f, s.d. = %5.2f \n' %(turnpointMean, turnpointSd))
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
                 resLineToWrite = resLineToWrite + '{0:5.3f}'.format(turnpointMeanList[j]) + self.prm["pref"]["general"]["csvSeparator"] + \
                                  '{0:5.3f}'.format(turnpointSdList[j]) + self.prm["pref"]["general"]["csvSeparator"] 
           
            resLineToWrite = resLineToWrite + self.prm[currBlock]['conditionLabel'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['listener'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['sessionLabel'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['allBlocks']['experimentLabel'] + self.prm["pref"]["general"]["csvSeparator"] +\
                             self.prm['blockEndDateString'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['blockEndTimeString'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             durString + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm[currBlock]['blockPosition'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm[currBlock]['experiment'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm[currBlock]['paradigm'] + self.prm["pref"]["general"]["csvSeparator"]

            resLineToWrite = self.getCommonTabFields(resLineToWrite)
            resLineToWrite = resLineToWrite + '\n'
            
            if method == 'transformedUpDown':
                self.writeResultsSummaryLine('Transformed Up-Down Interleaved', resLineToWrite)
            elif  method == 'weightedUpDown':
                self.writeResultsSummaryLine('Weighted Up-Down Interleaved', resLineToWrite)
            
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
        self.gauge.setValue(int(pcTot))
        
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
            resLineToWrite = resLineToWrite + '{0:5.3f}'.format(dp) + self.prm["pref"]["general"]["csvSeparator"] + \
                             '{0:5.2f}'.format(self.correctCount/self.trialCount*100) + self.prm["pref"]["general"]["csvSeparator"] + \
                             str(self.correctCount) + self.prm["pref"]["general"]["csvSeparator"] + \
                             str(self.trialCount) + self.prm["pref"]["general"]["csvSeparator"] +\
                             self.prm[currBlock]['conditionLabel'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['listener'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['sessionLabel'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['allBlocks']['experimentLabel'] + self.prm["pref"]["general"]["csvSeparator"] +\
                             self.prm['blockEndDateString'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['blockEndTimeString'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             durString + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm[currBlock]['blockPosition'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm[currBlock]['experiment'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm[currBlock]['paradigm'] + self.prm["pref"]["general"]["csvSeparator"]

            resLineToWrite = resLineToWrite + str(self.prm[currBlock]['nIntervals']) + self.prm["pref"]["general"]["csvSeparator"] 
            resLineToWrite = resLineToWrite + str(self.prm[currBlock]['nAlternatives']) + self.prm["pref"]["general"]["csvSeparator"]
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
      
        pcDone = self.trialCountAll / ((self.prm['nTrials'] + self.prm['nPracticeTrials'])*len(self.prm['conditions']))*100
        bp = int(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'])
        pcThisRep = (bp-1) / self.prm['storedBlocks']*100 + 1 / self.prm['storedBlocks']*pcDone
        pcTot = (self.prm['currentRepetition'] - 1) / self.prm['allBlocks']['repetitions']*100 + 1 / self.prm['allBlocks']['repetitions']*pcThisRep
        self.gauge.setValue(int(pcTot))

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
                resLineToWrite = resLineToWrite + '{0:5.3f}'.format(dprimeList[i]) + self.prm["pref"]["general"]["csvSeparator"] + \
                                 '{0:5.2f}'.format((self.correctCountCnds[self.prm['conditions'][i]]*100)/self.trialCountCnds[self.prm['conditions'][i]]) + self.prm["pref"]["general"]["csvSeparator"] + \
                                 str(self.correctCountCnds[self.prm['conditions'][i]]) + self.prm["pref"]["general"]["csvSeparator"] + \
                                 str(self.trialCountCnds[self.prm['conditions'][i]]) + self.prm["pref"]["general"]["csvSeparator"] 

            resLineToWrite = resLineToWrite + '{0:5.3f}'.format(dprimeAll) + self.prm["pref"]["general"]["csvSeparator"] + \
                             str(totalCorrectCount/totalTrialCount*100) + self.prm["pref"]["general"]["csvSeparator"] + \
                             str(totalCorrectCount) + self.prm["pref"]["general"]["csvSeparator"] + \
                             str(totalTrialCount) + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm[currBlock]['conditionLabel'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['listener'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['sessionLabel'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['allBlocks']['experimentLabel'] + self.prm["pref"]["general"]["csvSeparator"] +\
                             self.prm['blockEndDateString'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['blockEndTimeString'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             durString + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm[currBlock]['blockPosition'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm[currBlock]['experiment'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm[currBlock]['paradigm'] + self.prm["pref"]["general"]["csvSeparator"]

            resLineToWrite = resLineToWrite + str(self.prm[currBlock]['nIntervals']) + self.prm["pref"]["general"]["csvSeparator"] 
            resLineToWrite = resLineToWrite + str(self.prm[currBlock]['nAlternatives']) + self.prm["pref"]["general"]["csvSeparator"]
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
        self.gauge.setValue(int(pcTot))

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
                dp = dprime_yes_no_from_counts(A_correct, A_total, B_correct, B_total, self.prm["pref"]['general']['dprimeCorrection'])
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
            resLineToWrite = '{0:5.3f}'.format(dp) + self.prm["pref"]["general"]["csvSeparator"] 
            resLineToWrite = resLineToWrite + str(self.trialCount) + self.prm["pref"]["general"]["csvSeparator"]
            for i in range(len(self.prm['conditions'])):
                resLineToWrite = resLineToWrite + str(self.correctCountCnds[self.prm['conditions'][i]]) + self.prm["pref"]["general"]["csvSeparator"] + \
                                 str(self.trialCountCnds[self.prm['conditions'][i]]) + self.prm["pref"]["general"]["csvSeparator"]
            resLineToWrite = resLineToWrite + self.prm[currBlock]['conditionLabel'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['listener'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['sessionLabel'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['allBlocks']['experimentLabel'] + self.prm["pref"]["general"]["csvSeparator"] +\
                             self.prm['blockEndDateString'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['blockEndTimeString'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             durString + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm[currBlock]['blockPosition'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm[currBlock]['experiment'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm[currBlock]['paradigm'] + self.prm["pref"]["general"]["csvSeparator"]
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
                for j in range(len(self.prm['trialTypes'])):
                    self.trialCountCnds[self.prm['conditions'][i]][self.prm['trialTypes'][j]] = 0
                    self.correctCountCnds[self.prm['conditions'][i]][self.prm['trialTypes'][j]] = 0
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
        self.gauge.setValue(int(pcTot))

        
        if self.trialCountAll >= (self.prm['nTrials'] + self.prm['nPracticeTrials'])*len(self.prm['conditions']): # Block is completed

            self.writeResultsHeader('standard')
            for i in range(len(self.fullFileLines)):
                self.fullFile.write(self.fullFileLines[i])
            self.fullFileLog.write('\n')
            self.fullFile.write('\n')

            totalCorrectCount = 0
            subconditionTrialCount = [0 for number in range(len(self.prm['trialTypes']))]
            subconditionCorrectCount = [0 for number in range(len(self.prm['trialTypes']))]
            A_correct = []
            A_total = []
            B_correct = []
            B_total = []
            dp = []
            totalTrialCount = 0
            for i in range(len(self.prm['conditions'])):
                totalTrialCount = totalTrialCount + self.trialCount[i]
                thisCondTotalCorrectCount = 0
                for j in range(len(self.prm['trialTypes'])):
                    thisCondTotalCorrectCount = thisCondTotalCorrectCount + self.correctCountCnds[self.prm['conditions'][i]][self.prm['trialTypes'][j]]
                    subconditionCorrectCount[j] = subconditionCorrectCount[j] + self.correctCountCnds[self.prm['conditions'][i]][self.prm['trialTypes'][j]]
                    subconditionTrialCount[j] = subconditionTrialCount[j] + self.trialCountCnds[self.prm['conditions'][i]][self.prm['trialTypes'][j]]
                totalCorrectCount = totalCorrectCount + thisCondTotalCorrectCount

                #compute d-prime for each condition
                A_correct.append(self.correctCountCnds[self.prm['conditions'][i]][self.prm['trialTypes'][0]]) 
                A_total.append(self.trialCountCnds[self.prm['conditions'][i]][self.prm['trialTypes'][0]])
                B_correct.append(self.correctCountCnds[self.prm['conditions'][i]][self.prm['trialTypes'][1]]) 
                B_total.append(self.trialCountCnds[self.prm['conditions'][i]][self.prm['trialTypes'][1]])

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
                    

                for j in range(len(self.prm['trialTypes'])):
                    try:
                        thisPercentCorrect = self.correctCountCnds[self.prm['conditions'][i]][self.prm['trialTypes'][j]]/self.trialCountCnds[self.prm['conditions'][i]][self.prm['trialTypes'][j]]*100
                    except:
                        thisPercentCorrect = nan
                    for ftyp in [self.resFile, self.resFileLog]:
                        ftyp.write('No. Correct Subcondition %s = %d\n' %(self.prm['trialTypes'][j], self.correctCountCnds[self.prm['conditions'][i]][self.prm['trialTypes'][j]]))
                        ftyp.write('No. Total Subcondition %s = %d \n' %(self.prm['trialTypes'][j], self.trialCountCnds[self.prm['conditions'][i]][self.prm['trialTypes'][j]]))
                        ftyp.write('Percent Correct Subcondition %s = %5.2f \n' %(self.prm['trialTypes'][j], thisPercentCorrect))
                
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

            for j in range(len(self.prm['trialTypes'])):
                try:
                    thisPercentCorrect = subconditionCorrectCount[j]/subconditionTrialCount[j]*100
                except:
                    thisPercentCorrect = nan

                for ftyp in [self.resFile, self.resFileLog]:
                    ftyp.write('No. Correct Subcondition %s = %d\n' %(self.prm['trialTypes'][j], subconditionCorrectCount[j]))
                    ftyp.write('No. Total Subcondition %s = %d \n' %(self.prm['trialTypes'][j], subconditionTrialCount[j]))
                    ftyp.write('Percent Correct Subcondition %s = %5.2f \n' %(self.prm['trialTypes'][j], thisPercentCorrect))

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
            for j in range(len(self.prm['trialTypes'])):
                resLineToWrite = resLineToWrite + str(subconditionCorrectCount[j]) + self.prm['pref']["general"]["csvSeparator"] + \
                                 str(subconditionTrialCount[j]) + self.prm['pref']["general"]["csvSeparator"]
            for i in range(len(self.prm['conditions'])):
                resLineToWrite = resLineToWrite + '{0:5.3f}'.format(dp[i]) + self.prm['pref']["general"]["csvSeparator"] 
                resLineToWrite = resLineToWrite + str(self.trialCountCnds[self.prm['conditions'][i]][self.prm['trialTypes'][0]] + self.trialCountCnds[self.prm['conditions'][i]][self.prm['trialTypes'][1]]) + self.prm['pref']["general"]["csvSeparator"]
                for j in range(len(self.prm['trialTypes'])):
                    resLineToWrite = resLineToWrite + str(self.correctCountCnds[self.prm['conditions'][i]][self.prm['trialTypes'][j]]) + self.prm['pref']["general"]["csvSeparator"] + \
                            str(self.trialCountCnds[self.prm['conditions'][i]][self.prm['trialTypes'][j]])  + self.prm['pref']["general"]["csvSeparator"]

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
        self.gauge.setValue(int(pcTot))

        
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

    def sortResponseMultipleConstants1PairSameDifferent(self, buttonClicked):
        if self.prm['startOfBlock'] == True:
            self.prm['startOfBlock'] = False

            self.fullFileLines = []
            self.fullFileSummLines = []
            self.trialCount = {} #trial count by difference, excluding practice trials
            self.trialCountCnds = {} #trial count by difference and condition, excluding practice trials
            self.correctCountCnds = {}
            self.trialCountAll = {} #this includes also the practice trials
            for j in range(self.prm['nDifferences']):
                self.trialCount[j] = 0
                self.trialCountCnds[j] = {}
                self.correctCountCnds[j] = {}
                for i in range(len(self.prm['conditions'])):
                    self.trialCountCnds[j][self.prm['conditions'][i]] = 0
                    self.correctCountCnds[j][self.prm['conditions'][i]] = 0
                self.trialCountAll[j] = 0
        
        self.currentDifferenceName = self.prm['differenceNames'][self.prm['currentDifference']]
        self.trialCountAll[self.prm['currentDifference']] = self.trialCountAll[self.prm['currentDifference']] + 1
        if self.trialCountAll[self.prm['currentDifference']] > self.prm['nPracticeTrials']:
            self.trialCountCnds[self.prm['currentDifference']][self.currentCondition] = self.trialCountCnds[self.prm['currentDifference']][self.currentCondition] + 1
            self.trialCount[self.prm['currentDifference']] = self.trialCount[self.prm['currentDifference']] + 1
        if buttonClicked == self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback('correct')
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback('neutral')
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback('off')
            if self.trialCountAll[self.prm['currentDifference']] > self.prm['nPracticeTrials']:
                self.correctCountCnds[self.prm['currentDifference']][self.currentCondition] = self.correctCountCnds[self.prm['currentDifference']][self.currentCondition] + 1
            resp = '1'
        elif buttonClicked != self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback('incorrect')
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback('neutral')
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback('off')
            resp = '0'
        self.fullFileLog.write(   self.currentDifferenceName + '_' + self.stim1 + '-' + self.stim2 + '_' + self.currentCondition + '; ' + resp + '; ')
        self.fullFileLines.append(self.currentDifferenceName + '_' + self.stim1 + '-' + self.stim2 + '_' + self.currentCondition + '; ' + resp + '; ')
        self.fullFileSummLines.append([self.currentDifferenceName + self.prm['pref']["general"]["csvSeparator"] +
                                      self.stim1  + self.prm['pref']["general"]["csvSeparator"] +
                                      self.stim2 + self.prm['pref']["general"]["csvSeparator"] +
                                      self.currentCondition + self.prm['pref']["general"]["csvSeparator"] +
                                      resp + self.prm['pref']["general"]["csvSeparator"]])

        if 'additional_parameters_to_write' in self.prm:
            for p in range(len(self.prm['additional_parameters_to_write'])):
                self.fullFileLog.write(str(self.prm['additional_parameters_to_write'][p]))
                self.fullFileLines.append(str(self.prm['additional_parameters_to_write'][p]))
                self.fullFileSummLines[len(self.fullFileSummLines)-1].append(str(self.prm['additional_parameters_to_write'][p]) + self.prm['pref']["general"]["csvSeparator"])
                self.fullFileLog.write('; ')
                self.fullFileLines.append('; ')
        self.fullFileLog.write('\n')
        self.fullFileLines.append('\n')
        self.fullFileLog.flush()

        cnt = 0
        for j in range(self.prm['nDifferences']):
            cnt = cnt + self.trialCountAll[j]
        pcDone = cnt / ((self.prm['nTrials']+self.prm['nPracticeTrials']) *self.prm['nDifferences']) * 100
        bp = int(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'])
        pcThisRep = (bp-1) / self.prm['storedBlocks']*100 + 1 / self.prm['storedBlocks']*pcDone
        pcTot = (self.prm['currentRepetition'] - 1) / self.prm['allBlocks']['repetitions']*100 + 1 / self.prm['allBlocks']['repetitions']*pcThisRep
        self.gauge.setValue(int(pcTot))

     

        if self.trialCount[self.prm['currentDifference']] == self.prm['nTrials']:
            self.prm['differenceChoices'].remove(self.currentDifferenceName)

        # print('Trial Count:', self.trialCount)
        # print('Trial Count All:', self.trialCountAll)
        # print('Difference Choices:', self.prm['differenceChoices'])
        # print(self.currentDifferenceName)

        if len(self.prm['differenceChoices']) == 0:
            totalCorrectCount = {}
            for j in range(self.prm['nDifferences']):
                totalCorrectCount[j] = 0
                for i in range(len(self.prm['conditions'])):
                    totalCorrectCount[j] = totalCorrectCount[j] + self.correctCountCnds[j][self.prm['conditions'][i]]
            self.writeResultsHeader('standard')
            for i in range(len(self.fullFileLines)):
                self.fullFile.write(self.fullFileLines[i])
            self.fullFileLog.write('\n')
            self.fullFile.write('\n')
            self.fullFile.flush()
            self.fullFileLog.flush()
            A_correct = {}; A_total = {}; B_correct = {}; B_total = {}
            dp_IO = {}; dp_diff = {}
            for j in range(self.prm['nDifferences']):
                A_correct[j] = self.correctCountCnds[j][self.prm['conditions'][0]]
                A_total[j] = self.trialCountCnds[j][self.prm['conditions'][0]]
                B_correct[j] = self.correctCountCnds[j][self.prm['conditions'][1]]
                B_total[j] = self.trialCountCnds[j][self.prm['conditions'][1]]

                try:
                    dp_IO[j] = dprime_SD_from_counts(nCA=A_correct[j], nTA=A_total[j], nCB=B_correct[j], nTB=B_total[j], meth='IO', corr=self.prm['pref']['general']['dprimeCorrection'])
                except:
                    dp_IO[j] = nan
                try:
                    dp_diff[j] = dprime_SD_from_counts(nCA=A_correct[j], nTA=A_total[j], nCB=B_correct[j], nTB=B_total[j], meth='diff', corr=self.prm['pref']['general']['dprimeCorrection'])
                except:
                    dp_diff[j] = nan

                for ftyp in [self.resFile, self.resFileLog]:
                    ftyp.write("DIFFERENCE: " + self.prm['differenceNames'][j] + '\n')
                    ftyp.write('No. Correct = %d\n' %(totalCorrectCount[j]))
                    ftyp.write('No. Total = %d\n' %(self.trialCount[j]))
                    ftyp.write('Percent Correct = %5.2f \n' %(totalCorrectCount[j]/self.trialCount[j]*100))
                    ftyp.write("d-prime IO = %5.3f \n" %(dp_IO[j]))
                    ftyp.write("d-prime diff = %5.3f \n\n" %(dp_diff[j]))
                    
                    
                    for i in range(len(self.prm['conditions'])):
                        try:
                            thisPercentCorrect = (self.correctCountCnds[j][self.prm['conditions'][i]]*100)/self.trialCountCnds[j][self.prm['conditions'][i]]
                        except:
                            thisPercentCorrect = nan
                        ftyp.write('No. Correct Condition %s = %d\n' %(self.prm['conditions'][i], self.correctCountCnds[j][self.prm['conditions'][i]]))
                        ftyp.write('No. Total Condition %s = %d \n' %(self.prm['conditions'][i], self.trialCountCnds[j][self.prm['conditions'][i]]))
                        ftyp.write('Percent Correct Condition %s = %5.2f \n' %(self.prm['conditions'][i], thisPercentCorrect))
            
                    ftyp.write('\n\n')
                    ftyp.flush()

            self.getEndTime()
           
            currBlock = 'b' + str(self.prm['currentBlock'])
            durString = '{0:5.3f}'.format(self.prm['blockEndTime'] - self.prm['blockStartTime'])
            
            #'dprime condition listener session experimentLabel nCorrectA nTotalA nCorrectB nTotalB nCorrect nTotal date time duration block experiment'
            resLineToWrite = ''
            for j in range(self.prm['nDifferences']):
                resLineToWrite = resLineToWrite + '{0:5.3f}'.format(dp_IO[j]) + self.prm['pref']["general"]["csvSeparator"]
                resLineToWrite = resLineToWrite + '{0:5.3f}'.format(dp_diff[j]) + self.prm['pref']["general"]["csvSeparator"] 
                resLineToWrite = resLineToWrite + str(self.trialCount[j]) + self.prm['pref']["general"]["csvSeparator"]
                for i in range(len(self.prm['conditions'])):
                    resLineToWrite = resLineToWrite + str(self.correctCountCnds[j][self.prm['conditions'][i]]) + self.prm['pref']["general"]["csvSeparator"] + \
                                     str(self.trialCountCnds[j][self.prm['conditions'][i]]) + self.prm['pref']["general"]["csvSeparator"]
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
            self.writeResultsSummaryLine('Multiple Constants 1-Pair Same/Different', resLineToWrite)


            resLineToWriteSummFull = ""
            for i in range(len(self.fullFileSummLines)):
                resLineToWriteSummFull = resLineToWriteSummFull + " ".join(self.fullFileSummLines[i]) + \
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
             
                resLineToWriteSummFull = self.getCommonTabFields(resLineToWriteSummFull)
                resLineToWriteSummFull = resLineToWriteSummFull + '\n'
            self.writeResultsSummaryFullLine('Multiple Constants 1-Pair Same/Different', resLineToWriteSummFull)

            self.atBlockEnd()
           
        else: #block is not finished, move on to next trial
            self.doTrial()

    def sortResponseMultipleConstantsABX(self, buttonClicked):
        if self.prm['startOfBlock'] == True:
            self.prm['startOfBlock'] = False

            self.fullFileLines = []
            self.fullFileSummLines = []
            self.trialCount = {} #trial count by difference, excluding practice trials
            self.trialCountCnds = {} #trial count by difference and condition, excluding practice trials
            self.correctCountCnds = {}
            self.trialCountAll = {} #this includes also the practice trials
            for j in range(self.prm['nDifferences']):
                self.trialCount[j] = 0
                self.trialCountCnds[j] = {}
                self.correctCountCnds[j] = {}
                for i in range(len(self.prm['conditions'])):
                    self.trialCountCnds[j][self.prm['conditions'][i]] = 0
                    self.correctCountCnds[j][self.prm['conditions'][i]] = 0
                self.trialCountAll[j] = 0
        
        self.currentDifferenceName = self.prm['differenceNames'][self.prm['currentDifference']]
        self.trialCountAll[self.prm['currentDifference']] = self.trialCountAll[self.prm['currentDifference']] + 1
        if self.trialCountAll[self.prm['currentDifference']] > self.prm['nPracticeTrials']:
            self.trialCountCnds[self.prm['currentDifference']][self.currentCondition] = self.trialCountCnds[self.prm['currentDifference']][self.currentCondition] + 1
            self.trialCount[self.prm['currentDifference']] = self.trialCount[self.prm['currentDifference']] + 1
        if buttonClicked == self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback('correct')
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback('neutral')
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback('off')
            if self.trialCountAll[self.prm['currentDifference']] > self.prm['nPracticeTrials']:
                self.correctCountCnds[self.prm['currentDifference']][self.currentCondition] = self.correctCountCnds[self.prm['currentDifference']][self.currentCondition] + 1
            resp = '1'
        elif buttonClicked != self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback('incorrect')
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback('neutral')
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback('off')
            resp = '0'
        self.fullFileLog.write(   self.currentDifferenceName + '_' + self.stim1 + '-' + self.stim2 + '_' + self.stim3 + '_' + self.currentCondition + '; ' + resp + '; ')
        self.fullFileLines.append(self.currentDifferenceName + '_' + self.stim1 + '-' + self.stim2 + '_' + self.stim3 + '_' + self.currentCondition + '; ' + resp + '; ')
        self.fullFileSummLines.append([self.currentDifferenceName + self.prm['pref']["general"]["csvSeparator"] +
                                      self.stim1  + self.prm['pref']["general"]["csvSeparator"] +
                                      self.stim2 + self.prm['pref']["general"]["csvSeparator"] +
                                      self.stim3 + self.prm['pref']["general"]["csvSeparator"] +
                                      self.currentCondition + self.prm['pref']["general"]["csvSeparator"] +
                                      resp + self.prm['pref']["general"]["csvSeparator"]])

        if 'additional_parameters_to_write' in self.prm:
            for p in range(len(self.prm['additional_parameters_to_write'])):
                self.fullFileLog.write(str(self.prm['additional_parameters_to_write'][p]))
                self.fullFileLines.append(str(self.prm['additional_parameters_to_write'][p]))
                self.fullFileSummLines[len(self.fullFileSummLines)-1].append(str(self.prm['additional_parameters_to_write'][p]) + self.prm['pref']["general"]["csvSeparator"])
                self.fullFileLog.write('; ')
                self.fullFileLines.append('; ')
        self.fullFileLog.write('\n')
        self.fullFileLines.append('\n')
        self.fullFileLog.flush()

        cnt = 0
        for j in range(self.prm['nDifferences']):
            cnt = cnt + self.trialCountAll[j]
        pcDone = cnt / ((self.prm['nTrials']+self.prm['nPracticeTrials']) *self.prm['nDifferences']) * 100
        bp = int(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'])
        pcThisRep = (bp-1) / self.prm['storedBlocks']*100 + 1 / self.prm['storedBlocks']*pcDone
        pcTot = (self.prm['currentRepetition'] - 1) / self.prm['allBlocks']['repetitions']*100 + 1 / self.prm['allBlocks']['repetitions']*pcThisRep
        self.gauge.setValue(int(pcTot))

     
        if self.trialCount[self.prm['currentDifference']] == self.prm['nTrials']:
            self.prm['differenceChoices'].remove(self.currentDifferenceName)

        if len(self.prm['differenceChoices']) == 0:
            totalCorrectCount = {}
            for j in range(self.prm['nDifferences']):
                totalCorrectCount[j] = 0
                for i in range(len(self.prm['conditions'])):
                    totalCorrectCount[j] = totalCorrectCount[j] + self.correctCountCnds[j][self.prm['conditions'][i]]
            self.writeResultsHeader('standard')
            for i in range(len(self.fullFileLines)):
                self.fullFile.write(self.fullFileLines[i])
            self.fullFileLog.write('\n')
            self.fullFile.write('\n')
            self.fullFile.flush()
            self.fullFileLog.flush()
            A_correct = {}; A_total = {}; B_correct = {}; B_total = {}
            dp_IO = {}; dp_diff = {}
            for j in range(self.prm['nDifferences']):
                A_correct[j] = self.correctCountCnds[j][self.prm['conditions'][0]]
                A_total[j] = self.trialCountCnds[j][self.prm['conditions'][0]]
                B_correct[j] = self.correctCountCnds[j][self.prm['conditions'][1]]
                B_total[j] = self.trialCountCnds[j][self.prm['conditions'][1]]

                try:
                    dp_IO[j] = dprime_ABX_from_counts(nCA=A_correct[j], nTA=A_total[j], nCB=B_correct[j], nTB=B_total[j], meth='IO', corr=self.prm['pref']['general']['dprimeCorrection'])
                except:
                    dp_IO[j] = nan
                try:
                    dp_diff[j] = dprime_ABX_from_counts(nCA=A_correct[j], nTA=A_total[j], nCB=B_correct[j], nTB=B_total[j], meth='diff', corr=self.prm['pref']['general']['dprimeCorrection'])
                except:
                    dp_diff[j] = nan

                for ftyp in [self.resFile, self.resFileLog]:
                    ftyp.write("DIFFERENCE: " + self.prm['differenceNames'][j] + '\n')
                    ftyp.write('No. Correct = %d\n' %(totalCorrectCount[j]))
                    ftyp.write('No. Total = %d\n' %(self.trialCount[j]))
                    ftyp.write('Percent Correct = %5.2f \n' %(totalCorrectCount[j]/self.trialCount[j]*100))
                    ftyp.write("d-prime IO = %5.3f \n" %(dp_IO[j]))
                    ftyp.write("d-prime diff = %5.3f \n\n" %(dp_diff[j]))
                    
                    
                    for i in range(len(self.prm['conditions'])):
                        try:
                            thisPercentCorrect = (self.correctCountCnds[j][self.prm['conditions'][i]]*100)/self.trialCountCnds[j][self.prm['conditions'][i]]
                        except:
                            thisPercentCorrect = nan
                        ftyp.write('No. Correct Condition %s = %d\n' %(self.prm['conditions'][i], self.correctCountCnds[j][self.prm['conditions'][i]]))
                        ftyp.write('No. Total Condition %s = %d \n' %(self.prm['conditions'][i], self.trialCountCnds[j][self.prm['conditions'][i]]))
                        ftyp.write('Percent Correct Condition %s = %5.2f \n' %(self.prm['conditions'][i], thisPercentCorrect))
            
                    ftyp.write('\n\n')
                    ftyp.flush()

            self.getEndTime()
           
            currBlock = 'b' + str(self.prm['currentBlock'])
            durString = '{0:5.3f}'.format(self.prm['blockEndTime'] - self.prm['blockStartTime'])
            
            #'dprime condition listener session experimentLabel nCorrectA nTotalA nCorrectB nTotalB nCorrect nTotal date time duration block experiment'
            resLineToWrite = ''
            for j in range(self.prm['nDifferences']):
                resLineToWrite = resLineToWrite + '{0:5.3f}'.format(dp_IO[j]) + self.prm['pref']["general"]["csvSeparator"]
                resLineToWrite = resLineToWrite + '{0:5.3f}'.format(dp_diff[j]) + self.prm['pref']["general"]["csvSeparator"] 
                resLineToWrite = resLineToWrite + str(self.trialCount[j]) + self.prm['pref']["general"]["csvSeparator"]
                for i in range(len(self.prm['conditions'])):
                    resLineToWrite = resLineToWrite + str(self.correctCountCnds[j][self.prm['conditions'][i]]) + self.prm['pref']["general"]["csvSeparator"] + \
                                     str(self.trialCountCnds[j][self.prm['conditions'][i]]) + self.prm['pref']["general"]["csvSeparator"]
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
            self.writeResultsSummaryLine('Multiple Constants ABX', resLineToWrite)


            resLineToWriteSummFull = ""
            for i in range(len(self.fullFileSummLines)):
                resLineToWriteSummFull = resLineToWriteSummFull + " ".join(self.fullFileSummLines[i]) + \
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
             
                resLineToWriteSummFull = self.getCommonTabFields(resLineToWriteSummFull)
                resLineToWriteSummFull = resLineToWriteSummFull + '\n'
            self.writeResultsSummaryFullLine('Multiple Constants ABX', resLineToWriteSummFull)

            self.atBlockEnd()
           
        else: #block is not finished, move on to next trial
            self.doTrial()

    def sortResponsePEST(self, buttonClicked):
        #PEST SUPPORT IS EXPERIMENTAL, THE PROCEDURE IS VERY LITTLE TESTED!
        if self.prm['startOfBlock'] == True:
            self.prm['correctCount'] = 0
            self.prm['startOfBlock'] = False
            self.prm['currStepSize'] = copy.copy(self.prm['initialStepSize'])
            self.prm['nTrialsCurrLev'] = 0
            self.prm['nSteps'] = 0 
            self.prm['lastStepDoubled'] = False
            self.prm['stepBeforeLastReversalDoubled'] = False
            self.prm['trackDir'] = copy.copy(self.prm['corrTrackDir'])
            if self.prm['corrTrackDir'] == self.tr("Down"):
                self.prm['corrTrackSign'] = -1
                self.prm['incorrTrackSign'] = 1
                self.prm['incorrTrackDir'] = self.tr("Up")
            else:
                self.prm['corrTrackSign'] = 1
                self.prm['incorrTrackSign'] = -1
                self.prm['incorrTrackDir'] = self.tr("Down")
            
            self.fullFileLines = []
            self.fullFileSummLines = []
            self.prm['buttonCounter'] = [0 for i in range(self.prm['nAlternatives'])]
        self.prm['buttonCounter'][buttonClicked-1] = self.prm['buttonCounter'][buttonClicked-1] + 1

        #increment number of trials
        self.prm['nTrialsCurrLev'] = self.prm['nTrialsCurrLev'] +1
            
        if buttonClicked == self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback("correct")
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback("neutral")
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback("off")
            
            self.fullFileLog.write(str(self.prm['adaptiveParam']) + '; ')
            self.fullFileLines.append(str(self.prm['adaptiveParam']) + '; ')
            self.fullFileSummLines.append([str(self.prm['adaptiveParam']) + self.prm["pref"]["general"]["csvSeparator"]])
            self.fullFileLog.write('1; ')
            self.fullFileLines.append('1; ')
            self.fullFileSummLines[len(self.fullFileSummLines)-1].append('1' + self.prm["pref"]["general"]["csvSeparator"])
            if 'additional_parameters_to_write' in self.prm:
                for p in range(len(self.prm['additional_parameters_to_write'])):
                    self.fullFileLog.write(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileLines.append(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileSummLines[len(self.fullFileSummLines)-1].append(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileLog.write(' ;')
                    self.fullFileLines.append(' ;')
                    self.fullFileSummLines[len(self.fullFileSummLines)-1].append(self.prm["pref"]["general"]["csvSeparator"])
            self.fullFileLog.write('\n')
            self.fullFileLines.append('\n')
            self.prm['correctCount'] = self.prm['correctCount'] + 1
        elif buttonClicked != self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback("incorrect")
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback("neutral")
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback("off")
                               
            self.fullFileLog.write(str(self.prm['adaptiveParam']) + '; ')
            self.fullFileLines.append(str(self.prm['adaptiveParam']) + '; ')
            self.fullFileSummLines.append([str(self.prm['adaptiveParam']) + self.prm["pref"]["general"]["csvSeparator"]])
            self.fullFileLog.write('0; ')
            self.fullFileLines.append('0; ')
            self.fullFileSummLines[len(self.fullFileSummLines)-1].append('0' + self.prm["pref"]["general"]["csvSeparator"])
            if 'additional_parameters_to_write' in self.prm:
                for p in range(len(self.prm['additional_parameters_to_write'])):
                    self.fullFileLog.write(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileLines.append(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileSummLines[len(self.fullFileSummLines)-1].append(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileLog.write('; ')
                    self.fullFileLines.append('; ')
                    self.fullFileSummLines[len(self.fullFileSummLines)-1].append(self.prm["pref"]["general"]["csvSeparator"])
            self.fullFileLog.write('\n')
            self.fullFileLines.append('\n')
            

        #perform test
        # the expected number of correct responses at threshold is Pt*N
        #where Pt is the proportion correct tracked (e.g. 0.75), and N is the
        #number of trials run at the given level. If the number of correct
        #responses obtained is decidedly larger than the number of expected
        #correct responses at threshold then the track goes down. If the
        # number of correct responses obtained is decidedly smaller than
        #the number of expected correct responses at threshold then the
        #track goes up. But how much larger/smaller should the number of correct
        #responses be to be considered decidedly larger or smaller than the
        #expected proportion? This is governed by the parameter W, which defines
        #tolerance limits on the expecetd number of correct responses at threshold.
        #If W is small, the tolerance limits are small, and the track moves quickly to
        #another value. If W is large, the tolerance limits are large, and more evidence
        #needs to be collected before moving the track to a different value.

        expectedNCorrect = self.prm['percentCorrectTracked']/100*self.prm['nTrialsCurrLev']
        print('Correct count: ', self.prm['correctCount'])
        print('ExpectedNCorrect: ', expectedNCorrect)

        newStepSize = copy.copy(self.prm['currStepSize'])#temporary, it will be changed later if necessary

        if self.prm['correctCount'] >= expectedNCorrect + self.prm['W']:
            print("self.prm['correctCount'] >= expectedNCorrect + self.prm['W']")

            if self.prm['trackDir'] == self.prm['incorrTrackDir']: #CALL REVERSAL
                self.prm['trackDir'] = copy.copy(self.prm['corrTrackDir'])
                newStepSize = self.prm['currStepSize']/2 #halve step size at reversal (Rule 1)
                if self.prm['lastStepDoubled'] == True: #(see Rule 3)
                    self.prm['stepBeforeLastReversalDoubled'] = True
                self.prm['lastStepDoubled'] = False #we just reversed so we didn't double step
                self.prm['nSteps'] = 1 #re-initialize step counter. Should this be 1?
            elif self.prm['trackDir'] == self.prm['corrTrackDir']:
                self.prm['nSteps'] = self.prm['nSteps'] + 1
                if self.prm['nSteps'] < 3:
                    self.prm['lastStepDoubled'] = False
                elif self.prm['nSteps'] == 3:
                    if self.prm['stepBeforeLastReversalDoubled'] == False:
                        newStepSize = self.prm['currStepSize']*2
                        self.prm['lastStepDoubled'] = True
                    else:
                        self.prm['lastStepDoubled'] = False
                elif self.prm['nSteps'] > 3:
                    newStepSize = self.prm['currStepSize']*2
                    self.prm['lastStepDoubled'] = True

            #limit maximum step size
            if newStepSize > self.prm['maxStepSize']:
                newStepSize = self.prm['maxStepSize']

            self.prm['nTrialsCurrLev'] = 0
            self.prm['correctCount'] = 0
            self.prm['currStepSize'] = newStepSize

        
            if self.prm['adaptiveType'] == self.tr("Arithmetic"):
                self.prm['adaptiveParam'] = self.prm['adaptiveParam'] + (self.prm['currStepSize']*self.prm['corrTrackSign'])
            elif self.prm['adaptiveType'] == self.tr("Geometric"):
                self.prm['adaptiveParam'] = self.prm['adaptiveParam'] * (self.prm['currStepSize']**self.prm['corrTrackSign'])
                
        elif self.prm['correctCount'] <= expectedNCorrect - self.prm['W']:
            print("self.prm['correctCount'] <= expectedNCorrect - self.prm['W']")

            if self.prm['trackDir'] == self.prm['corrTrackDir']: #CALL REVERSAL
                self.prm['trackDir'] = copy.copy(self.prm['incorrTrackDir'])
                newStepSize = self.prm['currStepSize']/2 #halve step size at reversal
                if self.prm['lastStepDoubled'] == True:
                    self.prm['stepBeforeLastReversalDoubled'] = True
                self.prm['lastStepDoubled'] = False
                self.prm['nSteps'] = 1 #re-initialize counter. Should this be 1?
            elif self.prm['trackDir'] == self.prm['incorrTrackDir']:
                self.prm['nSteps'] = self.prm['nSteps'] + 1
                if self.prm['nSteps'] < 3:
                    self.prm['lastStepDoubled'] = False
                elif self.prm['nSteps'] == 3:
                    if self.prm['stepBeforeLastReversalDoubled'] == False:
                        newStepSize = self.prm['currStepSize']*2
                        self.prm['lastStepDoubled'] = True
                    else:
                        self.prm['lastStepDoubled'] = False
                elif self.prm['nSteps'] > 3:
                    newStepSize = self.prm['currStepSize']*2
                    self.prm['lastStepDoubled'] = True

            #limit maximum step size
            if newStepSize > self.prm['maxStepSize']:
                newStepSize = self.prm['maxStepSize']

            self.prm['nTrialsCurrLev'] = 0
            self.prm['correctCount'] = 0
            self.prm['currStepSize'] = newStepSize

            if self.prm['adaptiveType'] == self.tr("Arithmetic"):
                self.prm['adaptiveParam'] = self.prm['adaptiveParam'] + (self.prm['currStepSize']*self.prm['incorrTrackSign'])
            elif self.prm['adaptiveType'] == self.tr("Geometric"):
                self.prm['adaptiveParam'] = self.prm['adaptiveParam'] * (self.prm['currStepSize']**self.prm['incorrTrackSign'])
         
          
 

        print("Adaptive Difference")
        print(self.prm['adaptiveParam'])
        print("Current step: ")
        print(self.prm['currStepSize'])
        print("nSteps")
        print(self.prm['nSteps'])
        self.fullFileLog.flush()
        pcDone = 0#(self.prm['nTurnpoints'] / self.prm['totalTurnpoints']) * 100
        bp = int(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'])
        pcThisRep = (bp-1) / self.prm['storedBlocks']*100 + 1 / self.prm['storedBlocks']*pcDone
        pcTot = (self.prm['currentRepetition'] - 1) / self.prm['allBlocks']['repetitions']*100 + 1 / self.prm['allBlocks']['repetitions']*pcThisRep
        self.gauge.setValue(int(pcTot))
        if self.prm['currStepSize'] < self.prm['minStepSize']:
            self.writeResultsHeader('standard')
            #process results
            self.fullFileLog.write('\n')
            self.fullFileLines.append('\n')
            for i in range(len(self.fullFileLines)):
                self.fullFile.write(self.fullFileLines[i])
            if self.prm['adaptiveType'] == self.tr("Arithmetic"):
                self.resFile.write('\n\n')
                self.resFile.write('Threshold = %5.2f \n' %(self.prm['adaptiveParam']))
                self.resFileLog.write('\n\n')
                self.resFileLog.write('Threshold = %5.2f \n' %(self.prm['adaptiveParam']))
            elif self.prm['adaptiveType'] == self.tr("Geometric"):
                self.resFile.write('\n\n')
                self.resFile.write('Geometric Threshold = %5.2f \n' %(self.prm['adaptiveParam']))
                self.resFileLog.write('\n\n')
                self.resFileLog.write('Geometric Threshold = %5.2f \n' %(self.prm['adaptiveParam']))

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
            resLineToWrite = '{0:5.3f}'.format(self.prm['adaptiveParam']) + self.prm['pref']["general"]["csvSeparator"] + \
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

            self.writeResultsSummaryLine('PEST', resLineToWrite)


            resLineToWriteSummFull = ""
            for i in range(len(self.fullFileSummLines)):
              resLineToWriteSummFull = resLineToWriteSummFull + " ".join(self.fullFileSummLines[i]) + \
                             self.prm[currBlock]['conditionLabel'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['listener'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['sessionLabel'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['allBlocks']['experimentLabel'] + self.prm["pref"]["general"]["csvSeparator"] +\
                             self.prm['blockEndDateString'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm['blockEndTimeString'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             durString + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm[currBlock]['blockPosition'] + self.prm["pref"]["general"]["csvSeparator"] + \
                             self.prm[currBlock]['experiment'] + self.prm["pref"]["general"]["csvSeparator"] +\
                             self.prm[currBlock]['paradigm'] + self.prm["pref"]["general"]["csvSeparator"]
             
              resLineToWriteSummFull = self.getCommonTabFields(resLineToWriteSummFull)
              resLineToWriteSummFull = resLineToWriteSummFull + '\n'
            
            
            self.writeResultsSummaryFullLine('PEST', resLineToWriteSummFull)


            self.atBlockEnd()
            
        else:
            self.doTrial()


    def sortResponseMaximumLikelihood(self, buttonClicked):
        if self.prm['startOfBlock'] == True:
            if self.prm['psyFunLogScale'] == "Yes":
                scl = "log"
            elif self.prm['psyFunLogScale'] == "No":
                scl = "linear"
            self.prm['MLMidPointGrid'] = stimSpacingGrid(self.prm['psyFunLoMidPoint'], self.prm['psyFunHiMidPoint'], self.prm['psyFunMidPointStep'], scl)
            self.prm['MLLikelihood'] = numpy.zeros(len(self.prm['MLMidPointGrid']))
            self.prm['startOfBlock'] = False
            self.prm['MLStimLevels'] = []
            self.prm['MLResponses'] = []
            self.trialCount = 0
            self.fullFileLines = []
            self.prm['buttonCounter'] = [0 for i in range(self.prm['nAlternatives'])]
        currBlock = 'b' + str(self.prm['currentBlock'])
        self.prm['buttonCounter'][buttonClicked-1] = self.prm['buttonCounter'][buttonClicked-1] + 1
            
        if buttonClicked == self.correctButton:
            self.prm['MLResponses'].append(1)
            response = 1
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback("correct")
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback("neutral")
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback("off")
        elif buttonClicked != self.correctButton:
            self.prm['MLResponses'].append(0)
            response = 0
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback("incorrect")
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback("neutral")
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback("off")
            
        self.fullFileLog.write(str(self.prm['adaptiveParam']) + '; ')
        self.fullFileLines.append(str(self.prm['adaptiveParam']) + '; ')
        self.fullFileLog.write(str(response)+'; ')
        self.fullFileLines.append(str(response)+'; ')
        if 'additional_parameters_to_write' in self.prm:
            for p in range(len(self.prm['additional_parameters_to_write'])):
                self.fullFileLog.write(str(self.prm['additional_parameters_to_write'][p]))
                self.fullFileLines.append(str(self.prm['additional_parameters_to_write'][p]))
                self.fullFileLog.write(' ;')
                self.fullFileLines.append(' ;')
        self.fullFileLog.write('\n')
        self.fullFileLines.append('\n')
        self.prm['MLStimLevels'].append(self.prm['adaptiveParam'])
        if self.prm['psyFunLogScale'] == "No":
            ll = logisticLikelihood(self.prm['adaptiveParam'], response, self.prm['MLMidPointGrid'],
                                    self.prm['psyFunSlope'], 1/self.prm[currBlock]['nAlternatives'],
                                    self.prm['psyFunLapseRate'])
            self.prm['MLLikelihood'] = self.prm['MLLikelihood'] + ll
            mlIdx = numpy.where( self.prm['MLLikelihood']==max(self.prm['MLLikelihood']))[0]
            self.prm['adaptiveParam'] = invLogistic(self.prm['percentCorrectTracked']/100,
                                                         self.prm['MLMidPointGrid'][mlIdx],
                                                         self.prm['psyFunSlope'], 1/self.prm[currBlock]['nAlternatives'],
                                                         self.prm['psyFunLapseRate'])[0]
        elif self.prm['psyFunLogScale'] == "Yes":
            ll = logisticLikelihood(log(self.prm['adaptiveParam']), response, log(self.prm['MLMidPointGrid']),
                                    exp(self.prm['psyFunSlope']), 1/self.prm[currBlock]['nAlternatives'],
                                    self.prm['psyFunLapseRate'])
            self.prm['MLLikelihood'] = self.prm['MLLikelihood'] + ll
            mlIdx = numpy.where( self.prm['MLLikelihood']==max(self.prm['MLLikelihood']))[0]
            self.prm['adaptiveParam'] = exp(invLogistic(self.prm['percentCorrectTracked']/100,
                                                             log(self.prm['MLMidPointGrid'][mlIdx]),
                                                             exp(self.prm['psyFunSlope']),
                                                             1/self.prm[currBlock]['nAlternatives'],
                                                             self.prm['psyFunLapseRate'])[0])
            
        #print(self.prm['adaptiveParam'])
        self.trialCount = self.trialCount +1

        self.fullFileLog.flush()
        pcDone = (self.trialCount / self.prm['nTrials']) * 100
        bp = int(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'])
        pcThisRep = (bp-1) / self.prm['storedBlocks']*100 + 1 / self.prm['storedBlocks']*pcDone
        pcTot = (self.prm['currentRepetition'] - 1) / self.prm['allBlocks']['repetitions']*100 + 1 / self.prm['allBlocks']['repetitions']*pcThisRep
        self.gauge.setValue(int(pcTot))
        
        if self.trialCount == self.prm['nTrials']:
            self.writeResultsHeader('standard')
            self.fullFileLog.write('\n')
            self.fullFileLines.append('\n')
            for i in range(len(self.fullFileLines)):
                self.fullFile.write(self.fullFileLines[i])
            for i in range(len(self.prm['MLStimLevels'])):
                self.resFile.write('%5.2f ' %self.prm['MLStimLevels'][i])
                self.resFileLog.write('%5.2f ' %self.prm['MLStimLevels'][i])
   
            self.resFile.write('\n\n')
            self.resFile.write('threshold = %5.2f \n' %(self.prm['MLStimLevels'][-1]))
            self.resFileLog.write('\n\n')
            self.resFileLog.write('threshold = %5.2f \n' %(self.prm['MLStimLevels'][-1]))

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

            durString = '{0:5.3f}'.format(self.prm['blockEndTime'] - self.prm['blockStartTime'])
            resLineToWrite = '{0:5.3f}'.format(self.prm['MLStimLevels'][-1]) + self.prm['pref']["general"]["csvSeparator"] + \
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
            
            self.writeResultsSummaryLine('Maximum Likelihood', resLineToWrite)
     

            self.atBlockEnd()
        else:
            self.doTrial()


    def sortResponsePSI(self, buttonClicked):
        currBlock = 'b' + str(self.prm['currentBlock'])
        if self.prm['startOfBlock'] == True:
            self.fullFileLines = []
            self.fullFileSummLines = []
            if self.prm['margThresh'] == "Yes" or self.prm['margSlope'] == "Yes" or self.prm['margLapse'] == "Yes":
                ax = np.array([])
                if self.prm['margThresh'] == "Yes":
                    ax = numpy.append(ax, 0)
                if self.prm['margSlope'] == "Yes":
                    ax = numpy.append(ax, 1)
                if self.prm['margLapse'] == "Yes":
                    ax = numpy.append(ax, 2)
                ax = tuple(np.sort(ax))
            else:
                ax = None
                    

            gammax = 1/self.prm[currBlock]['nAlternatives']
            if self.prm['stimScale'] == "Linear":
                self.PSI = setupPSI(model=self.prm['psyFunType'],
                                    x0=self.prm['adaptiveParam'],
                                    xLim=(self.prm['stimLo'], self.prm['stimHi']),
                                    xStep=self.prm['stimStep'],
                                    stimScale=self.prm['stimScale'],
                                    alphaLim=(self.prm['loMidPoint'], self.prm['hiMidPoint']),
                                    alphaStep=self.prm['midPointStep'],
                                    alphaSpacing="Linear",
                                    alphaDist=self.prm['midPointPrior'],
                                    alphaMu=self.prm['midPointPriorMu'],
                                    alphaSTD=self.prm['midPointPriorSTD'],
                                    betaLim=(self.prm['loSlope'],self.prm['hiSlope']),
                                    betaStep=self.prm['slopeStep'],
                                    betaSpacing=self.prm['slopeSpacing'],
                                    betaDist=self.prm['slopePrior'],
                                    betaMu=self.prm['slopePriorMu'],
                                    betaSTD=self.prm['slopePriorSTD'],
                                    gamma=gammax,
                                    lambdaLim=(self.prm['loLapse'],self.prm['hiLapse']),
                                    lambdaStep=self.prm['lapseStep'],
                                    lambdaSpacing=self.prm['lapseSpacing'],
                                    lambdaDist=self.prm['lapsePrior'],
                                    lambdaMu=self.prm['lapsePriorMu'],
                                    lambdaSTD=self.prm['lapsePriorSTD'],
                                    marginalize = ax)
            elif self.prm['stimScale'] == "Logarithmic":
                self.PSI = setupPSI(model=self.prm['psyFunType'],
                                    x0=abs(self.prm['adaptiveParam']),
                                    xLim=(abs(self.prm['stimLo']), abs(self.prm['stimHi'])),
                                    xStep=self.prm['stimStep'],
                                    stimScale=self.prm['stimScale'],
                                    alphaLim=(abs(self.prm['loMidPoint']), abs(self.prm['hiMidPoint'])),
                                    alphaStep=self.prm['midPointStep'],
                                    alphaSpacing="Linear",
                                    alphaDist=self.prm['midPointPrior'],
                                    alphaMu=abs(self.prm['midPointPriorMu']),
                                    alphaSTD=self.prm['midPointPriorSTD'],
                                    betaLim=(self.prm['loSlope'],self.prm['hiSlope']),
                                    betaStep=self.prm['slopeStep'],
                                    betaSpacing=self.prm['slopeSpacing'],
                                    betaDist=self.prm['slopePrior'],
                                    betaMu=self.prm['slopePriorMu'],
                                    betaSTD=self.prm['slopePriorSTD'],
                                    gamma=gammax,
                                    lambdaLim=(self.prm['loLapse'],self.prm['hiLapse']),
                                    lambdaStep=self.prm['lapseStep'],
                                    lambdaSpacing=self.prm['lapseSpacing'],
                                    lambdaDist=self.prm['lapsePrior'],
                                    lambdaMu=self.prm['lapsePriorMu'],
                                    lambdaSTD=self.prm['lapsePriorSTD'],
                                    marginalize = ax)
                
            self.prm['startOfBlock'] = False
            self.trialCount = 0
            self.fullFileLines = []
            self.prm['buttonCounter'] = [0 for i in range(self.prm['nAlternatives'])]

        self.prm['buttonCounter'][buttonClicked-1] = self.prm['buttonCounter'][buttonClicked-1] + 1
            
        if buttonClicked == self.correctButton:
            response = 1
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback("correct")
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback("neutral")
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback("off")
        elif buttonClicked != self.correctButton:
            response = 0
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback("incorrect")
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback("neutral")
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback("off")

        self.fullFileSummLines.append([str(self.prm['adaptiveParam']) + self.prm['pref']["general"]["csvSeparator"]])
        self.fullFileLog.write(str(self.prm['adaptiveParam']) + '; ')
        self.fullFileLines.append(str(self.prm['adaptiveParam']) + '; ')
        self.fullFileLog.write(str(response)+'; ')
        self.fullFileLines.append(str(response)+'; ')
        self.fullFileSummLines[len(self.fullFileSummLines)-1].append(str(response) + self.prm['pref']["general"]["csvSeparator"])
        if 'additional_parameters_to_write' in self.prm:
             for p in range(len(self.prm['additional_parameters_to_write'])):
                 self.fullFileLog.write(str(self.prm['additional_parameters_to_write'][p]))
                 self.fullFileLines.append(str(self.prm['additional_parameters_to_write'][p]))
                 self.fullFileSummLines[len(self.fullFileSummLines)-1].append(str(self.prm['additional_parameters_to_write'][p]))
                 self.fullFileLog.write(' ;')
                 self.fullFileLines.append(' ;')
                 self.fullFileSummLines[len(self.fullFileSummLines)-1].append(self.prm['pref']["general"]["csvSeparator"])
        self.fullFileLog.write('\n')
        self.fullFileLines.append('\n')

        self.trialCount = self.trialCount +1

        self.fullFileLog.flush()
        pcDone = (self.trialCount / self.prm['nTrials']) * 100
        bp = int(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'])
        pcThisRep = (bp-1) / self.prm['storedBlocks']*100 + 1 / self.prm['storedBlocks']*pcDone
        pcTot = (self.prm['currentRepetition'] - 1) / self.prm['allBlocks']['repetitions']*100 + 1 / self.prm['allBlocks']['repetitions']*pcThisRep
        self.gauge.setValue(int(pcTot))
        
        if self.trialCount == self.prm['nTrials']:
            
            self.writeResultsHeader('standard')
            self.fullFileLog.write('\n')
            self.fullFileLines.append('\n')
            for i in range(len(self.fullFileLines)):
                self.fullFile.write(self.fullFileLines[i])
            self.resFile.write('\n\n')
            self.resFileLog.write('\n\n')
            self.resFile.write('Midpoint = %5.3f ' %self.PSI['est_midpoint'])
            self.resFileLog.write('Midpoint = %5.3f ' %self.PSI['est_midpoint'])
            self.resFile.write('\n')
            self.resFileLog.write('\n')
            self.resFile.write('Slope = %5.3f ' %self.PSI['est_slope'])
            self.resFileLog.write('Slope = %5.3f ' %self.PSI['est_slope'])
            self.resFile.write('\n')
            self.resFileLog.write('\n')
            self.resFile.write('Lapse = %5.3f ' %self.PSI['est_lapse'])
            self.resFileLog.write('Lapse = %5.3f ' %self.PSI['est_lapse'])
            self.resFile.write('\n\n')
            self.resFileLog.write('\n\n')
  

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

            durString = '{0:5.3f}'.format(self.prm['blockEndTime'] - self.prm['blockStartTime'])
            resLineToWrite = '{0:5.3f}'.format(self.PSI['est_midpoint']) + self.prm['pref']["general"]["csvSeparator"] + \
                             '{0:5.3f}'.format(self.PSI['est_slope']) + self.prm['pref']["general"]["csvSeparator"] + \
                             '{0:5.3f}'.format(self.PSI['est_lapse']) + self.prm['pref']["general"]["csvSeparator"] + \
                             '{0:d}'.format(int(self.prm["nTrials"])) + self.prm['pref']["general"]["csvSeparator"] + \
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
            
            self.writeResultsSummaryLine('PSI', resLineToWrite)

            resLineToWriteSummFull = ""
            for i in range(len(self.fullFileSummLines)):
              resLineToWriteSummFull = resLineToWriteSummFull + " ".join(self.fullFileSummLines[i]) + \
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
             
              resLineToWriteSummFull = self.getCommonTabFields(resLineToWriteSummFull)
              resLineToWriteSummFull = resLineToWriteSummFull + '\n'
            
            
            self.writeResultsSummaryFullLine('PSI', resLineToWriteSummFull)

            del self.PSI #clear memory
            self.atBlockEnd()
        else:
            self.PSI = PSI_update(self.PSI, response)
            if self.prm['stimScale'] == "Logarithmic":
                if self.prm['adaptiveParam'] >=0:
                    self.prm['adaptiveParam'] = self.PSI["xnextLinear"]
                else:
                    self.prm['adaptiveParam'] = -self.PSI["xnextLinear"]
            else:
                self.prm['adaptiveParam'] = self.PSI["xnextLinear"]
            # print("Est. thresh: " + str(self.PSI['est_midpoint']))  
            # print('Next Stim: ' + str(self.prm['adaptiveParam']))
            # print(self.PSI["phi"])
            self.doTrial()

    #PSI Est. Guess Rate
    def sortResponsePSIEstGuessRate(self, buttonClicked):
        currBlock = 'b' + str(self.prm['currentBlock'])
        if self.prm['startOfBlock'] == True:
            self.fullFileLines = []
            self.fullFileSummLines = []
            if self.prm['margThresh'] == "Yes" or self.prm['margSlope'] == "Yes" or self.prm['margGuess'] == "Yes" or self.prm['margLapse'] == "Yes":
                ax = np.array([])
                if self.prm['margThresh'] == "Yes":
                    ax = numpy.append(ax, 0)
                if self.prm['margSlope'] == "Yes":
                    ax = numpy.append(ax, 1)
                if self.prm['margGuess'] == "Yes":
                    ax = numpy.append(ax, 2)
                if self.prm['margLapse'] == "Yes":
                    ax = numpy.append(ax, 3)
                ax = tuple(np.sort(ax))
            else:
                ax = None
                    
            if self.prm['stimScale'] == "Linear":
                self.PSI = setupPSIEstGuessRate(model=self.prm['psyFunType'],
                                                x0=self.prm['adaptiveParam'],
                                                xLim=(self.prm['stimLo'], self.prm['stimHi']),
                                                xStep=self.prm['stimStep'],
                                                stimScale=self.prm['stimScale'],
                                                alphaLim=(self.prm['loMidPoint'], self.prm['hiMidPoint']),
                                                alphaStep=self.prm['midPointStep'],
                                                alphaSpacing="Linear",
                                                alphaDist=self.prm['midPointPrior'],
                                                alphaMu=self.prm['midPointPriorMu'],
                                                alphaSTD=self.prm['midPointPriorSTD'],
                                                betaLim=(self.prm['loSlope'],self.prm['hiSlope']),
                                                betaStep=self.prm['slopeStep'],
                                                betaSpacing=self.prm['slopeSpacing'],
                                                betaDist=self.prm['slopePrior'],
                                                betaMu=self.prm['slopePriorMu'],
                                                betaSTD=self.prm['slopePriorSTD'],
                                                gammaLim=(self.prm['loGuess'], self.prm['hiGuess']),
                                                gammaStep=self.prm['guessStep'],
                                                gammaSpacing=self.prm['guessSpacing'],
                                                gammaDist=self.prm['guessPrior'],
                                                gammaMu=self.prm['guessPriorMu'],
                                                gammaSTD=self.prm['guessPriorSTD'],
                                                lambdaLim=(self.prm['loLapse'],self.prm['hiLapse']),
                                                lambdaStep=self.prm['lapseStep'],
                                                lambdaSpacing=self.prm['lapseSpacing'],
                                                lambdaDist=self.prm['lapsePrior'],
                                                lambdaMu=self.prm['lapsePriorMu'],
                                                lambdaSTD=self.prm['lapsePriorSTD'],
                                                marginalize = ax)
            elif self.prm['stimScale'] == "Logarithmic":
                self.PSI = setupPSIEstGuessRate(model=self.prm['psyFunType'],
                                                x0=abs(self.prm['adaptiveParam']),
                                                xLim=(abs(self.prm['stimLo']), abs(self.prm['stimHi'])),
                                                xStep=self.prm['stimStep'],
                                                stimScale=self.prm['stimScale'],
                                                alphaLim=(abs(self.prm['loMidPoint']), abs(self.prm['hiMidPoint'])),
                                                alphaStep=self.prm['midPointStep'],
                                                alphaSpacing="Linear",
                                                alphaDist=self.prm['midPointPrior'],
                                                alphaMu=abs(self.prm['midPointPriorMu']),
                                                alphaSTD=self.prm['midPointPriorSTD'],
                                                betaLim=(self.prm['loSlope'],self.prm['hiSlope']),
                                                betaStep=self.prm['slopeStep'],
                                                betaSpacing=self.prm['slopeSpacing'],
                                                betaDist=self.prm['slopePrior'],
                                                betaMu=self.prm['slopePriorMu'],
                                                betaSTD=self.prm['slopePriorSTD'],
                                                gammaLim=(self.prm['loGuess'], self.prm['hiGuess']),
                                                gammaStep=self.prm['guessStep'],
                                                gammaSpacing=self.prm['guessSpacing'],
                                                gammaDist=self.prm['guessPrior'],
                                                gammaMu=self.prm['guessPriorMu'],
                                                gammaSTD=self.prm['guessPriorSTD'],
                                                lambdaLim=(self.prm['loLapse'],self.prm['hiLapse']),
                                                lambdaStep=self.prm['lapseStep'],
                                                lambdaSpacing=self.prm['lapseSpacing'],
                                                lambdaDist=self.prm['lapsePrior'],
                                                lambdaMu=self.prm['lapsePriorMu'],
                                                lambdaSTD=self.prm['lapsePriorSTD'],
                                                marginalize = ax)
                
            self.prm['startOfBlock'] = False
            self.trialCount = 0
            self.fullFileLines = []
            self.prm['buttonCounter'] = [0 for i in range(self.prm['nAlternatives'])]

        self.prm['buttonCounter'][buttonClicked-1] = self.prm['buttonCounter'][buttonClicked-1] + 1
            
        if buttonClicked == self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback("correct")
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback("neutral")
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback("off")
        elif buttonClicked != self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback("incorrect")
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback("neutral")
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback("off")

        if buttonClicked == self.prm["YesButton"]:
            response = 1 #here response indicate whether listener said "Yes", or equivalent, not whether the response was correct or not
        else:
            response = 0

        self.fullFileSummLines.append([str(self.prm['adaptiveParam']) + self.prm['pref']["general"]["csvSeparator"]])
        self.fullFileLog.write(str(self.prm['adaptiveParam']) + '; ')
        self.fullFileLines.append(str(self.prm['adaptiveParam']) + '; ')
        self.fullFileLog.write(str(response)+'; ')
        self.fullFileLines.append(str(response)+'; ')
        self.fullFileSummLines[len(self.fullFileSummLines)-1].append(str(response) + self.prm['pref']["general"]["csvSeparator"])
        if 'additional_parameters_to_write' in self.prm:
             for p in range(len(self.prm['additional_parameters_to_write'])):
                 self.fullFileLog.write(str(self.prm['additional_parameters_to_write'][p]))
                 self.fullFileLines.append(str(self.prm['additional_parameters_to_write'][p]))
                 self.fullFileSummLines[len(self.fullFileSummLines)-1].append(str(self.prm['additional_parameters_to_write'][p]))
                 self.fullFileLog.write(' ;')
                 self.fullFileLines.append(' ;')
                 self.fullFileSummLines[len(self.fullFileSummLines)-1].append(self.prm['pref']["general"]["csvSeparator"])
        self.fullFileLog.write('\n')
        self.fullFileLines.append('\n')

        self.trialCount = self.trialCount +1

        self.fullFileLog.flush()
        pcDone = (self.trialCount / self.prm['nTrials']) * 100
        bp = int(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'])
        pcThisRep = (bp-1) / self.prm['storedBlocks']*100 + 1 / self.prm['storedBlocks']*pcDone
        pcTot = (self.prm['currentRepetition'] - 1) / self.prm['allBlocks']['repetitions']*100 + 1 / self.prm['allBlocks']['repetitions']*pcThisRep
        self.gauge.setValue(int(pcTot))
        
        if self.trialCount == self.prm['nTrials']:
            
            self.writeResultsHeader('standard')
            self.fullFileLog.write('\n')
            self.fullFileLines.append('\n')
            for i in range(len(self.fullFileLines)):
                self.fullFile.write(self.fullFileLines[i])
            self.resFile.write('\n\n')
            self.resFileLog.write('\n\n')
            self.resFile.write('Midpoint = %5.3f ' %self.PSI['est_midpoint'])
            self.resFileLog.write('Midpoint = %5.3f ' %self.PSI['est_midpoint'])
            self.resFile.write('\n')
            self.resFileLog.write('\n')
            self.resFile.write('Slope = %5.3f ' %self.PSI['est_slope'])
            self.resFileLog.write('Slope = %5.3f ' %self.PSI['est_slope'])
            self.resFile.write('\n')
            self.resFileLog.write('\n')
            self.resFile.write('Guess = %5.3f ' %self.PSI['est_guess'])
            self.resFileLog.write('Guess = %5.3f ' %self.PSI['est_guess'])
            self.resFile.write('\n')
            self.resFileLog.write('\n')
            self.resFile.write('Lapse = %5.3f ' %self.PSI['est_lapse'])
            self.resFileLog.write('Lapse = %5.3f ' %self.PSI['est_lapse'])
            self.resFile.write('\n\n')
            self.resFileLog.write('\n\n')
  

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

            durString = '{0:5.3f}'.format(self.prm['blockEndTime'] - self.prm['blockStartTime'])
            resLineToWrite = '{0:5.3f}'.format(self.PSI['est_midpoint']) + self.prm['pref']["general"]["csvSeparator"] + \
                             '{0:5.3f}'.format(self.PSI['est_guess']) + self.prm['pref']["general"]["csvSeparator"] + \
                             '{0:5.3f}'.format(self.PSI['est_slope']) + self.prm['pref']["general"]["csvSeparator"] + \
                             '{0:5.3f}'.format(self.PSI['est_lapse']) + self.prm['pref']["general"]["csvSeparator"] + \
                             '{0:d}'.format(int(self.prm["nTrials"])) + self.prm['pref']["general"]["csvSeparator"] + \
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
            
            self.writeResultsSummaryLine('PSI - Est. Guess Rate', resLineToWrite)

            resLineToWriteSummFull = ""
            for i in range(len(self.fullFileSummLines)):
              resLineToWriteSummFull = resLineToWriteSummFull + " ".join(self.fullFileSummLines[i]) + \
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
             
              resLineToWriteSummFull = self.getCommonTabFields(resLineToWriteSummFull)
              resLineToWriteSummFull = resLineToWriteSummFull + '\n'
            
            
            self.writeResultsSummaryFullLine('PSI - Est. Guess Rate', resLineToWriteSummFull)

            del self.PSI #clear memory
            self.atBlockEnd()
        else:
            self.PSI = PSIEstGuessRate_update(self.PSI, response)
            if self.prm['stimScale'] == "Logarithmic":
                if self.prm['adaptiveParam'] >=0:
                    self.prm['adaptiveParam'] = self.PSI["xnextLinear"]
                else:
                    self.prm['adaptiveParam'] = -self.PSI["xnextLinear"]
            else:
                self.prm['adaptiveParam'] = self.PSI["xnextLinear"]
            # print("Est. thresh: " + str(self.PSI['est_midpoint']))  
            # print('Next Stim: ' + str(self.prm['adaptiveParam']))
            # print(self.PSI["phi"])
            self.doTrial()


    def sortResponseUML(self, buttonClicked):
        currBlock = 'b' + str(self.prm['currentBlock'])
        if self.prm['startOfBlock'] == True:
            self.fullFileLines = []
            self.fullFileSummLines = []

            gammax = 1/self.prm[currBlock]['nAlternatives']
            if self.prm['stimScale'] == "Linear":
                self.UML = setupUML(model=self.prm['psyFunType'],
                                    swptRule=self.prm['swptRule'],
                                    nDown=self.prm["numberCorrectNeeded"],
                                    centTend = self.prm["psyFunPosteriorSummary"],
                                    stimScale = self.prm['stimScale'],
                                    x0=self.prm['adaptiveParam'],
                                    xLim=(self.prm['stimLo'], self.prm['stimHi']),
                                    alphaLim=(self.prm['loMidPoint'], self.prm['hiMidPoint']),
                                    alphaStep=self.prm['midPointStep'],
                                    alphaSpacing="Linear",
                                    alphaDist=self.prm['midPointPrior'],
                                    alphaMu=self.prm['midPointPriorMu'],
                                    alphaSTD=self.prm['midPointPriorSTD'],
                                    betaLim=(self.prm['loSlope'], self.prm['hiSlope']),
                                    betaStep=self.prm['slopeStep'],
                                    betaSpacing=self.prm['slopeSpacing'],
                                    betaDist=self.prm['slopePrior'],
                                    betaMu=self.prm['slopePriorMu'],
                                    betaSTD=self.prm['slopePriorSTD'],
                                    gamma=gammax,
                                    lambdaLim=(self.prm['loLapse'], self.prm['hiLapse']),
                                    lambdaStep=self.prm['lapseStep'],
                                    lambdaSpacing=self.prm['lapseSpacing'],
                                    lambdaDist=self.prm['lapsePrior'],
                                    lambdaMu=self.prm['lapsePriorMu'],
                                    lambdaSTD=self.prm['lapsePriorSTD'],
                                    suggestedLambdaSwpt=self.prm['suggestedLambdaSwpt'],
                                    lambdaSwptPC=self.prm['lambdaSwptPC'])
            elif self.prm['stimScale'] == "Logarithmic":
                self.UML = setupUML(model=self.prm['psyFunType'],
                                    swptRule=self.prm['swptRule'],
                                    nDown=self.prm["numberCorrectNeeded"],
                                    centTend = self.prm["psyFunPosteriorSummary"],
                                    stimScale = self.prm['stimScale'],
                                    x0=abs(self.prm['adaptiveParam']),
                                    xLim=(abs(self.prm['stimLo']), abs(self.prm['stimHi'])),
                                    alphaLim=(abs(self.prm['loMidPoint']), abs(self.prm['hiMidPoint'])),
                                    alphaStep=abs(self.prm['midPointStep']),
                                    alphaSpacing="Linear",
                                    alphaDist=self.prm['midPointPrior'],
                                    alphaMu=self.prm['midPointPriorMu'],
                                    alphaSTD=self.prm['midPointPriorSTD'],
                                    betaLim=(self.prm['loSlope'], self.prm['hiSlope']),
                                    betaStep=self.prm['slopeStep'],
                                    betaSpacing=self.prm['slopeSpacing'],
                                    betaDist=self.prm['slopePrior'],
                                    betaMu=self.prm['slopePriorMu'],
                                    betaSTD=self.prm['slopePriorSTD'],
                                    gamma=gammax,
                                    lambdaLim=(self.prm['loLapse'], self.prm['hiLapse']),
                                    lambdaStep=self.prm['lapseStep'],
                                    lambdaSpacing=self.prm['lapseSpacing'],
                                    lambdaDist=self.prm['lapsePrior'],
                                    lambdaMu=self.prm['lapsePriorMu'],
                                    lambdaSTD=self.prm['lapsePriorSTD'],
                                    suggestedLambdaSwpt=abs(self.prm['suggestedLambdaSwpt']),
                                    lambdaSwptPC=self.prm['lambdaSwptPC'])
            
            if self.prm["saveUMLState"] == True:
                try:
                    self.UML["p"] = np.load(os.path.dirname(self.prm['resultsFile'])+self.prm[currBlock]['conditionLabel']+".npy")
                    print("Previous block state loaded")
                except:
                    print("Previous block state could not be loaded")
                    pass
            self.prm['startOfBlock'] = False
            self.trialCount = 0
            self.fullFileLines = []
            self.prm['buttonCounter'] = [0 for i in range(self.prm['nAlternatives'])]

        self.prm['buttonCounter'][buttonClicked-1] = self.prm['buttonCounter'][buttonClicked-1] + 1
            
        if buttonClicked == self.correctButton:
            response = 1
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback("correct")
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback("neutral")
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback("off")
        elif buttonClicked != self.correctButton:
            response = 0
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback("incorrect")
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback("neutral")
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback("off")

        self.fullFileSummLines.append([str(self.prm['adaptiveParam']) + self.prm['pref']["general"]["csvSeparator"]])
        self.fullFileLog.write(str(self.prm['adaptiveParam']) + '; ')
        self.fullFileLines.append(str(self.prm['adaptiveParam']) + '; ')
        self.fullFileLog.write(str(response)+'; ')
        self.fullFileLines.append(str(response)+'; ')
        self.fullFileSummLines[len(self.fullFileSummLines)-1].append(str(response) + self.prm['pref']["general"]["csvSeparator"])
        if 'additional_parameters_to_write' in self.prm:
             for p in range(len(self.prm['additional_parameters_to_write'])):
                 self.fullFileLog.write(str(self.prm['additional_parameters_to_write'][p]))
                 self.fullFileLines.append(str(self.prm['additional_parameters_to_write'][p]))
                 self.fullFileSummLines[len(self.fullFileSummLines)-1].append(str(self.prm['additional_parameters_to_write'][p]))
                 self.fullFileLog.write(' ;')
                 self.fullFileLines.append(' ;')
                 self.fullFileSummLines[len(self.fullFileSummLines)-1].append(self.prm['pref']["general"]["csvSeparator"])
        self.fullFileLog.write('\n')
        self.fullFileLines.append('\n')

        self.trialCount = self.trialCount +1

        self.fullFileLog.flush()
        pcDone = (self.trialCount / self.prm['nTrials']) * 100
        bp = int(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'])
        pcThisRep = (bp-1) / self.prm['storedBlocks']*100 + 1 / self.prm['storedBlocks']*pcDone
        pcTot = (self.prm['currentRepetition'] - 1) / self.prm['allBlocks']['repetitions']*100 + 1 / self.prm['allBlocks']['repetitions']*pcThisRep
        self.gauge.setValue(int(pcTot))
        
        if self.trialCount == self.prm['nTrials']:
            
            self.writeResultsHeader('standard')
            self.fullFileLog.write('\n')
            self.fullFileLines.append('\n')
            for i in range(len(self.fullFileLines)):
                self.fullFile.write(self.fullFileLines[i])
            self.resFile.write('\n\n')
            self.resFileLog.write('\n\n')
            self.resFile.write('Midpoint = %5.3f ' %self.UML['est_midpoint'])
            self.resFileLog.write('Midpoint = %5.3f ' %self.UML['est_midpoint'])
            self.resFile.write('\n')
            self.resFileLog.write('\n')
            self.resFile.write('Slope = %5.3f ' %self.UML['est_slope'])
            self.resFileLog.write('Slope = %5.3f ' %self.UML['est_slope'])
            self.resFile.write('\n')
            self.resFileLog.write('\n')
            self.resFile.write('Lapse = %5.3f ' %self.UML['est_lapse'])
            self.resFileLog.write('Lapse = %5.3f ' %self.UML['est_lapse'])
            self.resFile.write('\n\n')
            self.resFileLog.write('\n\n')
  

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

            durString = '{0:5.3f}'.format(self.prm['blockEndTime'] - self.prm['blockStartTime'])
            resLineToWrite = '{0:5.3f}'.format(self.UML['est_midpoint']) + self.prm['pref']["general"]["csvSeparator"] + \
                             '{0:5.3f}'.format(self.UML['est_slope']) + self.prm['pref']["general"]["csvSeparator"] + \
                             '{0:5.3f}'.format(self.UML['est_lapse']) + self.prm['pref']["general"]["csvSeparator"] + \
                             '{0:d}'.format(int(self.prm["nTrials"])) + self.prm['pref']["general"]["csvSeparator"] + \
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
            
            self.writeResultsSummaryLine('UML', resLineToWrite)

            resLineToWriteSummFull = ""
            for i in range(len(self.fullFileSummLines)):
              resLineToWriteSummFull = resLineToWriteSummFull + " ".join(self.fullFileSummLines[i]) + \
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
             
              resLineToWriteSummFull = self.getCommonTabFields(resLineToWriteSummFull)
              resLineToWriteSummFull = resLineToWriteSummFull + '\n'
            
            
            self.writeResultsSummaryFullLine('UML', resLineToWriteSummFull)
            if self.prm["saveUMLState"] == True:
                # if int("".join(np.__version__.split("."))) >=182:
                #                     np.save(os.path.dirname(self.prm['resultsFile'])+self.prm[currBlock]['conditionLabel']+".npy", self.UML["p"], allow_pickle=False, fix_imports=False)
                # else:
                np.save(os.path.dirname(self.prm['resultsFile'])+self.prm[currBlock]['conditionLabel']+".npy", self.UML["p"])#, allow_pickle=False, fix_imports=False)
            del self.UML #clear memory
            self.atBlockEnd()
        else:
            self.UML = UML_update(self.UML, response)
            if self.prm['stimScale'] == "Logarithmic":
                if self.prm['adaptiveParam'] >=0:
                    self.prm['adaptiveParam'] = self.UML["xnextLinear"]
                else:
                    self.prm['adaptiveParam'] = -self.UML["xnextLinear"]
            else:
                self.prm['adaptiveParam'] = self.UML["xnextLinear"]
            # print("Est. thresh: " + str(self.UML['est_midpoint']))  
            # print('Next Stim: ' + str(self.prm['adaptiveParam']))
            # print(self.UML["phi"])
            self.doTrial()

    def sortResponseUMLEstGuessRate(self, buttonClicked):
        currBlock = 'b' + str(self.prm['currentBlock'])
        if self.prm['startOfBlock'] == True:
            self.fullFileLines = []
            self.fullFileSummLines = []

            if self.prm['stimScale'] == "Linear":
                self.UML = setupUMLEstGuessRate(model=self.prm['psyFunType'],
                                                swptRule=self.prm['swptRule'],
                                                nDown=self.prm["numberCorrectNeeded"],
                                                centTend = self.prm["psyFunPosteriorSummary"],
                                                stimScale = self.prm['stimScale'],
                                                x0=self.prm['adaptiveParam'],
                                                xLim=(self.prm['stimLo'], self.prm['stimHi']),
                                                alphaLim=(self.prm['loMidPoint'], self.prm['hiMidPoint']),
                                                alphaStep=self.prm['midPointStep'],
                                                alphaSpacing="Linear",
                                                alphaDist=self.prm['midPointPrior'],
                                                alphaMu=self.prm['midPointPriorMu'],
                                                alphaSTD=self.prm['midPointPriorSTD'],
                                                betaLim=(self.prm['loSlope'], self.prm['hiSlope']),
                                                betaStep=self.prm['slopeStep'],
                                                betaSpacing=self.prm['slopeSpacing'],
                                                betaDist=self.prm['slopePrior'],
                                                betaMu=self.prm['slopePriorMu'],
                                                betaSTD=self.prm['slopePriorSTD'],
                                                gammaLim=(self.prm['loGuess'], self.prm['hiGuess']),
                                                gammaStep=self.prm['guessStep'],
                                                gammaSpacing=self.prm['guessSpacing'],
                                                gammaDist=self.prm['guessPrior'],
                                                gammaMu=self.prm['guessPriorMu'],
                                                gammaSTD=self.prm['guessPriorSTD'],
                                                lambdaLim=(self.prm['loLapse'], self.prm['hiLapse']),
                                                lambdaStep=self.prm['lapseStep'],
                                                lambdaSpacing=self.prm['lapseSpacing'],
                                                lambdaDist=self.prm['lapsePrior'],
                                                lambdaMu=self.prm['lapsePriorMu'],
                                                lambdaSTD=self.prm['lapsePriorSTD'],
                                                suggestedLambdaSwpt=self.prm['suggestedLambdaSwpt'],
                                                lambdaSwptPC=self.prm['lambdaSwptPC'])
            elif self.prm['stimScale'] == "Logarithmic":
                self.UML = setupUMLEstGuessRate(model=self.prm['psyFunType'],
                                                swptRule=self.prm['swptRule'],
                                                nDown=self.prm["numberCorrectNeeded"],
                                                centTend = self.prm["psyFunPosteriorSummary"],
                                                stimScale = self.prm['stimScale'],
                                                x0=abs(self.prm['adaptiveParam']),
                                                xLim=(abs(self.prm['stimLo']), abs(self.prm['stimHi'])),
                                                alphaLim=(abs(self.prm['loMidPoint']), abs(self.prm['hiMidPoint'])),
                                                alphaStep=abs(self.prm['midPointStep']),
                                                alphaSpacing="Linear",
                                                alphaDist=self.prm['midPointPrior'],
                                                alphaMu=self.prm['midPointPriorMu'],
                                                alphaSTD=self.prm['midPointPriorSTD'],
                                                betaLim=(self.prm['loSlope'], self.prm['hiSlope']),
                                                betaStep=self.prm['slopeStep'],
                                                betaSpacing=self.prm['slopeSpacing'],
                                                betaDist=self.prm['slopePrior'],
                                                betaMu=self.prm['slopePriorMu'],
                                                betaSTD=self.prm['slopePriorSTD'],
                                                gammaLim=(self.prm['loGuess'], self.prm['hiGuess']),
                                                gammaStep=self.prm['guessStep'],
                                                gammaSpacing=self.prm['guessSpacing'],
                                                gammaDist=self.prm['guessPrior'],
                                                gammaMu=self.prm['guessPriorMu'],
                                                gammaSTD=self.prm['guessPriorSTD'],
                                                lambdaLim=(self.prm['loLapse'], self.prm['hiLapse']),
                                                lambdaStep=self.prm['lapseStep'],
                                                lambdaSpacing=self.prm['lapseSpacing'],
                                                lambdaDist=self.prm['lapsePrior'],
                                                lambdaMu=self.prm['lapsePriorMu'],
                                                lambdaSTD=self.prm['lapsePriorSTD'],
                                                suggestedLambdaSwpt=abs(self.prm['suggestedLambdaSwpt']),
                                                lambdaSwptPC=self.prm['lambdaSwptPC'])

            self.prm['startOfBlock'] = False
            self.trialCount = 0
            self.fullFileLines = []
            self.prm['buttonCounter'] = [0 for i in range(self.prm['nAlternatives'])]

        self.prm['buttonCounter'][buttonClicked-1] = self.prm['buttonCounter'][buttonClicked-1] + 1
            
        if buttonClicked == self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback("correct")
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback("neutral")
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback("off")
        elif buttonClicked != self.correctButton:
            response = 0
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback("incorrect")
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback("neutral")
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback("off")

        if buttonClicked == self.prm["YesButton"]:
            response = 1 #here response indicate whether listener said "Yes", or equivalent, not whether the response was correct or not
        else:
            response = 0
            
        self.fullFileSummLines.append([str(self.prm['adaptiveParam']) + self.prm['pref']["general"]["csvSeparator"]])
        self.fullFileLog.write(str(self.prm['adaptiveParam']) + '; ')
        self.fullFileLines.append(str(self.prm['adaptiveParam']) + '; ')
        self.fullFileLog.write(str(response)+'; ')
        self.fullFileLines.append(str(response)+'; ')
        self.fullFileSummLines[len(self.fullFileSummLines)-1].append(str(response) + self.prm['pref']["general"]["csvSeparator"])
        if 'additional_parameters_to_write' in self.prm:
             for p in range(len(self.prm['additional_parameters_to_write'])):
                 self.fullFileLog.write(str(self.prm['additional_parameters_to_write'][p]))
                 self.fullFileLines.append(str(self.prm['additional_parameters_to_write'][p]))
                 self.fullFileSummLines[len(self.fullFileSummLines)-1].append(str(self.prm['additional_parameters_to_write'][p]))
                 self.fullFileLog.write(' ;')
                 self.fullFileLines.append(' ;')
                 self.fullFileSummLines[len(self.fullFileSummLines)-1].append(self.prm['pref']["general"]["csvSeparator"])
        self.fullFileLog.write('\n')
        self.fullFileLines.append('\n')

        self.trialCount = self.trialCount +1

        self.fullFileLog.flush()
        pcDone = (self.trialCount / self.prm['nTrials']) * 100
        bp = int(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'])
        pcThisRep = (bp-1) / self.prm['storedBlocks']*100 + 1 / self.prm['storedBlocks']*pcDone
        pcTot = (self.prm['currentRepetition'] - 1) / self.prm['allBlocks']['repetitions']*100 + 1 / self.prm['allBlocks']['repetitions']*pcThisRep
        self.gauge.setValue(int(pcTot))
        
        if self.trialCount == self.prm['nTrials']:
            
            self.writeResultsHeader('standard')
            self.fullFileLog.write('\n')
            self.fullFileLines.append('\n')
            for i in range(len(self.fullFileLines)):
                self.fullFile.write(self.fullFileLines[i])
            self.resFile.write('\n\n')
            self.resFileLog.write('\n\n')
            self.resFile.write('Midpoint = %5.3f ' %self.UML['est_midpoint'])
            self.resFileLog.write('Midpoint = %5.3f ' %self.UML['est_midpoint'])
            self.resFile.write('\n')
            self.resFileLog.write('\n')
            self.resFile.write('Guess = %5.3f ' %self.UML['est_guess'])
            self.resFileLog.write('Guess = %5.3f ' %self.UML['est_guess'])
            self.resFile.write('\n')
            self.resFileLog.write('\n')
            self.resFile.write('Slope = %5.3f ' %self.UML['est_slope'])
            self.resFileLog.write('Slope = %5.3f ' %self.UML['est_slope'])
            self.resFile.write('\n')
            self.resFileLog.write('\n')
            self.resFile.write('Lapse = %5.3f ' %self.UML['est_lapse'])
            self.resFileLog.write('Lapse = %5.3f ' %self.UML['est_lapse'])
            self.resFile.write('\n\n')
            self.resFileLog.write('\n\n')
  

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

            durString = '{0:5.3f}'.format(self.prm['blockEndTime'] - self.prm['blockStartTime'])
            resLineToWrite = '{0:5.3f}'.format(self.UML['est_midpoint']) + self.prm['pref']["general"]["csvSeparator"] + \
                             '{0:5.3f}'.format(self.UML['est_guess']) + self.prm['pref']["general"]["csvSeparator"] + \
                             '{0:5.3f}'.format(self.UML['est_slope']) + self.prm['pref']["general"]["csvSeparator"] + \
                             '{0:5.3f}'.format(self.UML['est_lapse']) + self.prm['pref']["general"]["csvSeparator"] + \
                             '{0:d}'.format(int(self.prm['nTrials'])) + self.prm['pref']["general"]["csvSeparator"] + \
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
            
            self.writeResultsSummaryLine('UML - Est. Guess Rate', resLineToWrite)

            resLineToWriteSummFull = ""
            for i in range(len(self.fullFileSummLines)):
              resLineToWriteSummFull = resLineToWriteSummFull + " ".join(self.fullFileSummLines[i]) + \
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
             
              resLineToWriteSummFull = self.getCommonTabFields(resLineToWriteSummFull)
              resLineToWriteSummFull = resLineToWriteSummFull + '\n'
            
            
            self.writeResultsSummaryFullLine('UML - Est. Guess Rate', resLineToWriteSummFull)

            del self.UML #clear memory
            self.atBlockEnd()
        else:
            self.UML = UMLEstGuessRate_update(self.UML, response)
            if self.prm['stimScale'] == "Logarithmic":
                if self.prm['adaptiveParam'] >=0:
                    self.prm['adaptiveParam'] = self.UML["xnextLinear"]
                else:
                    self.prm['adaptiveParam'] = -self.UML["xnextLinear"]
            else:
                self.prm['adaptiveParam'] = self.UML["xnextLinear"]
            # print("Est. thresh: " + str(self.UML['est_midpoint']))  
            # print('Next Stim: ' + str(self.prm['adaptiveParam']))
            # print(self.UML["phi"])
            self.doTrial()
            

            
    def sortResponseMultipleConstantsOddOneOut(self, buttonClicked):
        if self.prm['startOfBlock'] == True: #Initialize counts and data structures
            self.prm['startOfBlock'] = False

            self.prm['ones'] = 0
            self.prm['twos'] = 0
            self.prm['threes'] = 0
            self.fullFileLines = []
            self.fullFileSummLines = []
            self.trialCountCnds = {}
            self.correctCountCnds = {}
            for i in range(self.prm['nDifferences']):
                self.trialCountCnds[self.prm['conditions'][i]] = 0
                self.correctCountCnds[self.prm['conditions'][i]] = 0
            self.prm['buttonCounter'] = [0 for i in range(self.prm['nAlternatives'])]
        self.prm['buttonCounter'][buttonClicked-1] = self.prm['buttonCounter'][buttonClicked-1] +1

        self.trialCountCnds[self.currentCondition] = self.trialCountCnds[self.currentCondition] +1

        if buttonClicked == self.correctButton:
            if self.trialCountCnds[self.currentCondition] > self.prm['nPracticeTrials']:
                self.correctCountCnds[self.currentCondition] = self.correctCountCnds[self.currentCondition] +1
            resp = 1
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback("correct")
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback("neutral")
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback("off")
        elif buttonClicked != self.correctButton:
            resp = 0
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback("incorrect")
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback("neutral")
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback("off")


        self.fullFileLog.write(self.currentCondition + '; ' + str(resp) + '; ')
        self.fullFileLines.append(self.currentCondition + '; ' + str(resp) + '; ')
        self.fullFileSummLines.append([self.currentCondition + self.prm['pref']["general"]["csvSeparator"] +
                                       str(resp) + self.prm['pref']["general"]["csvSeparator"]])
        if 'additional_parameters_to_write' in self.prm:
            for p in range(len(self.prm['additional_parameters_to_write'])):
                self.fullFileLog.write(str(self.prm['additional_parameters_to_write'][p]))
                self.fullFileLines.append(str(self.prm['additional_parameters_to_write'][p]))
                self.fullFileSummLines[len(self.fullFileSummLines)-1].append(str(self.prm['additional_parameters_to_write'][p]) + self.prm['pref']["general"]["csvSeparator"])
                self.fullFileLog.write('; ')
                self.fullFileLines.append('; ')
        self.fullFileLog.write('\n')
        self.fullFileLines.append('\n')
        self.fullFileLog.flush()


        cnt = 0
        for j in range(self.prm['nDifferences']):
            cnt = cnt + self.trialCountCnds[self.prm['conditions'][j]]
        pcDone = cnt / ((self.prm['nTrials']+self.prm['nPracticeTrials']) *self.prm['nDifferences']) * 100
        bp = int(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'])
        pcThisRep = (bp-1) / self.prm['storedBlocks']*100 + 1 / self.prm['storedBlocks']*pcDone
        pcTot = (self.prm['currentRepetition'] - 1) / self.prm['allBlocks']['repetitions']*100 + 1 / self.prm['allBlocks']['repetitions']*pcThisRep
        self.gauge.setValue(int(pcTot))

        if self.trialCountCnds[self.currentCondition] == self.prm['nTrials']:
            self.prm['comparisonChoices'].remove(self.currentCondition)
        if len(self.prm['comparisonChoices']) == 0: #Block is completed

            dp_diff = {}; dp_IO = {}
            prCorr = {}
            for cnd in self.prm['conditions']:
                prCorr[cnd] = self.correctCountCnds[cnd] / self.trialCountCnds[cnd]
                try:
                    dp_IO[cnd] = dprime_oddity(prCorr[cnd], meth="IO")
                except:
                    dp_IO[cnd] = nan
                try:
                    dp_diff[cnd] = dprime_oddity(prCorr[cnd], meth="diff")
                except:
                    dp_diff[cnd] = nan
 
                    
            self.writeResultsHeader('standard')
            for i in range(len(self.fullFileLines)):
                self.fullFile.write(self.fullFileLines[i])
            self.fullFileLog.write('\n')
            self.fullFile.write('\n')
            
            for ftyp in [self.resFile, self.resFileLog]:
                for cnd in self.prm['conditions']:
                    ftyp.write('Condition %s\n\n' %(cnd))
                    ftyp.write('No. Correct = %d\n' %(self.correctCountCnds[cnd]))
                    ftyp.write('No. Trials = %d\n' %(self.trialCountCnds[cnd]))
                    ftyp.write('Percent Correct = %5.3f\n' %(prCorr[cnd]*100))
                    ftyp.write('d-prime IO = %5.3f\n' %(dp_IO[cnd]))
                    ftyp.write('d-prime diff = %5.3f\n' %(dp_diff[cnd]))
                    ftyp.write('\n\n')

                for i in range(self.prm['nAlternatives']):
                     ftyp.write("B{0} = {1}".format(i+1, self.prm['buttonCounter'][i]))
                     if i != self.prm['nAlternatives']-1:
                         ftyp.write(', ')
                ftyp.write('\n\n')

                ftyp.flush()
            
            self.fullFile.flush()
            self.fullFileLog.flush()

            self.getEndTime()

            currBlock = 'b' + str(self.prm['currentBlock'])
            durString = '{0:5.3f}'.format(self.prm['blockEndTime'] - self.prm['blockStartTime'])
            
            resLineToWrite = ""#str(self.prm['nTrials']) + self.prm['pref']["general"]["csvSeparator"]
            for cnd in self.prm['conditions']:
                resLineToWrite = resLineToWrite + str(self.correctCountCnds[cnd]) + self.prm['pref']["general"]["csvSeparator"] + \
                                 str(self.trialCountCnds[cnd]) + self.prm['pref']["general"]["csvSeparator"] + \
                                 str(prCorr[cnd]*100) + self.prm['pref']["general"]["csvSeparator"] + \
                                 str(dp_IO[cnd]) + self.prm['pref']["general"]["csvSeparator"] + \
                                 str(dp_diff[cnd]) + self.prm['pref']["general"]["csvSeparator"] 
                                
                                 
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
            self.writeResultsSummaryLine('Multiple Constants Odd One Out', resLineToWrite)

            resLineToWriteSummFull = ""
            for i in range(len(self.fullFileSummLines)):
                resLineToWriteSummFull = resLineToWriteSummFull + " ".join(self.fullFileSummLines[i]) + \
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
             
                resLineToWriteSummFull = self.getCommonTabFields(resLineToWriteSummFull)
                resLineToWriteSummFull = resLineToWriteSummFull + '\n'
                
            self.writeResultsSummaryFullLine('Multiple Constants Odd One Out', resLineToWriteSummFull)

            self.atBlockEnd()
          

        else:
            self.doTrial()

    def sortResponseMultipleConstantsSoundComparison(self, buttonClicked):
        if self.prm['startOfBlock'] == True: #Initialize counts and data structures
            self.prm['startOfBlock'] = False

            self.prm['ones'] = 0
            self.prm['twos'] = 0
            self.prm['threes'] = 0
            self.fullFileLines = []
            self.stimCount = {}
            self.trialCountCnds = {}
            #self.correctCountCnds = {}
            for i in range(self.prm['nDifferences']):
                self.stimCount[self.prm['conditions'][i]] = [0,0,0]
                self.trialCountCnds[self.prm['conditions'][i]] = 0
                #self.correctCountCnds[self.prm['conditions'][i]] = 0
            self.prm['buttonCounter'] = [0 for i in range(self.prm['nAlternatives'])]
        self.prm['buttonCounter'][buttonClicked-1] = self.prm['buttonCounter'][buttonClicked-1] +1

        self.trialCountCnds[self.currentCondition] = self.trialCountCnds[self.currentCondition] +1

     
        if self.prm["responseLight"] == self.tr("Neutral"):
            self.responseLight.giveFeedback("neutral")
        elif self.prm["responseLight"] == self.tr("None"):
            self.responseLight.giveFeedback("off")
      

        if self.trialCountCnds[self.currentCondition] > self.prm['nPracticeTrials']:
            if buttonClicked == 1:
                self.stimCount[self.currentCondition][self.prm['currStimOrder'][0]] = self.stimCount[self.currentCondition][self.prm['currStimOrder'][0]]+1   
            elif buttonClicked == 2:
                self.stimCount[self.currentCondition][self.prm['currStimOrder'][1]] = self.stimCount[self.currentCondition][self.prm['currStimOrder'][1]]+1   
            elif buttonClicked == 3:
                self.stimCount[self.currentCondition][self.prm['currStimOrder'][2]] = self.stimCount[self.currentCondition][self.prm['currStimOrder'][2]]+1   

        resp = str(self.prm['currStimOrder'][buttonClicked-1]+1)
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
        pcDone = cnt / self.prm['nTrials'] *len(self.prm['conditions']) * 100
        bp = int(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'])
        pcThisRep = (bp-1) / self.prm['storedBlocks']*100 + 1 / self.prm['storedBlocks']*pcDone
        pcTot = (self.prm['currentRepetition'] - 1) / self.prm['allBlocks']['repetitions']*100 + 1 / self.prm['allBlocks']['repetitions']*pcThisRep
        self.gauge.setValue(int(pcTot))
        

        if self.trialCountCnds[self.currentCondition] == self.prm['nTrials']:
            self.prm['comparisonChoices'].remove(self.currentCondition)
        if len(self.prm['comparisonChoices']) == 0: #Block is completed
                    
            self.writeResultsHeader('standard')
            for i in range(len(self.fullFileLines)):
                self.fullFile.write(self.fullFileLines[i])
            self.fullFileLog.write('\n')
            self.fullFile.write('\n')
            
            for ftyp in [self.resFile, self.resFileLog]:
                for cnd in self.prm['conditions']:
                    ftyp.write('Condition %s\n\n' %(cnd))
                    ftyp.write('\n')
                    ftyp.write('Stimulus 1 = %d/%d; Percent = %5.2f\n' %(self.stimCount[cnd][0], self.prm['nTrials'], self.stimCount[cnd][0]/self.prm['nTrials']*100))
                    ftyp.write('Stimulus 2 = %d/%d; Percent = %5.2f\n' %(self.stimCount[cnd][1], self.prm['nTrials'], self.stimCount[cnd][1]/self.prm['nTrials']*100))
                    ftyp.write('Stimulus 3 = %d/%d; Percent = %5.2f\n' %(self.stimCount[cnd][2], self.prm['nTrials'], self.stimCount[cnd][2]/self.prm['nTrials']*100))
                    ftyp.write('\n\n')

                for i in range(self.prm['nAlternatives']):
                     ftyp.write("B{0} = {1}".format(i+1, self.prm['buttonCounter'][i]))
                     if i != self.prm['nAlternatives']-1:
                         ftyp.write(', ')
                ftyp.write('\n\n')

                ftyp.flush()
            
            self.fullFile.flush()
            self.fullFileLog.flush()

            self.getEndTime()

            currBlock = 'b' + str(self.prm['currentBlock'])
            durString = '{0:5.3f}'.format(self.prm['blockEndTime'] - self.prm['blockStartTime'])
            
            resLineToWrite = str(self.prm['nTrials']) + self.prm['pref']["general"]["csvSeparator"]
            for cnd in self.prm['conditions']:
                resLineToWrite = resLineToWrite + str(self.stimCount[cnd][0]) + self.prm['pref']["general"]["csvSeparator"] + \
                                 str(self.stimCount[cnd][0]/self.prm['nTrials']*100) + self.prm['pref']["general"]["csvSeparator"] + \
                                 str(self.stimCount[cnd][1]) + self.prm['pref']["general"]["csvSeparator"] + \
                                 str(self.stimCount[cnd][1]/self.prm['nTrials']*100) + self.prm['pref']["general"]["csvSeparator"] + \
                                 str(self.stimCount[cnd][2]) + self.prm['pref']["general"]["csvSeparator"] + \
                                 str(self.stimCount[cnd][2]/self.prm['nTrials']*100) + self.prm['pref']["general"]["csvSeparator"] 
                                 
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
            self.writeResultsSummaryLine('Multiple Constants Sound Comparison', resLineToWrite)

            self.atBlockEnd()
          

        else:
            self.doTrial()

    def sortResponseAdaptiveDigitSpan(self, buttonClicked):
        if self.prm['startOfBlock'] == True:
            self.prm['correct'] = []
            self.prm['sequenceLength'] = []
            self.prm['nTrialsSequence'] = 0
            self.prm['startOfBlock'] = False
            
            self.fullFileLines = []
            self.fullFileSummLines = []

        self.prm['nTrialsSequence'] = self.prm['nTrialsSequence'] +1
        self.prm['sequenceLength'].append(self.prm['adaptiveParam'])
        if buttonClicked == self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback("correct")
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback("neutral")
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback("off")
            
            self.fullFileLog.write(str(self.prm['adaptiveParam']) + '; ')
            self.fullFileLines.append(str(self.prm['adaptiveParam']) + '; ')
            self.fullFileSummLines.append([str(self.prm['adaptiveParam']) + self.prm['pref']["general"]["csvSeparator"]])
            self.fullFileLog.write('1; ')
            self.fullFileLines.append('1; ')
            self.fullFileSummLines[len(self.fullFileSummLines)-1].append('1' + self.prm['pref']["general"]["csvSeparator"])
            if 'additional_parameters_to_write' in self.prm:
                for p in range(len(self.prm['additional_parameters_to_write'])):
                    self.fullFileLog.write(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileLines.append(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileSummLines[len(self.fullFileSummLines)-1].append(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileLog.write(' ;')
                    self.fullFileLines.append(' ;')
                    self.fullFileSummLines[len(self.fullFileSummLines)-1].append(self.prm['pref']["general"]["csvSeparator"])
            self.prm['correct'].append(1)
            #self.prm['adaptiveParam'] = self.prm['adaptiveParam']+1
            #self.runAnotherTrial = True
                
        elif buttonClicked != self.correctButton:
            if self.prm["responseLight"] == self.tr("Feedback"):
                self.responseLight.giveFeedback("incorrect")
            elif self.prm["responseLight"] == self.tr("Neutral"):
                self.responseLight.giveFeedback("neutral")
            elif self.prm["responseLight"] == self.tr("None"):
                self.responseLight.giveFeedback("off")
                
            self.fullFileLog.write(str(self.prm['adaptiveParam']) + '; ')
            self.fullFileLines.append(str(self.prm['adaptiveParam']) + '; ')
            self.fullFileSummLines.append([str(self.prm['adaptiveParam']) + self.prm['pref']["general"]["csvSeparator"]])
            self.fullFileLog.write('0; ')
            self.fullFileLines.append('0; ')
            self.fullFileSummLines[len(self.fullFileSummLines)-1].append('0' + self.prm['pref']["general"]["csvSeparator"])
            if 'additional_parameters_to_write' in self.prm:
                for p in range(len(self.prm['additional_parameters_to_write'])):
                    self.fullFileLog.write(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileLines.append(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileSummLines[len(self.fullFileSummLines)-1].append(str(self.prm['additional_parameters_to_write'][p]))
                    self.fullFileLog.write('; ')
                    self.fullFileLines.append('; ')
                    self.fullFileSummLines[len(self.fullFileSummLines)-1].append(self.prm['pref']["general"]["csvSeparator"])
        
            self.prm['correct'].append(0)
            #if self.prm['correct'][len(self.prm['correct'])-2] == 1: 
            #    self.runAnotherTrial = True
            #elif self.prm['correct'][len(self.prm['correct'])-2] == 0: #got two consecutive incorrect responses
            #    self.runAnotherTrial = False

        self.fullFileLog.write(str(buttonClicked) + '; ')
        self.fullFileLines.append(str(buttonClicked) + '; ')
        self.fullFileLog.write('\n')
        self.fullFileLines.append('\n')
        self.fullFileSummLines[len(self.fullFileSummLines)-1].append(str(buttonClicked))
        self.fullFileSummLines[len(self.fullFileSummLines)-1].append(self.prm['pref']["general"]["csvSeparator"])
        self.fullFileLog.flush()
        # pcDone = (self.prm['nTurnpoints'] / self.prm['totalTurnpoints']) * 100
        # bp = int(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition'])
        # pcThisRep = (bp-1) / self.prm['storedBlocks']*100 + 1 / self.prm['storedBlocks']*pcDone
        # pcTot = (self.prm['currentRepetition'] - 1) / self.prm['allBlocks']['repetitions']*100 + 1 / self.prm['allBlocks']['repetitions']*pcThisRep
        # self.gauge.setValue(int(pcTot))
        #if self.runAnotherTrial == False:
        if self.prm['nTrialsSequence'] == 2:
            if self.prm['correct'][len(self.prm['correct'])-1] == 1 or self.prm['correct'][len(self.prm['correct'])-2] == 1:
                keepGoing = True
                self.prm['adaptiveParam'] = self.prm['adaptiveParam']+1
                self.prm['nTrialsSequence'] = 0
            else:
                keepGoing = False
        else:
            keepGoing = True

        if keepGoing == False:
            self.gauge.setValue(100)
            self.writeResultsHeader('standard')
            self.fullFileLog.write('\n')
            self.fullFileLines.append('\n')
            digitSpan = int(self.prm['adaptiveParam'] -1)
            digitSpanScore = np.sum(np.array(self.prm['correct']))
            for i in range(len(self.fullFileLines)):
                self.fullFile.write(self.fullFileLines[i])
            self.resFile.write("Longest Digit Span = " + str(digitSpan) + '\n')
            self.resFile.write("Digit Span Score= " + str(digitSpanScore) + '\n')

            self.resFile.write('\n\n')
            self.resFile.flush()
            self.resFileLog.write('\n\n')
            self.resFileLog.flush()
            self.getEndTime()

            currBlock = 'b' + str(self.prm['currentBlock'])
            durString = '{0:5.3f}'.format(self.prm['blockEndTime'] - self.prm['blockStartTime'])
            resLineToWrite = str(digitSpan) + self.prm['pref']["general"]["csvSeparator"] + \
                             str(digitSpanScore) + self.prm['pref']["general"]["csvSeparator"] + \
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
            
            self.writeResultsSummaryLine('Digit Span', resLineToWrite)

            resLineToWriteSummFull = ""
            for i in range(len(self.fullFileSummLines)):
              resLineToWriteSummFull = resLineToWriteSummFull + " ".join(self.fullFileSummLines[i]) + \
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
             
              resLineToWriteSummFull = self.getCommonTabFields(resLineToWriteSummFull)
              resLineToWriteSummFull = resLineToWriteSummFull + '\n'
            
            
            self.writeResultsSummaryFullLine('Digit Span', resLineToWriteSummFull)

            self.atBlockEnd()
            
        else:
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

            if self.prm['allBlocks']['responseMode'] in [self.tr("Automatic"), self.tr("Simulated Listener"), self.tr("Psychometric")]:
                self.onClickStatusButton()
                
    def atBlockEnd(self):
        self.writeResultsFooter('log');  self.writeResultsFooter('standard')

        bp = int(self.prm['b'+str(self.prm["currentBlock"])]["blockPosition"])
        cb = (self.prm['currentRepetition']-1)*self.prm["storedBlocks"]+bp
        self.blockGauge.setValue(cb)
        self.blockGauge.setFormat(self.prm['rbTrans'].translate('rb', "Blocks Completed") +  ': ' + str(cb) + '/' + str(self.prm['storedBlocks']*self.prm['allBlocks']['repetitions']))
        
        if self.prm['allBlocks']['sendTriggers'] == True:
            thisSnd = pureTone(440, 0, -200, 80, 10, "Both", self.prm['allBlocks']['sampRate'], 100)
            #playCmd = self.prm['pref']['sound']['playCommand']
            time.sleep(1)
            self.audioManager.playSoundWithTrigger(thisSnd, self.prm['allBlocks']['sampRate'], self.prm['allBlocks']['nBits'], False, 'OFFTrigger.wav', self.prm["pref"]["general"]["OFFTrigger"])
            print("SENDING END TRIGGER", self.prm["pref"]["general"]["OFFTrigger"])

        if self.prm['currentRepetition'] == self.prm['allBlocks']['repetitions'] and int(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition']) + self.prm['pref']['email']['nBlocksNotify'] == self.prm['storedBlocks']:
            cmd = self.parseCustomCommandArguments(self.prm['pref']["general"]["nBlocksCustomCommand"])
            if len(cmd) > 0:
                self.executerThread.executeCommand([cmd])
            if self.prm['pref']['email']['notifyEnd'] == True:
                self.sendEndNotification()
        if int(self.prm['b'+str(self.prm['currentBlock'])]['blockPosition']) < self.prm['storedBlocks']:
            self.parent().onClickNextBlockPositionButton()
            if self.prm['allBlocks']['responseMode'] == self.tr("Automatic") or self.prm['allBlocks']['responseMode'] == self.tr("Simulated Listener") or self.prm['allBlocks']['responseMode'] == self.tr("Psychometric"):
                self.onClickStatusButton()
            else:
                return
        else:
            self.whenFinished()
        self.prm['cmdOutFileHandle'].flush()
        
    def getEndTime(self):
        self.prm['blockEndTime'] = time.time()
        self.prm['blockEndTimeStamp'] = QDateTime.toString(QDateTime.currentDateTime(), self.currLocale.dateTimeFormat(self.currLocale.FormatType.ShortFormat)) 
        self.prm['blockEndDateString'] = QDate.toString(QDate.currentDate(), self.currLocale.dateFormat(self.currLocale.FormatType.ShortFormat)) 
        self.prm['blockEndTimeString'] = QTime.toString(QTime.currentTime(), self.currLocale.timeFormat(self.currLocale.FormatType.ShortFormat)) 
        
    def getStartTime(self):
        self.prm['blockStartTime'] = time.time()
        self.prm['blockStartTimeStamp'] = QDateTime.toString(QDateTime.currentDateTime(), self.currLocale.dateTimeFormat(self.currLocale.FormatType.ShortFormat)) 
        self.prm['blockStartDateString'] = QDate.toString(QDate.currentDate(), self.currLocale.dateFormat(self.currLocale.FormatType.ShortFormat)) 
        self.prm['blockStartTimeString'] = QTime.toString(QTime.currentTime(), self.currLocale.timeFormat(self.currLocale.FormatType.ShortFormat)) 
        

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
            elif self.prm['allBlocks']['responseMode'] == self.tr("Psychometric"):
                thisFile.write('Psychometric Listener Function: ' + str(self.prm[currBlock]['psyListFun']) + '\n')
                thisFile.write('Psychometric Listener Function Fit: ' + str(self.prm[currBlock]['psyListFunFit']) + '\n')
                thisFile.write('Psychometric Listener Midpoint: ' + str(self.prm[currBlock]['psyListMidpoint']) + '\n')
                thisFile.write('Psychometric Listener Slope: ' + str(self.prm[currBlock]['psyListSlope']) + '\n')
                thisFile.write('Psychometric Listener Lapse: ' + str(self.prm[currBlock]['psyListLapse']) + '\n')
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
            thisFile.write('Response Light Type: ' + self.prm['responseLightType'] + '\n')
            thisFile.write('Response Light Duration (ms): ' + self.currLocale.toString(self.prm[currBlock]['responseLightDuration']) + '\n')
            if self.prm[self.parent().currExp]["hasISIBox"] == True:
                thisFile.write('ISI:           ' + self.currLocale.toString(self.prm['isi']) + '\n')
            if self.prm[self.parent().currExp]["hasPreTrialInterval"] == True:
                thisFile.write('Pre-Trial Interval:           ' + self.prm[currBlock]['preTrialInterval'] + '\n')
                if self.prm[currBlock]['preTrialInterval'] == self.tr("Yes"):
                    thisFile.write('Pre-Trial Interval ISI:           ' + self.currLocale.toString(self.prm[currBlock]['preTrialIntervalISI']) + '\n')
            if self.prm[self.parent().currExp]["hasPrecursorInterval"] == True:
                thisFile.write('Precursor Interval:           ' + self.prm[currBlock]['precursorInterval'] + '\n')
                if self.prm[currBlock]['precursorInterval'] == self.tr("Yes"):
                    thisFile.write('Precursor Interval ISI:           ' + self.currLocale.toString(self.prm[currBlock]['precursorIntervalISI']) + '\n')
            if self.prm[self.parent().currExp]["hasPostcursorInterval"] == True:
                thisFile.write('Postcursor Interval:           ' + self.prm[currBlock]['postcursorInterval'] + '\n')
                if self.prm[currBlock]['postcursorInterval'] == self.tr("Yes"):
                    thisFile.write('Postcursor Interval ISI:           ' + self.currLocale.toString(self.prm[currBlock]['postcursorIntervalISI']) + '\n')
            if self.prm[self.parent().currExp]["hasAltReps"] == True:
                thisFile.write('Alternated (AB) Reps.:         ' + self.currLocale.toString(self.prm['altReps']) + '\n')
                thisFile.write('Alternated (AB) Reps. ISI (ms):         ' + self.currLocale.toString(self.prm['altRepsISI']) + '\n')

            thisFile.write('\n')

            for j in range(len(self.prm[currBlock]['chooser'])):
                if j not in self.parent().choosersToHide:
                    thisFile.write(self.parent().chooserLabel[j].text() + ' ' + self.prm[currBlock]['chooser'][j] + '\n')
            for j in range(len(self.prm[currBlock]['fileChooser'])):
                if j not in self.parent().fileChoosersToHide:
                    thisFile.write(self.parent().fileChooserButton[j].text() + ' ' + self.prm[currBlock]['fileChooser'][j] + '\n')
            for j in range(len(self.prm[currBlock]['dirChooser'])):
                if j not in self.parent().dirChoosersToHide:
                    thisFile.write(self.parent().dirChooserButton[j].text() + ' ' + self.prm[currBlock]['dirChooser'][j] + '\n')
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
        if paradigm in ['Transformed Up-Down', 'Transformed Up-Down Limited', 'Weighted Up-Down', 'Weighted Up-Down Limited']:
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
        elif paradigm in ['Transformed Up-Down Hybrid', 'Weighted Up-Down Hybrid']:
            headerToWrite = 'threshold_' +  self.prm['adaptiveType'].lower() + self.prm['pref']["general"]["csvSeparator"] + \
                            'SD' + self.prm['pref']["general"]["csvSeparator"] + \
                            'nCorrAtMaxLev' + self.prm['pref']["general"]["csvSeparator"] + \
                            'nTotAtMaxLev' + self.prm['pref']["general"]["csvSeparator"] + \
                            'percCorrAtMaxLev' + self.prm['pref']["general"]["csvSeparator"] + \
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

        elif paradigm in ['Transformed Up-Down Interleaved', 'Weighted Up-Down Interleaved']:
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
                            'nCorrect_same'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'nTotal_same'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'nCorrect_different'+ self.prm['pref']["general"]["csvSeparator"] + \
                            'nTotal_different'+ self.prm['pref']["general"]["csvSeparator"] + \
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
        elif paradigm in ['Multiple Constants 1-Pair Same/Different']:
            headerToWrite = ''
            for j in range(self.prm['nDifferences']):
                headerToWrite =  headerToWrite + 'dprime_IO_pair' + str(j+1) +  self.prm['pref']["general"]["csvSeparator"] + \
                                'dprime_diff_pair' + str(j+1) + self.prm['pref']["general"]["csvSeparator"] + \
                                'nTotal_pair'+ str(j+1) + self.prm['pref']["general"]["csvSeparator"] + \
                                'nCorrect_same_pair'+ str(j+1) + self.prm['pref']["general"]["csvSeparator"] + \
                                'nTotal_same_pair'+ str(j+1) + self.prm['pref']["general"]["csvSeparator"] + \
                                'nCorrect_different_pair'+ str(j+1) + self.prm['pref']["general"]["csvSeparator"] + \
                                'nTotal_different_pair'+ str(j+1) + self.prm['pref']["general"]["csvSeparator"] 
                                
                
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
        elif paradigm in ['Multiple Constants ABX']:
            headerToWrite = ''
            for j in range(self.prm['nDifferences']):
                headerToWrite =  headerToWrite + 'dprime_IO_pair' + str(j+1) +  self.prm['pref']["general"]["csvSeparator"] + \
                                'dprime_diff_pair' + str(j+1) + self.prm['pref']["general"]["csvSeparator"] + \
                                'nTotal_pair'+ str(j+1) + self.prm['pref']["general"]["csvSeparator"] + \
                                'nCorrect_A_pair'+ str(j+1) + self.prm['pref']["general"]["csvSeparator"] + \
                                'nTotal_A_pair'+ str(j+1) + self.prm['pref']["general"]["csvSeparator"] + \
                                'nCorrect_B_pair'+ str(j+1) + self.prm['pref']["general"]["csvSeparator"] + \
                                'nTotal_B_pair'+ str(j+1) + self.prm['pref']["general"]["csvSeparator"] 
                                
                
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

        elif paradigm in ['PEST']:
            headerToWrite = 'threshold_' +  self.prm['adaptiveType'].lower() + self.prm['pref']["general"]["csvSeparator"] + \
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
        elif paradigm in ['Multiple Constants Odd One Out']:
            headerToWrite = ""#'nTrials' + self.prm['pref']["general"]["csvSeparator"]
            for i in range(len(self.prm['conditions'])):
                headerToWrite = headerToWrite + 'nCorr_subcnd'+str(i+1) + self.prm['pref']["general"]["csvSeparator"] + \
                                'nTrials_subcnd'+str(i+1) + self.prm['pref']["general"]["csvSeparator"] + \
                                'percCorr_subcnd'+str(i+1) + self.prm['pref']["general"]["csvSeparator"] + \
                                'dprime_IO_subcnd'+str(i+1) + self.prm['pref']["general"]["csvSeparator"] +\
                                'dprime_diff_subcnd'+str(i+1) + self.prm['pref']["general"]["csvSeparator"]  
                                
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
        elif paradigm in ['Multiple Constants Sound Comparison']:
            headerToWrite = 'nTrials' + self.prm['pref']["general"]["csvSeparator"]
            for i in range(len(self.prm['conditions'])):
                headerToWrite = headerToWrite + 'stim1_count_subcnd' + str(i+1) + self.prm['pref']["general"]["csvSeparator"] + \
                                'stim1_percent_subcnd' + str(i+1) + self.prm['pref']["general"]["csvSeparator"] + \
                                'stim2_count_subcnd' + str(i+1) + self.prm['pref']["general"]["csvSeparator"] + \
                                'stim2_percent_subcnd' + str(i+1) + self.prm['pref']["general"]["csvSeparator"] + \
                                'stim3_count_subcnd' + str(i+1) + self.prm['pref']["general"]["csvSeparator"] + \
                                'stim3_percent_subcnd' + str(i+1) + self.prm['pref']["general"]["csvSeparator"] 
                                
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
        elif paradigm in ['Maximum Likelihood']:
            headerToWrite = 'threshold' +  self.prm['pref']["general"]["csvSeparator"] + \
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
        elif paradigm in ['PSI', 'UML']:
            headerToWrite = 'threshold' +  self.prm['pref']["general"]["csvSeparator"] + \
                            'slope' +  self.prm['pref']["general"]["csvSeparator"] + \
                            'lapse' +  self.prm['pref']["general"]["csvSeparator"] + \
                            'nTrials' +  self.prm['pref']["general"]["csvSeparator"] + \
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
        elif paradigm in ['PSI - Est. Guess Rate', 'UML - Est. Guess Rate']:
            headerToWrite = 'threshold' +  self.prm['pref']["general"]["csvSeparator"] + \
                            'guess' +  self.prm['pref']["general"]["csvSeparator"] + \
                            'slope' +  self.prm['pref']["general"]["csvSeparator"] + \
                            'lapse' +  self.prm['pref']["general"]["csvSeparator"] + \
                            'nTrials' +  self.prm['pref']["general"]["csvSeparator"] + \
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
        elif paradigm in ['Digit Span']:
            headerToWrite = 'longest_span' + self.prm['pref']["general"]["csvSeparator"] + \
                            'span_score' + self.prm['pref']["general"]["csvSeparator"] + \
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
        for i in range(len(self.prm[currBlock]['dirChooserCheckBox'])):
            if self.prm[currBlock]['dirChooserCheckBox'][i] == True:
                headerToWrite = headerToWrite + self.prm[currBlock]['dirChooserButton'][i] + self.prm['pref']["general"]["csvSeparator"]
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

        if self.prm[self.parent().currExp]["hasAltReps"] == True:
            if self.prm[currBlock]['altRepsCheckBox'] == True:
                headerToWrite = headerToWrite + 'Alternated (AB) Reps.' + self.prm['pref']["general"]["csvSeparator"]
                headerToWrite = headerToWrite + 'Alternated (AB) Reps. ISI (ms)' + self.prm['pref']["general"]["csvSeparator"]
                
        if self.prm[currBlock]['responseLightCheckBox'] == True:
            headerToWrite = headerToWrite + 'Response Light' + self.prm['pref']["general"]["csvSeparator"]
        if self.prm[currBlock]['responseLightTypeCheckBox'] == True:
            headerToWrite = headerToWrite + 'Response Light Type' + self.prm['pref']["general"]["csvSeparator"]
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

    def writeResultsSummaryFullLine(self, paradigm, resultsLine):
        if paradigm in ['Transformed Up-Down', 'Transformed Up-Down Limited', 'Weighted Up-Down', 'Weighted Up-Down Limited', 'PEST', 'Transformed Up-Down Hybrid', 'Weighted Up-Down Hybrid']:
            headerToWrite = 'adaptive_difference' + self.prm['pref']["general"]["csvSeparator"] + \
                            'response' + self.prm['pref']["general"]["csvSeparator"]
            if 'additional_parameters_to_write' in self.prm:
                for p in range(len(self.prm['additional_parameters_to_write_labels'])):
                    headerToWrite = headerToWrite + self.prm['additional_parameters_to_write_labels'][p] +  self.prm['pref']["general"]["csvSeparator"]
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
     
        if paradigm in ['PSI', 'UML', "PSI - Est. Guess Rate", "UML - Est. Guess Rate"]:
            headerToWrite = 'adaptive_difference' + self.prm['pref']["general"]["csvSeparator"] + \
                            'response' + self.prm['pref']["general"]["csvSeparator"]
            if 'additional_parameters_to_write' in self.prm:
                for p in range(len(self.prm['additional_parameters_to_write_labels'])):
                    headerToWrite = headerToWrite + self.prm['additional_parameters_to_write_labels'][p] +  self.prm['pref']["general"]["csvSeparator"]
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

        if paradigm in ['Multiple Constants 1-Pair Same/Different']:
            headerToWrite = 'pair' + self.prm['pref']["general"]["csvSeparator"] + \
                            'stim1' + self.prm['pref']["general"]["csvSeparator"] + \
                            'stim2' + self.prm['pref']["general"]["csvSeparator"] + \
                            'case' + self.prm['pref']["general"]["csvSeparator"] + \
                            'response' + self.prm['pref']["general"]["csvSeparator"]
            if 'additional_parameters_to_write' in self.prm:
                for p in range(len(self.prm['additional_parameters_to_write_labels'])):
                    headerToWrite = headerToWrite + self.prm['additional_parameters_to_write_labels'][p] +  self.prm['pref']["general"]["csvSeparator"]
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

        if paradigm in ['Multiple Constants ABX']:
            headerToWrite = 'pair' + self.prm['pref']["general"]["csvSeparator"] + \
                            'A' + self.prm['pref']["general"]["csvSeparator"] + \
                            'B' + self.prm['pref']["general"]["csvSeparator"] + \
                            'X' + self.prm['pref']["general"]["csvSeparator"] + \
                            'case' + self.prm['pref']["general"]["csvSeparator"] + \
                            'response' + self.prm['pref']["general"]["csvSeparator"]
            if 'additional_parameters_to_write' in self.prm:
                for p in range(len(self.prm['additional_parameters_to_write_labels'])):
                    headerToWrite = headerToWrite + self.prm['additional_parameters_to_write_labels'][p] +  self.prm['pref']["general"]["csvSeparator"]
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
        if paradigm in ['Multiple Constants Odd One Out']:
            headerToWrite = 'subcondition' + self.prm['pref']["general"]["csvSeparator"] + \
                            'response' + self.prm['pref']["general"]["csvSeparator"]
            if 'additional_parameters_to_write' in self.prm:
                for p in range(len(self.prm['additional_parameters_to_write_labels'])):
                    headerToWrite = headerToWrite + self.prm['additional_parameters_to_write_labels'][p] +  self.prm['pref']["general"]["csvSeparator"]
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
        if paradigm in ['Digit Span']:
            headerToWrite = 'sequence_length' + self.prm['pref']["general"]["csvSeparator"] + \
                            'response' + self.prm['pref']["general"]["csvSeparator"]
            if 'additional_parameters_to_write' in self.prm:
                for p in range(len(self.prm['additional_parameters_to_write_labels'])):
                    headerToWrite = headerToWrite + self.prm['additional_parameters_to_write_labels'][p] +  self.prm['pref']["general"]["csvSeparator"]
                headerToWrite = headerToWrite + "response_sequence" +  self.prm['pref']["general"]["csvSeparator"]
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
        for i in range(len(self.prm[currBlock]['dirChooserCheckBox'])):
            if self.prm[currBlock]['dirChooserCheckBox'][i] == True:
                headerToWrite = headerToWrite + self.prm[currBlock]['dirChooserButton'][i] + self.prm['pref']["general"]["csvSeparator"]
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

        if self.prm[self.parent().currExp]["hasAltReps"] == True:
            if self.prm[currBlock]['altRepsCheckBox'] == True:
                headerToWrite = headerToWrite + 'Alternated (AB) Reps.' + self.prm['pref']["general"]["csvSeparator"]
                headerToWrite = headerToWrite + 'Alternated (AB) Reps. ISI (ms)' + self.prm['pref']["general"]["csvSeparator"]
                
        if self.prm[currBlock]['responseLightCheckBox'] == True:
            headerToWrite = headerToWrite + 'Response Light' + self.prm['pref']["general"]["csvSeparator"]
        if self.prm[currBlock]['responseLightTypeCheckBox'] == True:
            headerToWrite = headerToWrite + 'Response Light Type' + self.prm['pref']["general"]["csvSeparator"]
        if self.prm[currBlock]['responseLightDurationCheckBox'] == True:
            headerToWrite = headerToWrite + 'Response Light Duration' + self.prm['pref']["general"]["csvSeparator"]
              
        headerToWrite = headerToWrite + '\n'
        if os.path.exists(self.prm['resultsFile'].split('.txt')[0]+ self.prm['pref']["general"]["resTableFileSuffix"]+self.prm["pref"]["general"]["fullFileSuffix"]+'.csv') == False: #case 1 file does not exist yet
            self.resFileSummaryFull = open(self.prm['resultsFile'].split('.txt')[0]+ self.prm['pref']["general"]["resTableFileSuffix"]+self.prm["pref"]["general"]["fullFileSuffix"]+'.csv', 'w')
            self.resFileSummaryFull.write(headerToWrite)
            self.resFileSummaryFull.write(resultsLine)
            self.resFileSummaryFull.close()
        else:
            self.resFileSummaryFull = open(self.prm['resultsFile'].split('.txt')[0]+ self.prm['pref']["general"]["resTableFileSuffix"]+self.prm["pref"]["general"]["fullFileSuffix"]+'.csv', 'r')
            allLines = self.resFileSummaryFull.readlines()
            self.resFileSummaryFull.close()
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
                    if  allLines[i][0:8] == 'adaptive' or allLines[i][0:4] == 'perc' or allLines[i][0:9] == 'threshold':
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
            self.resFileSummaryFull = open(self.prm['resultsFile'].split('.txt')[0]+ self.prm['pref']["general"]["resTableFileSuffix"]+self.prm["pref"]["general"]["fullFileSuffix"]+'.csv', 'w')
            self.resFileSummaryFull.writelines(allLines)
            self.resFileSummaryFull.close()
            
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

        for i in range(len(self.prm[currBlock]['dirChooserCheckBox'])):
            if self.prm[currBlock]['dirChooserCheckBox'][i] == True:
                resLineToWrite = resLineToWrite + self.prm[currBlock]['dirChooser'][i].split(':')[0] + self.prm['pref']["general"]["csvSeparator"]

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

        if self.prm[self.parent().currExp]["hasAltReps"] == True:
            if self.prm[currBlock]['altRepsCheckBox'] == True:
                resLineToWrite = resLineToWrite + str(self.prm[currBlock]['altReps']) + self.prm['pref']["general"]["csvSeparator"]
                resLineToWrite = resLineToWrite + str(self.prm[currBlock]['altRepsISI']) + self.prm['pref']["general"]["csvSeparator"]
       
        if self.prm[currBlock]['responseLightCheckBox'] == True:
            resLineToWrite = resLineToWrite + self.prm[currBlock]['responseLight'] + self.prm['pref']["general"]["csvSeparator"]
        if self.prm[currBlock]['responseLightTypeCheckBox'] == True:
            resLineToWrite = resLineToWrite + self.prm[currBlock]['responseLightType'] + self.prm['pref']["general"]["csvSeparator"]

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
                       self.pychovariablesSubstitute[self.pychovariables.index("[resFileTrial]")],
                       self.pychovariablesSubstitute[self.pychovariables.index("[resTable]")]] #self.prm['resultsFile'], self.prm['resultsFile'].split('.txt')[0]+self.prm['pref']["general"]["fullFileSuffix"]+'.txt']
        if self.prm["allBlocks"]["procRes"] == True:
            filesToSend.append(self.pychovariablesSubstitute[self.pychovariables.index("[resFileSess]")])#self.prm['resultsFile'].split('.txt')[0] + self.prm['pref']["general"]["resFileSuffix"]+'.txt')
        if self.prm["allBlocks"]["procResTable"] == True:
            filesToSend.append(self.pychovariablesSubstitute[self.pychovariables.index("[resTableSess]")])
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
        if self.prm['paradigm'] in [self.tr("Transformed Up-Down"),
                                    self.tr("Weighted Up-Down"),
                                    self.tr("Transformed Up-Down Limited"),
                                    self.tr("Weighted Up-Down Limited"),
                                    self.tr("PEST")]:
            processResultsAdaptive([resFilePath])
        elif self.prm['paradigm'] in [self.tr("Transformed Up-Down Interleaved"),
                                      self.tr("Weighted Up-Down Interleaved")]:
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
        if self.prm['paradigm'] in [self.tr("Transformed Up-Down"),
                                    self.tr("Weighted Up-Down"),
                                    self.tr("Transformed Up-Down Limited"),
                                    self.tr("Weighted Up-Down Limited"),
                                    self.tr("PEST")]:
            procResTableAdaptive([resFilePath], fout=None, separator=separator)
        elif self.prm['paradigm'] in [self.tr("Transformed Up-Down Interleaved"),
                                      self.tr("Weighted Up-Down Interleaved")]:
            procResTableAdaptiveInterleaved([resFilePath], fout=None, separator=separator)
        elif self.prm['paradigm'] in [self.tr("Constant 1-Interval 2-Alternatives")]:
            procResTableConstant1Int2Alt([resFilePath], fout=None, separator=separator, dprimeCorrection=self.prm['pref']['general']['dprimeCorrection'])
        elif self.prm['paradigm'] in [self.tr("Multiple Constants 1-Interval 2-Alternatives")]:
            procResTableMultipleConstants1Int2Alt([resFilePath], fout=None, separator=separator, dprimeCorrection=self.prm['pref']['general']['dprimeCorrection'])
        elif self.prm['paradigm'] in [self.tr("Constant m-Intervals n-Alternatives")]:
            procResTableConstantMIntNAlt([resFilePath], fout=None, separator=separator)
        elif self.prm['paradigm'] in [self.tr("Multiple Constants m-Intervals n-Alternatives")]:
            procResTableMultipleConstantsMIntNAlt([resFilePath], fout=None, separator=separator)
        elif self.prm['paradigm'] in [self.tr("Constant 1-Pair Same/Different")]:
            procResTableConstant1PairSameDifferent([resFilePath], fout=None, separator=separator, dprimeCorrection=self.prm['pref']['general']['dprimeCorrection'])
        elif self.prm['paradigm'] in [self.tr("Multiple Constants 1-Pair Same/Different")]:
            procResTableMultipleConstants1PairSameDifferent([resFilePath], fout=None, separator=separator, dprimeCorrection=self.prm['pref']['general']['dprimeCorrection'])
        elif self.prm['paradigm'] in [self.tr("Multiple Constants ABX")]:
            procResTableMultipleConstantsABX([resFilePath], fout=None, separator=separator, dprimeCorrection=self.prm['pref']['general']['dprimeCorrection'])
        elif self.prm['paradigm'] in [self.tr("Multiple Constants Odd One Out")]:
            procResTableMultipleConstantsOddOneOut([resFilePath], fout=None, separator=separator)


    def plotDataEnd(self, winPlot, pdfPlot):
        if self.prm['appData']['plotting_available']: 
            resFilePath = self.pychovariablesSubstitute[self.pychovariables.index("[resTable]")]
            summaryResFilePath = resFilePath.split('.csv')[0] + self.prm["pref"]["general"]["sessSummResFileSuffix"] + '.csv'
            separator = self.parent().prm['pref']["general"]["csvSeparator"]

            resProcTableAvailable = True

            if self.prm['paradigm'] in [self.tr("Transformed Up-Down"),
                                        self.tr("Weighted Up-Down"),
                                        self.tr("Transformed Up-Down Limited"),
                                        self.tr("Weighted Up-Down Limited"),
                                        self.tr("PEST")]:
                paradigm = 'adaptive'
            elif self.prm['paradigm'] in [self.tr("Transformed Up-Down Interleaved"),
                                          self.tr("Weighted Up-Down Interleaved")]:
                paradigm = 'adaptive_interleaved'
            elif self.prm['paradigm'] in [self.tr("Constant 1-Interval 2-Alternatives")]:
                paradigm = 'constant1Interval2Alternatives'
            elif self.prm['paradigm'] in [self.tr("Constant m-Intervals n-Alternatives")]:
                paradigm = 'constantMIntervalsNAlternatives'
            elif self.prm['paradigm'] in [self.tr("Multiple Constants 1-Interval 2-Alternatives")]:
                paradigm = 'multipleConstants1Interval2Alternatives'
            elif self.prm['paradigm'] in [self.tr("Constant m-Intervals n-Alternatives")]:
                paradigm ='constantMIntervalsNAlternatives'
            elif self.prm['paradigm'] in [self.tr("Multiple Constants m-Intervals n-Alternatives")]:
                paradigm = 'multipleConstantsMIntervalsNAlternatives'
            elif self.prm['paradigm'] in [self.tr("Constant 1-Pair Same/Different")]:
                paradigm = 'constant1PairSD'
            elif self.prm['paradigm'] in [self.tr("Multiple Constants 1-Pair Same/Different")]:
                paradigm = 'multipleConstants1PairSD'
            elif self.prm['paradigm'] in [self.tr("Multiple Constants ABX")]:
                paradigm = 'multipleConstantsABX'
           
            if self.prm['paradigm'] in ["UML", "PSI"]:
                resProcTableAvailable = False

            if resProcTableAvailable == True:
                categoricalPlot(self, 'average', summaryResFilePath, winPlot, pdfPlot, paradigm, separator, None, self.prm)

                
    def parseCustomCommandArguments(self, cmd):
        for vr in self.pychovariables:
            cmd = str.replace(cmd, vr, self.pychovariablesSubstitute[self.pychovariables.index(vr)])
            
        return cmd
                
    def playEndMessage(self):
        idx = get_list_indices(self.prm['pref']['general']['endMessageFilesUse'], "\u2713")
        idChosen = random.choice(idx)
        msgSnd, fs = self.audioManager.loadWavFile(self.prm['pref']['general']['endMessageFiles'][idChosen], self.prm['pref']['general']['endMessageLevels'][idChosen], self.prm['allBlocks']['maxLevel'], 'Both')
        self.playThread.playThreadedSound(msgSnd, fs, self.prm['allBlocks']['nBits'], self.prm['pref']['sound']['playCommand'], False, 'foo.wav')

          
class responseLight(QWidget):
    def __init__(self, parent):
        super(responseLight, self).__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding,
                                       QSizePolicy.Policy.Expanding))
        self.correctLightColor = QColor(*self.parent().parent().prm["pref"]["resp_box"]["correctLightColor"])
        self.incorrectLightColor = QColor(*self.parent().parent().prm["pref"]["resp_box"]["incorrectLightColor"])
        self.neutralLightColor = QColor(*self.parent().parent().prm["pref"]["resp_box"]["neutralLightColor"])
        self.offLightColor = QColor(*self.parent().parent().prm["pref"]["resp_box"]["offLightColor"])
        
        self.borderColor = Qt.GlobalColor.black
        self.lightColor = self.offLightColor#Qt.black
        self.feedbackText = ""
        self.responseLightType = self.tr("Light") #this is just for inizialization purposes
        self.rb = self.parent() #response box
        self.cw = self.parent().parent() #control window

        # self.correctSmiley = QIcon.fromTheme("face-smile", QIcon(":/face-smile"))
        # self.incorrectSmiley = QIcon.fromTheme("face-sad", QIcon(":/face-sad"))
        # self.neutralSmiley = QIcon.fromTheme("face-plain", QIcon(":/face-plain"))
        self.correctSmiley = QIcon(":/face-smile")
        self.incorrectSmiley = QIcon(":/face-sad")
        self.neutralSmiley = QIcon(":/face-plain")
        self.offSmiley = QIcon() #create just a null icon
        self.feedbackSmiley = self.offSmiley
    def giveFeedback(self, feedback):
        currBlock = 'b'+ str(self.parent().parent().prm['currentBlock'])
        self.responseLightType = self.parent().parent().prm[currBlock]['responseLightType']
        self.setStatus(feedback)
        self.parent().repaint()
        QApplication.processEvents()
        time.sleep(self.parent().parent().prm[currBlock]['responseLightDuration']/1000)
        self.setStatus('off')
        self.parent().repaint()
        QApplication.processEvents()
        
    def setStatus(self, status):
        self.correctLightColor = QColor(*self.cw.prm["pref"]["resp_box"]["correctLightColor"])
        self.incorrectLightColor = QColor(*self.cw.prm["pref"]["resp_box"]["incorrectLightColor"])
        self.neutralLightColor = QColor(*self.cw.prm["pref"]["resp_box"]["neutralLightColor"])
        self.offLightColor = QColor(*self.cw.prm["pref"]["resp_box"]["offLightColor"])
        if self.responseLightType in [self.tr("Light"), self.tr("Light & Text"), self.tr("Light & Smiley"), self.tr("Light & Text & Smiley")]:
            if status == 'correct':
                self.lightColor = self.correctLightColor#Qt.green
            elif status == 'incorrect':
                self.lightColor = self.incorrectLightColor #Qt.red
            elif status == 'neutral':
                self.lightColor = self.neutralLightColor #Qt.white
            elif status == 'off':
                self.lightColor = self.offLightColor #Qt.black
        if self.responseLightType in [self.tr("Text"), self.tr("Light & Text"), self.tr("Text & Smiley"), self.tr("Light & Text & Smiley")]:
            if status == 'correct':
                if self.cw.prm["pref"]["resp_box"]["correctTextFeedbackUserSet"] == True:
                    self.feedbackText = self.cw.prm["pref"]["resp_box"]["userSetCorrectTextFeedback"]
                else:
                    self.feedbackText = self.cw.prm['rbTrans'].translate('rb', self.cw.prm["pref"]["resp_box"]["correctTextFeedback"])
                self.penColor = QColor(*self.cw.prm["pref"]["resp_box"]["correctTextColor"])
            elif status == 'incorrect':
                if self.cw.prm["pref"]["resp_box"]["incorrectTextFeedbackUserSet"] == True:
                    self.feedbackText = self.cw.prm["pref"]["resp_box"]["userSetIncorrectTextFeedback"]
                else:
                    self.feedbackText = self.cw.prm['rbTrans'].translate('rb', self.cw.prm["pref"]["resp_box"]["incorrectTextFeedback"])
                self.penColor = QColor(*self.cw.prm["pref"]["resp_box"]["incorrectTextColor"])
            elif status == 'neutral':
                if self.cw.prm["pref"]["resp_box"]["neutralTextFeedbackUserSet"] == True:
                    self.feedbackText = self.cw.prm["pref"]["resp_box"]["userSetNeutralTextFeedback"]
                else:
                    self.feedbackText = self.cw.prm['rbTrans'].translate('rb', self.cw.prm["pref"]["resp_box"]["neutralTextFeedback"])
                self.penColor = QColor(*self.cw.prm["pref"]["resp_box"]["neutralTextColor"])
            elif status == 'off':
                if self.cw.prm["pref"]["resp_box"]["offTextFeedbackUserSet"] == True:
                    self.feedbackText = self.cw.prm["pref"]["resp_box"]["userSetOffTextFeedback"]
                else:
                    self.feedbackText = self.cw.prm['rbTrans'].translate('rb', self.cw.prm["pref"]["resp_box"]["offTextFeedback"])
                self.penColor = QColor(*self.cw.prm["pref"]["resp_box"]["offTextColor"])
        if self.responseLightType in [self.tr("Smiley"), self.tr("Light & Smiley"), self.tr("Text & Smiley"), self.tr("Light & Text & Smiley")]:
            if status == 'correct':
                self.feedbackSmiley = self.correctSmiley
            elif status == 'incorrect':
                self.feedbackSmiley = self.incorrectSmiley
            elif status == 'neutral':
                self.feedbackSmiley = self.neutralSmiley
            elif status == 'off':
                self.feedbackSmiley = self.offSmiley

    def paintEvent(self, event=None):
        if self.responseLightType == self.tr("Light"):
            painter = QPainter(self)
            painter.setViewport(0,0,self.width(),self.height())
            painter.setPen(self.borderColor)
            painter.setBrush(self.lightColor)
            painter.drawRect(int(self.width()/60), int(self.height()/60), self.width()-int(self.width()/30), self.height())
        elif self.responseLightType == self.tr("Text"):
            painter = QPainter(self)
            painter.setViewport(0,0,self.width(),self.height())
            painter.setBrush(self.offLightColor)
            painter.drawRect(int(self.width()/60), int(self.height()/60), self.width()-int(self.width()/30), self.height())
            r = QtCore.QRectF(0,0,self.width(),self.height())
            painter.setPen(self.penColor)
            qfont = QFont()
            qfont.fromString(self.cw.prm["pref"]["resp_box"]["responseLightFont"])
            painter.setFont(qfont)
            painter.drawText(r, Qt.AlignmentFlag.AlignCenter, self.feedbackText)
        elif self.responseLightType == self.tr("Smiley"):
            painter = QPainter(self)
            painter.setViewport(0,0,self.width(),self.height())
            painter.setBrush(self.offLightColor)
            rect = painter.drawRect(int(self.width()/60), int(self.height()/60), self.width()-int(self.width()/30), self.height())
            rect = QRect(int(self.width()/60), int(self.height()/60), int(self.width()-self.width()/30), self.height())
            self.feedbackSmiley.paint(painter, rect, Qt.AlignmentFlag.AlignCenter)
        elif self.responseLightType == self.tr("Light & Text"):
            painter = QPainter(self)
            painter.setViewport(0,0,self.width(),self.height())
            painter.setPen(self.borderColor)
            painter.setBrush(self.lightColor)
            painter.drawRect(int(self.width()/60), int(self.height()/60), self.width()-int(self.width()/30), self.height())
            r = QtCore.QRectF(0,0,self.width(),self.height())
            painter.setPen(self.penColor)
            qfont = QFont()
            qfont.fromString(self.cw.prm["pref"]["resp_box"]["responseLightFont"])
            painter.setFont(qfont)
            painter.drawText(r, Qt.AlignmentFlag.AlignCenter, self.feedbackText)
        elif self.responseLightType == self.tr("Light & Smiley"):
            painter = QPainter(self)
            painter.setViewport(0,0,self.width(),self.height())
            painter.setBrush(self.lightColor)
            rect = painter.drawRect(int(self.width()/60), int(self.height()/60), self.width()-int(self.width()/30), self.height())
            rect = QRect(int(self.width()/60), int(self.height()/60), int(self.width()-self.width()/30), self.height())
            self.feedbackSmiley.paint(painter, rect, Qt.AlignmentFlag.AlignCenter)
        elif self.responseLightType == self.tr("Text & Smiley"):
            painter = QPainter(self)
            painter.setViewport(0,0,self.width(),self.height())
            painter.setBrush(self.offLightColor)
            rect = painter.drawRect(int(self.width()/60), int(self.height()/60), self.width()-int(self.width()/30), self.height())
            rectRight = QRect(int(self.width()/60), int(self.height()/60), self.width()+int(self.width()/2), self.height())
            self.feedbackSmiley.paint(painter, rectRight, Qt.AlignmentFlag.AlignCenter)
            rectLeft = QRect(int(self.width()/60), int(self.height()/60), self.width()-int(self.width()/2), self.height())
            self.feedbackSmiley.paint(painter, rectLeft, Qt.AlignmentFlag.AlignCenter)
            r = QtCore.QRectF(0,0,self.width(), self.height())
            painter.setPen(self.penColor)
            qfont = QFont()
            qfont.fromString(self.cw.prm["pref"]["resp_box"]["responseLightFont"])
            painter.setFont(qfont)
            painter.drawText(r, Qt.AlignmentFlag.AlignCenter, self.feedbackText)
        elif self.responseLightType == self.tr("Light & Text & Smiley"):
            painter = QPainter(self)
            painter.setViewport(0,0,self.width(),self.height())
            painter.setBrush(self.lightColor)
            rect = painter.drawRect(int(self.width()/60), int(self.height()/60), self.width()-int(self.width()/30), self.height())
            rectRight = QRect(int(self.width()/60), int(self.height()/60), self.width()+int(self.width()/2), self.height())
            self.feedbackSmiley.paint(painter, rectRight, Qt.AlignmentFlag.AlignCenter)
            rectLeft = QRect(int(self.width()/60), int(self.height()/60), self.width()-int(self.width()/2), self.height())
            self.feedbackSmiley.paint(painter, rectLeft, Qt.AlignmentFlag.AlignCenter)
            r = QtCore.QRectF(0, 0, self.width(), self.height())
            painter.setPen(self.penColor)
            qfont = QFont()
            qfont.fromString(self.cw.prm["pref"]["resp_box"]["responseLightFont"])
            painter.setFont(qfont)
            painter.drawText(r, Qt.AlignmentFlag.AlignCenter, self.feedbackText)

class intervalLight(QFrame):

    def __init__(self, parent):
        QFrame.__init__(self, parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.borderColor = Qt.GlobalColor.red
        self.lightColor = Qt.GlobalColor.black
    def setStatus(self, status):
        if status == 'on':
            self.lightColor = Qt.GlobalColor.white
        elif status == 'off':
            self.lightColor = Qt.GlobalColor.black
        self.parent().repaint()
        QApplication.processEvents()
    def paintEvent(self, event=None):
        painter = QPainter(self)
        painter.setViewport(0, 0, self.width(),self.height())
        painter.setPen(self.borderColor)
        painter.setBrush(self.lightColor)
        painter.fillRect(int(self.width()/60), int(self.height()/60), self.width()-int(self.width()/30), self.height(), self.lightColor)


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


# class ValidDigitSequence(QValidator):
#     def __init__(self, parent):
#         QValidator.__init__(self, parent)

#     def validate(self, s, pos):
        
#         self.regexp = QRegExp("[0-9]+")
#         if s == "":
#             return (QValidator.Intermediate, s, pos)
#         elif not self.regexp.exactMatch(s):
#             return (QValidator.Invalid, s, pos)
#         else:
#             return (QValidator.Acceptable, s, pos)
