# -*- coding: utf-8 -*-

"""
This experiment can be used to measure thresholds for level discrimination.

"""

from ..pyqtver import*

if pyqtversion == 5:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtWidgets import QApplication
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtWidgets import QApplication
    
from pychoacoustics.sndlib import*
from .._version_info import*
from numpy import log10



def initialize_level_discrimination(prm):
    exp_name = QApplication.translate("","Level Discrimination","")
    prm["experimentsChoices"].append(exp_name)
    prm[exp_name] = {}
    prm[exp_name]["paradigmChoices"] = [QApplication.translate("","Transformed Up-Down",""),
                                        QApplication.translate("","Weighted Up-Down",""),
                                        QApplication.translate("","Constant m-Intervals n-Alternatives",""),
                                        QApplication.translate("","PEST",""),
                                        QApplication.translate("","PSI",""),
                                        QApplication.translate("","UML","")]

    prm[exp_name]["opts"] = ["hasISIBox", "hasAlternativesChooser", "hasFeedback",
                             "hasAltReps"]
    prm[exp_name]['defaultAdaptiveType'] = QApplication.translate("","Geometric","")
    prm[exp_name]['defaultNIntervals'] = 2
    prm[exp_name]['defaultNAlternatives'] = 2
    prm[exp_name]["execString"] = "level_discrimination"
    prm[exp_name]["version"] = __name__ + ' ' + pychoacoustics_version + ' ' + pychoacoustics_builddate

    return prm

def select_default_parameters_level_discrimination(parent, par):
   
    field = []
    fieldLabel = []
    chooser = []
    chooserLabel = []
    chooserOptions = []

    fieldLabel.append(parent.tr("Frequency (Hz)"))
    field.append(1000)

    fieldLabel.append(parent.tr("Pedestal Level (dB SPL)"))
    field.append(30)

    fieldLabel.append(parent.tr("Pedestal Spectrum Level (dB SPL)"))
    field.append(30)
    
    fieldLabel.append(parent.tr("Noise Low Frequency (Hz)"))
    field.append(1000)
    
    fieldLabel.append(parent.tr("Noise High Frequency (Hz)"))
    field.append(2000)
    
    fieldLabel.append(parent.tr("Delta L (dB)"))
    field.append(10)

    fieldLabel.append(parent.tr("Delta L Limit (dB)"))
    field.append(100)
    
    fieldLabel.append(parent.tr("Weber Fraction (dB)"))
    field.append(10)

    fieldLabel.append(parent.tr("Weber Fraction Limit (dB)"))
    field.append(100)
    
    fieldLabel.append(parent.tr("Duration (ms)"))
    field.append(180)
    
    fieldLabel.append(parent.tr("Ramps (ms)"))
    field.append(10)
    
    fieldLabel.append(parent.tr("Noise 1 Low Frequency (Hz)"))
    field.append(0)
    
    fieldLabel.append(parent.tr("Noise 1 High Frequency (Hz)"))
    field.append(1000)
    
    fieldLabel.append(parent.tr("Noise 1 Spectrum Level (dB SPL)"))
    field.append(20)
    
    fieldLabel.append(parent.tr("Noise 2 Low Frequency (Hz)"))
    field.append(2000)
    
    fieldLabel.append(parent.tr("Noise 2 High Frequency (Hz)"))
    field.append(3000)
    
    fieldLabel.append(parent.tr("Noise 2 Spectrum Level (dB SPL)"))
    field.append(20)
        
    
    chooserOptions.append([parent.tr("Right"), parent.tr("Left"), parent.tr("Both")])
    chooserLabel.append(parent.tr("Ear:"))
    chooser.append(parent.tr("Both"))
    chooserOptions.append([parent.tr("Sinusoid"), parent.tr("Noise")])
    chooserLabel.append(parent.tr("Signal Type:"))
    chooser.append(parent.tr("Noise"))
    chooserOptions.append([parent.tr("White"), parent.tr("Pink"), parent.tr("None")])
    chooserLabel.append(parent.tr("Additional Noise:"))
    chooser.append(parent.tr("None"))
    chooserOptions.append([parent.tr("Delta L"), parent.tr("Weber Fraction")])
    chooserLabel.append(parent.tr("JND:"))
    chooser.append(parent.tr("Delta L"))
    
    prm = {}
    prm['field'] = field
    prm['fieldLabel'] = fieldLabel
    prm['chooser'] = chooser
    prm['chooserLabel'] = chooserLabel
    prm['chooserOptions'] =  chooserOptions

    return prm

