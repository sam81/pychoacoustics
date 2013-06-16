

pyrcc4 -o ../pychoacoustics_pack/qrc_resources.py ../resources.qrc
pylupdate4 -verbose pychoacoustics.pro
lrelease -verbose pychoacoustics.pro

mv *.qm ../translations/