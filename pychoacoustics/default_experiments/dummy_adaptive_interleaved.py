# -*- coding: utf-8 -*-

"""
Dummy experiment to test adaptive procedures

"""

from ..pyqtver import*
from .._version_info import*
import numpy

if pyqtversion == 5:
    from PyQt5.QtWidgets import QApplication
elif pyqtversion == 6:
    from PyQt6.QtWidgets import QApplication

                                                                              
def initialize_dummy_adaptive_interleaved(prm):
    exp_name = "Dummy Adaptive Interleaved"
    prm["experimentsChoices"].append(exp_name)
    prm[exp_name] = {}
    prm[exp_name]["paradigmChoices"] = ["Transformed Up-Down Interleaved",
                                        "Weighted Up-Down Interleaved",
                                        "Multiple Constants m-Intervals n-Alternatives"]

    prm[exp_name]["opts"] = ["hasAlternativesChooser", "hasNTracksChooser", "hasNDifferencesChooser"]
    prm[exp_name]['defaultAdaptiveType'] = QApplication.translate("","Geometric","")
    prm[exp_name]['defaultNIntervals'] = 2
    prm[exp_name]['defaultNAlternatives'] = 2
    prm[exp_name]["execString"] = "dummy_adaptive_interleaved"
    prm[exp_name]["version"] = __name__ + ' ' + pychoacoustics_version + ' ' + pychoacoustics_builddate
    
    return prm

def select_default_parameters_dummy_adaptive_interleaved(parent, par):
   
    field = []
    fieldLabel = []
    chooser = []
    chooserLabel = []
    chooserOptions = []

    nDifferences = par['nDifferences']
    
    for i in range(nDifferences):

        fieldLabel.append("Difference " + str(i+1))
        field.append(20)
    
    
    prm = {}
    prm['field'] = field
    prm['fieldLabel'] = fieldLabel
    prm['chooser'] = chooser
    prm['chooserLabel'] = chooserLabel
    prm['chooserOptions'] =  chooserOptions

    return prm

    
def doTrial_dummy_adaptive_interleaved(parent):
    currBlock = 'b'+ str(parent.prm['currentBlock'])
    if parent.prm['startOfBlock'] == True:
        nDifferences = parent.prm['nDifferences']
        parent.prm['adaptiveParam'] = []
        parent.prm['conditions'] = []
        for i in range(nDifferences):
            parent.prm['adaptiveParam'].append(parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Difference " + str(i+1))])
            parent.prm['conditions'].append('Difference ' + str(i+1))
            parent.writeResultsHeader('log')

    parent.currentCondition = parent.prm['conditions'][parent.prm['currentDifference']] 
    nAlternatives = parent.prm[currBlock]['nAlternatives']
    nIntervals = parent.prm[currBlock]['nIntervals']
        
    if nAlternatives == nIntervals:
        parent.correctInterval = numpy.random.randint(0, nIntervals)
        parent.correctButton = parent.correctInterval + 1
    elif nAlternatives == nIntervals-1:
        parent.correctInterval = numpy.random.randint(1, nIntervals)
        parent.correctButton = parent.correctInterval 
