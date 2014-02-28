# -*- coding: utf-8 -*-

"""
Measure thresholds for the detection of differences in
fundamental frequency (F0) between two tones. Different tone
types are supported, including harmonic complex tones, narrowband-noise
complex tones, complex dichotic-pitch tones and iterated rippled noise.


The available fields are:

- F0 (Hz) :
    Fundamental frequency of the standard tones.
- Lower F0 (Hz) :
    Lowest F0 in case of F0 roving
- Upper F0 :
    Highest F0 in case of F0 roving
- Starting Difference (%) : 
    Starting F0 difference between standard and comparison stimuli in percent of the standard F0
- Delta F0 Limit (%)
    Maximum F0 difference allowed between standard and comparison stimuli in percent of the standard F0
- Bandwidth (Hz)
    Width of each harmonic band for narrowband noise and Huggins pitch, in Hz
- Bandwidth (Cents)
    Width of each harmonic band for narrowband noise 2 and simple dichotic pitch, in cents
- Spacing (Cents)
    Spacing in cents between the random-phase sinusoids used for constructing dichotic-pitch or narrowband noise 2 stimuli
- ITD (micro s)
    Interaural time difference of the decorralated frequency bands of dichotic pitch stimuli, in micro seconds
- IPD (radians)
    Interaural phase difference of the decorralated frequency bands of dichotic pitch stimuli
- Narrow Band Component Level (dB SPL)
    Level of the harmonic narrow-noise bands of narrowband noise 2 stimuli
- Iterations :
    Number of delay-add iteration for IRN generation
- Gain:
    Gain applied to dealyed version of the signal in IRN generation
- Low Harmonic: 
    Lowest harmonic number
- High Harmonic:
    Highest harmonic number
- Low Freq. (Hz):
    Low frequency cutoff for filter applied to the tone
- High Freq. (Hz):
    High frequency cutoff for filter applied to the tone
- Low Stop:
    
- High Stop:
    
- Harmonic Level (dB SPL):
    Level of each harmonic in dB SPL
- Spectrum Level (dB SPL):
    
- Component Level (dB SPL):

- Duration (ms) :
    Tone duration (excluding ramps), in ms
- Ramps (ms) :
    Duration of each ramp, in ms
    
- Noise 1 Low Freq. (Hz):
    Low-frequency cutoff for the first noise band 
- Noise 1 High Freq. (Hz):
    High-frequency cutoff for the first noise band
- Noise 1 S. Level (dB SPL):
    Spectrum level of the first noise band in dB SPL
- Noise 2 Low Freq. (Hz):
    Low-frequency cutoff for the second noise band 
- Noise 2 High Freq. (Hz):
    High-frequency cutoff for the second noise band
- Noise 2 S. Level (dB SPL):
    Spectrum level of the second noise band in dB SPL
- Stretch (%)'
    Stretch to apply to each harmonic, in percentage of the harmonic frequency
    

The available choosers are:

- Ear: [``Right``, ``Left``, ``Both``]
    The ear to which the signal will be presented

"""

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
from numpy import ceil, floor

                                                                                         
def initialize_F0DL(prm):
    exp_name = QApplication.translate("","F0DL","")
    prm["experimentsChoices"].append(exp_name)
    prm[exp_name] = {}
    prm[exp_name]["paradigmChoices"] = [QApplication.translate("","Transformed Up-Down",""),
                                        QApplication.translate("","Weighted Up-Down",""),
                                        QApplication.translate("","Constant m-Intervals n-Alternatives",""),
                                        QApplication.translate("","PEST","")]
    prm[exp_name]["opts"] = ["hasISIBox", "hasAlternativesChooser", "hasFeedback", "hasIntervalLights"]
    prm[exp_name]['defaultAdaptiveType'] = QApplication.translate("","Geometric","")
    prm[exp_name]['defaultNIntervals'] = 2
    prm[exp_name]['defaultNAlternatives'] = 2
    prm[exp_name]["execString"] = "F0DL"
    prm[exp_name]["version"] = __name__ + ' ' + pychoacoustics_version + ' ' + pychoacoustics_builddate
    #prm[exp_name]["version"] = __name__ + ' ' + labexp_version + ' ' + labexp_builddate
    
    return prm

