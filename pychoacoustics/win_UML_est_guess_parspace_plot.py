# -*- coding: utf-8 -*- 
#   Copyright (C) 2008-2017 Samuele Carcagno <sam.carcagno@gmail.com>
#   This file is part of pychoacoustics

#    pychoacoustics is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    pychoacoustics is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with pychoacoustics.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, unicode_literals
import matplotlib

from .pyqtver import*
if pyqtversion == 4:
    from PyQt4 import QtGui, QtCore
    from PyQt4.QtGui import QCheckBox, QIcon, QHBoxLayout, QMainWindow, QPushButton, QVBoxLayout, QWidget
    # import the Qt4Agg FigureCanvas object, that binds Figure to
    # Qt4Agg backend. It also inherits from QWidget
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
    # import the NavigationToolbar Qt4Agg widget
    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
    matplotlib.rcParams['backend'] = "Qt4Agg"
    matplotlib.rcParams['backend.qt4'] = "PyQt4"
elif pyqtversion == -4:
    from PySide import QtGui, QtCore
    from PySide.QtGui import QCheckBox, QIcon, QHBoxLayout, QMainWindow, QPushButton, QVBoxLayout, QWidget
    # import the Qt4Agg FigureCanvas object, that binds Figure to
    # Qt4Agg backend. It also inherits from QWidget
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
    # import the NavigationToolbar Qt4Agg widget
    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
    matplotlib.rcParams['backend'] = "Qt4Agg"
    matplotlib.rcParams['backend.qt4'] = "PySide"
elif pyqtversion == 5:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtWidgets import QCheckBox, QHBoxLayout, QMainWindow, QPushButton, QVBoxLayout, QWidget
    from PyQt5.QtGui import QIcon
    # import the Qt4Agg FigureCanvas object, that binds Figure to
    # Qt4Agg backend. It also inherits from QWidget
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    # import the NavigationToolbar Qt4Agg widget
    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
    matplotlib.rcParams['backend'] = "Qt5Agg"
# Matplotlib Figure object
from matplotlib.figure import Figure

from matplotlib.widgets import Cursor
import numpy as np
import copy, os
from numpy import arange, ceil, floor, linspace, log10
from matplotlib.lines import Line2D

import matplotlib.pyplot as plt
import matplotlib as mpl
#import pandas as pd
import matplotlib.font_manager as fm

from .pysdt import*
from .UML_method_est_guess import*

#mpl.rcParams['font.family'] = 'sans-serif'

#fontPath = os.path.abspath(os.path.dirname(__file__)+'/../') + '/data/Ubuntu-R.ttf'
#fontPath = '/media/ntfsShared/lin_home/auditory/code/pychoacoustics/pychoacoustics-qt4/development/dev/data/Ubuntu-R.ttf'
#prop = fm.FontProperties(fname=fontPath)
#mpl.rcParams.update({'font.size': 16})



def log_10_product(x, pos):
    """The two args are the value and tick position.
    Label ticks with the product of the exponentiation"""
    return '%1i' % (x)
def nextPow10Up(val):
    p = int(ceil(log10(val)))
    return p

def nextPow10Down(val):
    p = int(floor(log10(val)))
    return p

