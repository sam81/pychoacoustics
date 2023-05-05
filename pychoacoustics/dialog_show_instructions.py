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
    from PyQt5.QtCore import QLocale
    from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QPushButton, QSizePolicy, QTextBrowser, QVBoxLayout
    from PyQt5.QtGui import QFont
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtCore import QLocale
    from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QPushButton, QSizePolicy, QTextBrowser, QVBoxLayout
    from PyQt6.QtGui import QFont
import random

class showInstructionsDialog(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.prm = self.parent().prm
        self.currLocale = self.parent().prm['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.NumberOption.OmitGroupSeparator | self.currLocale.NumberOption.RejectGroupSeparator)
        #self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
       
        self.vBoxSizer = QVBoxLayout()
        self.hBoxSizer = QVBoxLayout()
        self.browser = QTextBrowser()
        self.browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.setMinimumHeight(80)
        self.buttonBox.buttons()[0].setMinimumHeight(80)
        self.hBoxSizer.addWidget(self.buttonBox)
        cw = self.parent().parent()
        if cw.prm["storedBlocks"] > 0:
            storedInstr = cw.prm['b'+ str(cw.prm['currentBlock'])]['instructions']
            if len(storedInstr) > 0:
                self.browser.append(storedInstr)
            else:
                self.browser.append(self.tr("Sorry, there are no instructions for this task."))
        else:
            storedInstr = self.parent().parent().instructionsTF.toPlainText()
            if len(storedInstr) > 0:
                self.browser.append(storedInstr)
            else:
                self.browser.append(self.tr("Sorry, there are no instructions for this task."))
        self.browser.append("\n\nPress the ESC key to exit this screen.")

        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(22)
        self.browser.setFont(font)
        
        self.vBoxSizer.addWidget(self.browser)
        self.vBoxSizer.addLayout(self.hBoxSizer)
        #self.vBoxSizer.setSizeConstraint(QLayout.SetFixedSize)
        
        self.setLayout(self.vBoxSizer)
        self.setWindowTitle(self.tr("Task Instructions"))
        #self.resize(900, 600)
        self.showFullScreen()
        #self.show()

       
