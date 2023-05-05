# -*- coding: utf-8 -*-

"""
ABX task for WAV files.

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


def initialize_wav_ABX(prm):
    exp_name = QApplication.translate("","WAV ABX","")
    prm["experimentsChoices"].append(exp_name)
    prm[exp_name] = {}
    prm[exp_name]["paradigmChoices"] = [QApplication.translate("","Multiple Constants ABX","")]
    prm[exp_name]["opts"] = ["hasISIBox", "hasFeedback", "hasNDifferencesChooser"]
    prm[exp_name]['defaultNIntervals'] = 3
    prm[exp_name]['defaultNAlternatives'] = 2
    prm[exp_name]["buttonLabels"] = ["A", "B"]#[prm['buttonTranslator'].translate('rb', "Same"), prm['buttonTranslator'].translate('rb', "Different")]
    prm[exp_name]["execString"] = "wav_ABX"
    prm[exp_name]["version"] = __name__ + ' ' + pychoacoustics_version + ' ' + pychoacoustics_builddate

    return prm

def select_default_parameters_wav_ABX(parent, par):
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
        fileChooserButton.append("Pair "+str(i+1)+" WAV1")
        fileChooser.append("")
        fileChooserButton.append("Pair "+str(i+1)+" WAV2")
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


def doTrial_wav_ABX(parent):
    currBlock = 'b'+ str(parent.prm['currentBlock'])
    if parent.prm['startOfBlock'] == True:
        parent.prm['additional_parameters_to_write'] = {}
        parent.prm['conditions'] = ["A", "B"]
        parent.prm['differenceChoices'] = [] #these are removed as the number of trials for each difference is reached
        parent.prm['differenceNames'] = [] #these are permanent
        parent.prm['currStimOrder'] = [0,1,2]
        #parent.correctButton = random.choice([1,2]) #this is just in case of automatic response
        for i in range(parent.prm['nDifferences']):
            parent.prm['differenceChoices'].append("Pair"+str(i+1))
            parent.prm['differenceNames'].append("Pair"+str(i+1))
        
        parent.writeResultsHeader('log')
        
    level = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Level (dB SPL)"))]
    channel = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(parent.tr("Ear:"))]

    wavfiles = []
    for i in range(parent.prm['nDifferences']):
        a = parent.prm[currBlock]['fileChooser'][parent.prm['fileChooserButton'].index(parent.tr("Pair "+str(i+1)+" WAV1"))]
        b = parent.prm[currBlock]['fileChooser'][parent.prm['fileChooserButton'].index(parent.tr("Pair "+str(i+1)+" WAV2"))]
        wavfiles.append([a,b])
    
 
    currentDifference =  random.choice(parent.prm['differenceChoices'])
    parent.prm['currentDifference'] = parent.prm['differenceNames'].index(currentDifference)#random.choice(range(len(parent.prm['differenceChoices'])))
    parent.currentCondition =  random.choice(parent.prm['conditions'])
    if parent.currentCondition == "A":
        parent.correctButton = 1
    elif parent.currentCondition == "B":
        parent.correctButton = 2
    stimChoices = ['WAV1', 'WAV2']
    parent.stim1 = random.choice(stimChoices)
    
    soundList = []
    fsList = []
    nBitsList = []

    (thisSnd, thisFs, thisNbits) = parent.audioManager.loadWavFile(wavfiles[parent.prm['currentDifference']][stimChoices.index(parent.stim1)], level, parent.prm['maxLevel'], channel, parent.prm['sampRate'])
    soundList.append(thisSnd)
    fsList.append(thisFs)
    nBitsList.append(thisNbits)
    if parent.stim1 == "WAV1":
        parent.stim2 = "WAV2"
    else:
        parent.stim2 = "WAV1"

    if parent.currentCondition == "A":
        parent.stim3 = parent.stim1
    else:
        parent.stim3 = parent.stim2


    (thisSnd, thisFs, thisNbits) = parent.audioManager.loadWavFile(wavfiles[parent.prm['currentDifference']][stimChoices.index(parent.stim2)], level, parent.prm['maxLevel'], channel, parent.prm['sampRate'])
    soundList.append(thisSnd)
    fsList.append(thisFs)
    nBitsList.append(thisNbits)

    (thisSnd, thisFs, thisNbits) = parent.audioManager.loadWavFile(wavfiles[parent.prm['currentDifference']][stimChoices.index(parent.stim3)], level, parent.prm['maxLevel'], channel, parent.prm['sampRate'])
    soundList.append(thisSnd)
    fsList.append(thisFs)
    nBitsList.append(thisNbits)

    parent.playSoundsWavComp(soundList)#, fsList, nBitsList)
