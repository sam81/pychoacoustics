#!/bin/sh

cd ../pychoacoustics/doc
./mkdoc.sh

cd ../../prep-release

python3 do_pyside.py
./mkupdate.sh
./distbuild.sh 
