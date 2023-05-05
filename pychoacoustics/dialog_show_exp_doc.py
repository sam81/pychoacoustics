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
    from PyQt5.QtWidgets import QDialog, QDesktopWidget, QDialogButtonBox, QPushButton, QSizePolicy, QTextBrowser, QVBoxLayout
    from PyQt5.QtGui import QFont
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtCore import QLocale
    from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QPushButton, QSizePolicy, QTextBrowser, QVBoxLayout
    from PyQt6.QtGui import QFont
    
import random

class showExpDocDialog(QDialog):
    def __init__(self, parent, docText, expName):
        QDialog.__init__(self, parent)
        self.prm = self.parent().prm
        self.currLocale = self.parent().prm['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.NumberOption.OmitGroupSeparator | self.currLocale.NumberOption.RejectGroupSeparator)
       
        self.vBoxSizer = QVBoxLayout()
        self.browser = QTextBrowser()
        self.browser.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

      
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

        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttonBox.accepted.connect(self.accept)
        self.vBoxSizer.addWidget(buttonBox)
        
        self.setLayout(self.vBoxSizer)
        self.setWindowTitle(self.tr(expName) + " - " + self.tr("documentation"))
        if pyqtversion == 5:
            screen = QDesktopWidget().screenGeometry()
        elif pyqtversion == 6:
            screen = self.screen().geometry()
        wd = int(screen.width()/3)
        ht = int(0.8*screen.height())
        self.resize(wd, ht)
        self.show()
  