def select_default_parameters_F0DL(parent, par):
   
    field = []
    fieldLabel = []
    chooser = []
    chooserLabel = []
    chooserOptions = []
    
    fieldLabel.append( parent.tr("F0 (Hz)"))
    field.append(440)
    
    fieldLabel.append( parent.tr("Lower F0 (Hz)"))
    field.append(396)
    
    fieldLabel.append(parent.tr("Upper F0 (Hz)"))
    field.append(484)
    
    fieldLabel.append(parent.tr("Starting Difference (%)"))
    field.append(20)
    
    fieldLabel.append(parent.tr("Delta F0 Limit (%)"))
    field.append(200)
    
    fieldLabel.append(parent.tr("Bandwidth (Hz)"))
    field.append(50)
    
    fieldLabel.append(parent.tr("Bandwidth (Cents)"))
    field.append(100)

    fieldLabel.append(parent.tr("Bandwidth (ERBs)"))
    field.append(1)
    
    fieldLabel.append(parent.tr("ITD (micro s)"))
    field.append(320)
    
    fieldLabel.append(parent.tr("IPD (radians)"))
    field.append(3.14159)#265)
    
    fieldLabel.append(parent.tr("Iterations"))
    field.append(16)
    
    fieldLabel.append(parent.tr("Gain"))
    field.append(1)
    
    fieldLabel.append( parent.tr("Low Harmonic"))
    field.append(1)
    
    fieldLabel.append(parent.tr("High Harmonic"))
    field.append(20)
    
    fieldLabel.append(parent.tr("Low Freq. (Hz)"))
    field.append(0)
    
    fieldLabel.append( parent.tr("High Freq. (Hz)"))
    field.append(2000)
    
    fieldLabel.append( parent.tr("Low Stop"))
    field.append(0.8)
    
    fieldLabel.append( parent.tr("High Stop"))
    field.append(1.2)
    
    fieldLabel.append(parent.tr("Harmonic Level (dB SPL)"))
    field.append(50)
    
    fieldLabel.append(parent.tr("Spectrum Level (dB SPL)"))
    field.append(50)
    
    fieldLabel.append(parent.tr("Duration (ms)"))
    field.append(180)
    
    fieldLabel.append(parent.tr("Ramp (ms)"))
    field.append(10)
    
    fieldLabel.append(parent.tr("Noise 1 Low Freq. (Hz)"))
    field.append(0)
    
    fieldLabel.append( parent.tr("Noise 1 High Freq. (Hz)"))
    field.append(1000)
    
    fieldLabel.append(parent.tr("Noise 1 S. Level (dB SPL)"))
    field.append(-200)
    
    fieldLabel.append(parent.tr("Noise 2 Low Freq. (Hz)"))
    field.append(2000)
    
    fieldLabel.append(parent.tr("Noise 2 High Freq. (Hz)"))
    field.append(3000)
    
    fieldLabel.append(parent.tr("Noise 2 S. Level (dB SPL)"))
    field.append(-200)
    
    fieldLabel.append(parent.tr("Stretch (%)"))
    field.append(0)
    

       
    chooserOptions.append([parent.tr("Right"), parent.tr("Left"), parent.tr("Both"), parent.tr("Odd Left"), parent.tr("Odd Right")])
    chooserLabel.append(parent.tr("Ear:"))
    chooser.append(parent.tr("Both"))

    chooserOptions.append([parent.tr("Sinusoid"), parent.tr("Narrowband Noise"), parent.tr("IRN"), parent.tr("Huggins Pitch")])
    chooserLabel.append(parent.tr("Type:"))
    chooser.append(parent.tr("Sinusoid"))

    chooserOptions.append([parent.tr("Sine"), parent.tr("Cosine"), parent.tr("Alternating"), parent.tr("Schroeder"), parent.tr("Random")])
    chooserLabel.append(parent.tr("Phase:"))
    chooser.append(parent.tr("Sine"))

    chooserOptions.append([parent.tr("White"), parent.tr("Pink"), parent.tr("None")])
    chooserLabel.append(parent.tr("Noise Type:"))
    chooser.append(parent.tr("White"))

    chooserOptions.append([parent.tr("Yes"), parent.tr("No")])
    chooserLabel.append(parent.tr("Fix Spectrum Level:"))
    chooser.append(parent.tr("No"))

    chooserOptions.append([parent.tr("With F0"), parent.tr("No")])
    chooserLabel.append(parent.tr("Vary Harm. No.:"))
    chooser.append(parent.tr("No"))

    chooserOptions.append([parent.tr("Add Same"), parent.tr("Add Original")])
    chooserLabel.append(parent.tr("IRN Type:"))
    chooser.append(parent.tr("Add Same"))

    chooserOptions.append([parent.tr("Hz"), parent.tr("Cent"), parent.tr("ERB")])
    chooserLabel.append(parent.tr("Bandwidth Unit:"))
    chooser.append(parent.tr("Hz"))

    chooserOptions.append([parent.tr("NoSpi"), parent.tr("NpiSo")])
    chooserLabel.append(parent.tr("Phase relationship:"))
    chooser.append(parent.tr("NoSpi"))

    chooserOptions.append([parent.tr("IPD Stepped"), parent.tr("IPD Linear"), parent.tr("IPD Random"), parent.tr("ITD")])
    chooserLabel.append(parent.tr("Dichotic Difference:"))
    chooser.append( parent.tr("IPD Stepped"))

    chooserOptions.append([parent.tr("No"), parent.tr("Yes - Log"), parent.tr("Yes - Linear")])
    chooserLabel.append(parent.tr("Roving:"))
    chooser.append(parent.tr("No"))

    chooserOptions.append([parent.tr("Harmonic"), parent.tr("Harmonic Stretched")])
    chooserLabel.append(parent.tr("Harmonicity:"))
    chooser.append(parent.tr("Harmonic"))
   

    prm = {}
  
    prm['field'] = field
    prm['fieldLabel'] = fieldLabel
    prm['chooser'] = chooser
    prm['chooserLabel'] = chooserLabel
    prm['chooserOptions'] =  chooserOptions

    return prm

