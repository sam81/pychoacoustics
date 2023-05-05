# -*- coding: utf-8 -*-

"""
Odd-one-out task for WAV files.

For each comparison WAV number 3 should be selected as the odd one.

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

                                                                                         
def initialize_wav_odd_one_out(prm):
    exp_name = QApplication.translate("","WAV Odd-One-Out","")
    prm["experimentsChoices"].append(exp_name)
    prm[exp_name] = {}
    prm[exp_name]["paradigmChoices"] = [QApplication.translate("","Multiple Constants Odd One Out","")]
    prm[exp_name]["opts"] = ["hasISIBox", "hasFeedback", "hasNDifferencesChooser"]
    prm[exp_name]['defaultNIntervals'] = 3
    prm[exp_name]['defaultNAlternatives'] = 3
    prm[exp_name]["buttonLabels"] = [prm['buttonTranslator'].translate('rb', "1"), prm['buttonTranslator'].translate('rb', "2"), prm['buttonTranslator'].translate('rb', "3")]
    prm[exp_name]["execString"] = "wav_odd_one_out"
    prm[exp_name]["version"] = __name__ + ' ' + pychoacoustics_version + ' ' + pychoacoustics_builddate

    return prm

def select_default_parameters_wav_odd_one_out(parent, par):
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
        fileChooserButton.append("Pair"+str(i+1)+" Standard WAV")
        fileChooser.append("")
        fileChooserButton.append("Pair"+str(i+1)+" Odd WAV")
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


def doTrial_wav_odd_one_out(parent):
    currBlock = 'b'+ str(parent.prm['currentBlock'])
    if parent.prm['startOfBlock'] == True:
        parent.prm['additional_parameters_to_write'] = {}
        parent.prm['conditions'] = []
        parent.prm['comparisonChoices'] = []
        #parent.prm['currStimOrder'] = [0,1,2]
        for i in range(parent.prm['nDifferences']):
            parent.prm['conditions'].append("Pair"+str(i+1))
            parent.prm['comparisonChoices'].append("Pair"+str(i+1))
        
        parent.writeResultsHeader('log')
        
    level = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Level (dB SPL)"))]
    channel = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(parent.tr("Ear:"))]

    wavfiles = []
    for i in range(parent.prm['nDifferences']):
        a = parent.prm[currBlock]['fileChooser'][parent.prm['fileChooserButton'].index(parent.tr("Pair"+str(i+1)+" Standard WAV"))]
        b = parent.prm[currBlock]['fileChooser'][parent.prm['fileChooserButton'].index(parent.tr("Pair"+str(i+1)+" Odd WAV"))]
        wavfiles.append([a,b])

    
    parent.currentCondition =  random.choice(parent.prm['comparisonChoices'])
    (stimulusCorrect, fs, nBits) = parent.audioManager.loadWavFile(wavfiles[parent.prm['conditions'].index(parent.currentCondition)][1], level, parent.prm['maxLevel'], channel, parent.prm['sampRate'])
    
    stimulusIncorrect = []
    fsIncorrect = []
    nBitsIncorrect = []
    for i in range(2):
        (thisSnd, thisFs, thisNbits) = parent.audioManager.loadWavFile(wavfiles[parent.prm['conditions'].index(parent.currentCondition)][0], level, parent.prm['maxLevel'], channel, parent.prm['sampRate'])
        stimulusIncorrect.append(thisSnd)
                                                                   
    parent.playRandomisedIntervals(stimulusCorrect, stimulusIncorrect)
