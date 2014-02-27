# -*- coding: utf-8 -*- 

from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, unicode_literals
from ..pyqtver import*
if pyqtversion == 4:
    from PyQt4 import QtGui, QtCore
    from PyQt4.QtGui import QApplication
elif pyqtversion == -4:
    from PySide import QtGui, QtCore
    from PySide.QtGui import QApplication
elif pyqtversion == 5:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtWidgets import QApplication
    
from .._version_info import*
from pychoacoustics.sndlib import*
import random


                                                                                         
def initialize_wav_comparison(prm):
    exp_name = QApplication.translate("","WAV Comparison","", QApplication.UnicodeUTF8)
    prm["experimentsChoices"].append(exp_name)
    prm[exp_name] = {}
    prm[exp_name]["paradigmChoices"] = [QApplication.translate("","Odd One Out","", QApplication.UnicodeUTF8)]
    prm[exp_name]["opts"] = ["hasISIBox", "hasFeedback", "hasIntervalLights", "hasNDifferencesChooser"]
    prm[exp_name]['defaultNIntervals'] = 3
    prm[exp_name]['defaultNAlternatives'] = 3
    prm[exp_name]["buttonLabels"] = [prm['buttonTranslator'].translate('rb', "1"), prm['buttonTranslator'].translate('rb', "2"), prm['buttonTranslator'].translate('rb', "3")]
    prm[exp_name]["execString"] = "wav_comparison"
    prm[exp_name]["version"] = __name__ + ' ' + pychoacoustics_version + ' ' + pychoacoustics_builddate
    #prm[exp_name]["version"] = __name__ + ' ' + labexp_version + ' ' + labexp_builddate

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

# def get_fields_to_hide_wav_comparison(parent):

#     pass


def doTrial_wav_comparison(parent):
    currBlock = 'b'+ str(parent.prm['currentBlock'])
    if parent.prm['startOfBlock'] == True:
        parent.prm['additional_parameters_to_write'] = {}
        parent.prm['conditions'] = []
        parent.prm['comparisonChoices'] = []
        parent.prm['currStimOrder'] = [0,1,2]
        parent.correctButton = random.choice([1,2,3]) #this is just in case of automatic response
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
    soundList = []
    fsList = []
    nBitsList = []
    for i in range(3):
        print(wavfiles[parent.prm['conditions'].index(parent.currentCondition)][parent.prm['currStimOrder'][i]])
        (thisSnd, thisFs, thisNbits) = parent.audioManager.loadWavFile(wavfiles[parent.prm['conditions'].index(parent.currentCondition)][parent.prm['currStimOrder'][i]], level, parent.prm['maxLevel'], channel)
        soundList.append(thisSnd)
        fsList.append(thisFs)
        nBitsList.append(thisNbits)
    parent.playSoundsWavComp(soundList, fsList, nBitsList)
