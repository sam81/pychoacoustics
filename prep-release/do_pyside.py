#! /usr/bin/env python
# -*- coding: utf-8 -*- 

import copy, os

thisDir = os.getcwd()
#read the current pyat version
f = open('../pychoacoustics/pyqtver.py', 'r')
pyqtverLines = f.readlines()
pyqtverLinesPyside = copy.copy(pyqtverLines)
f.close()
for i in range(len(pyqtverLinesPyside)):
    if pyqtverLinesPyside[i].strip().split('=')[0].strip() == "pyqtversion":
           pyqtverLinesPyside[i] = "pyqtversion = -4\n"

#Change pyqtver to pyside
f = open('../pychoacoustics/pyqtver.py', 'w')
f.writelines(pyqtverLinesPyside)
f.close()

os.system('pyside-rcc -py3 -o ../pychoacoustics/qrc_resources.py ../resources.qrc')
os.system('pyside-lupdate -verbose pychoacoustics.pro')
os.system('lrelease -verbose pychoacoustics.pro')
os.system('mv *.qm ../translations/')

os.chdir('../')
os.system('python3 setup-pyside.py sdist --formats=gztar,zip')
os.system('python3 setup-pyside.py bdist_wininst')

#revert
os.chdir('prep-release')
f = open('../pychoacoustics/pyqtver.py', 'w')
f.writelines(pyqtverLines)
f.close()

os.system('pyrcc4 -py3 -o ../pychoacoustics/qrc_resources.py ../resources.qrc')
os.system('pylupdate4 -verbose pychoacoustics.pro')
os.system('lrelease -verbose pychoacoustics.pro')
os.system('mv *.qm ../translations/')
