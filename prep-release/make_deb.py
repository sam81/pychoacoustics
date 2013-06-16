#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, time

f = open('../setup.py', 'r')
ln = f.readlines()
f.close()
for i in range(len(ln)):
    if ln[i].strip().split('=')[0].strip() == "version":
           ver = ln[i].strip().split('=')[1].strip()
           ver = ver[1:len(ver)-2]
tarball_path = "../dist/pychoacoustics-" + ver + ".tar.gz"
cmd = "cp " + tarball_path + " ../../builddir"
os.system(cmd)

f = open('debian/changelog', 'r')
ln = f.readlines()
f.close()

l0 = ['pychoacoustics (' + ver + ') unstable; urgency=low',
      '\n\n',
      '  * New upstream release',
      '\n\n',
      ' -- Samuele Carcagno <sam.carcagno@gmail.com>  ' + time.strftime("%a, %d %b %Y %H:%M:%S +0100", time.gmtime()),
      '\n\n']
l0.extend(ln)
f = open('debian/changelog', 'w')
ln = f.writelines(l0)
f.close()

os.chdir('../../builddir/')

cmd2 = "tar -xvf " + "pychoacoustics-" + ver + ".tar.gz"
os.system(cmd2)

cmd3 = "cp -R " + "../dev/prep-release/debian/ ./pychoacoustics-" + ver
os.system(cmd3)


os.chdir("pychoacoustics-" + ver)
os.system("dpkg-buildpackage -F")
