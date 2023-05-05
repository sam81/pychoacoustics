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

import sys
import time

class redirectStreamToFile():
    def __init__(self, logfile):
        timeStamp = ''+ time.strftime("%d/%m/%y %H:%M:%S", time.localtime()) + ' ' + '\n'
        self.stdout = sys.stdout
        self.log = open(logfile, 'a')
        self.log.write("**********")
        self.log.write(timeStamp)
 
    def write(self, text):
        try: #stdout is None with pythonw causing an error
            self.stdout.write(text)
            self.log.write(text)
            self.log.flush()
        except:
            pass
 
    def close(self):
        try:
            self.stdout.close()
            self.log.close()
        except:
            pass
