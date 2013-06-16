# -*- coding: utf-8 -*-
from sndlib import*


                                                                                         
def initialize_freq(prm):
    exp_name = "Frequency Discrimination Demo"
    prm["experimentsChoices"].append(exp_name)
    prm[exp_name] = {}
    prm[exp_name]["paradigmChoices"] = ["Adaptive",
                                        "Weighted Up/Down",
                                        "Constant m-Intervals n-Alternatives"]

    prm[exp_name]["opts"] = ["hasISIBox", "hasAlternativesChooser", "hasFeedback",
                             "hasIntervalLights"]
    prm[exp_name]['defaultAdaptiveType'] = QApplication.translate("","Geometric","", QApplication.UnicodeUTF8)
    prm[exp_name]['defaultNIntervals'] = 2
    prm[exp_name]['defaultNAlternatives'] = 2
    prm[exp_name]["execString"] = "freq"
    return prm

def select_default_parameters_freq(parent, par):
   
    field = []
    fieldLabel = []
    chooser = []
    chooserLabel = []
    chooserOptions = []
    
    fieldLabel.append("Frequency (Hz)")
    field.append(1000)

    fieldLabel.append("Starting Difference (%)")
    field.append(20)
    
    fieldLabel.append("Level (dB SPL)")
    field.append(50)
    
    fieldLabel.append("Duration (ms)")
    field.append(180)
    
    fieldLabel.append("Ramps (ms)")
    field.append(10)

    
    chooserOptions.append(["Right",
                           "Left",
                           "Both"])
    chooserLabel.append("Ear:")
    chooser.append("Right")
   
    
    prm = {}
    prm['field'] = field
    prm['fieldLabel'] = fieldLabel
    prm['chooser'] = chooser
    prm['chooserLabel'] = chooserLabel
    prm['chooserOptions'] =  chooserOptions

    return prm

def get_fields_to_hide_freq(parent):
    pass
    
def doTrial_freq(parent):
    currBlock = 'b'+ str(parent.prm['currentBlock'])
    if parent.prm['startOfBlock'] == True:
        parent.prm['additional_parameters_to_write'] = {}
        parent.prm['adaptiveDifference'] = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Starting Difference (%)")]
        parent.prm['conditions'] = [str(parent.prm['adaptiveDifference'])]

        parent.writeResultsHeader('log')
    parent.currentCondition = parent.prm['conditions'][0]

    frequency = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Frequency (Hz)")]
    level = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Level (dB SPL)")] 
    duration = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Duration (ms)")] 
    ramps = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Ramps (ms)")]
    phase = 0
    channel = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index("Ear:")]
    
    correctFrequency = frequency + (frequency*parent.prm['adaptiveDifference'])/100
    parent.stimulusCorrect = pureTone(correctFrequency, phase, level, duration, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])

      
            
    parent.stimulusIncorrect = []
    for i in range((parent.prm['nIntervals']-1)):
        thisSnd = pureTone(frequency, phase, level, duration, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
        parent.stimulusIncorrect.append(thisSnd)
    parent.playRandomisedIntervals(parent.stimulusCorrect, parent.stimulusIncorrect)
