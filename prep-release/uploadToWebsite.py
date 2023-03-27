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
fPaths = ["../dist/pychoacoustics-" + ver + ".tar.gz",
          "../dist/pychoacoustics-" + ver + ".zip"]

for fPath in fPaths:
    print("Uploading: " + fPath)
    fHandle = open(fPath, 'rb')
    session.storbinary("STOR " + fPath.split('/')[2], fHandle)

htmlPagePath = "/media/ntfsShared/lin_home/dc/devel/websites/xoom-website/altervista/pychoacoustics/pychoacoustics.html"
fIn = open(htmlPagePath, "r")
lns = fIn.readlines()
fIn.close()


for i in range(len(lns)):
    if lns[i][0:26] == '<li> <a href="pych_builds/':
        if lns[i].split("</a>")[1].strip() == 'Linux/UNIX source package (PyQt5)</li>':
            lns[i] = '<li> <a href="pych_builds/pychoacoustics-'+ver+'.tar.gz">pychoacoustics-'+ver+'.tar.gz</a> Linux/UNIX source package (PyQt5)</li>\n'
        elif lns[i].split("</a>")[1].strip() == 'Windows source package (PyQt5)</li>':
            lns[i] = '<li> <a href="pych_builds/pychoacoustics-'+ver+'.zip">pychoacoustics-'+ver+'.zip</a> Windows source package (PyQt5)</li>\n'

        
fOut = open(htmlPagePath, 'w')
fOut.writelines(lns)
fOut.close()

session.cwd('../')
fHandle = open(htmlPagePath, 'rb')
session.storbinary("STOR " + "pychoacoustics.html", fHandle)