def get_fields_to_hide_level_discrimination(parent):
    if parent.chooser[parent.prm['chooserLabel'].index(parent.tr("JND:"))].currentText() == parent.tr("Delta L"):
        parent.fieldsToHide = [parent.prm['fieldLabel'].index(parent.tr("Weber Fraction (dB)")),
                               parent.prm['fieldLabel'].index(parent.tr("Weber Fraction Limit (dB)"))]
        parent.fieldsToShow = [parent.prm['fieldLabel'].index(parent.tr("Delta L (dB)")),
                               parent.prm['fieldLabel'].index(parent.tr("Delta L Limit (dB)"))]
    elif parent.chooser[parent.prm['chooserLabel'].index(parent.tr("JND:"))].currentText() == parent.tr("Weber Fraction"):
        parent.fieldsToHide = [parent.prm['fieldLabel'].index(parent.tr("Delta L (dB)")),
                               parent.prm['fieldLabel'].index(parent.tr("Delta L Limit (dB)"))]
        parent.fieldsToShow = [parent.prm['fieldLabel'].index(parent.tr("Weber Fraction (dB)")),
                               parent.prm['fieldLabel'].index(parent.tr("Weber Fraction Limit (dB)"))]

    if parent.chooser[parent.prm['chooserLabel'].index(parent.tr("Signal Type:"))].currentText() == parent.tr("Noise"):
        parent.fieldsToShow.extend([parent.prm['fieldLabel'].index(parent.tr("Noise Low Frequency (Hz)")),
                                    parent.prm['fieldLabel'].index(parent.tr("Noise High Frequency (Hz)")),
                                    parent.prm['fieldLabel'].index(parent.tr("Pedestal Spectrum Level (dB SPL)"))])
        parent.fieldsToHide.extend([parent.prm['fieldLabel'].index(parent.tr("Pedestal Level (dB SPL)")),
                                    parent.prm['fieldLabel'].index(parent.tr("Frequency (Hz)"))])
    elif parent.chooser[parent.prm['chooserLabel'].index(parent.tr("Signal Type:"))].currentText() == parent.tr("Sinusoid"):
        parent.fieldsToShow.extend([parent.prm['fieldLabel'].index(parent.tr("Pedestal Level (dB SPL)")),
                                    parent.prm['fieldLabel'].index(parent.tr("Frequency (Hz)"))])
        parent.fieldsToHide.extend([parent.prm['fieldLabel'].index(parent.tr("Noise Low Frequency (Hz)")),
                                    parent.prm['fieldLabel'].index(parent.tr("Noise High Frequency (Hz)")),
                                    parent.prm['fieldLabel'].index(parent.tr("Pedestal Spectrum Level (dB SPL)"))])

    if parent.chooser[parent.prm['chooserLabel'].index(parent.tr("Additional Noise:"))].currentText() == parent.tr("None"):
        parent.fieldsToHide.extend([parent.prm['fieldLabel'].index(parent.tr("Noise 1 Low Frequency (Hz)")),
                                    parent.prm['fieldLabel'].index(parent.tr("Noise 1 High Frequency (Hz)")),
                                    parent.prm['fieldLabel'].index(parent.tr("Noise 1 Spectrum Level (dB SPL)")),
                                    parent.prm['fieldLabel'].index(parent.tr("Noise 2 Low Frequency (Hz)")),
                                    parent.prm['fieldLabel'].index(parent.tr("Noise 2 High Frequency (Hz)")),
                                    parent.prm['fieldLabel'].index(parent.tr("Noise 2 Spectrum Level (dB SPL)"))])
    else:
        parent.fieldsToShow.extend([parent.prm['fieldLabel'].index(parent.tr("Noise 1 Low Frequency (Hz)")),
                                    parent.prm['fieldLabel'].index(parent.tr("Noise 1 High Frequency (Hz)")),
                                    parent.prm['fieldLabel'].index(parent.tr("Noise 1 Spectrum Level (dB SPL)")),
                                    parent.prm['fieldLabel'].index(parent.tr("Noise 2 Low Frequency (Hz)")),
                                    parent.prm['fieldLabel'].index(parent.tr("Noise 2 High Frequency (Hz)")),
                                    parent.prm['fieldLabel'].index(parent.tr("Noise 2 Spectrum Level (dB SPL)"))])
