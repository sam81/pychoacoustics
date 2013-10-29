# -*- coding: utf-8 -*-

"""
This experiment can be used to measure thresholds for detecting a signal in quiet.
The signal can be either a pure tone or a narrow-band noise.

The available fields are:

- Frequency (Hz) :
    Signal center frequency in Hz
- Bandwidth (Hz) :
    The bandwidth of the signal in Hz (only applicable if
    signal type is Narrowband Noise)
- Level (dB SPL) :
    Signal level (for constant procedures), or starting signal level
    (for adaptive procedures), in dB SPL
- Duration (ms) :
    Signal duration (excluding ramps), in ms
- Ramps (ms) :
    Duration of each ramp, in ms

The available choosers are:

- Ear: [``Right``, ``Left``, ``Both``]
    The ear to which the signal will be presented
- Signal Type: [``Sinusoid``, ``Narrowband Noise``]
    The signal type. If ``Sinusoid`` the signal will be a pure tone, if ``Narrowband Noise``, the signal will be a narrow-band noise

"""

from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, unicode_literals
from ..pyqtver import*
if pyqtversion == 4:
    from PyQt4 import QtGui, QtCore
    from PyQt4.QtGui import QApplication
elif pyqtversion == 5:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtWidgets import QApplication
from ..sndlib import*
from numpy import log10



def initialize_audiogram(prm):
    exp_name = QApplication.translate("","Audiogram","", QApplication.UnicodeUTF8)
    prm["experimentsChoices"].append(exp_name)
    prm[exp_name] = {}
    prm[exp_name]["paradigmChoices"] = [QApplication.translate("","Adaptive","", QApplication.UnicodeUTF8),
                                        QApplication.translate("","Weighted Up/Down","", QApplication.UnicodeUTF8),
                                        QApplication.translate("","Constant m-Intervals n-Alternatives","", QApplication.UnicodeUTF8)]

    prm[exp_name]["opts"] = ["hasISIBox", "hasAlternativesChooser", "hasFeedback",
                             "hasIntervalLights"]
    prm[exp_name]['defaultAdaptiveType'] = QApplication.translate("","Arithmetic","", QApplication.UnicodeUTF8)
    prm[exp_name]['defaultNIntervals'] = 2
    prm[exp_name]['defaultNAlternatives'] = 2
    prm[exp_name]["execString"] = "audiogram"
    return prm

def select_default_parameters_audiogram(parent, par):
   
    field = []
    fieldLabel = []
    chooser = []
    chooserLabel = []
    chooserOptions = []
    
    fieldLabel.append(QApplication.translate("","Frequency (Hz)","", QApplication.UnicodeUTF8))
    field.append(1000)
    
    fieldLabel.append(QApplication.translate("","Bandwidth (Hz)","", QApplication.UnicodeUTF8))
    field.append(10)
    
    fieldLabel.append(QApplication.translate("","Level (dB SPL)","", QApplication.UnicodeUTF8))
    field.append(50)
    
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
    chooserLabel.append(QApplication.translate("","Signal Type:","", QApplication.UnicodeUTF8))
    chooser.append(QApplication.translate("","Sinusoid","", QApplication.UnicodeUTF8))
    
    prm = {}
    prm['field'] = field
    prm['fieldLabel'] = fieldLabel
    prm['chooser'] = chooser
    prm['chooserLabel'] = chooserLabel
    prm['chooserOptions'] =  chooserOptions

    return prm

def get_fields_to_hide_audiogram(parent):
    if parent.chooser[parent.prm['chooserLabel'].index(QApplication.translate("","Signal Type:","", QApplication.UnicodeUTF8))].currentText() == QApplication.translate("","Sinusoid","", QApplication.UnicodeUTF8):
        parent.fieldsToHide = [parent.prm['fieldLabel'].index(QApplication.translate("","Bandwidth (Hz)","", QApplication.UnicodeUTF8))]
    else:
        parent.fieldsToShow = [parent.prm['fieldLabel'].index(QApplication.translate("","Bandwidth (Hz)","", QApplication.UnicodeUTF8))]
    
def doTrial_audiogram(parent):

    currBlock = 'b'+ str(parent.prm['currentBlock'])
    if parent.prm['startOfBlock'] == True:
        parent.prm['additional_parameters_to_write'] = {}
        parent.prm['adaptiveDifference'] = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(QApplication.translate("","Level (dB SPL)","", QApplication.UnicodeUTF8))]
        parent.prm['conditions'] = [str(parent.prm['adaptiveDifference'])]

        parent.writeResultsHeader('log')
    parent.currentCondition = parent.prm['conditions'][0]
    frequency = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(QApplication.translate("","Frequency (Hz)","", QApplication.UnicodeUTF8))] 
    bandwidth = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(QApplication.translate("","Bandwidth (Hz)","", QApplication.UnicodeUTF8))] 
    phase = 0
    correctLevel = parent.prm['adaptiveDifference']
    incorrectLevel = -200
    duration = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(QApplication.translate("","Duration (ms)","", QApplication.UnicodeUTF8))] 
    ramps = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(QApplication.translate("","Ramps (ms)","", QApplication.UnicodeUTF8))] 
    channel = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(QApplication.translate("","Ear:","", QApplication.UnicodeUTF8))]
    sndType = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(QApplication.translate("","Signal Type:","", QApplication.UnicodeUTF8))]

    if sndType == QApplication.translate("","Narrowband Noise","", QApplication.UnicodeUTF8):
        if bandwidth > 0:
            parent.stimulusCorrect = steepNoise(frequency-(bandwidth/2), frequency+(bandwidth/2), correctLevel - (10*log10(bandwidth)),
                                                duration, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
        else:
            parent.stimulusCorrect = pureTone(frequency, phase, correctLevel, duration, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
    elif sndType == QApplication.translate("","Sinusoid","", QApplication.UnicodeUTF8):
        parent.stimulusCorrect = pureTone(frequency, phase, correctLevel, duration, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
      
            
    parent.stimulusIncorrect = []
    for i in range((parent.prm['nIntervals']-1)):
        thisSnd = pureTone(frequency, phase, incorrectLevel, duration, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
        parent.stimulusIncorrect.append(thisSnd)
    parent.playRandomisedIntervals(parent.stimulusCorrect, parent.stimulusIncorrect)
