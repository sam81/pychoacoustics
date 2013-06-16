#!/bin/sh

cd ../doc
./mkdoc.sh
cp pychoacoustics_manual/pychoacoustics_manual.pdf ../pychoacoustics_pack/doc/
cp -R build/html/ ../pychoacoustics_pack/doc/modules/

cd ../prep-release
./mkupdate.sh
./distbuild.sh 
