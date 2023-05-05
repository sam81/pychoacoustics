# -*- coding: utf-8 -*-

"""
This experiment can be used to find out which of three different sounds is judged as the most dissimilar from the other two (the odd one out).

The procedure used is similar to the odd-one-out procedure, however, in this experiment all three sounds are different, while in the odd-one-out procedure two of the sounds are the same, or the physical attribute of interest (e.g. frequency, intensity) is the same between two of the sounds. The task in this experiment is subjective, there is no correct response.

This task was used by Carcagno and Plack [2011, JARO 12: 503–517, DOI:10.1007/s10162-011-0266-3] to test whether listeners would perceive an unresolved complex tone with partials summed in ALT phase as more similar (in pitch) to an unresolved complex tone with the same F0 with partials summed in SINE phase, or to a resolved complex tone with double the F0. The pitch of unresolved complex tones with harmonics summed in ALT phase is generally found to be an octave higher than the pitch of unresolved complex tones summed in SINE phase. Therefore, listeners should choose the 110 SINE stimulus
as the odd one out.

"""

from ..pyqtver import*

if pyqtversion == 5:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtWidgets import QApplication
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtWidgets import QApplication
    
from .._version_info import*
from pychoacoustics.sndlib import*
import random

                                                                                         
def initialize_wav_comparison(prm):
    exp_name = QApplication.translate("","WAV Comparison","")
    prm["experimentsChoices"].append(exp_name)
    prm[exp_name] = {}
    prm[exp_name]["paradigmChoices"] = [QApplication.translate("","Multiple Constants Sound Comparison","")]
    prm[exp_name]["opts"] = ["hasISIBox", "hasNDifferencesChooser"]
    prm[exp_name]['defaultNIntervals'] = 3
    prm[exp_name]['defaultNAlternatives'] = 3
    prm[exp_name]["buttonLabels"] = [prm['buttonTranslator'].translate('rb', "1"), prm['buttonTranslator'].translate('rb', "2"), prm['buttonTranslator'].translate('rb', "3")]
    prm[exp_name]["execString"] = "wav_comparison"
    prm[exp_name]["version"] = __name__ + ' ' + pychoacoustics_version + ' ' + pychoacoustics_builddate

    return prm

def select_default_parameters_wav_comparison(parent, par):
    nDifferences = par['nDifferences']

    field = []
    fieldLabel = []
    chooser = []
    chooserLabel = []
    chooserOptions = []
    fileChooser = []
    fileChooserButton = []
    
    fieldLabel.append( parent.tr("Level (dB SPL)"))
    field.append(60)

    chooserOptions.append([parent.tr("Original"), parent.tr("Right"), parent.tr("Left")])
    chooserLabel.append(parent.tr("Ear:"))
    chooser.append(parent.tr("Original"))

    for i in range(nDifferences):
        fileChooserButton.append("Comparison"+str(i+1)+" WAV1")
        fileChooser.append("")
        fileChooserButton.append("Comparison"+str(i+1)+" WAV2")
        fileChooser.append("")
        fileChooserButton.append("Comparison"+str(i+1)+" WAV3")
        fileChooser.append("")
   

    prm = {}
  
    prm['field'] = field
    prm['fieldLabel'] = fieldLabel
    prm['chooser'] = chooser
    prm['chooserLabel'] = chooserLabel
    prm['chooserOptions'] =  chooserOptions
    prm['fileChooser'] = fileChooser
    prm['fileChooserButton'] = fileChooserButton

    return prm


def doTrial_wav_comparison(parent):
    currBlock = 'b'+ str(parent.prm['currentBlock'])
    if parent.prm['startOfBlock'] == True:
        parent.prm['additional_parameters_to_write'] = {}
        parent.prm['conditions'] = []
        parent.prm['comparisonChoices'] = []
        parent.prm['currStimOrder'] = [0,1,2]
        for i in range(parent.prm['nDifferences']):
            parent.prm['conditions'].append("Comparison"+str(i+1))
            parent.prm['comparisonChoices'].append("Comparison"+str(i+1))
        
        parent.writeResultsHeader('log')

    level = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Level (dB SPL)"))]
    channel = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(parent.tr("Ear:"))]

    wavfiles = []
    for i in range(parent.prm['nDifferences']):
        a = parent.prm[currBlock]['fileChooser'][parent.prm['fileChooserButton'].index(parent.tr("Comparison"+str(i+1)+" WAV1"))]
        b = parent.prm[currBlock]['fileChooser'][parent.prm['fileChooserButton'].index(parent.tr("Comparison"+str(i+1)+" WAV2"))]
        c = parent.prm[currBlock]['fileChooser'][parent.prm['fileChooserButton'].index(parent.tr("Comparison"+str(i+1)+" WAV3"))]
        wavfiles.append([a,b,c])


    parent.currentCondition =  random.choice(parent.prm['comparisonChoices'])

    numpy.random.shuffle(parent.prm['currStimOrder'])
    parent.correctButton = parent.prm['currStimOrder'].index(2)+1 #WAV3 always the "correct" one, although in the WAV comparison task there may not be a "correct" choice
    
    soundList = []
    fsList = []
    nBitsList = []
    for i in range(3):
        print(wavfiles[parent.prm['conditions'].index(parent.currentCondition)][parent.prm['currStimOrder'][i]])
        (thisSnd, thisFs, thisNbits) = parent.audioManager.loadWavFile(wavfiles[parent.prm['conditions'].index(parent.currentCondition)][parent.prm['currStimOrder'][i]], level, parent.prm['maxLevel'], channel, parent.prm['sampRate'])
        soundList.append(thisSnd)

    parent.playSoundsWavComp(soundList)

    
