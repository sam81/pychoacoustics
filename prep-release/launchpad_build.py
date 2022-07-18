#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, distro, time

pparev = input("ppa revision number: ")
pparev = '-ppa'+str(pparev)
#pparev = ''
series = input("distro series: ")

thisDir = os.getcwd()
#get current version number from setup.py
f = open('../setup.py', 'r')
ln = f.readlines()
f.close()
for i in range(len(ln)):
    if ln[i].strip().split('=')[0].strip() == "version":
           ver = ln[i].strip().split('=')[1].strip()
           ver = ver[1:len(ver)-2]
tarball_path = "../dist/pychoacoustics-" + ver + ".tar.gz"
buildpath = "../../pkg_source_build/" + distro.linux_distribution()[0] + '_' + series 

if os.path.exists(buildpath) == False:
    os.makedirs(buildpath)

#copy tarball to the build directory
cmd = "cp " + tarball_path + " " + buildpath
os.system(cmd)

#update debian changelog
f = open('launchpad/debian/changelog', 'r')
ln = f.readlines()
f.close()

l0 = ['pychoacoustics (' + ver + pparev + '~'+series+') '+ series+'; urgency=low',
      '\n\n',
      '  * New upstream release',
      '\n\n',
      ' -- Samuele Carcagno <sam.carcagno@gmail.com>  ' + time.strftime("%a, %d %b %Y %H:%M:%S +0100", time.gmtime()),
      '\n\n']
l0.extend(ln)
f = open('launchpad/debian/changelog', 'w')
ln = f.writelines(l0)
f.close()

#move to the build directory
os.chdir(buildpath)
#os.system("mv " + "pychoacoustics-" + ver + ".tar.gz " + "pychoacoustics-" + ver + pparev + ".tar.gz")
#unpack the tarball
cmd2 = "tar -xvf " + "pychoacoustics-" + ver + ".tar.gz"
os.system(cmd2)
#change name
#os.system("mv " + "pychoacoustics-" + ver + " " + "pychoacoustics-" + ver )

#copy debian files in the package build directory
cmd3 = "cp -R " + "../../pychoacoustics/prep-release/launchpad/debian ./pychoacoustics-" + ver 
os.system(cmd3)

#move into package build directory
os.chdir("pychoacoustics-" + ver)
#build the package
#For Debian
#os.system("dpkg-buildpackage -F")

#For Launchpad Upload
os.system("debuild -S -sa")

#back to the buildpath directory
os.chdir("../")
#upload to launchpad
uploadCmd = "dput ppa:samuele-carcagno/hearinglab " + "pychoacoustics_"+ ver + pparev + "~" + series + "_source.changes"
os.system(uploadCmd)
