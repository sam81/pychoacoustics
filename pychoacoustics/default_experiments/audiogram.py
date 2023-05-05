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
    (for adaptive procedures), in dB SPL. If the signal type is narrowband noise
    the level if the total level, not the spectrum level.
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

from ..pyqtver import*

if pyqtversion == 5:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtWidgets import QApplication
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtWidgets import QApplication
    
from ..sndlib import*
from .._version_info import*
from numpy import log10



def initialize_audiogram(prm):
    exp_name = QApplication.translate("","Audiogram","")
    prm["experimentsChoices"].append(exp_name)
    prm[exp_name] = {}
    prm[exp_name]["paradigmChoices"] = [QApplication.translate("","Transformed Up-Down",""),
                                        QApplication.translate("","Weighted Up-Down",""),
                                        QApplication.translate("","Constant m-Intervals n-Alternatives",""),
                                        QApplication.translate("","PEST",""),
                                        QApplication.translate("","PSI",""),
                                        QApplication.translate("","UML","")]

    prm[exp_name]["opts"] = ["hasISIBox", "hasAlternativesChooser", "hasFeedback"]
    prm[exp_name]['defaultAdaptiveType'] = QApplication.translate("","Arithmetic","")
    prm[exp_name]['defaultNIntervals'] = 2
    prm[exp_name]['defaultNAlternatives'] = 2
    prm[exp_name]["execString"] = "audiogram"
    prm[exp_name]["version"] = __name__ + ' ' + pychoacoustics_version + ' ' + pychoacoustics_builddate

    return prm

def select_default_parameters_audiogram(parent, par):
   
    field = []
    fieldLabel = []
    chooser = []
    chooserLabel = []
    chooserOptions = []
    
    fieldLabel.append(QApplication.translate("","Frequency (Hz)",""))
    field.append(1000)
    
    fieldLabel.append(QApplication.translate("","Bandwidth (Hz)",""))
    field.append(10)
    
    fieldLabel.append(QApplication.translate("","Level (dB SPL)",""))
    field.append(50)
    
    fieldLabel.append(QApplication.translate("","Duration (ms)",""))
    field.append(180)
    
    fieldLabel.append(QApplication.translate("","Ramps (ms)",""))
    field.append(10)

    
    chooserOptions.append([QApplication.translate("","Right",""),
                           QApplication.translate("","Left",""),
                           QApplication.translate("","Both","")])
    chooserLabel.append(QApplication.translate("","Ear:",""))
    chooser.append(QApplication.translate("","Right",""))
    chooserOptions.append([QApplication.translate("","Sinusoid",""),
                           QApplication.translate("","Narrowband Noise","")])
    chooserLabel.append(QApplication.translate("","Signal Type:",""))
    chooser.append(QApplication.translate("","Sinusoid",""))
    
    prm = {}
    prm['field'] = field
    prm['fieldLabel'] = fieldLabel
    prm['chooser'] = chooser
    prm['chooserLabel'] = chooserLabel
    prm['chooserOptions'] =  chooserOptions

    return prm

def get_fields_to_hide_audiogram(parent):
    if parent.chooser[parent.prm['chooserLabel'].index(QApplication.translate("","Signal Type:",""))].currentText() == QApplication.translate("","Sinusoid",""):
        parent.fieldsToHide = [parent.prm['fieldLabel'].index(QApplication.translate("","Bandwidth (Hz)",""))]
    else:
        parent.fieldsToShow = [parent.prm['fieldLabel'].index(QApplication.translate("","Bandwidth (Hz)",""))]
    
def doTrial_audiogram(parent):

    currBlock = 'b'+ str(parent.prm['currentBlock'])
    if parent.prm['startOfBlock'] == True:
        parent.prm['additional_parameters_to_write'] = {}
        parent.prm['adaptiveParam'] = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(QApplication.translate("","Level (dB SPL)",""))]
        parent.prm['conditions'] = [str(parent.prm['adaptiveParam'])]

        parent.writeResultsHeader('log')
    parent.currentCondition = parent.prm['conditions'][0]
    frequency = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(QApplication.translate("","Frequency (Hz)",""))] 
    bandwidth = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(QApplication.translate("","Bandwidth (Hz)",""))] 
    phase = 0
    correctLevel = parent.prm['adaptiveParam']
    incorrectLevel = -200
    duration = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(QApplication.translate("","Duration (ms)",""))] 
    ramps = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(QApplication.translate("","Ramps (ms)",""))] 
    channel = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(QApplication.translate("","Ear:",""))]
    sndType = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(QApplication.translate("","Signal Type:",""))]

    if sndType == QApplication.translate("","Narrowband Noise",""):
        if bandwidth > 0:
            parent.stimulusCorrect = steepNoise(frequency-(bandwidth/2), frequency+(bandwidth/2), correctLevel - (10*log10(bandwidth)),
                                                duration, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
        else:
            parent.stimulusCorrect = pureTone(frequency, phase, correctLevel, duration, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
    elif sndType == QApplication.translate("","Sinusoid",""):
        parent.stimulusCorrect = pureTone(frequency, phase, correctLevel, duration, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
      
            
    parent.stimulusIncorrect = []
    for i in range((parent.prm['nIntervals']-1)):
        thisSnd = pureTone(frequency, phase, incorrectLevel, duration, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
        parent.stimulusIncorrect.append(thisSnd)
    parent.playRandomisedIntervals(parent.stimulusCorrect, parent.stimulusIncorrect)
