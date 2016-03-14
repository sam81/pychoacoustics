# -*- coding: utf-8 -*-

"""
Dummy experiment for several constant paradigms.

"""

from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, unicode_literals
#from PyQt4 import QtGui, QtCore
#from PyQt4.QtGui import QApplication
import random, sys
from .._version_info import*
from pychoacoustics.sndlib import*
                                                                                         

def initialize_dummy_multiple_constants(prm):
    exp_name = "Dummy Constant 1-Interval 2-Alternatives"
    prm["experimentsChoices"].append(exp_name)
    prm[exp_name] = {}
    prm[exp_name]["paradigmChoices"] = ["Multiple Constants 1-Interval 2-Alternatives",
                                        "Multiple Constants 1-Pair Same/Different",
                                        "Multiple Constants ABX",
                                        "Multiple Constants Odd One Out"]

    prm[exp_name]["opts"] = ["hasFeedback", "hasNDifferencesChooser"]

    prm[exp_name]["buttonLabels"] = ["A", "B"]
    prm[exp_name]['defaultNIntervals'] = 1
    prm[exp_name]['defaultNAlternatives'] = 2
    
    prm[exp_name]["execString"] = "dummy_multiple_constant"
    prm[exp_name]["version"] = __name__ + ' ' + pychoacoustics_version + ' ' + pychoacoustics_builddate
    
    return prm

def select_default_parameters_dummy_multiple_constants(parent, par):
    nDifferences = par['nDifferences']

    field = []
    fieldLabel = []
    chooser = []
    chooserLabel = []
    chooserOptions = []

    for i in range(nDifferences):
        fieldLabel.append(parent.tr("Constant " + str(i+1)))
        field.append(50)
    

    prm = {}
    prm['field'] = field
    prm['fieldLabel'] = fieldLabel
    prm['chooser'] = chooser
    prm['chooserLabel'] = chooserLabel
    prm['chooserOptions'] =  chooserOptions

    return prm


def doTrial_dummy_multiple_constants(parent):
  
    currBlock = 'b'+ str(parent.prm['currentBlock'])
    if parent.prm['startOfBlock'] == True:
        parent.writeResultsHeader('log')
        parent.prm['conditions'] = ["A","B"]
        parent.prm['differenceChoices'] = [] #these are removed as the number of trials for each difference is reached
        parent.prm['comparisonChoices'] = [] #these are removed as the number of trials for each difference is reached
        parent.prm['differenceNames'] = [] #these are permanent
        #parent.correctButton = random.choice([1,2]) #this is just in case of automatic response
        for i in range(parent.prm['nDifferences']):
            parent.prm['differenceChoices'].append("Constant "+str(i+1))
            parent.prm['differenceNames'].append("Constant " +str(i+1))
            parent.prm['comparisonChoices'].append("Constant "+str(i+1))

    currentDifference =  random.choice(parent.prm['differenceChoices'])
    parent.currentCondition = random.choice(parent.prm['conditions'])
    if parent.currentCondition == 'A':
        parent.correctButton = 1
    elif parent.currentCondition == 'B':
        parent.correctButton = 2


    lev    = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Constant")]


 
 
   
