#! /usr/bin/env python
# -*- coding: utf-8 -*-  

import copy, os

rootDir = "/media/ntfsShared/lin_home/auditory/code/pychoacoustics/"
thisDir = os.getcwd()

#read the current pyqt version
f = open(rootDir+'pychoacoustics/pyqtver.py', 'r')
pyqtverLines = f.readlines()
pyqtverLinesPyQt6 = copy.copy(pyqtverLines)
f.close()
for i in range(len(pyqtverLinesPyQt6)):
    if pyqtverLinesPyQt6[i].strip().split('=')[0].strip() == "pyqtversion":
           pyqtverLinesPyQt6[i] = "pyqtversion = 6\n"
           if int(pyqtverLines[i].strip().split('=')[1].strip()) == 6:
               update_resources = False
           else:
               update_resources = True
               
#Change pyqtver to PyQt6
f = open(rootDir + 'pychoacoustics/pyqtver.py', 'w')
f.writelines(pyqtverLinesPyQt6)
f.close()

if update_resources == True:
    os.chdir(rootDir+"prep-release/")
    os.system('/usr/bin/sh mkupdate_pyqt6.sh')
    os.chdir(thisDir)
