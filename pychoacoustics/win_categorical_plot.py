# -*- coding: utf-8 -*- 
#   Copyright (C) 2008-2023 Samuele Carcagno <sam.carcagno@gmail.com>
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

import matplotlib
from cycler import cycler

from .pyqtver import*

if pyqtversion == 5:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtWidgets import QCheckBox, QHBoxLayout, QMainWindow, QVBoxLayout, QWidget
    # import the Qt4Agg FigureCanvas object, that binds Figure to
    # Qt4Agg backend. It also inherits from QWidget
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    # import the NavigationToolbar Qt4Agg widget
    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
    matplotlib.rcParams['backend'] = "Qt5Agg"
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtWidgets import QCheckBox, QHBoxLayout, QMainWindow, QVBoxLayout, QWidget
    # import the QtAgg FigureCanvas object, that binds Figure to
    # QtAgg backend. It also inherits from QWidget
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
    # import the NavigationToolbar QtAgg widget
    from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
    matplotlib.rcParams['backend'] = "QtAgg"
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
from .utils_general import*

#mpl.rcParams['font.family'] = 'sans-serif'

#fontPath = os.path.abspath(os.path.dirname(__file__)+'/../') + '/data/Ubuntu-R.ttf'
#fontPath = '/media/ntfsShared/lin_home/auditory/code/pychoacoustics/pychoacoustics-qt4/development/dev/data/Ubuntu-R.ttf'
#prop = fm.FontProperties(fname=fontPath)
#mpl.rcParams.update({'font.size': 16})