def get_fields_to_hide_F0DL(parent):
    if parent.chooser[parent.prm['chooserLabel'].index(parent.tr("Type:"))].currentText() == parent.tr("Sinusoid"):
        parent.fieldsToHide = [parent.prm['fieldLabel'].index(parent.tr("Bandwidth (Hz)")),
                               parent.prm['fieldLabel'].index(parent.tr("Bandwidth (Cents)")),
                               parent.prm['fieldLabel'].index(parent.tr("Bandwidth (ERBs)")),
                               parent.prm['fieldLabel'].index(parent.tr("ITD (micro s)")),
                               parent.prm['fieldLabel'].index(parent.tr("IPD (radians)")),
                               parent.prm['fieldLabel'].index(parent.tr("Iterations")),
                               parent.prm['fieldLabel'].index(parent.tr("Gain")),
                               parent.prm['fieldLabel'].index(parent.tr("Spectrum Level (dB SPL)"))]
        parent.fieldsToShow = [parent.prm['fieldLabel'].index(parent.tr("Harmonic Level (dB SPL)"))]
        parent.choosersToHide = [parent.prm['chooserLabel'].index(parent.tr("IRN Type:")),
                                 parent.prm['chooserLabel'].index(parent.tr("Bandwidth Unit:")),
                                 parent.prm['chooserLabel'].index(parent.tr("Phase relationship:")),
                                 parent.prm['chooserLabel'].index(parent.tr("Dichotic Difference:"))]
        parent.choosersToShow = [parent.prm['chooserLabel'].index(parent.tr("Ear:")),
                                 parent.prm['chooserLabel'].index(parent.tr("Phase:")), #sine cos schroeder, etc
                                 parent.prm['chooserLabel'].index(parent.tr("Noise Type:")), #white, pink
                                 parent.prm['chooserLabel'].index(parent.tr("Fix Spectrum Level:")), #fixed, non-fixed
                                 parent.prm['chooserLabel'].index(parent.tr("Vary Harm. No.:")), # with F0, no
                                 parent.prm['chooserLabel'].index(parent.tr("Harmonicity:"))] #Harmonic, stretched
          
    elif parent.chooser[parent.prm['chooserLabel'].index(parent.tr("Type:"))].currentText() == parent.tr("Narrowband Noise"): 
        parent.fieldsToHide = [parent.prm['fieldLabel'].index(parent.tr("ITD (micro s)")),
                               parent.prm['fieldLabel'].index(parent.tr("IPD (radians)")),
                               parent.prm['fieldLabel'].index(parent.tr("Iterations")),
                               parent.prm['fieldLabel'].index(parent.tr("Gain")),
                               parent.prm['fieldLabel'].index(parent.tr("Harmonic Level (dB SPL)"))]
        parent.fieldsToShow = [parent.prm['fieldLabel'].index(parent.tr("Spectrum Level (dB SPL)"))]
        parent.choosersToHide = [parent.prm['chooserLabel'].index(parent.tr("Phase:")), #sine cos schroeder, etc
                                 parent.prm['chooserLabel'].index(parent.tr("IRN Type:")),
                                 parent.prm['chooserLabel'].index(parent.tr("Phase relationship:")), #NoSpi, NpiSo
                                 parent.prm['chooserLabel'].index(parent.tr("Dichotic Difference:"))] #IPD, ITD
        parent.choosersToShow = [parent.prm['chooserLabel'].index(parent.tr("Ear:")),
                                 parent.prm['chooserLabel'].index(parent.tr("Noise Type:")), #white, pink
                                 parent.prm['chooserLabel'].index(parent.tr("Bandwidth Unit:")),
                                 parent.prm['chooserLabel'].index(parent.tr("Fix Spectrum Level:")), #fixed, non-fixed
                                 parent.prm['chooserLabel'].index(parent.tr("Vary Harm. No.:")), # with F0, no
                                 parent.prm['chooserLabel'].index(parent.tr("Harmonicity:"))] #Harmonic, stretched

    elif parent.chooser[parent.prm['chooserLabel'].index(parent.tr("Type:"))].currentText() == parent.tr("IRN"):
        parent.fieldsToHide = [parent.prm['fieldLabel'].index(parent.tr("Low Harmonic")),
                               parent.prm['fieldLabel'].index(parent.tr("High Harmonic")),
                               parent.prm['fieldLabel'].index(parent.tr("Bandwidth (Hz)")),
                               parent.prm['fieldLabel'].index(parent.tr("Bandwidth (Cents)")),
                               parent.prm['fieldLabel'].index(parent.tr("Bandwidth (ERBs)")),
                               parent.prm['fieldLabel'].index(parent.tr("ITD (micro s)")),
                               parent.prm['fieldLabel'].index(parent.tr("IPD (radians)")),
                               parent.prm['fieldLabel'].index(parent.tr("Harmonic Level (dB SPL)")),
                               parent.prm['fieldLabel'].index(parent.tr("Stretch (%)"))]
        parent.fieldsToShow = [parent.prm['fieldLabel'].index(parent.tr("Iterations")),
                               parent.prm['fieldLabel'].index(parent.tr("Gain")),
                               parent.prm['fieldLabel'].index(parent.tr("Spectrum Level (dB SPL)"))]
        parent.choosersToShow = [parent.prm['chooserLabel'].index(parent.tr("Ear:")), #left, right, both, odd left, odd right
                                 parent.prm['chooserLabel'].index(parent.tr("Noise Type:")), #white, pink
                                 parent.prm['chooserLabel'].index(parent.tr("IRN Type:"))]
        parent.choosersToHide = [parent.prm['chooserLabel'].index(parent.tr("Phase:")), #sine cos schroeder, etc
                                 parent.prm['chooserLabel'].index(parent.tr("Fix Spectrum Level:")), #fixed, non-fixed
                                 parent.prm['chooserLabel'].index(parent.tr("Vary Harm. No.:")), # with F0, no
                                 parent.prm['chooserLabel'].index(parent.tr("Phase relationship:")), #NoSpi, NpiSo
                                 parent.prm['chooserLabel'].index(parent.tr("Bandwidth Unit:")),
                                 parent.prm['chooserLabel'].index(parent.tr("Dichotic Difference:")), #IPD, ITD
                                 parent.prm['chooserLabel'].index(parent.tr("Harmonicity:"))] #Harmonic, stretched
                          
                          
    elif parent.chooser[parent.prm['chooserLabel'].index(parent.tr("Type:"))].currentText() == parent.tr("Huggins Pitch"):
        parent.fieldsToHide = [parent.prm['fieldLabel'].index(parent.tr("Iterations")),
                               parent.prm['fieldLabel'].index(parent.tr("Gain")),
                               parent.prm['fieldLabel'].index(parent.tr("Harmonic Level (dB SPL)"))]
        parent.fieldsToShow = [parent.prm['fieldLabel'].index(parent.tr("Spectrum Level (dB SPL)"))]
        parent.choosersToShow = [parent.prm['chooserLabel'].index(parent.tr("Phase relationship:")), #NoSpi, NpiSo
                                 parent.prm['chooserLabel'].index(parent.tr("Harmonicity:")),
                                 parent.prm['chooserLabel'].index(parent.tr("Bandwidth Unit:")),
                                 parent.prm['chooserLabel'].index(parent.tr("Dichotic Difference:"))] #IPD stepped, IPD linear, ITD etc..
        parent.choosersToHide = [parent.prm['chooserLabel'].index(parent.tr("Ear:")), #left, right, both, odd left, odd right
                                 parent.prm['chooserLabel'].index(parent.tr("Phase:")), #sine cos schroeder, etc
                                 parent.prm['chooserLabel'].index(parent.tr("Noise Type:")), #white, pink
                                 parent.prm['chooserLabel'].index(parent.tr("Fix Spectrum Level:")), #fixed, non-fixed
                                 parent.prm['chooserLabel'].index(parent.tr("Vary Harm. No.:")), # with F0, no
                                 parent.prm['chooserLabel'].index(parent.tr("IRN Type:"))]

        if parent.chooser[parent.prm['chooserLabel'].index(parent.tr("Dichotic Difference:"))].currentText() in [parent.tr("IPD Stepped"), parent.tr("IPD Linear"), parent.tr("IPD Random")]:
            parent.fieldsToHide.extend([parent.prm['fieldLabel'].index(parent.tr("ITD (micro s)"))])
            parent.fieldsToShow.extend([parent.prm['fieldLabel'].index(parent.tr("IPD (radians)"))])
        elif parent.chooser[parent.prm['chooserLabel'].index(parent.tr("Dichotic Difference:"))].currentText() == parent.tr("ITD"):
            parent.fieldsToHide.extend([parent.prm['fieldLabel'].index(parent.tr("IPD (radians)"))])
            parent.fieldsToShow.extend([parent.prm['fieldLabel'].index(parent.tr("ITD (micro s)"))])

    if parent.chooser[parent.prm['chooserLabel'].index(parent.tr("Type:"))].currentText() in [parent.tr("Narrowband Noise"), parent.tr("Huggins Pitch")]:
        if parent.chooser[parent.prm['chooserLabel'].index(parent.tr("Bandwidth Unit:"))].currentText() == parent.tr("Hz"):
            parent.fieldsToHide.extend([parent.prm['fieldLabel'].index(parent.tr("Bandwidth (Cents)")),
                                        parent.prm['fieldLabel'].index(parent.tr("Bandwidth (ERBs)"))])
            parent.fieldsToShow.extend([parent.prm['fieldLabel'].index(parent.tr("Bandwidth (Hz)"))])
        elif parent.chooser[parent.prm['chooserLabel'].index(parent.tr("Bandwidth Unit:"))].currentText() == parent.tr("Cent"):
            parent.fieldsToHide.extend([parent.prm['fieldLabel'].index(parent.tr("Bandwidth (Hz)")),
                                        parent.prm['fieldLabel'].index(parent.tr("Bandwidth (ERBs)"))])
            parent.fieldsToShow.extend([parent.prm['fieldLabel'].index(parent.tr("Bandwidth (Cents)"))])
        elif parent.chooser[parent.prm['chooserLabel'].index(parent.tr("Bandwidth Unit:"))].currentText() == parent.tr("ERB"):
            parent.fieldsToHide.extend([parent.prm['fieldLabel'].index(parent.tr("Bandwidth (Hz)")),
                                        parent.prm['fieldLabel'].index(parent.tr("Bandwidth (Cents)"))])
            parent.fieldsToShow.extend([parent.prm['fieldLabel'].index(parent.tr("Bandwidth (ERBs)"))])

            
 
          
    if parent.chooser[parent.prm['chooserLabel'].index(QApplication.translate("","Roving:",""))].currentText() == QApplication.translate("","No",""):
        parent.fieldsToHide.extend([parent.prm['fieldLabel'].index(parent.tr("Lower F0 (Hz)")), parent.prm['fieldLabel'].index(parent.tr("Upper F0 (Hz)"))])
        parent.fieldsToShow.extend([parent.prm['fieldLabel'].index(parent.tr("F0 (Hz)"))])
    else:
        parent.fieldsToHide.extend([parent.prm['fieldLabel'].index(parent.tr("F0 (Hz)"))]);
        parent.fieldsToShow.extend([parent.prm['fieldLabel'].index(parent.tr("Lower F0 (Hz)")), parent.prm['fieldLabel'].index(parent.tr("Upper F0 (Hz)"))])

    if parent.chooser[parent.prm['chooserLabel'].index(parent.tr("Harmonicity:"))].currentText() == parent.tr("Harmonic"):
        parent.fieldsToHide.extend([parent.prm['fieldLabel'].index(parent.tr("Stretch (%)"))])
    elif parent.chooser[parent.prm['chooserLabel'].index(parent.tr("Harmonicity:"))].currentText() == parent.tr("Harmonic Stretched"):
        parent.fieldsToShow.extend([parent.prm['fieldLabel'].index(parent.tr("Stretch (%)"))])


    #Noise Type
    if parent.chooser[parent.prm['chooserLabel'].index(QApplication.translate("","Noise Type:",""))].currentText() == QApplication.translate("","None",""):
        parent.fieldsToHide.extend([parent.prm['fieldLabel'].index(parent.tr("Noise 1 Low Freq. (Hz)")),
                                    parent.prm['fieldLabel'].index(parent.tr("Noise 1 High Freq. (Hz)")),
                                    parent.prm['fieldLabel'].index(parent.tr("Noise 1 S. Level (dB SPL)")),
                                    parent.prm['fieldLabel'].index(parent.tr("Noise 2 Low Freq. (Hz)")),
                                    parent.prm['fieldLabel'].index(parent.tr("Noise 2 High Freq. (Hz)")),
                                    parent.prm['fieldLabel'].index(parent.tr("Noise 2 S. Level (dB SPL)"))])
    else:
        parent.fieldsToShow.extend([parent.prm['fieldLabel'].index(parent.tr("Noise 1 Low Freq. (Hz)")),
                                    parent.prm['fieldLabel'].index(parent.tr("Noise 1 High Freq. (Hz)")),
                                    parent.prm['fieldLabel'].index(parent.tr("Noise 1 S. Level (dB SPL)")),
                                    parent.prm['fieldLabel'].index(parent.tr("Noise 2 Low Freq. (Hz)")),
                                    parent.prm['fieldLabel'].index(parent.tr("Noise 2 High Freq. (Hz)")),
                                    parent.prm['fieldLabel'].index(parent.tr("Noise 2 S. Level (dB SPL)"))])

        
    if (parent.chooser[parent.prm['chooserLabel'].index(QApplication.translate("","Type:",""))].currentText() == QApplication.translate("","Simple Dichotic","") or
        parent.chooser[parent.prm['chooserLabel'].index(QApplication.translate("","Type:",""))].currentText() == QApplication.translate("","Narrowband Noise 2","")):
        parent.fieldsToHide.extend([parent.prm['fieldLabel'].index(parent.tr("Low Stop")), parent.prm['fieldLabel'].index(parent.tr("High Stop"))])
        
    else:
        parent.fieldsToShow.extend([parent.prm['fieldLabel'].index(parent.tr("Low Stop")), parent.prm['fieldLabel'].index(parent.tr("High Stop"))])

