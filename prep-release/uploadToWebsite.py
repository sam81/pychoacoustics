import ftplib, os, platform

passwd = input('FTP password: ')
session = ftplib.FTP('ftp.samcarcagno.altervista.org', 'samcarcagno', passwd)
session.cwd('pychoacoustics/pych_builds')


f = open('../setup.py', 'r')
ln = f.readlines()
f.close()
for i in range(len(ln)):
    if ln[i].strip().split('=')[0].strip() == "version":
           ver = ln[i].strip().split('=')[1].strip()
           ver = ver[1:len(ver)-2]
fNames = ["../dist/pychoacoustics-" + ver + ".tar.gz",
          "../dist/pychoacoustics-" + ver + ".zip"
          "../dist/pychoacoustics-pyqt4-" + ver + ".tar.gz"
          "../dist/pychoacoustics-pyqt4-" + ver + ".zip"
          "../dist/pychoacoustics-pyside-" + ver + ".tar.gz"
          "../dist/pychoacoustics-pyside-" + ver + ".zip"]
          
for fName in fNames:
    fHandle = open(fName, 'rb')
    session.storebinary("STOR " + fName, fHandle)

htmlPagePath = "/media/ntfsShared/lin_home/dc/devel/websites/xoom-website/xoom/pychoacoustics/pychoacoustics.html"
fIn = open(htmlPagePath, "r")
lns = fIn.readlines()
fIn.close()


for i in range(len(lns)):
    if lns[i][0:26] == '<li> <a href="pych_builds/':
        if lns[i].split("</a>")[1] == ' Linux/UNIX source package (PyQt5)</li>\n':
            lns[i] = '<li> <a href="pych_builds/pychoacoustics-'+ver+'.tar.gz">pychoacoustics-'+ver+'.tar.gz<a> Linux/UNIX source package (PyQt5)</li>'
        elif lns[i].split("</a>")[1] == ' Windows source package (PyQt5)</li>\n':
            lns[i] = '<li> <a href="pych_builds/pychoacoustics-'+ver+'.zip">pychoacoustics-'+ver+'.zip</a> Windows source package (PyQt5)</li>'
        elif lns[i].split("</a>")[1] == ' Linux/UNIX source package (PyQt4)</li>\n':
            lns[i] = '<li> <a href="pych_builds/pychoacoustics-pyqt4-'+ver+'.tar.gz">pychoacoustics-pyqt4-'+ver+'.tar.gz<a> Linux/UNIX source package (PyQt4)</li>'
        elif lns[i].split("</a>")[1] == ' Windows source package (PyQt4)</li>\n':
            lns[i] = '<li> <a href="pych_builds/pychoacoustics-pyqt4-'+ver+'.zip">pychoacoustics-pyqt4-'+ver+'.zip</a> Windows source package (PyQt4)</li>'
        elif lns[i].split("</a>")[1] == ' Linux/UNIX source package (PySide)</li>\n':
            lns[i] = '<li> <a href="pych_builds/pychoacoustics-pyside-'+ver+'.tar.gz">pychoacoustics-pyside-'+ver+'.tar.gz<a> Linux/UNIX source package (PySide)</li>'
        elif lns[i].split("</a>")[1] == ' Windows source package (PySide)</li>\n':
            lns[i] = '<li> <a href="pych_builds/pychoacoustics-pyside-'+ver+'.zip">pychoacoustics-pyside-'+ver+'.zip</a> Windows source package (PySide)</li>'
        
fOut = open(htmlPathPage, 'w')
fOut.writelines(lns)
fOut.close()

session.cwd('../')
fHandle = open(htmlPathPage, 'rb')
session.storebinary("STOR " + htmlPathPage, fHandle)