class categoricalPlot(QMainWindow):
    def __init__(self, parent, plot_type, fName, winPlot, pdfPlot, paradigm, csv_separator, plot_params, prm):
        QMainWindow.__init__(self, parent)
        
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.prm = prm
        self.paradigm = paradigm
        self.fName = fName
        self.plotSupportedParadigms = ["adaptive",
                                       "adaptive_interleaved",
                                       "constant1Interval2Alternatives",
                                       "constant1PairSD",
                                       "constantMIntervalsNAlternatives",
                                       "multipleConstantsABX",
                                       "multipleConstants1PairSD",
                                       "multipleConstants1Interval2Alternatives",
                                       "multipleConstantsMIntervalsNAlternatives"]
            
        self.pchs = ["o", "s", "v", "p", "h", "8", "*", "x", "+", "d", ",", "^", "<", ">", "1", "2", "3", "4", "H", "D", ".", "|", "_"]  
        #[0, 'H', 2, 3, 4, '<', 6, 'h', 'x', '1', '^', 'o', '8', 'v', ',', '.', '3', 'D', '4', '', 5, '|', '*', 1, 7, '2', 'd', 's', '>', '+', ' ', '_', 'p']

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
        mpl.rcParams['axes.prop_cycle'] = cycler('color', ["#000000", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7"])

        
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
        #self.currLocale.setNumberOptions(self.currLocale.NumberOption.OmitGroupSeparator | self.currLocale.NumberOption.RejectGroupSeparator)

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

        self.mw = QWidget(self)
        self.vbl = QVBoxLayout(self.mw)
        self.fig = Figure(figsize=(8,8))#facecolor=self.canvasColor, dpi=self.dpi)
        if self.paradigm in ["constantMIntervalsNAlternatives",
                             "multipleConstants1PairSD",
                             "multipleConstantsABX",
                             "multipleConstantsMIntervalsNAlternatives"]:
            self.fig = Figure(figsize=(12,8))#facecolor=self.canvasColor, dpi=self.dpi)
            self.ax = self.fig.add_subplot(121)
            self.ax2 = self.fig.add_subplot(122)
        else:
            self.fig = Figure(figsize=(8,8))#facecolor=self.canvasColor, dpi=self.dpi)
            self.ax = self.fig.add_subplot(111)
       
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.mw)
       
        self.ntb = NavigationToolbar(self.canvas, self.mw)
        self.gridOn = QCheckBox(self.tr("Grid"))
        self.gridOn.stateChanged[int].connect(self.toggleGrid)
        
       

        self.ntbBox = QHBoxLayout()
        self.ntbBox.addWidget(self.ntb)
        self.ntbBox.addWidget(self.gridOn)
        
        self.vbl.addWidget(self.canvas)
        self.vbl.addLayout(self.ntbBox)
        self.mw.setFocus()
        self.setCentralWidget(self.mw)

        if self.checkMultipleHeaders(self.fName):
            self.ax.text(0, 0.5, "The table files appear to contain multiple headers.\n Usually this happens because they contain results \n from different experiments/procedures or \n different check box selections. These table processing \n functions cannot process these types of files, \n and automatic plots are not supported.")
            if pdfPlot == True:
                self.fig.savefig(self.fName.split('.')[0] + '.pdf', format='pdf')
            if winPlot == True:
                self.show()
                self.canvas.draw()
            else:
                self.deleteLater()
            
            return
        if paradigm not in self.plotSupportedParadigms:
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
        self.dats = self.dats.sort_values('condition')
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
                powd = prevPow10(10**(self.ax.get_ylim()[0]))
                powup = nextPow10(10**(self.ax.get_ylim()[1]))
                majTicks = arange(powd, powup+1)
                self.ax.set_yticks(majTicks)
                yTickLabels = []
                for tick in majTicks:
                    yTickLabels.append(str(10.0**tick))
                self.ax.set_yticklabels(yTickLabels)
                minTicks = []
                for i in range(len(majTicks)-1):
                    minTicks.extend(log10(linspace(10.0**majTicks[i], 10.0**majTicks[i+1], 10)))
                self.ax.set_yticks(minTicks, minor=True)

        elif self.paradigm == 'adaptive_interleaved':
            if 'threshold_arithmetic_track1' in self.dats.keys():
                thresh_key = 'threshold_arithmetic_track'
                procedure = 'arithmetic'
            elif 'threshold_geometric_track1' in self.dats.keys():
                thresh_key = 'threshold_geometric_track'
                procedure = 'geometric'

            nTracks = 0
            keys = self.dats.columns.values
            for key in keys:
                if procedure == "arithmetic":
                    if key[0:26] == 'threshold_arithmetic_track':
                        nTracks = nTracks +1
                elif procedure == "geometric":
                    if key[0:25] == 'threshold_geometric_track':
                        nTracks = nTracks +1

            nCnds = len(self.dats[thresh_key+str(1)])
            xaxvals = np.arange(nCnds)
            self.ax.set_xticks(xaxvals)
            self.ax.set_xticklabels(self.dats['condition'])
            self.ax.set_xlim(-0.5, nCnds-0.5)
            self.ax.set_ylabel(r'Threshold $\pm$ s.e.', fontsize='large')
            self.ax.set_xlabel('Condition', fontsize='large')
            self.ax.xaxis.set_label_coords(0.5, -0.08)
            self.ax.yaxis.set_label_coords(-0.1, 0.5)
            for tr in range(nTracks):
                if procedure == 'arithmetic':
                    self.ax.errorbar(xaxvals, self.dats[thresh_key+str(tr+1)], xerr=0, yerr=self.dats['SE_track'+str(tr+1)], fmt='o',
                                     capthick=1, capsize=5, marker=self.pchs[tr], markersize=10, label="Track"+str(tr+1))
                elif procedure == 'geometric':
                    self.ax.plot(xaxvals, log10(self.dats[thresh_key+str(tr+1)]), marker=self.pchs[tr], markersize=10, label="Track"+str(tr+1), lw=0)
                    capsize = 0.03
                    for i in range(len(xaxvals)):
                        lo = log10(self.dats[thresh_key+str(tr+1)][i]) - log10(self.dats['SE_track'+str(tr+1)][i])
                        hi = log10(self.dats[thresh_key+str(tr+1)][i]) + log10(self.dats['SE_track'+str(tr+1)][i])
                        l = Line2D([xaxvals[i], xaxvals[i]],[lo, hi])
                        top = Line2D([xaxvals[i]-capsize, xaxvals[i]+capsize], [hi, hi])
                        bot = Line2D([xaxvals[i]-capsize, xaxvals[i]+capsize], [lo, lo])
                        self.ax.add_line(l)
                        self.ax.add_line(top)
                        self.ax.add_line(bot)
                    powd = prevPow10(10.0**(self.ax.get_ylim()[0]))
                    powup = nextPow10(10.0**(self.ax.get_ylim()[1]))
                    majTicks = arange(powd, powup+1)
                    self.ax.set_yticks(majTicks)
                    yTickLabels = []
                    for tick in majTicks:
                        yTickLabels.append(str(10.0**tick))
                    self.ax.set_yticklabels(yTickLabels)
                    minTicks = []
                    for i in range(len(majTicks)-1):
                        minTicks.extend(log10(linspace(10.0**majTicks[i], 10.0**majTicks[i+1], 10)))
                    self.ax.set_yticks(minTicks, minor=True)

            yl = self.ax.get_ylim(); r = (yl[1]-yl[0])*10/100
            self.ax.set_ylim(yl[0]-r/2, yl[1]+r*4) 

            handles, labels = self.ax.get_legend_handles_labels()
            if procedure == "arithmetic":
                handles = [h[0] for h in handles]
            self.ax.legend(handles, labels, numpoints=1, ncol=2)



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
            nSubCond = 0
            keys = self.dats.columns.values
            for key in keys:
                if key[0:11] == 'dprime_subc':
                    nSubCond = nSubCond +1

            nCnds = len(self.dats['dprime_subc1'])
            xaxvals = np.arange(nCnds)
            p1s = []
            for subc in range(nSubCond):
                p1 = self.ax.plot(xaxvals, self.dats['dprime_subc'+str(subc+1)], marker=self.pchs[subc], lw=0, label="Subc. "+str(subc+1), markersize=10)
                self.ax.set_xticks(xaxvals)
                self.ax.set_xticklabels(self.dats['condition'])
                self.ax.set_xlim(-0.5, nCnds-0.5)
                self.ax.set_ylabel("d'", fontsize='large', style='italic')
                self.ax.set_xlabel('Condition', fontsize='large')
                self.ax.xaxis.set_label_coords(0.5, -0.08)
                self.ax.yaxis.set_label_coords(-0.1, 0.5)
                #self.ax.set_title("d'", style="italic")
                p1s.append(p1)

            yl = self.ax.get_ylim(); r = (yl[1]-yl[0])*10/100
            self.ax.set_ylim(yl[0]-r/2, yl[1]+r/2) 

            handles, labels = self.ax.get_legend_handles_labels()
            self.ax.legend(handles, labels, numpoints=1, ncol=2)


        elif self.paradigm == 'constantMIntervalsNAlternatives':
            nCnds = len(self.dats['dprime'])
            xaxvals = np.arange(nCnds)
            p1 = self.ax.plot(xaxvals, self.dats['dprime'], marker="o", lw=0, markersize=10)
            p2 = self.ax2.plot(xaxvals, self.dats['perc_corr'], marker="o", lw=0, markersize=10)
            self.ax.set_xticks(xaxvals)
            self.ax.set_xticklabels(self.dats['condition'])
            self.ax.set_xlim(-0.5, nCnds-0.5)
            self.ax.set_ylabel("d'", fontsize='large', style='italic')
            self.ax.set_xlabel('Condition', fontsize='large')
            self.ax.xaxis.set_label_coords(0.5, -0.08)
            self.ax.yaxis.set_label_coords(-0.17, 0.5)
            self.ax.set_title("d'")

            self.ax2.set_xticks(xaxvals)
            self.ax2.set_xticklabels(self.dats['condition'])
            self.ax2.set_xlim(-0.5, nCnds-0.5)
            self.ax2.set_ylabel("Percent Correct", fontsize='large', style='italic')
            self.ax2.set_xlabel('Condition', fontsize='large')
            self.ax2.xaxis.set_label_coords(0.5, -0.08)
            self.ax2.yaxis.set_label_coords(-0.17, 0.5)
            self.ax2.set_title("Percent Correct")

            yl = self.ax.get_ylim(); r = (yl[1]-yl[0])*10/100
            self.ax.set_ylim(yl[0]-r/2, yl[1]+r/2) 
            yl = self.ax2.get_ylim(); r = (yl[1]-yl[0])*10/100
            self.ax2.set_ylim(yl[0]-r/2, yl[1]+r/2)
            self.fig.subplots_adjust(wspace=0.3)    

        elif self.paradigm == 'multipleConstantsMIntervalsNAlternatives':
            nSubCond = 0
            keys = self.dats.columns.values
            for key in keys:
                if key[0:11] == 'dprime_subc':
                    nSubCond = nSubCond +1
                   
            nCnds = len(self.dats['dprime_subc1'])
            xaxvals = np.arange(nCnds)
            p1s = []; p2s = []
            for subc in range(nSubCond):
                p1 = self.ax.plot(xaxvals, self.dats['dprime_subc'+str(subc+1)], marker=self.pchs[subc], lw=0, label="Diff. "+str(subc+1), markersize=10)
                p2 = self.ax2.plot(xaxvals, self.dats['perc_corr_subc'+str(subc+1)], marker=self.pchs[subc], lw=0, label="Diff. "+str(subc+1), markersize=10)
            self.ax.set_xticks(xaxvals)
            self.ax.set_xticklabels(self.dats['condition'])
            self.ax.set_xlim(-0.5, nCnds-0.5)
            self.ax.set_ylabel("d'", fontsize='large', style='italic')
            self.ax.set_xlabel('Condition', fontsize='large')
            self.ax.xaxis.set_label_coords(0.5, -0.08)
            self.ax.yaxis.set_label_coords(-0.17, 0.5)
            self.ax.set_title("d'", style="italic")

            self.ax2.set_xticks(xaxvals)
            self.ax2.set_xticklabels(self.dats['condition'])
            self.ax2.set_xlim(-0.5, nCnds-0.5)
            self.ax2.set_ylabel("Percent Correct", fontsize='large', style='italic')
            self.ax2.set_xlabel('Condition', fontsize='large')
            self.ax2.xaxis.set_label_coords(0.5, -0.08)
            self.ax2.yaxis.set_label_coords(-0.17, 0.5)
            self.ax2.set_title("Percent Correct")

            yl = self.ax.get_ylim(); r = (yl[1]-yl[0])*10/100
            self.ax.set_ylim(yl[0]-r/2, yl[1]+r*4) 
            yl = self.ax2.get_ylim(); r = (yl[1]-yl[0])*10/100
            self.ax2.set_ylim(yl[0]-r/2, yl[1]+r*4)
            self.fig.subplots_adjust(wspace=0.3)

            handles, labels = self.ax.get_legend_handles_labels()
            self.ax.legend(handles, labels, numpoints=1, ncol=2)
            handles2, labels2 = self.ax2.get_legend_handles_labels()
            self.ax2.legend(handles2, labels2, numpoints=1, ncol=2)

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
            yl = self.ax.get_ylim(); r = (yl[1]-yl[0])*10/100
            self.ax.set_ylim(yl[0]-r/2, yl[1]+r*4) 
            self.ax.legend([p1[0], p2[0]], ["IO", "Diff."], numpoints=1)
        elif self.paradigm in ['multipleConstants1PairSD',
                               'multipleConstantsABX']:
            nSubCond = 0
            keys = self.dats.columns.values
            for key in keys:
                if key[0:14] == 'dprime_IO_pair':
                    nSubCond = nSubCond +1

            nCnds = len(self.dats['dprime_IO_pair1'])
            xaxvals = np.arange(nCnds)
            p1s = []; p2s = []
            for subc in range(nSubCond):
                p1 = self.ax.plot(xaxvals, self.dats['dprime_IO_pair'+str(subc+1)], marker=self.pchs[subc], lw=0, label="pair"+str(subc+1), markersize=10)
                p2 = self.ax2.plot(xaxvals, self.dats['dprime_diff_pair'+str(subc+1)], marker=self.pchs[subc], lw=0, label="pair"+str(subc+1), markersize=10)
                self.ax.set_xticks(xaxvals)
                self.ax.set_xticklabels(self.dats['condition'])
                self.ax.set_xlim(-0.5, nCnds-0.5)
                self.ax.set_ylabel("d'", fontsize='large', style='italic')
                self.ax.set_xlabel('Condition', fontsize='large')
                self.ax.xaxis.set_label_coords(0.5, -0.08)
                self.ax.yaxis.set_label_coords(-0.1, 0.5)
                self.ax.set_title("d' IO")
                p1s.append(p1)

                self.ax2.set_xticks(xaxvals)
                self.ax2.set_xticklabels(self.dats['condition'])
                self.ax2.set_xlim(-0.5, nCnds-0.5)
                self.ax2.set_ylabel("d'", fontsize='large', style='italic')
                self.ax2.set_xlabel('Condition', fontsize='large')
                self.ax2.xaxis.set_label_coords(0.5, -0.08)
                self.ax2.yaxis.set_label_coords(-0.1, 0.5)
                self.ax2.set_title("d' diff")
                p2s.append(p2)
            yl = self.ax.get_ylim(); r = (yl[1]-yl[0])*10/100
            self.ax.set_ylim(yl[0]-r/2, yl[1]+r*4) 
            yl = self.ax2.get_ylim(); r = (yl[1]-yl[0])*10/100
            self.ax2.set_ylim(yl[0]-r/2, yl[1]+r*4) 

            handles, labels = self.ax.get_legend_handles_labels()
            self.ax.legend(handles, labels, numpoints=1, ncol=2)
            handles2, labels2 = self.ax2.get_legend_handles_labels()
            self.ax2.legend(handles2, labels2, numpoints=1, ncol=2)


    def toggleGrid(self, state):
        self.ax.grid(True)
        if self.gridOn.isChecked():
            self.ax.grid(True)#True, color=self.gridColor, linewidth=self.gridLineWidth)
            self.ax.grid(True, 'minor', linewidth=0.6)#True, color=self.gridColor, linewidth=self.gridLineWidth)
            try:
                self.ax2.grid(True)#True, color=self.gridColor, linewidth=self.gridLineWidth)
                self.ax2.grid(True, 'minor', linewidth=0.6)#True, color=self.gridColor, linewidth=self.gridLineWidth)
            except:
                pass
        else:
            self.ax.grid(False)
            self.ax.grid(False, 'minor')
            try:
                self.ax2.grid(False)
                self.ax2.grid(False, 'minor')
            except:
                pass

        self.canvas.draw()

    def checkMultipleHeaders(self, fName):
        f = open(fName, 'r')
        l = f.readlines()
        if l[0] == "The table files appear to contain multiple headers.\n":
            return True
        else:
            return False


