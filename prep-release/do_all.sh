#!/bin/sh

cd ../pychoacoustics/doc
./mkdoc.sh

cd ../../prep-release

#python3 do_pyside.py
#python3 do_pyqt4.py
./mkupdate_pyqt5.sh
./distbuild.sh 