def doTrial_level_discrimination(parent):

    currBlock = 'b'+ str(parent.prm['currentBlock'])
    if parent.prm['startOfBlock'] == True:
        parent.prm['additional_parameters_to_write'] = {}
        if parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(parent.tr("JND:"))] == parent.tr("Delta L"):
            parent.prm['adaptiveParam'] = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Delta L (dB)"))]
        elif parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(parent.tr("JND:"))] == parent.tr("Weber Fraction"):
            parent.prm['adaptiveParam'] = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Weber Fraction (dB)"))]
        parent.prm['conditions'] = [str(parent.prm['adaptiveParam'])]

        parent.writeResultsHeader('log')
    parent.currentCondition = parent.prm['conditions'][0]
    frequency = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Frequency (Hz)"))] 

    phase = 0

    noiseLoFreq = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Noise Low Frequency (Hz)"))]
    noiseHiFreq = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Noise High Frequency (Hz)"))]
    incorrectLevelSin = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Pedestal Level (dB SPL)"))]
    incorrectLevelNoise = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Pedestal Spectrum Level (dB SPL)"))]
    deltaLLimit = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Delta L Limit (dB)"))]
    weberFractionLimit = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Weber Fraction Limit (dB)"))]
    duration = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Duration (ms)"))] 
    ramps = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Ramps (ms)"))]
    noise1LowFreq       = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Noise 1 Low Frequency (Hz)"))]
    noise1HighFreq      = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Noise 1 High Frequency (Hz)"))]
    noise1SpectrumLevel = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Noise 1 Spectrum Level (dB SPL)"))]
    noise2LowFreq       = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Noise 2 Low Frequency (Hz)"))]
    noise2HighFreq      = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Noise 2 High Frequency (Hz)"))]
    noise2SpectrumLevel = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Noise 2 Spectrum Level (dB SPL)"))]
    
    channel   = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(parent.tr("Ear:"))]
    sndType   = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(parent.tr("Signal Type:"))]
    noiseType = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(parent.tr("Additional Noise:"))]

    altReps = parent.prm['altReps']
    altRepsISI = parent.prm['altRepsISI']
    lowStop = 0.8
    highStop = 1.2
    
    if sndType == parent.tr("Sinusoid"):
        incorrectLevel = incorrectLevelSin
    elif sndType == parent.tr("Noise"):
        incorrectLevel = incorrectLevelNoise
 
    if parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(parent.tr("JND:"))] == parent.tr("Delta L"):
        if parent.prm['adaptiveParam'] < -deltaLLimit:
            parent.prm['adaptiveParam'] = -deltaLLimit
        elif  parent.prm['adaptiveParam'] > deltaLLimit:
            parent.prm['adaptiveParam'] = deltaLLimit
        correctLevel = incorrectLevel + parent.prm['adaptiveParam']
    if parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(parent.tr("JND:"))] == parent.tr("Weber Fraction"):
        if  parent.prm['adaptiveParam'] > weberFractionLimit:
            parent.prm['adaptiveParam'] = weberFractionLimit
        # correct level computation for Weber:
        # L = level
        # I = 10*(L/10)
        # DW = 10*log10(DI/I)
        # so DI = 10^(DW/10) * I
        # and the intensity of the comparison is:
        # I + DI = 10^(L/10) + 10^(L/10) * 10^(DW/10) = 10^(L/10) * (1 + 10^(DW/10))
        #and the level of the comparison
        # 10*log10(I+DI) = 10*log10(10^(L/10) * (1 + 10^(DW/10)))
        correctLevel = 10*log10(10**(incorrectLevel/10) * (1 + 10**(parent.prm['adaptiveParam']/10)))
       
    if altReps == 0:
        nCorrectTones = 1
        nIncorrectTones = parent.prm['nIntervals']-1
    else:
        nCorrectTones = altReps
        nIncorrectTones = (parent.prm['nIntervals']-1)*altReps*2 + altReps
    correctTones = []; incorrectTones = []


    nSamples = int(round(duration/1000 * parent.prm['sampRate']))
    nRamp = int(round(ramps/1000 * parent.prm['sampRate']))
    nTot = nSamples + (nRamp * 2)

    for nt in range(nCorrectTones):
        if sndType == parent.tr("Noise"):
            thisStim = broadbandNoise(correctLevel, duration+ramps*2+20, 0,
                                                    channel, parent.prm['sampRate'],
                                                    parent.prm['maxLevel'])
            thisStim = fir2Filt(noiseLoFreq*lowStop, noiseLoFreq,
                                              noiseHiFreq, noiseHiFreq*highStop,
                                              thisStim, parent.prm['sampRate'])
            thisStim = thisStim[int(round(0.01*parent.prm['sampRate'])):int(round(0.01*parent.prm['sampRate']))+nTot,]
            thisStim = gate(ramps, thisStim, parent.prm['sampRate'])

        elif sndType == parent.tr("Sinusoid"):
            thisStim = pureTone(frequency, phase, correctLevel, duration,
                                              ramps, channel, parent.prm['sampRate'],
                                              parent.prm['maxLevel'])
        if noiseType != parent.tr("None"):
            noise = broadbandNoise(noise1SpectrumLevel, duration + ramps*2+20, 0, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
            if noiseType == parent.tr("Pink"):
                noise = makePink(noise, parent.prm['sampRate'])
            noise1 = fir2Filt(noise1LowFreq*lowStop, noise1LowFreq, noise1HighFreq, noise1HighFreq*highStop, noise, parent.prm['sampRate'])
            noise2 = scale(noise2SpectrumLevel - noise1SpectrumLevel, noise)
            noise2 = fir2Filt(noise2LowFreq*lowStop, noise2LowFreq, noise2HighFreq, noise2HighFreq*highStop, noise2, parent.prm['sampRate'])
            noise = noise1 + noise2
            noise = noise[int(round(0.01*parent.prm['sampRate'])):int(round(0.01*parent.prm['sampRate']))+thisStim.shape[0],]
            noise = gate(ramps, noise, parent.prm['sampRate'])
            thisStim = thisStim + noise
        correctTones.append(thisStim)


    for i in range(nIncorrectTones):
        if sndType == parent.tr("Noise"):
            thisSnd = broadbandNoise(incorrectLevel, duration+ramps*2+20, 0,
                                     channel, parent.prm['sampRate'],
                                     parent.prm['maxLevel'])
            thisSnd = fir2Filt(noiseLoFreq*lowStop, noiseLoFreq,
                               noiseHiFreq, noiseHiFreq*highStop,
                               thisSnd, parent.prm['sampRate'])
            thisSnd = thisSnd[int(round(0.01*parent.prm['sampRate'])):int(round(0.01*parent.prm['sampRate']))+nTot,]
            thisSnd = gate(ramps, thisSnd, parent.prm['sampRate'])
        elif sndType == parent.tr("Sinusoid"):
            thisSnd = pureTone(frequency, phase, incorrectLevel, duration, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])

        if noiseType != parent.tr("None"):
            noise = broadbandNoise(noise1SpectrumLevel, duration + ramps*2+20, 0, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
            if noiseType == parent.tr("Pink"):
                noise = makePink(noise, parent.prm['sampRate'])
            noise1 = fir2Filt(noise1LowFreq*lowStop, noise1LowFreq, noise1HighFreq, noise1HighFreq*highStop, noise, parent.prm['sampRate'])
            noise2 = scale(noise2SpectrumLevel - noise1SpectrumLevel, noise)
            noise2 = fir2Filt(noise2LowFreq*lowStop, noise2LowFreq, noise2HighFreq, noise2HighFreq*highStop, noise2, parent.prm['sampRate'])
            noise = noise1 + noise2
            noise = noise[int(round(0.01*parent.prm['sampRate'])):int(round(0.01*parent.prm['sampRate']))+thisSnd.shape[0],]
            noise = gate(ramps, noise, parent.prm['sampRate'])
            thisSnd = thisSnd + noise

        incorrectTones.append(thisSnd)

    if altReps == 0:
        parent.stimulusCorrect = correctTones[0]
        parent.stimulusIncorrect = incorrectTones
    else:
        altRepsSilence = makeSilence(altRepsISI, parent.prm['sampRate'])
        sCorr = concatenate((incorrectTones.pop(), altRepsSilence, correctTones.pop()), axis=0)
        for i in range(altReps-1):
            sCorr = concatenate((sCorr, altRepsSilence, incorrectTones.pop(), altRepsSilence, correctTones.pop()), axis=0)
        parent.stimulusCorrect = sCorr

        parent.stimulusIncorrect = []
        for i in range(parent.prm['nIntervals']-1):
            sIncorr = concatenate((incorrectTones.pop(), altRepsSilence, incorrectTones.pop()), axis=0)
            for i in range(altReps-1):
                sIncorr = concatenate((sIncorr, altRepsSilence, incorrectTones.pop(), altRepsSilence, incorrectTones.pop()), axis=0)
            parent.stimulusIncorrect.append(sIncorr)
  
    parent.playRandomisedIntervals(parent.stimulusCorrect, parent.stimulusIncorrect)
