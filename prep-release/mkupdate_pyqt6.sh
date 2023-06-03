#!/bin/sh


pylupdate6 --ts pychoacoustics_el.ts --ts pychoacoustics_en_GB.ts --ts pychoacoustics_en_US.ts --ts pychoacoustics_es.ts --ts pychoacoustics_fr.ts --ts pychoacoustics_it.ts ../pychoacoustics/__main__.py ../pychoacoustics/audio_manager.py ../pychoacoustics/control_window.py ../pychoacoustics/dialog_edit_preferences.py ../pychoacoustics/dialog_edit_experimenters.py ../pychoacoustics/dialog_edit_phones.py ../pychoacoustics/dialog_show_fortune.py ../pychoacoustics/global_parameters.py ../pychoacoustics/response_box.py ../pychoacoustics/stats_utils.py ../pychoacoustics/default_experiments/audiogram.py ../pychoacoustics/default_experiments/audiogram_mf.py ../pychoacoustics/default_experiments/freq.py ../pychoacoustics/default_experiments/wav_comparison.py ../pychoacoustics/default_experiments/wav_sameDifferent.py ../pychoacoustics/sndlib.py

lrelease -verbose pychoacoustics.pro
mv *.qm ../translations/

rcc -g python ../resources.qrc | sed '0,/PySide2/s//PyQt6/' > ../pychoacoustics/qrc_resources.py





