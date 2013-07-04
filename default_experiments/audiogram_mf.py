# -*- coding: utf-8 -*-

"""
Run audiogram_mf
"""

from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, unicode_literals
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication
from sndlib import*
from numpy import log10
                                                                            

def initialize_audiogram_mf(prm):
    exp_name = QApplication.translate("","audiogram_mf","", QApplication.UnicodeUTF8)
    prm["experimentsChoices"].append(exp_name)
    prm[exp_name] = {}
    prm[exp_name]["paradigmChoices"] = [QApplication.translate("","Adaptive Interleaved","", QApplication.UnicodeUTF8),
                                                                                                      QApplication.translate("","Weighted Up/Down","", QApplication.UnicodeUTF8),
                                                                                                      QApplication.translate("","Multiple Constants m-Intervals n-Alternatives","", QApplication.UnicodeUTF8)]
                                                                                                   
                                                                                                   
    prm[exp_name]["opts"] = ["hasISIBox", "hasAlternativesChooser", "hasFeedback",
                                                                                           "hasIntervalLights"]
    prm[exp_name]['defaultAdaptiveType'] = QApplication.translate("","Arithmetic","", QApplication.UnicodeUTF8)
    prm[exp_name]['defaultNIntervals'] = 2
    prm[exp_name]['defaultNAlternatives'] = 2
    
    prm[exp_name]["execString"] = "audiogram_mf"
    return prm

def select_default_parameters_audiogram_mf(parent, par):
    if 'nDifferences' not in par:
        par['nDifferences'] = 3
    nDifferences = par['nDifferences']
   
    field = []
    fieldLabel = []
    chooser = []
    chooserLabel = []
    chooserOptions = []

    for i in range(nDifferences):
        fieldLabel.append(parent.tr("Frequency (Hz) " + str(i+1)))
        field.append(1000+1000*i)
        fieldLabel.append(QApplication.translate("","Level (dB SPL) " + str(i+1),"", QApplication.UnicodeUTF8))
        field.append(50)
    
    fieldLabel.append(QApplication.translate("","Bandwidth (Hz)","", QApplication.UnicodeUTF8))
    field.append(10)
    
    fieldLabel.append(QApplication.translate("","Duration (ms)","", QApplication.UnicodeUTF8))
    field.append(180)
    
    fieldLabel.append(QApplication.translate("","Ramps (ms)","", QApplication.UnicodeUTF8))
    field.append(10)

    
    chooserOptions.append([QApplication.translate("","Right","", QApplication.UnicodeUTF8),
                           QApplication.translate("","Left","", QApplication.UnicodeUTF8),
                           QApplication.translate("","Both","", QApplication.UnicodeUTF8)])
    chooserLabel.append(QApplication.translate("","Ear:","", QApplication.UnicodeUTF8))
    chooser.append(QApplication.translate("","Right","", QApplication.UnicodeUTF8))
    chooserOptions.append([QApplication.translate("","Sinusoid","", QApplication.UnicodeUTF8),
                           QApplication.translate("","Narrowband Noise","", QApplication.UnicodeUTF8)])
    chooserLabel.append(QApplication.translate("","Type:","", QApplication.UnicodeUTF8))
    chooser.append(QApplication.translate("","Sinusoid","", QApplication.UnicodeUTF8))

    prm = {}
    prm['field'] = field
    prm['fieldLabel'] = fieldLabel
    prm['chooser'] = chooser
    prm['chooserLabel'] = chooserLabel
    prm['chooserOptions'] =  chooserOptions

    return prm

def get_fields_to_hide_audiogram_mf(parent):
    if parent.chooser[parent.prm['chooserLabel'].index(QApplication.translate("","Type:","", QApplication.UnicodeUTF8))].currentText() == QApplication.translate("","Sinusoid","", QApplication.UnicodeUTF8):
        parent.fieldsToHide = [parent.prm['fieldLabel'].index(QApplication.translate("","Bandwidth (Hz)","", QApplication.UnicodeUTF8))]
    else:
        parent.fieldsToShow = [parent.prm['fieldLabel'].index(QApplication.translate("","Bandwidth (Hz)","", QApplication.UnicodeUTF8))]
    
def doTrial_audiogram_mf(parent):
    currBlock = 'b'+ str(parent.prm['currentBlock'])
    nDifferences = parent.prm['nDifferences']
    frequency = []
    if parent.prm['startOfBlock'] == True:
        parent.prm['additional_parameters_to_write'] = {}
        parent.prm['conditions'] = []
        parent.prm['adaptiveDifference'] = []
        for i in range(nDifferences):
            parent.prm['conditions'].append(str(parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(QApplication.translate("","Frequency (Hz) " + str(i+1),"", QApplication.UnicodeUTF8))]))
            parent.prm['adaptiveDifference'].append(parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(QApplication.translate("","Level (dB SPL) " + str(i+1),"", QApplication.UnicodeUTF8))])
        parent.writeResultsHeader('log')

    for i in range(nDifferences):
        frequency.append(parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(QApplication.translate("","Frequency (Hz) " + str(i+1),"", QApplication.UnicodeUTF8))])

    #these fields are necessary for the two procedures (multiple constants, adaptive interleaved)
    parent.currentCondition = parent.prm['conditions'][parent.prm['currentDifference']] #this is necessary for counting correct/total trials
    correctLevel = parent.prm['adaptiveDifference'][parent.prm['currentDifference']]
    
    currentFrequency = frequency[parent.prm['currentDifference']]
    bandwidth = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(QApplication.translate("","Bandwidth (Hz)","", QApplication.UnicodeUTF8))] 
    phase = 0
    
    incorrectLevel = -200
    duration = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(QApplication.translate("","Duration (ms)","", QApplication.UnicodeUTF8))] 
    ramps = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(QApplication.translate("","Ramps (ms)","", QApplication.UnicodeUTF8))] 
    channel = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(QApplication.translate("","Ear:","", QApplication.UnicodeUTF8))]
    sndType = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(QApplication.translate("","Type:","", QApplication.UnicodeUTF8))]

    if sndType == QApplication.translate("","Narrowband Noise","", QApplication.UnicodeUTF8):
        if bandwidth > 0:
            parent.stimulusCorrect = steepNoise(currentFrequency-(bandwidth/2), currentFrequency+(bandwidth/2), correctLevel - (10*log10(bandwidth)),
                                                duration, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
        else:
            parent.stimulusCorrect = pureTone(currentFrequency, phase, correctLevel, duration, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
    elif sndType == QApplication.translate("","Sinusoid","", QApplication.UnicodeUTF8):
        parent.stimulusCorrect = pureTone(currentFrequency, phase, correctLevel, duration, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
      
            
    parent.stimulusIncorrect = []
    for i in range((parent.prm['nIntervals']-1)):
        thisSnd = pureTone(currentFrequency, phase, incorrectLevel, duration, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
        parent.stimulusIncorrect.append(thisSnd)
    parent.playRandomisedIntervals(parent.stimulusCorrect, parent.stimulusIncorrect)
