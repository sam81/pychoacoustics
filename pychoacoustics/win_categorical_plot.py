# -*- coding: utf-8 -*- 
#   Copyright (C) 2010-2014 Samuele Carcagno <sam.carcagno@gmail.com>
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
from .pyqtver import*
if pyqtversion == 4:
    from PyQt4 import QtGui, QtCore
    # import the Qt4Agg FigureCanvas object, that binds Figure to
    # Qt4Agg backend. It also inherits from QWidget
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
    # import the NavigationToolbar Qt4Agg widget
    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
elif pyqtversion == -4:
    from PySide import QtGui, QtCore
    # import the Qt4Agg FigureCanvas object, that binds Figure to
    # Qt4Agg backend. It also inherits from QWidget
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
    # import the NavigationToolbar Qt4Agg widget
    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
elif pyqtversion == 5:
    from PyQt5 import QtGui, QtCore
    # import the Qt4Agg FigureCanvas object, that binds Figure to
    # Qt4Agg backend. It also inherits from QWidget
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    # import the NavigationToolbar Qt4Agg widget
    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QTAgg as NavigationToolbar
# Matplotlib Figure object
from matplotlib.figure import Figure

from matplotlib.widgets import Cursor
import numpy as np
import copy, os
from numpy import arange, ceil, floor, linspace, log10
from matplotlib.lines import Line2D

import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import matplotlib.font_manager as fm

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