class UMLEstGuessRateParSpacePlot(QMainWindow):
    def __init__(self, parent):
        QMainWindow.__init__(self, parent)
        
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        #self.prm = prm
     
            
        self.pchs = ["o", "s", "v", "p", "h", "8", "*", "x", "+", "d", ",", "^", "<", ">", "1", "2", "3", "4", "H", "D", ".", "|", "_"]  


        mpl.rcParams['xtick.major.size'] = 6
        mpl.rcParams['xtick.minor.size'] = 4
        mpl.rcParams['xtick.major.width'] = 1
        mpl.rcParams['xtick.minor.width'] = 1
        mpl.rcParams['ytick.major.size'] = 9
        mpl.rcParams['ytick.minor.size'] = 5
        mpl.rcParams['ytick.major.width'] = 0.8
        mpl.rcParams['ytick.minor.width'] = 0.8
        mpl.rcParams['xtick.direction'] = 'out'
        mpl.rcParams['ytick.direction'] = 'out'
        mpl.rcParams['font.size'] = 14
        mpl.rcParams['figure.facecolor'] = 'white'
        mpl.rcParams['lines.color'] = 'black'
        mpl.rcParams['axes.color_cycle'] = ["#000000", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7"]#['k', 'b', 'g', 'r', 'c', 'm', 'y']

        self.mw = QWidget(self)
        self.vbl = QVBoxLayout(self.mw)
        self.fig = Figure(figsize=(8,8))#facecolor=self.canvasColor, dpi=self.dpi)
        self.ax1 = self.fig.add_subplot(221)
        self.ax2 = self.fig.add_subplot(222)
        self.ax3 = self.fig.add_subplot(223)
        self.ax4 = self.fig.add_subplot(224)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.mw)
        self.ntb = NavigationToolbar(self.canvas, self.mw)
      

        self.logAxisMidpoint = QCheckBox(self.tr("Midpoint Log Axis"))
        self.logAxisMidpoint.stateChanged[int].connect(self.toggleMidpointLogAxis)

        self.logAxisSlope = QCheckBox(self.tr("Slope Log Axis"))
        self.logAxisSlope.stateChanged[int].connect(self.toggleSlopeLogAxis)

        self.logAxisGuess = QCheckBox(self.tr("Guess Log Axis"))
        self.logAxisGuess.stateChanged[int].connect(self.toggleGuessLogAxis)

        self.logAxisLapse = QCheckBox(self.tr("Lapse Log Axis"))
        self.logAxisLapse.stateChanged[int].connect(self.toggleLapseLogAxis)

        self.updateButton = QPushButton(self.tr("Update"), self)
        self.updateButton.setIcon(QIcon.fromTheme("view-refresh", QIcon(":/view-refresh")))
        self.updateButton.clicked.connect(self.onClickUpdateButton)
        
        self.ntbBox = QHBoxLayout()
        self.ntbBox.addWidget(self.ntb)
        self.ntbBox.addWidget(self.logAxisMidpoint)
        self.ntbBox.addWidget(self.logAxisSlope)
        self.ntbBox.addWidget(self.logAxisGuess)
        self.ntbBox.addWidget(self.logAxisLapse)
        self.ntbBox.addWidget(self.updateButton)
        self.vbl.addWidget(self.canvas)
        self.vbl.addLayout(self.ntbBox)
        self.mw.setFocus()
        self.setCentralWidget(self.mw)

        self.getUMLPars()
        if self.stimScaling == "Linear":
            self.logAxisMidpoint.setChecked(False)
            self.plotDataMidpoint()
        elif self.stimScaling == "Logarithmic":
            self.logAxisMidpoint.setChecked(True)
            self.plotDataMidpointLogAxis()

        if self.slopeSpacing == "Linear":
            self.logAxisSlope.setChecked(False)
            self.plotDataSlope()
        elif self.slopeSpacing == "Logarithmic":
            self.logAxisSlope.setChecked(True)
            self.plotDataSlopeLogAxis()

        if self.guessSpacing == "Linear":
            self.logAxisGuess.setChecked(False)
            self.plotDataGuess()
        elif self.guessSpacing == "Logarithmic":
            self.logAxisGuess.setChecked(True)
            self.plotDataGuessLogAxis()

        if self.lapseSpacing == "Linear":
            self.logAxisLapse.setChecked(False)
            self.plotDataLapse()
        elif self.lapseSpacing == "Logarithmic":
            self.logAxisLapse.setChecked(True)
            self.plotDataLapseLogAxis()

        self.fig.suptitle(self.tr("UML Parameter Space"))
        self.show()
        self.canvas.draw()

    def getUMLPars(self):
        self.psyFun = self.parent().psyFunChooser.currentText()
        self.loStim = self.parent().currLocale.toDouble(self.parent().loStim.text())[0]
        self.hiStim = self.parent().currLocale.toDouble(self.parent().hiStim.text())[0]
        self.stimScaling = self.parent().stimScalingChooser.currentText()
        self.loMidPoint = self.parent().currLocale.toDouble(self.parent().loMidPoint.text())[0]
        self.hiMidPoint = self.parent().currLocale.toDouble(self.parent().hiMidPoint.text())[0]
        self.threshGridStep = self.parent().currLocale.toDouble(self.parent().threshGridStep.text())[0]
        self.threshPrior = self.parent().threshPriorChooser.currentText()
        self.threshPriorMu = self.parent().currLocale.toDouble(self.parent().threshPriorMu.text())[0]
        self.threshPriorSTD = self.parent().currLocale.toDouble(self.parent().threshPriorSTD.text())[0]
        self.loSlope = self.parent().currLocale.toDouble(self.parent().loSlope.text())[0]
        self.hiSlope = self.parent().currLocale.toDouble(self.parent().hiSlope.text())[0]
        self.slopeGridStep =  self.parent().currLocale.toDouble(self.parent().slopeGridStep.text())[0]
        self.slopeSpacing = self.parent().slopeSpacingChooser.currentText()
        self.slopePrior = self.parent().slopePriorChooser.currentText()
        self.slopePriorMu = self.parent().currLocale.toDouble(self.parent().slopePriorMu.text())[0]
        self.slopePriorSTD = self.parent().currLocale.toDouble(self.parent().slopePriorSTD.text())[0]

        self.loGuess = self.parent().currLocale.toDouble(self.parent().loGuess.text())[0]
        self.hiGuess = self.parent().currLocale.toDouble(self.parent().hiGuess.text())[0]
        self.guessGridStep =  self.parent().currLocale.toDouble(self.parent().guessGridStep.text())[0]
        self.guessSpacing = self.parent().guessSpacingChooser.currentText()
        self.guessPrior = self.parent().guessPriorChooser.currentText()
        self.guessPriorMu = self.parent().currLocale.toDouble(self.parent().guessPriorMu.text())[0]
        self.guessPriorSTD = self.parent().currLocale.toDouble(self.parent().guessPriorSTD.text())[0]
        
        self.loLapse = self.parent().currLocale.toDouble(self.parent().loLapse.text())[0]
        self.hiLapse = self.parent().currLocale.toDouble(self.parent().hiLapse.text())[0]
        self.lapseGridStep =  self.parent().currLocale.toDouble(self.parent().lapseGridStep.text())[0]
        self.lapseSpacing = self.parent().lapseSpacingChooser.currentText()
        self.lapsePrior = self.parent().lapsePriorChooser.currentText()
        self.lapsePriorMu = self.parent().currLocale.toDouble(self.parent().lapsePriorMu.text())[0]
        self.lapsePriorSTD = self.parent().currLocale.toDouble(self.parent().lapsePriorSTD.text())[0]
        self.nAlternatives = int(self.parent().nAlternativesChooser.currentText())

        if self.stimScaling == "Linear":
            self.UML = setupUMLEstGuessRate(model=self.psyFun,
                                swptRule="Up-Down",
                                nDown=2,
                                centTend = "Mean",
                                stimScale = self.stimScaling,
                                x0=1,
                                xLim=(self.loStim, self.hiStim),
                                alphaLim=(self.loMidPoint, self.hiMidPoint),
                                alphaStep=self.threshGridStep,
                                alphaSpacing="Linear",
                                alphaDist=self.threshPrior,
                                alphaMu=self.threshPriorMu,
                                alphaSTD=self.threshPriorSTD,
                                betaLim=(self.loSlope, self.hiSlope),
                                betaStep=self.slopeGridStep,
                                betaSpacing=self.slopeSpacing,
                                betaDist=self.slopePrior,
                                betaMu=self.slopePriorMu,
                                betaSTD=self.slopePriorSTD,
                                gammaLim=(self.loGuess, self.hiGuess),
                                gammaStep=self.guessGridStep,
                                gammaSpacing=self.guessSpacing,
                                gammaDist=self.guessPrior,
                                gammaMu=self.guessPriorMu,
                                gammaSTD=self.guessPriorSTD,
                                lambdaLim=(self.loLapse, self.hiLapse),
                                lambdaStep=self.lapseGridStep,
                                lambdaSpacing=self.lapseSpacing,
                                lambdaDist=self.lapsePrior,
                                lambdaMu=self.lapsePriorMu,
                                lambdaSTD=self.lapsePriorSTD)
        elif self.stimScaling == "Logarithmic":
            self.UML = setupUMLEstGuessRate(model=self.psyFun,
                                swptRule="Up-Down",
                                nDown=2,
                                centTend = "Mean",
                                stimScale = self.stimScaling,
                                x0=1,
                                xLim=(abs(self.loStim), abs(self.hiStim)),
                                alphaLim=(abs(self.loMidPoint), abs(self.hiMidPoint)),
                                alphaStep=self.threshGridStep,
                                alphaSpacing="Linear",
                                alphaDist=self.threshPrior,
                                alphaMu=abs(self.threshPriorMu),
                                alphaSTD=self.threshPriorSTD,
                                betaLim=(self.loSlope, self.hiSlope),
                                betaStep=self.slopeGridStep,
                                betaSpacing=self.slopeSpacing,
                                betaDist=self.slopePrior,
                                betaMu=self.slopePriorMu,
                                betaSTD=self.slopePriorSTD,
                                gammaLim=(self.loGuess, self.hiGuess),
                                gammaStep=self.guessGridStep,
                                gammaSpacing=self.guessSpacing,
                                gammaDist=self.guessPrior,
                                gammaMu=self.guessPriorMu,
                                gammaSTD=self.guessPriorSTD,
                                lambdaLim=(self.loLapse, self.hiLapse),
                                lambdaStep=self.lapseGridStep,
                                lambdaSpacing=self.lapseSpacing,
                                lambdaDist=self.lapsePrior,
                                lambdaMu=self.lapsePriorMu,
                                lambdaSTD=self.lapsePriorSTD)
        
    def plotDataMidpoint(self):
        self.ax1.clear()
        self.A = setPrior(self.UML["a"], self.UML["par"]["alpha"])
        
        if self.stimScaling == "Linear":
            markerline, stemlines, baseline = self.ax1.stem(self.UML["alpha"], self.A[:,0,0,0], 'k')
        elif self.stimScaling == "Logarithmic":
            markerline, stemlines, baseline = self.ax1.stem(exp(self.UML["alpha"]), self.A[:,0,0,0], 'k')
            if self.loStim < 0:
                self.ax1.set_xticklabels(list(map(str, -self.ax1.get_xticks())))
            
        plt.setp(markerline, 'markerfacecolor', 'k')
        nAlpha = len(self.A[:,0,0])
        self.ax1.set_title("Midpoint, #Points " + str(nAlpha))

    def plotDataSlope(self):
        self.ax2.clear()
        self.B = setPrior(self.UML["b"], self.UML["par"]["beta"])
        markerline, stemlines, baseline = self.ax2.stem(self.UML["beta"], self.B[0,:,0,0], 'k')
        plt.setp(markerline, 'markerfacecolor', 'k')
        nBeta = len(self.B[0,:,0,0])
        self.ax2.set_title("Slope, #Points " + str(nBeta))

    def plotDataGuess(self):
        self.ax4.clear()
        self.G = setPrior(self.UML["g"], self.UML["par"]["gamma"])
        markerline, stemlines, baseline = self.ax4.stem(self.UML["gamma"], self.G[0,0,:,0], 'k')
        plt.setp(markerline, 'markerfacecolor', 'k')
        nGamma = len(self.G[0,0,:,0])
        self.ax4.set_title("Guess, #Points " + str(nGamma))

    def plotDataLapse(self):
        self.ax3.clear()
        L = setPrior(self.UML["l"], self.UML["par"]["lambda"])
        markerline, stemlines, baseline = self.ax3.stem(self.UML["lambda"], L[0,0,0,:], 'k')
        plt.setp(markerline, 'markerfacecolor', 'k')
        nLambda = len(L[0,0,0,:])
        self.ax3.set_title("Lapse, #Points " + str(nLambda))


    def plotDataMidpointLogAxis(self):
        self.ax1.clear()
        self.A = setPrior(self.UML["a"], self.UML["par"]["alpha"])
        
        if self.stimScaling == "Linear":
            x = self.UML["alpha"]
        elif self.stimScaling == "Logarithmic":
            x = exp(self.UML["alpha"])
        markerline, stemlines, baseline = self.ax1.stem(log10(x), self.A[:,0,0,0], 'k')

        powd = nextPow10Down(10**(self.ax1.get_xlim()[0]))
        powup = nextPow10Up(10**(self.ax1.get_xlim()[1]))
        majTicks = arange(powd, powup+1)
        self.ax1.set_xticks(majTicks)
        xTickLabels = []
        for tick in majTicks:
            if self.stimScaling == "Logarithmic" and self.loStim < 0:
                xTickLabels.append(str(-10**tick))
            else:
                xTickLabels.append(str(10**tick))
        self.ax1.set_xticklabels(xTickLabels)
        minTicks = []
        for i in range(len(majTicks)-1):
            minTicks.extend(log10(linspace(10**majTicks[i], 10**majTicks[i+1], 10)))
        self.ax1.set_xticks(minTicks, minor=True)
            
        plt.setp(markerline, 'markerfacecolor', 'k')
        nAlpha = len(self.A[:,0,0,0])
        self.ax1.set_title("Midpoint, #Points " + str(nAlpha))

        # if self.stimScaling == "Logarithmic":
        #     if self.loStim < 0:
        #         self.ax1.set_xlim(self.ax1.get_xlim()[::-1])
    def plotDataSlopeLogAxis(self):
        self.ax2.clear()
        self.B = setPrior(self.UML["b"], self.UML["par"]["beta"])
        markerline, stemlines, baseline = self.ax2.stem(log10(self.UML["beta"]), self.B[0,:,0,0], 'k')
        plt.setp(markerline, 'markerfacecolor', 'k')

        powd = nextPow10Down(10**(self.ax2.get_xlim()[0]))
        powup = nextPow10Up(10**(self.ax2.get_xlim()[1]))
        majTicks = arange(powd, powup+1)
        self.ax2.set_xticks(majTicks)
        xTickLabels = []
        for tick in majTicks:
            xTickLabels.append(str(10**tick))
        self.ax2.set_xticklabels(xTickLabels)
        minTicks = []
        for i in range(len(majTicks)-1):
            minTicks.extend(log10(linspace(10**majTicks[i], 10**majTicks[i+1], 10)))
        self.ax2.set_xticks(minTicks, minor=True)
        
        nBeta = len(self.B[0,:,0,0])
        self.ax2.set_title("Slope, #Points " + str(nBeta))

    def plotDataGuessLogAxis(self):
        self.ax4.clear()
        self.G = setPrior(self.UML["g"], self.UML["par"]["gamma"])
        markerline, stemlines, baseline = self.ax4.stem(log10(self.UML["gamma"]), self.G[0,0,:,0], 'k')
        plt.setp(markerline, 'markerfacecolor', 'k')

        powd = nextPow10Down(10**(self.ax4.get_xlim()[0]))
        powup = nextPow10Up(10**(self.ax4.get_xlim()[1]))
        majTicks = arange(powd, powup+1)
        self.ax2.set_xticks(majTicks)
        xTickLabels = []
        for tick in majTicks:
            xTickLabels.append(str(10**tick))
        self.ax4.set_xticklabels(xTickLabels)
        minTicks = []
        for i in range(len(majTicks)-1):
            minTicks.extend(log10(linspace(10**majTicks[i], 10**majTicks[i+1], 10)))
        self.ax4.set_xticks(minTicks, minor=True)
        
        nGamma = len(self.G[0,0,:,0])
        self.ax4.set_title("Guess, #Points " + str(nGamma))

    def plotDataLapseLogAxis(self):
        self.ax3.clear()
        L = setPrior(self.UML["l"], self.UML["par"]["lambda"])
        markerline, stemlines, baseline = self.ax3.stem(log10(self.UML["lambda"]), L[0,0,0,:], 'k')
        plt.setp(markerline, 'markerfacecolor', 'k')

        powd = nextPow10Down(10**(self.ax3.get_xlim()[0]))
        powup = nextPow10Up(10**(self.ax3.get_xlim()[1]))
        majTicks = arange(powd, powup+1)
        self.ax3.set_xticks(majTicks)
        xTickLabels = []
        for tick in majTicks:
            xTickLabels.append(str(10**tick))
        self.ax3.set_xticklabels(xTickLabels)
        minTicks = []
        for i in range(len(majTicks)-1):
            minTicks.extend(log10(linspace(10**majTicks[i], 10**majTicks[i+1], 10)))
        self.ax3.set_xticks(minTicks, minor=True)
        
        nLambda = len(L[0,0,0,:])
        self.ax3.set_title("Lapse, #Points " + str(nLambda))

    def onClickUpdateButton(self):
        self.getUMLPars()
        
        if self.logAxisMidpoint.isChecked() == False:
            self.plotDataMidpoint()
        else:
            self.plotDataMidpointLogAxis()

        if self.logAxisSlope.isChecked() == False:
            self.plotDataSlope()
        else:
            self.plotDataSlopeLogAxis()

        if self.logAxisGuess.isChecked() == False:
            self.plotDataGuess()
        else:
            self.plotDataGuessLogAxis()

        if self.logAxisLapse.isChecked() == False:
            self.plotDataLapse()
        else:
            self.plotDataLapseLogAxis()

        self.canvas.draw()
        
    def toggleMidpointLogAxis(self):
        if self.logAxisMidpoint.isChecked() == True:
            self.plotDataMidpointLogAxis()
        else:
            self.plotDataMidpoint()
        self.canvas.draw()

    def toggleSlopeLogAxis(self):
        if self.logAxisSlope.isChecked() == True:
            self.plotDataSlopeLogAxis()
        else:
            self.plotDataSlope()
        self.canvas.draw()

    def toggleGuessLogAxis(self):
        if self.logAxisGuess.isChecked() == True:
            self.plotDataGuessLogAxis()
        else:
            self.plotDataGuess()
        self.canvas.draw()

    def toggleLapseLogAxis(self):
        if self.logAxisLapse.isChecked() == True:
            self.plotDataLapseLogAxis()
        else:
            self.plotDataLapse()
        self.canvas.draw()
           




