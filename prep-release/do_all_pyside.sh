#!/bin/sh

cd ../pychoacoustics/doc
./mkdoc.sh

cd ../../prep-release
./mkupdate_pyside.sh
./distbuild.sh 