class categoricalPlot(QtGui.QMainWindow):
    def __init__(self, parent, plot_type, fName, winPlot, pdfPlot, paradigm, csv_separator, plot_params, prm):
        QtGui.QMainWindow.__init__(self, parent)
        
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.prm = prm
        self.paradigm = paradigm
        self.fName = fName

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
        mpl.rcParams['axes.color_cycle'] =  ['k', 'b', 'g', 'r', 'c', 'm', 'y']

        
        #dark background
        ## mpl.rcParams['lines.color'] = 'white'
        ## mpl.rcParams['patch.edgecolor'] = 'white'
        ## mpl.rcParams['text.color'] = 'white'
        ## mpl.rcParams['axes.facecolor'] = 'black'
        ## mpl.rcParams['axes.edgecolor'] = 'white'
        ## mpl.rcParams['axes.labelcolor'] = 'white'
        ## mpl.rcParams['axes.color_cycle'] = ['#81b1d2', '#fa8174', '#bfbbd9', '#feffb3', '#8dd3c7',  '#81b1d2', '#fdb462', '#b3de69', '#bc82bd', '#ccebc4', '#ffed6f']
        ## mpl.rcParams['xtick.color'] = 'white'
        ## mpl.rcParams['ytick.color'] = 'white'
        ## mpl.rcParams['grid.color'] = 'white'
        ## mpl.rcParams['figure.facecolor'] = 'black'
        ## mpl.rcParams['figure.edgecolor'] = 'black'
        ## mpl.rcParams['savefig.facecolor'] = 'black'
        ## mpl.rcParams['savefig.edgecolor'] = 'black'

        #ggplot
        ## mpl.rcParams['patch.linewidth'] = 0.5
        ## mpl.rcParams['patch.facecolor'] = '#348ABD'  # blue
        ## mpl.rcParams['patch.edgecolor'] = '#EEEEEE'
        ## mpl.rcParams['patch.antialiased'] = True

        ## #mpl.rcParams['font.size'] = 10.0

        ## mpl.rcParams['axes.facecolor'] = '#E5E5E5'
        ## mpl.rcParams['axes.edgecolor'] = 'white'
        ## mpl.rcParams['axes.linewidth'] = 1
        #mpl.rcParams['axes.grid'] = True
        ## mpl.rcParams['axes.titlesize'] = 'x-large'
        ## mpl.rcParams['axes.labelsize'] = 'large'
        ## mpl.rcParams['axes.labelcolor'] = '#555555'
        ## mpl.rcParams['axes.axisbelow'] = True       # grid/ticks are below elements (eg lines, text)

        ## mpl.rcParams['axes.color_cycle'] = '#348ABD', '#E24A33', '#988ED5', '#777777', '#FBC15E', '#8EBA42', '#FFB5B8'
        ## # E24A33 : red
        ## # 348ABD : blue
        ## # 988ED5 : purple
        ## # 777777 : gray
        ## # FBC15E : yellow
        ## # 8EBA42 : green
        ## # FFB5B8 : pink
        
        ## mpl.rcParams['xtick.color'] = '#555555'
        ## mpl.rcParams['xtick.direction'] = 'out'
        
        ## mpl.rcParams['ytick.color'] = '#555555'
        ## mpl.rcParams['ytick.direction'] = 'out'
        
        ## mpl.rcParams['grid.color'] = 'white'
        ## mpl.rcParams['grid.linestyle'] = '-'    # solid line

        ## mpl.rcParams['figure.facecolor'] = 'white'
        ## mpl.rcParams['figure.edgecolor'] = '0.50'

        #self.currLocale = self.parent().prm['data']['currentLocale']
        #self.currLocale.setNumberOptions(self.currLocale.OmitGroupSeparator | self.currLocale.RejectGroupSeparator)

        #define some parameters before axes creation
        ## self.canvasColor = pltColorFromQColor(self.prm['pref']['canvasColor'])
        ## self.backgroundColor = pltColorFromQColor(self.prm['pref']['backgroundColor'])
        ## self.axesColor = pltColorFromQColor(self.prm['pref']['axes_color'])
        ## self.tickLabelColor = pltColorFromQColor(self.prm['pref']['tick_label_color'])
        ## self.gridColor = pltColorFromQColor(self.prm['pref']['grid_color'])
        ## self.axesLabelColor = pltColorFromQColor(self.prm['pref']['axes_label_color'])
        ## self.labelFontFamily = self.prm['pref']['label_font_family']
        ## self.labelFontWeight = self.prm['pref']['label_font_weight']
        ## self.labelFontStyle = self.prm['pref']['label_font_style']
        ## self.labelFontSize = self.prm['pref']['label_font_size']
        ## self.labelFont = font_manager.FontProperties(family=self.labelFontFamily, weight=self.labelFontWeight, style= self.labelFontStyle, size=self.labelFontSize)
        
        #self.majorTickLength = 2 #self.prm['pref']['major_tick_length']
        ## self.majorTickWidth = self.prm['pref']['major_tick_width']
        #self.minorTickLength = 1 #self.prm['pref']['minor_tick_length']
        ## self.minorTickWidth = self.prm['pref']['minor_tick_width']
        ## self.tickLabelFontFamily = self.prm['pref']['tick_label_font_family']
        ## self.tickLabelFontWeight = self.prm['pref']['tick_label_font_weight']
        ## self.tickLabelFontStyle = self.prm['pref']['tick_label_font_style']
        ## self.tickLabelFontSize = self.prm['pref']['tick_label_font_size']
        ## self.tickLabelFont = font_manager.FontProperties(family=self.tickLabelFontFamily, weight=self.tickLabelFontWeight, style= self.tickLabelFontStyle, size=self.tickLabelFontSize)
        ## self.xAxisLabel = ''
        ## self.yAxisLabel = ''
        ## self.dpi = self.prm['pref']['dpi']
        ## self.spinesLineWidth = self.prm['pref']['spines_line_width']
        ## self.gridLineWidth = self.prm['pref']['grid_line_width']

        self.mw = QtGui.QWidget(self)
        self.vbl = QtGui.QVBoxLayout(self.mw)
        self.fig = Figure(figsize=(8,8))#facecolor=self.canvasColor, dpi=self.dpi)
        self.ax = self.fig.add_subplot(111)
       
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.mw)
       
        self.ntb = NavigationToolbar(self.canvas, self.mw)
        self.gridOn = QtGui.QCheckBox(self.tr('Grid'))
        #self.gridOn.setChecked(True) #= QtGui.QCheckBox(self.tr('Grid'))
        #self.connect(self.gridOn, QtCore.SIGNAL('stateChanged(int)'), self.toggleGrid)
        self.gridOn.stateChanged[int].connect(self.toggleGrid)
        
       

        self.ntbBox = QtGui.QHBoxLayout()
        self.ntbBox.addWidget(self.ntb)
        self.ntbBox.addWidget(self.gridOn)
        
        self.vbl.addWidget(self.canvas)
        self.vbl.addLayout(self.ntbBox)
        self.mw.setFocus()
        self.setCentralWidget(self.mw)

        if self.checkMultipleHeaders(self.fName):
            self.ax.text(0, 0.5, "The table files appear to contain multiple headers.\n Usually this happens because they contain results \n from different experiments/procedures or \n different check box selections. These table processing \n functions cannot process these type of files, \n and automatic plots are not supported.")
            if pdfPlot == True:
                self.fig.savefig(self.fName.split('.')[0] + '.pdf', format='pdf')
            if winPlot == True:
                self.show()
                self.canvas.draw()
            else:
                self.deleteLater()
            
            return
        if paradigm not in ['adaptive', 'constant1Interval2Alternatives', 'constant1PairSD']:
            self.ax.text(0, 0.5, "Sorry, plotting not yet supported for \n" + paradigm + " paradigm")
            if pdfPlot == True:
                self.fig.savefig(self.fName.split('.')[0] + '.pdf', format='pdf')
            if winPlot == True:
                self.show()
                self.canvas.draw()
            else:
                self.deleteLater()
            
            return
        
        self.dats = pd.read_csv(self.fName, sep=csv_separator)
        idx = copy.copy(self.dats.index)
        self.dats = self.dats.sort('condition')
        self.dats.index = idx
        self.plotData()

        if pdfPlot == True:
             self.fig.savefig(self.fName.split('.')[0] + '.pdf', format='pdf')
        if winPlot == True:
            self.show()
            self.canvas.draw()
        else:
            self.deleteLater()
        
    def plotData(self):
        if self.paradigm == 'adaptive':
            if 'threshold_arithmetic' in self.dats.keys():
                thresh_key = 'threshold_arithmetic'
                procedure = 'arithmetic'
            elif 'threshold_geometric' in self.dats.keys():
                thresh_key = 'threshold_geometric'
                procedure = 'geometric'
            nCnds = len(self.dats[thresh_key])
            xaxvals = np.arange(nCnds)
            self.ax.set_xticks(xaxvals)
            self.ax.set_xticklabels(self.dats['condition'])
            self.ax.set_xlim(-0.5, nCnds-0.5)
            self.ax.set_ylabel(r'Threshold $\pm$ s.e.', fontsize='large')
            self.ax.set_xlabel('Condition', fontsize='large')
            self.ax.xaxis.set_label_coords(0.5, -0.08)
            self.ax.yaxis.set_label_coords(-0.1, 0.5)
            if procedure == 'arithmetic':
                self.ax.errorbar(xaxvals, self.dats[thresh_key], xerr=0, yerr=self.dats['SE'], fmt='o',
                                 capthick=1, capsize=5, marker='o', markersize=10)
            elif procedure == 'geometric':
                self.ax.plot(xaxvals, log10(self.dats[thresh_key]), 'o', markersize=10)
                capsize = 0.03
                for i in range(len(xaxvals)):
                    lo = log10(self.dats[thresh_key][i]) - log10(self.dats['SE'][i])
                    hi = log10(self.dats[thresh_key][i]) + log10(self.dats['SE'][i])
                    l = Line2D([xaxvals[i], xaxvals[i]],[lo, hi])
                    top = Line2D([xaxvals[i]-capsize, xaxvals[i]+capsize], [hi, hi])
                    bot = Line2D([xaxvals[i]-capsize, xaxvals[i]+capsize], [lo, lo])
                    self.ax.add_line(l)
                    self.ax.add_line(top)
                    self.ax.add_line(bot)
                powd = nextPow10Down(10**(self.ax.get_ylim()[0]))
                powup = nextPow10Up(10**(self.ax.get_ylim()[1]))
                majTicks = arange(powd, powup+1)
                self.ax.set_yticks(majTicks)
                yTickLabels = []
                for tick in majTicks:
                    yTickLabels.append(str(10**tick))
                self.ax.set_yticklabels(yTickLabels)
                minTicks = []
                for i in range(len(majTicks)-1):
                    minTicks.extend(log10(linspace(10**majTicks[i], 10**majTicks[i+1], 10)))
                self.ax.set_yticks(minTicks, minor=True)

        elif self.paradigm == 'adaptive_interleaved':
            pass
        elif self.paradigm == 'constant1Interval2Alternatives':
            nCnds = len(self.dats['dprime'])
            xaxvals = np.arange(nCnds)
            self.ax.errorbar(xaxvals, self.dats['dprime'], xerr=0, yerr=0, fmt='o',
                         capthick=0, capsize=0, marker='o', markersize=10)
            self.ax.set_xticks(xaxvals)
            self.ax.set_xticklabels(self.dats['condition'])
            self.ax.set_xlim(-0.5, nCnds-0.5)
            self.ax.set_ylabel("d'", fontsize='large', style='italic')
            self.ax.set_xlabel('Condition', fontsize='large')
            self.ax.xaxis.set_label_coords(0.5, -0.08)
            self.ax.yaxis.set_label_coords(-0.1, 0.5)

            
        elif self.paradigm == 'multipleConstants1Interval2Alternatives':
            pass
        elif self.paradigm == 'constantMIntervalsNAlternatives':
            pass
        elif self.paradigm == 'multipleConstantsMIntervalsNAlternatives':
            pass
        elif self.paradigm == 'constant1PairSD':
            nCnds = len(self.dats['dprime_IO'])
            xaxvals = np.arange(nCnds)
            p1 = self.ax.errorbar(xaxvals, self.dats['dprime_IO'], xerr=0, yerr=0, fmt='o',
                         capthick=0, capsize=0, marker='o', markersize=10)
            p2 = self.ax.errorbar(xaxvals, self.dats['dprime_diff'], xerr=0, yerr=0, fmt='o',
                             capthick=0, capsize=0, marker='s', markersize=10)
            self.ax.set_xticks(xaxvals)
            self.ax.set_xticklabels(self.dats['condition'])
            self.ax.set_xlim(-0.5, nCnds-0.5)
            self.ax.set_ylabel("d'", fontsize='large', style='italic')
            self.ax.set_xlabel('Condition', fontsize='large')
            self.ax.xaxis.set_label_coords(0.5, -0.08)
            self.ax.yaxis.set_label_coords(-0.1, 0.5)
            self.ax.legend([p1[0], p2[0]], ["IO", "Diff."], numpoints=1)

    def toggleGrid(self, state):
        self.ax.grid(True)
        if self.gridOn.isChecked():
            self.ax.grid(True)#True, color=self.gridColor, linewidth=self.gridLineWidth)
            self.ax.grid(True, 'minor', linewidth=0.6)#True, color=self.gridColor, linewidth=self.gridLineWidth)
        else:
            self.ax.grid(False)
            self.ax.grid(False, 'minor')
        self.canvas.draw()

    def checkMultipleHeaders(self, fName):
        f = open(fName, 'r')
        l = f.readlines()
        if l[0] == "The table files appear to contain multiple headers.\n":
            return True
        else:
            return False
        
        
