#! /usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright (C) 2008-2013 Samuele Carcagno <sam.carcagno@gmail.com>
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
#import sip
#sip.setapi("QString", 2)

from PyQt4 import QtGui, QtCore
import signal
import argparse, fnmatch, os, sys, time, traceback
from pychoacoustics_pack import qrc_resources
from pychoacoustics_pack import global_parameters
from pychoacoustics_pack.control_window import*
signal.signal(signal.SIGINT, signal.SIG_DFL)
#
import logging
local_dir = os.path.expanduser("~") +'/.local/share/data/pychoacoustics/'
if os.path.exists(local_dir) == False:
    os.makedirs(local_dir)
stderrFile = os.path.expanduser("~") +'/.local/share/data/pychoacoustics/pychoacoustics_stderr_log.txt'

logging.basicConfig(filename=stderrFile,level=logging.DEBUG,)

def excepthook(except_type, except_val, tbck):
    """ Show errors in message box"""
    # recover traceback
    tb = traceback.format_exception(except_type, except_val, tbck)
    def onClickSaveTbButton():
        ftow = QtGui.QFileDialog.getSaveFileName(None, 'Choose where to save the traceback', "traceback.txt", 'All Files (*)')
        if len(ftow) > 0:
            if fnmatch.fnmatch(ftow, '*.txt') == False:
                ftow = ftow + '.txt'
            fName = open(ftow, 'w')
            fName.write("".join(tb))
            fName.close()
    
    
    
    diag = QtGui.QDialog(None, Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
    diag.window().setWindowTitle("Critical Error!")
    siz = QtGui.QVBoxLayout()
    lay = QtGui.QVBoxLayout()
    saveTbButton = QtGui.QPushButton("Save Traceback", diag)
    QtCore.QObject.connect(saveTbButton,
                           QtCore.SIGNAL('clicked()'), onClickSaveTbButton)
    lab = QLabel("Sorry, something went wrong. The attached traceback can help you troubleshoot the problem: \n\n" + "".join(tb))
    lab.setMargin(10)
    lab.setWordWrap(True)
    lab.setTextInteractionFlags(Qt.TextSelectableByMouse)
    lab.setStyleSheet("QLabel { background-color: white }");
    lay.addWidget(lab)

    sc = QtGui.QScrollArea()
    sc.setWidget(lab)
    siz.addWidget(sc)#SCROLLAREA IS A WIDGET SO IT NEEDS TO BE ADDED TO A LAYOUT

    buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Cancel)
        
    diag.connect(buttonBox, QtCore.SIGNAL("accepted()"),
                 diag, QtCore.SLOT("accept()"))
    diag.connect(buttonBox, QtCore.SIGNAL("rejected()"),
                 diag, QtCore.SLOT("reject()"))
    siz.addWidget(saveTbButton)
    siz.addWidget(buttonBox)
    diag.setLayout(siz)
    


    diag.exec_()

    timeStamp = ''+ time.strftime("%d/%m/%y %H:%M:%S", time.localtime()) + ' ' + '\n'
    logMsg = timeStamp + ''.join(tb)
    logging.debug(logMsg)

 

