

pyrcc4 -py3 -o ../pychoacoustics/qrc_resources.py ../resources.qrc
pylupdate4 -verbose pychoacoustics.pro
lrelease -verbose pychoacoustics.pro

mv *.qm ../translations/