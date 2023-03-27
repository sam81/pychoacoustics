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

from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, unicode_literals
from .pyqtver import*
if pyqtversion == 4:
    from PyQt4 import QtGui, QtCore
    from PyQt4.QtCore import QLocale
    from PyQt4.QtGui import QDialog, QDesktopWidget, QDialogButtonBox, QFont, QPushButton, QSizePolicy, QTextBrowser, QVBoxLayout
elif pyqtversion == -4:
    from PySide import QtGui, QtCore
    from PySide.QtCore import QLocale
    from PySide.QtGui import QDialog, QDesktopWidget, QDialogButtonBox, QFont, QPushButton, QSizePolicy, QTextBrowser, QVBoxLayout
elif pyqtversion == 5:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtCore import QLocale
    from PyQt5.QtWidgets import QDialog, QDesktopWidget, QDialogButtonBox, QPushButton, QSizePolicy, QTextBrowser, QVBoxLayout
    from PyQt5.QtGui import QFont
import random

class showExpDocDialog(QDialog):
    def __init__(self, parent, docText, expName):
        QDialog.__init__(self, parent)
        self.prm = self.parent().prm
        self.currLocale = self.parent().prm['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.OmitGroupSeparator | self.currLocale.RejectGroupSeparator)
       
        self.vBoxSizer = QVBoxLayout()
        self.browser = QTextBrowser()
        self.browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

      
        self.browser.append(docText)
        self.browser.verticalScrollBar().setValue(self.browser.verticalScrollBar().minimum())
        cursor = self.browser.textCursor();
        
        cursor.setPosition(0);
        self.browser.setTextCursor(cursor);
        
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.browser.setFont(font)
        
        self.vBoxSizer.addWidget(self.browser)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.accepted.connect(self.accept)
        self.vBoxSizer.addWidget(buttonBox)
        
        self.setLayout(self.vBoxSizer)
        self.setWindowTitle(self.tr(expName) + " - " + self.tr("documentation"))
        screen = QDesktopWidget().screenGeometry()
        wd = int(screen.width()/3)
        ht = int(0.8*screen.height())
        self.resize(wd, ht)
        self.show()
  
