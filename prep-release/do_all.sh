#!/bin/sh

cd ../pychoacoustics/doc
./mkdoc.sh

cd ../../prep-release

python3 do_pyside.py
./mkupdate_pyqt5.sh
./distbuild.sh 
