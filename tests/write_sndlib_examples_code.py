#! /usr/bin/env python
# -*- coding: utf-8 -*-

fIn = open("../pychoacoustics/sndlib.py", "r")
lns = fIn.readlines()
fIn.close()

startPoints = []
stopPoints = []
for i in range(len(lns)):
    thisLine = lns[i]
    if thisLine.strip() == "Examples":
        startPoints.append(i+2)
        endFound = False; l = i+2
        while endFound == False:
            if lns[l].strip() == '"""':
                stopPoints.append(l)
                endFound = True
            l = l+1



exLines = []
exLines.append("#! /usr/bin/env python \n")
exLines.append("# -*- coding: utf-8 -*- \n")
exLines.append("import os, sys \n")
exLines.append("sys.path.insert(0, os.path.abspath('../')) \n")
exLines.append("from pychoacoustics.sndlib import* \n")
for i in range(len(startPoints)):
    for l in range(stopPoints[i]-startPoints[i]):
        if lns[startPoints[i]+l].strip()[0:3] == ">>>" or lns[startPoints[i]+l].strip()[0:3] == "...":
            ll = len(lns[startPoints[i]+l].strip())
            thisLine = lns[startPoints[i]+l].strip()[3:ll]
        else:
            thisLine = lns[startPoints[i]+l].strip()
        exLines.append(thisLine.strip() + "\n")

fOut = open("sndlib_examples_code.py", "w")
fOut.writelines(exLines)
fOut.close()



