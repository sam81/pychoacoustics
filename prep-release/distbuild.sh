#!/bin/sh
cd ..
python3 setup.py sdist --formats=gztar,zip
python3 setup.py bdist_wininst #--install-script‭ ‬postinstall.py

