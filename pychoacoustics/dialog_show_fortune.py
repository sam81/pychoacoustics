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
    from PyQt5.QtWidgets import QDialog, QPushButton, QSizePolicy, QTextBrowser, QVBoxLayout
    from PyQt5.QtGui import QFont
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtCore import QLocale
    from PyQt6.QtWidgets import QDialog, QPushButton, QSizePolicy, QTextBrowser, QVBoxLayout
    from PyQt6.QtGui import QFont
    
import random

class showFortuneDialog(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.prm = self.parent().prm
        self.currLocale = self.parent().prm['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.NumberOption.OmitGroupSeparator | self.currLocale.NumberOption.RejectGroupSeparator)
       
        self.vBoxSizer = QVBoxLayout()
        self.hBoxSizer = QVBoxLayout()
        self.browser = QTextBrowser()
        self.browser.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.anotherFortuneButton = QPushButton(self.tr("One More!"), self)
        self.anotherFortuneButton.clicked.connect(self.onClickAnotherFortuneButton)
        self.hBoxSizer.addWidget(self.anotherFortuneButton)

        idx = random.choice(range(len(self.prm['appData']['fortunesList'])))

        self.browser.append(self.prm['appData']['fortunesList'][idx]['quote'])
        self.browser.append('\n')
        self.browser.append(self.prm['appData']['fortunesList'][idx]['author'])
        self.browser.append("In:" + self.prm['appData']['fortunesList'][idx]['source'])

        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.browser.setFont(font)
        
        self.vBoxSizer.addWidget(self.browser)
        self.vBoxSizer.addLayout(self.hBoxSizer)
        #self.vBoxSizer.setSizeConstraint(QLayout.SetFixedSize)
        
        self.setLayout(self.vBoxSizer)
        self.setWindowTitle(self.tr("pychoacoustics - fortunes"))
        self.resize(450, 450)
        self.show()
    def onClickAnotherFortuneButton(self):
        self.browser.clear()
        idx = random.choice(range(len(self.prm['appData']['fortunesList'])))

        self.browser.append(self.prm['appData']['fortunesList'][idx]['quote'])
        self.browser.append('\n')
        self.browser.append(self.prm['appData']['fortunesList'][idx]['author'])
        self.browser.append("In:" + self.prm['appData']['fortunesList'][idx]['source'])
       
