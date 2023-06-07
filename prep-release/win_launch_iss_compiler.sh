#!/bin/sh


#mkdir ../build/exe.win-amd64-3.11/doc
#mkdir ../build/exe.win-amd64-3.11/prm_files

# wine cmd /c "Z:\media\ntfsShared\lin_home\auditory\code\pychoacoustics\prep-release\winbuild.bat"

# rsync -r ../build/exe.win-amd64-3.11/lib/pychoacoustics/doc/ ../build/exe.win-amd64-3.11/doc/
# rsync -r ../build/exe.win-amd64-3.11/lib/pychoacoustics/prm_files/ ../build/exe.win-amd64-3.11/prm_files/


wine cmd /c "Z:\media\ntfsShared\lin_home\auditory\code\pychoacoustics\prep-release\win_launch_iss_compiler.bat"
