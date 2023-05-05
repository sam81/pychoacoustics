# -*- coding: utf-8 -*-

"""
Measure d' for the detection of a pure tone in a Yes/No task.

The available fields are:

- Frequency (Hz) :
    The frequency of the pure tone signal
- Duration (ms) :
    Tone duration (excluding ramps), in ms
- Ramps (ms) :
    Duration of each ramp, in ms
- Level (dB SPL):
    Level of the signal in dB SPL.

The available choosers are:

- Ear: [``Right``, ``Left``, ``Both``]
    The ear to which the signal will be presented

"""

#from PyQt4 import QtGui, QtCore
#from PyQt4.QtGui import QApplication
import random, sys
from .._version_info import*
from pychoacoustics.sndlib import*
                                                                                         

def initialize_sig_detect_multi(prm):
    exp_name = "Demo Signal Detection Multiple Constants"
    prm["experimentsChoices"].append(exp_name)
    prm[exp_name] = {}
    prm[exp_name]["paradigmChoices"] = ["Multiple Constants 1-Interval 2-Alternatives"]

    prm[exp_name]["opts"] = ["hasFeedback", "hasNDifferencesChooser"]

    prm[exp_name]["buttonLabels"] = ["Yes", "No"]
    prm[exp_name]['defaultNIntervals'] = 1
    prm[exp_name]['defaultNAlternatives'] = 2
    
    prm[exp_name]["execString"] = "sig_detect_multi"
    prm[exp_name]["version"] = __name__ + ' ' + pychoacoustics_version + ' ' + pychoacoustics_builddate
    
    return prm

def select_default_parameters_sig_detect_multi(parent, par):
    nDifferences = par['nDifferences']
    
    field = []
    fieldLabel = []
    chooser = []
    chooserLabel = []
    chooserOptions = []

    for i in range(nDifferences):
        fieldLabel.append(parent.tr("Frequency (Hz) " + str(i+1)))
        field.append(1000+i)
    
    
    fieldLabel.append(parent.tr("Duration (ms)"))
    field.append(2)
    
    
    fieldLabel.append(parent.tr("Ramps (ms)"))
    field.append(4)

    fieldLabel.append(parent.tr("Level (dB SPL)"))
    field.append(40)
    

    chooserOptions.append([parent.tr("Right"), parent.tr("Left"), parent.tr("Both")])
    chooserLabel.append(parent.tr("Channel:"))
    chooser.append(parent.tr("Both"))
        
    

    prm = {}
    prm['field'] = field
    prm['fieldLabel'] = fieldLabel
    prm['chooser'] = chooser
    prm['chooserLabel'] = chooserLabel
    prm['chooserOptions'] =  chooserOptions

    return prm


def doTrial_sig_detect_multi(parent):
  
    currBlock = 'b'+ str(parent.prm['currentBlock'])
    if parent.prm['startOfBlock'] == True:
        parent.writeResultsHeader('log')
        parent.prm['trialTypes'] = ["signal_present","signal_absent"]
        parent.prm['conditions'] = []
        nDifferences = parent.prm['nDifferences']
        for i in range(nDifferences):
            parent.prm['conditions'].append('Frequency (Hz) ' + str(parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Frequency (Hz) ") + str(i+1))])) #this is for the sortResponse routine

    parent.currentCondition =  parent.prm['conditions'][parent.prm['currentDifference']] 
    parent.currentSubcondition = random.choice(parent.prm['trialTypes'])

    if parent.currentSubcondition == "signal_present":
        parent.correctButton = 1
    elif parent.currentSubcondition == "signal_absent":
        parent.correctButton = 2
        
    currentFreq = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Frequency (Hz) ") + str(parent.prm['conditions'].index(parent.currentCondition)+1))]

    dur     = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Duration (ms)")]
    ramps   = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Ramps (ms)")]
    lev     = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Level (dB SPL)")]
    phase   = 0
    channel = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(parent.tr("Channel:"))]
   

    if parent.currentSubcondition == 'signal_absent':
        lev = -200
    sig = pureTone(currentFreq, phase, lev, dur, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])

 
    parent.playSequentialIntervals([sig])
   
