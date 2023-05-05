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
    from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QGridLayout, QLabel, QLineEdit
    from PyQt5.QtGui import QIntValidator
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QGridLayout, QLabel, QLineEdit
    from PyQt6.QtGui import QIntValidator
    
class swapBlocksDialog(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)

        self.prm = self.parent().prm
        self.currLocale = self.parent().prm['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.NumberOption.OmitGroupSeparator | self.currLocale.NumberOption.RejectGroupSeparator)
      
        grid = QGridLayout()
        n = 0
            
        blockALabel = QLabel(self.tr('Block A: '))
        grid.addWidget(blockALabel, n, 0)
        self.blockAWidget = QLineEdit(str(self.prm['currentBlock']))
        self.blockAWidget.setValidator(QIntValidator(self))
        grid.addWidget(self.blockAWidget, n, 1)

        blockBLabel = QLabel(self.tr('Block B: '))
        grid.addWidget(blockBLabel, n, 2)
        self.blockBWidget = QLineEdit('')
        self.blockBWidget.setValidator(QIntValidator(self))
        grid.addWidget(self.blockBWidget, n, 3)
        
        n = n+1
        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|
                                     QDialogButtonBox.StandardButton.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        grid.addWidget(buttonBox, n, 3)
        self.setLayout(grid)
        self.setWindowTitle(self.tr("Swap Blocks"))

  
        