def main(argv):

    prm = {}
    prm['calledWithPrm'] = False
    prm['calledWithReset'] = False
    prm['calledWithRecursionDepth'] = False
    prm['calledWithAutostart'] = False
    prm['hideWins'] = False
    prm['quit'] = False
    prm['progbar'] = False
    prm['blockProgbar'] = False
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file", help="Load parameters file", nargs='?', const='', default='')
    parser.add_argument("-r", "--results", help="Results file")
    parser.add_argument("-l", "--listener", help="Listener Name")
    parser.add_argument("-s", "--session", help="Session Label")
    parser.add_argument("-c", "--conceal", help="Hide Control and Parameters Windows", action="store_true")
    parser.add_argument("-p", "--progbar", help="Show the progress bar", action="store_true")
    parser.add_argument("-b", "--blockprogbar", help="Show the block progress bar", action="store_true")
    parser.add_argument("-q", "--quit", help="Quit after finished", action="store_true")
    parser.add_argument("-a", "--autostart", help="Automatically start the first stored block", action="store_true")
    parser.add_argument("-x", "--recursion-depth", help="Sets the maximum recursion depth", type=int)
    parser.add_argument("-k", "--reset", help="Reset block positions", action="store_true")
    parser.add_argument("-g", "-graphicssystem", "--graphicssystem", help="Sets the backend to be used for on-screen widgets and QPixmaps. Available options are native (default) raster and opengl (experimental)")#, choices=['raster', 'opengl', 'native'])
    parser.add_argument("-d", "--display", help="This option is only valid for X11 and sets the X display (default is $DISPLAY)")


    args = parser.parse_args()

    if len(args.file) > 0:
        prm['calledWithPrm'] = True
        prm['prmFile'] = args.file
    if args.results:
        prm['resultsFile'] = args.results
    if args.listener:
        prm['listener'] = args.listener
    if args.session:
        prm['sessionLabel'] = args.session
    if args.conceal:
        prm['hideWins'] = True
    if args.progbar:
        prm['progbar'] = True
    if args.blockprogbar:
        prm['blockProgbar'] = True
    if args.quit:
        prm['quit'] = True
    if args.autostart:
        prm['calledWithAutostart'] = True
    if args.recursion_depth:
        prm['calledWithRecursionDepth'] = True
        prm['cmdLineMaxRecursionDepth'] = args.recursion_depth
    if args.reset:
        prm['calledWithReset'] = True
    if args.graphicssystem:
        prm['graphicssystem'] = args.graphicssystem
    if args.display:
        prm['display'] = args.display
  
   
   
    
    prm = global_parameters.get_prefs(prm)
    callArgs = sys.argv
    if 'display' in prm:
        callArgs = callArgs + ['-display', prm['display']]
    if 'graphicssystem' in prm:
        callArgs = callArgs + ['-graphicssystem', prm['graphicssystem']]
    app = QtGui.QApplication(callArgs)
     

    sys.excepthook = excepthook
    #LOCALE LOADING
    # qtTranslator is the translator for default qt component labels (OK, cancel button dialogs etc...)
    locale = QtCore.QLocale().system().name() #returns a string such as en_US
    qtTranslator = QtCore.QTranslator()
    if qtTranslator.load("qt_" + locale, ":/translations/"):
        app.installTranslator(qtTranslator)
    # appTranslator is the translator for labels created for the program
    appTranslator = QtCore.QTranslator()
    if appTranslator.load("pychoacoustics_" + locale, ":/translations/"):
        app.installTranslator(appTranslator)
    prm['currentLocale'] = QtCore.QLocale(locale)
    QtCore.QLocale.setDefault(prm['currentLocale'])
    prm['currentLocale'].setNumberOptions(prm['currentLocale'].OmitGroupSeparator | prm['currentLocale'].RejectGroupSeparator)

    if prm['pref']['country'] != "System Settings":
        locale =  prm['pref']['language']  + '_' + prm['pref']['country']#returns a string such as en_US
        qtTranslator = QtCore.QTranslator()
        if qtTranslator.load("qt_" + locale, ":/translations/"):
            app.installTranslator(qtTranslator)
        appTranslator = QtCore.QTranslator()
        if appTranslator.load("pychoacoustics_" + locale, ":/translations/") or locale == "en_US":
            app.installTranslator(appTranslator)
            prm['currentLocale'] = QtCore.QLocale(locale)
            QtCore.QLocale.setDefault(prm['currentLocale'])
            prm['currentLocale'].setNumberOptions(prm['currentLocale'].OmitGroupSeparator | prm['currentLocale'].RejectGroupSeparator)
    responseBoxLocale =  prm['pref']['responseBoxLanguage']  + '_' + prm['pref']['responseBoxCountry']#returns a string such as en_US
    responseBoxTranslator = QtCore.QTranslator()
    responseBoxTranslator.load("pychoacoustics_" + responseBoxLocale, ":/translations/")
    prm['rbTrans'] = responseBoxTranslator
    prm = global_parameters.set_global_parameters(prm)
    app.setWindowIcon(QtGui.QIcon(":/Machovka_Headphones.svg"))
    x = pychControlWin(parent=None, prm=prm)
    sys.exit(app.exec_())
    




if __name__ == "__main__":
    main(sys.argv[1:])
