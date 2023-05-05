# -*- coding: utf-8 -*-

"""
Match the frequency of two pure tones differing in level.

"""

from ..pyqtver import*
from .._version_info import*
from pychoacoustics.sndlib import pureTone
import numpy

if pyqtversion == 5:
    from PyQt5.QtWidgets import QApplication
elif pyqtversion == 6:
    from PyQt6.QtWidgets import QApplication

                                                                              
def initialize_lev_match(prm):
    exp_name = "Demo Level Matching"
    prm["experimentsChoices"].append(exp_name)
    prm[exp_name] = {}
    prm[exp_name]["paradigmChoices"] = ["Transformed Up-Down Interleaved",
                                        "Weighted Up-Down Interleaved"]

    prm[exp_name]["opts"] = ["hasISIBox", "hasAlternativesChooser"]
    prm[exp_name]['defaultAdaptiveType'] = "Arithmetic"
    prm[exp_name]['defaultNIntervals'] = 2
    prm[exp_name]['defaultNAlternatives'] = 2
    prm[exp_name]['defaultNTracks'] = 2
    prm[exp_name]["execString"] = "lev_match"
    prm[exp_name]["version"] = __name__ + ' ' + pychoacoustics_version + ' ' + pychoacoustics_builddate
    
    return prm

def select_default_parameters_lev_match(parent, par):
   
    field = []
    fieldLabel = []
    chooser = []
    chooserLabel = []
    chooserOptions = []

    fieldLabel.append("Starting Level Track 1 (dB SPL)")
    field.append(75)

    fieldLabel.append("Starting Level Track 2 (dB SPL)")
    field.append(55)

    fieldLabel.append(parent.tr("Frequency Standard Tone (Hz)"))
    field.append(1000)

    fieldLabel.append(parent.tr("Frequency Comparison Tone (Hz)"))
    field.append(250)

    fieldLabel.append(parent.tr("Level Standard Tone (dB SPL)"))
    field.append(65)

    fieldLabel.append(parent.tr("Duration (ms)"))
    field.append(180)
    
    fieldLabel.append(parent.tr("Ramps (ms)"))
    field.append(10)

    chooserOptions.append(["Right", "Left", "Both"])
    chooserLabel.append(QApplication.translate("","Ear:",""))
    chooser.append(QApplication.translate("","Both",""))

    
    prm = {}
    prm['field'] = field
    prm['fieldLabel'] = fieldLabel
    prm['chooser'] = chooser
    prm['chooserLabel'] = chooserLabel
    prm['chooserOptions'] =  chooserOptions

    return prm

    
def doTrial_lev_match(parent):
    currBlock = 'b'+ str(parent.prm['currentBlock'])
    if parent.prm['startOfBlock'] == True:
        parent.prm['adaptiveParam'] = []
        parent.prm['adaptiveParam'].append(parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Starting Level Track 1 (dB SPL)")])
        parent.prm['adaptiveParam'].append(parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Starting Level Track 2 (dB SPL)")])
        parent.writeResultsHeader('log')


  
    standardFrequency = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Frequency Standard Tone (Hz)")]
    comparisonFrequency = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Frequency Comparison Tone (Hz)")]
    standardLevel = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Level Standard Tone (dB SPL)")]
    duration = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Duration (ms)")] 
    ramps = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Ramps (ms)")]
    phase = 0
    channel = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index("Ear:")]

    comparisonLevel = parent.prm['adaptiveParam'][parent.prm['currentDifference']]

    comparisonTone = pureTone(comparisonFrequency, phase, comparisonLevel, duration, ramps,
                               channel, parent.prm['sampRate'], parent.prm['maxLevel'])

    standardToneList = []
    for i in range((parent.prm['nIntervals']-1)):
        thisSnd = pureTone(standardFrequency, phase, standardLevel, duration, ramps, channel,
                           parent.prm['sampRate'], parent.prm['maxLevel'])
        standardToneList.append(thisSnd)
    parent.playRandomisedIntervals(comparisonTone, standardToneList)
