#!/bin/sh

cd ../pychoacoustics/doc
./mkdoc.sh

cd ../../prep-release
./mkupdate.sh
./distbuild.sh 
