#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os

os.system("rm -r ../windows_installer/sound_source_id")

ver_to_build = input("Version to build: ")
os.system("tar -xvf ../dist/sound_source_id-"+ver_to_build+".tar.gz --directory ../windows_installer/")
os.system("mv ../windows_installer/sound_source_id-"+ver_to_build+ " ../windows_installer/sound_source_id")

os.chdir("../windows_installer/sound_source_id")

os.system("wine cmd /c python setup_cx.py build")

os.system("rsync -r ./build/exe.win-amd64-3.11/lib/sound_source_id/doc/ ./build/exe.win-amd64-3.11/doc/")
os.system("rsync -r ./build/exe.win-amd64-3.11/lib/sound_source_id/prm_files/ ./build/exe.win-amd64-3.11/prm_files/")


os.system("/usr/bin/bash ../../prep-release/win_launch_iss_compiler.sh")