def doTrial_F0DL(parent):
    currBlock = 'b'+ str(parent.prm['currentBlock'])
    if parent.prm['startOfBlock'] == True:
        parent.prm['additional_parameters_to_write'] = {}
        parent.prm['adaptiveDifference'] = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(QApplication.translate("","Starting Difference (%)",""))] 
        parent.prm['conditions'] = [str(parent.prm['adaptiveDifference'])]
        parent.writeResultsHeader('log')

    parent.currentCondition = parent.prm['conditions'][0] #this is necessary for constant m-intervals n-alternatives procedure
    F0                  = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("F0 (Hz)"))]
    F0Lower             = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Lower F0 (Hz)"))]
    F0Higher            = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Upper F0 (Hz)"))]
    deltaF0Limit        = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Delta F0 Limit (%)"))]
    bandwidthHz         = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Bandwidth (Hz)"))]
    bandwidthCents      = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Bandwidth (Cents)"))]
    bandwidthERBs       = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Bandwidth (ERBs)"))]
    itd                 = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("ITD (micro s)"))]
    ipd                 = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("IPD (radians)"))]
    iterations          = int(parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Iterations"))])
    gain                = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Gain"))]
    lowHarm             = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Low Harmonic"))]
    highHarm            = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("High Harmonic"))]
    lowFreq             = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Low Freq. (Hz)"))]
    highFreq            = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("High Freq. (Hz)"))]
    lowStopComplex      = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Low Stop"))]
    highStopComplex     = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("High Stop"))]
    harmonicLevel       = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Harmonic Level (dB SPL)"))]
    spectrumLevel       = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Spectrum Level (dB SPL)"))]
    duration            = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Duration (ms)"))]
    ramp                = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Ramp (ms)"))]
    noise1LowFreq       = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Noise 1 Low Freq. (Hz)"))]
    noise1HighFreq      = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Noise 1 High Freq. (Hz)"))]
    noise1SpectrumLevel = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Noise 1 S. Level (dB SPL)"))]
    noise2LowFreq       = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Noise 2 Low Freq. (Hz)"))]
    noise2HighFreq      = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Noise 2 High Freq. (Hz)"))]
    noise2SpectrumLevel = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Noise 2 S. Level (dB SPL)"))]
    stretch             = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(parent.tr("Stretch (%)"))]

    channel            = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(parent.tr("Ear:"))]
    harmType           = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(parent.tr("Type:"))]
    harmPhase          = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(parent.tr("Phase:"))]
    noiseType          = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(parent.tr("Noise Type:"))]
    fixSpectrumLevel   = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(parent.tr("Fix Spectrum Level:"))]
    adjustHarmonicN    = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(parent.tr("Vary Harm. No.:"))]
    irnConfiguration   = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(parent.tr("IRN Type:"))]
    bandwidthUnit      = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(parent.tr("Bandwidth Unit:"))]
    hugginsPhaseRel    = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(parent.tr("Phase relationship:"))]
    dichoticDifference = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(parent.tr("Dichotic Difference:"))]
    roving             = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(parent.tr("Roving:"))]
    harmonicity        = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(parent.tr("Harmonicity:"))]
    if dichoticDifference in [parent.tr("IPD Stepped"), parent.tr("IPD Linear"), parent.tr("IPD Random")]:
        dichoticDifferenceValue = ipd
    elif dichoticDifference == parent.tr("ITD"):
        dichoticDifferenceValue = itd

    if bandwidthUnit == parent.tr("Hz"):
        bandwidth = bandwidthHz
    elif bandwidthUnit == parent.tr("Cent"):
        bandwidth = bandwidthCents
    elif bandwidthUnit == parent.tr("ERB"):
        bandwidth = bandwidthERBs
        
    lowStop = lowStopComplex
    highStop = highStopComplex
    if harmonicity == parent.tr("Harmonic"):
        stretch = 0

    # limit F0% difference
    if parent.prm['adaptiveDifference'] < -deltaF0Limit:
        parent.prm['adaptiveDifference'] = -deltaF0Limit
    elif  parent.prm['adaptiveDifference'] > deltaF0Limit:
        parent.prm['adaptiveDifference'] = deltaF0Limit

    if roving == parent.tr("Yes - Log"):
        dist = numpy.random.uniform(0, log2(F0Higher/F0Lower))
        F0 = F0Lower*2**(dist)
    elif roving == parent.tr("Yes - Linear"):
        F0 = numpy.random.uniform(F0Lower, F0Higher)
    parent.currF0 = F0

    corrF0 = F0 + (F0 * parent.prm['adaptiveDifference']) / 100
    stretchHz = (corrF0*stretch)/100 
    
    if fixSpectrumLevel == parent.tr("Fixed") and harmType in [parent.tr("Sinusoid"), parent.tr("Narrowband Noise")]:
        corrHarmonicLevel = harmonicLevel + 10 * log10(corrF0/F0)
        corrSpectrumLevel = spectrumLevel + 10 * log10(corrF0/F0) #for narrowband noise
    else:
        corrHarmonicLevel = harmonicLevel
        corrSpectrumLevel = spectrumLevel

    nyq = parent.prm['sampRate'] / 2
    if (highHarm * F0) + stretchHz >= nyq:
        highHarm = ceil((nyq-stretchHz) / F0) -1

    #adjust the harmonic number to fill filter passband
    if adjustHarmonicN == parent.tr("With F0"):
        if highHarm != 1:
            if lowHarm != 1:
                corrLowHarm = floor(lowHarm * F0 / corrF0)
            else:
                corrLowHarm =  1
            corrHighHarm = ceil(highHarm * F0 / corrF0)
        else:
            corrLowHarm =  1
            corrHighHarm =  1
    else:
        corrLowHarm = lowHarm
        corrHighHarm = highHarm

    if (corrHighHarm * corrF0) + stretchHz >= nyq:
        corrHighHarm = ceil((nyq-stretchHz) / corrF0) -1
 
    corrLowHarm = int(corrLowHarm); corrHighHarm = int(corrHighHarm);
    lowHarm = int(lowHarm); highHarm = int(highHarm);

    if harmType == parent.tr("Sinusoid"):
        parent.stimulusCorrect = complexTone(corrF0, harmPhase, corrLowHarm, corrHighHarm, stretch, corrHarmonicLevel, duration, ramp, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
    elif harmType == parent.tr("Narrowband Noise"):
        parent.stimulusCorrect = harmComplFromNarrowbandNoise(corrF0, corrLowHarm, corrHighHarm, corrSpectrumLevel, bandwidth, bandwidthUnit, stretch, duration, ramp, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
    elif harmType == parent.tr("IRN"):
        delay = 1/corrF0
        parent.stimulusCorrect = makeIRN(delay, gain, iterations, irnConfiguration, spectrumLevel, duration, ramp, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
    elif harmType == parent.tr("Huggins Pitch"):
        parent.stimulusCorrect = makeHugginsPitch(corrF0, corrLowHarm, corrHighHarm, spectrumLevel, bandwidth,
                                                  bandwidthUnit, dichoticDifference, dichoticDifferenceValue,
                                                  hugginsPhaseRel, stretch, "White", duration, ramp, parent.prm['sampRate'],
                                                  parent.prm['maxLevel'])
        channel = parent.tr("Both")
        

    parent.stimulusCorrect = fir2Filt(lowFreq*lowStopComplex, lowFreq, highFreq, highFreq*highStopComplex, parent.stimulusCorrect, parent.prm['sampRate'])
        
    if noiseType != parent.tr("None"):
        if channel == parent.tr("Odd Left") or channel == parent.tr("Odd Right"): #alternating harmonics, different noise to the two ears
            noiseR = broadbandNoise(noise1SpectrumLevel, duration + ramp*6, 0, parent.tr("Right"), parent.prm['sampRate'], parent.prm['maxLevel'])
            noiseL = broadbandNoise(noise1SpectrumLevel, duration + ramp*6, 0, parent.tr("Left"), parent.prm['sampRate'], parent.prm['maxLevel'])
            noise = noiseR + noiseL
        else:
            noise = broadbandNoise(noise1SpectrumLevel, duration + ramp*6, 0, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
        if noiseType == parent.tr("Pink"):
            noise = makePink(noise, parent.prm['sampRate'])
        noise1 = fir2Filt(noise1LowFreq*lowStop, noise1LowFreq, noise1HighFreq, noise1HighFreq*highStop, noise, parent.prm['sampRate'])
        noise2 = scale(noise2SpectrumLevel - noise1SpectrumLevel, noise)
        noise2 = fir2Filt(noise2LowFreq*lowStop, noise2LowFreq, noise2HighFreq, noise2HighFreq*highStop, noise2, parent.prm['sampRate'])
        noise = noise1 + noise2
        noise = noise[0:parent.stimulusCorrect.shape[0],]
        noise = gate(ramp, noise, parent.prm['sampRate'])
        parent.stimulusCorrect = parent.stimulusCorrect + noise 


    parent.stimulusIncorrect = []
    for i in range((parent.prm['nIntervals']-1)):
        if harmType == parent.tr("Sinusoid"):
            thisSnd = complexTone(F0, harmPhase, lowHarm, highHarm, stretch, harmonicLevel, duration, ramp, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
        elif harmType == parent.tr("Narrowband Noise"):
            thisSnd = harmComplFromNarrowbandNoise(F0, lowHarm, highHarm, spectrumLevel, bandwidth, bandwidthUnit, stretch, duration, ramp, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
        elif harmType == parent.tr("IRN"):
            delay = 1/F0
            thisSnd = makeIRN(delay, gain, iterations, irnConfiguration, spectrumLevel, duration, ramp, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
        elif harmType == parent.tr("Huggins Pitch"):
            thisSnd = makeHugginsPitch(F0, lowHarm, highHarm, spectrumLevel, bandwidth, bandwidthUnit,
                                       dichoticDifference, dichoticDifferenceValue, hugginsPhaseRel, stretch, "White",
                                       duration, ramp, parent.prm['sampRate'], parent.prm['maxLevel'])
            channel = parent.tr("Both")
    
        thisSnd = fir2Filt(lowFreq*lowStopComplex, lowFreq, highFreq, highFreq*highStopComplex, thisSnd, parent.prm['sampRate'])

        if noiseType != parent.tr("None"):
            if channel == parent.tr("Odd Left") or channel == parent.tr("Odd Right"): #alternating harmonics, different noise to the two ears
                noiseR = broadbandNoise(noise1SpectrumLevel, duration + ramp*6, 0, parent.tr("Right"), parent.prm['sampRate'], parent.prm['maxLevel'])
                noiseL = broadbandNoise(noise1SpectrumLevel, duration + ramp*6, 0, parent.tr("Left"), parent.prm['sampRate'], parent.prm['maxLevel'])
                noise = noiseR + noiseL
            else:
                noise = broadbandNoise(noise1SpectrumLevel, duration + ramp*6, 0, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
            if noiseType == parent.tr("Pink"):
                noise = makePink(noise, parent.prm['sampRate'])
            noise1 = fir2Filt(noise1LowFreq*lowStop, noise1LowFreq, noise1HighFreq, noise1HighFreq*highStop, noise, parent.prm['sampRate'])
            noise2 = scale(noise2SpectrumLevel - noise1SpectrumLevel, noise)
            noise2 = fir2Filt(noise2LowFreq*lowStop, noise2LowFreq, noise2HighFreq, noise2HighFreq*highStop, noise2, parent.prm['sampRate'])
            noise = noise1 + noise2
            noise = noise[0:thisSnd.shape[0],]
            noise = gate(ramp, noise, parent.prm['sampRate'])
            thisSnd = thisSnd + noise 

        parent.stimulusIncorrect.append(thisSnd)

                    
    parent.prm['additional_parameters_to_write'][0] = parent.currF0
    parent.playRandomisedIntervals(parent.stimulusCorrect, parent.stimulusIncorrect)
