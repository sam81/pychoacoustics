#!/bin/sh
cd ..
python3 setup.py sdist --formats=gztar,zip
python3 setup.py bdist_wininst #--install-script‭ ‬postinstall.py

python3 setup_ver.py sdist --formats=gztar,zip
python3 setup_ver.py bdist_wininst #--install-script‭ ‬postinstall.py
