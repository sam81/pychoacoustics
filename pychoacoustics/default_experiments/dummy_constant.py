# -*- coding: utf-8 -*-

"""
Dummy experiment for several constant paradigms.

"""


import random, sys
from .._version_info import*
from pychoacoustics.sndlib import*
                                                                                         

def initialize_dummy_constant(prm):
    exp_name = "Dummy Constant 1-Interval 2-Alternatives"
    prm["experimentsChoices"].append(exp_name)
    prm[exp_name] = {}
    prm[exp_name]["paradigmChoices"] = ["Constant 1-Interval 2-Alternatives",
                                        "Constant 1-Pair Same/Different"]

    prm[exp_name]["opts"] = ["hasFeedback"]

    prm[exp_name]["buttonLabels"] = ["A", "B"]
    prm[exp_name]['defaultNIntervals'] = 1
    prm[exp_name]['defaultNAlternatives'] = 2
    
    prm[exp_name]["execString"] = "dummy_constant"
    prm[exp_name]["version"] = __name__ + ' ' + pychoacoustics_version + ' ' + pychoacoustics_builddate
    
    return prm

def select_default_parameters_dummy_constant(parent, par):
   
    field = []
    fieldLabel = []
    chooser = []
    chooserLabel = []
    chooserOptions = []

    fieldLabel.append(parent.tr("Constant"))
    field.append(50)
    

    prm = {}
    prm['field'] = field
    prm['fieldLabel'] = fieldLabel
    prm['chooser'] = chooser
    prm['chooserLabel'] = chooserLabel
    prm['chooserOptions'] =  chooserOptions

    return prm


def doTrial_dummy_constant(parent):
  
    currBlock = 'b'+ str(parent.prm['currentBlock'])
    if parent.prm['startOfBlock'] == True:
        parent.writeResultsHeader('log')
        parent.prm['conditions'] = ["A","B"]

    parent.currentCondition = random.choice(parent.prm['conditions'])
    if parent.currentCondition == 'A':
        parent.correctButton = 1
    elif parent.currentCondition == 'B':
        parent.correctButton = 2


    lev    = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Constant")]


 
 
   
