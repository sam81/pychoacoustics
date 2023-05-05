# -*- coding: utf-8 -*-

"""
This experiment can be used to measure thresholds for detecting a signal in quiet.
The signal can be either a pure tone or a narrow-band noise. Several signal frequencies
can be tested within the same block of trials.

The available fields are:

- Frequency (Hz) :
    Signal center frequency in Hz
- Bandwidth (Hz) :
    The bandwidth of the signal in Hz (only applicable
    if signal type is Narrowband Noise)
- Level (dB SPL) :
    Signal level (for constant procedures), or starting signal level (for adaptive procedures), in dB SPL
- Duration (ms) :
    Signal duration (excluding ramps), in ms
- Ramps (ms) :
    Duration of each ramp, in ms

The available choosers are:

- Ear:         [``Right``, ``Left``, ``Both``]
    The ear to which the signal will be presented
- Signal Type: [``Sinusoid``, ``Narrowband Noise``]
    The signal type. If ``Sinusoid`` the signal will be a pure tone,
    if ``Narrowband Noise``, the signal will be a narrow-band noise

"""

from ..pyqtver import*

if pyqtversion == 5:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtWidgets import QApplication
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtWidgets import QApplication

from .._version_info import*
from ..sndlib import*
from numpy import log10
                                                                            

def initialize_audiogram_mf(prm):
    exp_name = QApplication.translate("","Demo Audiogram Multiple Frequencies","")
    prm["experimentsChoices"].append(exp_name)
    prm[exp_name] = {}
    prm[exp_name]["paradigmChoices"] = [QApplication.translate("","Transformed Up-Down Interleaved",""),
                                        QApplication.translate("","Weighted Up-Down Interleaved",""),
                                        QApplication.translate("","Multiple Constants m-Intervals n-Alternatives","")]
                                                                                                   
                                                                                                   
    prm[exp_name]["opts"] = ["hasISIBox", "hasAlternativesChooser", "hasFeedback",
                             "hasNTracksChooser"]
    prm[exp_name]['defaultAdaptiveType'] = QApplication.translate("","Arithmetic","")
    prm[exp_name]['defaultNIntervals'] = 2
    prm[exp_name]['defaultNAlternatives'] = 2
    prm[exp_name]['defaultNTracks'] = 4
    
    prm[exp_name]["execString"] = "audiogram_mf"
    prm[exp_name]["version"] = __name__ + ' ' + pychoacoustics_version + ' ' + pychoacoustics_builddate
    
    return prm

def select_default_parameters_audiogram_mf(parent, par):
   
    nDifferences = par['nDifferences']
   
    field = []
    fieldLabel = []
    chooser = []
    chooserLabel = []
    chooserOptions = []

    for i in range(nDifferences):
        fieldLabel.append(parent.tr("Frequency (Hz) " + str(i+1)))
        field.append(1000+1000*i)
        fieldLabel.append(QApplication.translate("","Level (dB SPL) " + str(i+1),""))
        field.append(50)
    
    fieldLabel.append(QApplication.translate("","Bandwidth (Hz)",""))
    field.append(10)
    
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
    chooserLabel.append(QApplication.translate("","Type:",""))
    chooser.append(QApplication.translate("","Sinusoid",""))

    prm = {}
    prm['field'] = field
    prm['fieldLabel'] = fieldLabel
    prm['chooser'] = chooser
    prm['chooserLabel'] = chooserLabel
    prm['chooserOptions'] =  chooserOptions

    return prm

def get_fields_to_hide_audiogram_mf(parent):
    if parent.chooser[parent.prm['chooserLabel'].index(QApplication.translate("","Type:",""))].currentText() == QApplication.translate("","Sinusoid",""):
        parent.fieldsToHide = [parent.prm['fieldLabel'].index(QApplication.translate("","Bandwidth (Hz)",""))]
    else:
        parent.fieldsToShow = [parent.prm['fieldLabel'].index(QApplication.translate("","Bandwidth (Hz)",""))]
    
def doTrial_audiogram_mf(parent):
    currBlock = 'b'+ str(parent.prm['currentBlock'])
    nDifferences = parent.prm['nDifferences']
    frequency = []
    if parent.prm['startOfBlock'] == True:
        parent.prm['additional_parameters_to_write'] = {}
        parent.prm['conditions'] = []
        parent.prm['adaptiveParam'] = []
        for i in range(nDifferences):
            parent.prm['conditions'].append(str(parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(QApplication.translate("","Frequency (Hz) " + str(i+1),""))]))
            parent.prm['adaptiveParam'].append(parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(QApplication.translate("","Level (dB SPL) " + str(i+1),""))])
        parent.writeResultsHeader('log')

    for i in range(nDifferences):
        frequency.append(parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(QApplication.translate("","Frequency (Hz) " + str(i+1),""))])

    #these fields are necessary for the two procedures (multiple constants, adaptive interleaved)
    parent.currentCondition = parent.prm['conditions'][parent.prm['currentDifference']] #this is necessary for counting correct/total trials
    correctLevel = parent.prm['adaptiveParam'][parent.prm['currentDifference']]
    
    currentFrequency = frequency[parent.prm['currentDifference']]
    bandwidth = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(QApplication.translate("","Bandwidth (Hz)",""))] 
    phase = 0
    
    incorrectLevel = -200
    duration = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(QApplication.translate("","Duration (ms)",""))] 
    ramps = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(QApplication.translate("","Ramps (ms)",""))] 
    channel = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(QApplication.translate("","Ear:",""))]
    sndType = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(QApplication.translate("","Type:",""))]

    if sndType == QApplication.translate("","Narrowband Noise",""):
        if bandwidth > 0:
            parent.stimulusCorrect = steepNoise(currentFrequency-(bandwidth/2), currentFrequency+(bandwidth/2), correctLevel - (10*log10(bandwidth)),
                                                duration, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
        else:
            parent.stimulusCorrect = pureTone(currentFrequency, phase, correctLevel, duration, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
    elif sndType == QApplication.translate("","Sinusoid",""):
        parent.stimulusCorrect = pureTone(currentFrequency, phase, correctLevel, duration, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
      
            
    parent.stimulusIncorrect = []
    for i in range((parent.prm['nIntervals']-1)):
        thisSnd = pureTone(currentFrequency, phase, incorrectLevel, duration, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
        parent.stimulusIncorrect.append(thisSnd)
    parent.playRandomisedIntervals(parent.stimulusCorrect, parent.stimulusIncorrect)
