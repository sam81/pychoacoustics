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
from PyQt4.QtCore import QLocale
import random

class showFortuneDialog(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.prm = self.parent().prm
        self.currLocale = self.parent().prm['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.OmitGroupSeparator | self.currLocale.RejectGroupSeparator)
        #self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
       
        self.vBoxSizer = QtGui.QVBoxLayout()
        self.hBoxSizer = QtGui.QVBoxLayout()
        self.browser = QtGui.QTextBrowser()
        self.browser.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.anotherFortuneButton = QtGui.QPushButton(self.tr("One More!"), self)
        #QtCore.QObject.connect(self.anotherFortuneButton,
        #                       QtCore.SIGNAL('clicked()'), self.onClickAnotherFortuneButton)
        self.anotherFortuneButton.clicked.connect(self.onClickAnotherFortuneButton)
        self.hBoxSizer.addWidget(self.anotherFortuneButton)

        idx = random.choice(range(len(self.prm['appData']['fortunesList'])))

        self.browser.append(self.prm['appData']['fortunesList'][idx]['quote'])
        self.browser.append('\n')
        self.browser.append(self.prm['appData']['fortunesList'][idx]['author'])
        self.browser.append("In:" + self.prm['appData']['fortunesList'][idx]['source'])

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.browser.setFont(font)
        
        self.vBoxSizer.addWidget(self.browser)
        self.vBoxSizer.addLayout(self.hBoxSizer)
        #self.vBoxSizer.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        
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
       
