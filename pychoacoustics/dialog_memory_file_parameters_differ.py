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
    from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem, QTextBrowser, QVBoxLayout
    from PyQt5.QtGui import QFont
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtCore import QLocale
    from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem, QTextBrowser, QVBoxLayout
    from PyQt6.QtGui import QFont
import random

from .dialog_show_par_diff import*

class dialogMemoryFileParametersDiffer(QDialog):
    def __init__(self, parent, text, diffText):
        QDialog.__init__(self, parent)
        self.prm = self.parent().prm
        self.currLocale = self.parent().prm['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.NumberOption.OmitGroupSeparator | self.currLocale.NumberOption.RejectGroupSeparator)
        self.diffText = diffText
        self.vBoxSizer = QVBoxLayout()
        self.hBoxSizer = QHBoxLayout()
        self.textTF = QLabel(text)
        self.vBoxSizer.addWidget(self.textTF)

        self.yesButt = QPushButton(self.tr("Yes"), self)
        self.noButt = QPushButton(self.tr("No"), self)
        self.showDiffButt = QPushButton(self.tr("Show Differences"), self)
        self.cancelButt = QPushButton(self.tr("Cancel"), self)
        self.hBoxSizer.addItem(QSpacerItem(10,10, QSizePolicy.Expanding))
        self.hBoxSizer.addWidget(self.yesButt)
        self.hBoxSizer.addWidget(self.noButt)
        self.hBoxSizer.addWidget(self.showDiffButt)
        self.hBoxSizer.addWidget(self.cancelButt)
        self.vBoxSizer.addLayout(self.hBoxSizer)
        self.showDiffButt.clicked.connect(self.onClickShowDiffButt)
        self.cancelButt.clicked.connect(self.onClickCancelButt)
        self.yesButt.clicked.connect(self.accept)
        self.noButt.clicked.connect(self.reject)
        
        self.setLayout(self.vBoxSizer)
        self.setWindowTitle(self.tr("Warning"))
        self.show()
  
    def onClickShowDiffButt(self):
        dia = dialogShowParDiff(self, self.diffText)

    def onClickCancelButt(self):
        self.parent().exitFlag = False
        self.accept()
