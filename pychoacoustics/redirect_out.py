# -*- coding: utf-8 -*-

#   Copyright (C) 2008-2024 Samuele Carcagno <sam.carcagno@gmail.com>
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
    from PyQt5.QtWidgets import QPlainTextEdit
elif pyqtversion == 6:
    from PyQt6.QtWidgets import QPlainTextEdit

class OutputWindow(QPlainTextEdit):
    def write(self, txt):
        self.appendPlainText(str(txt))

