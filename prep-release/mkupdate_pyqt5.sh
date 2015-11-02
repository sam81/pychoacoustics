#!/bin/sh

pyrcc5 -o ../pychoacoustics/qrc_resources.py ../resources.qrc
pylupdate5 -verbose pychoacoustics.pro
lrelease -verbose pychoacoustics.pro

mv *.qm ../translations/
