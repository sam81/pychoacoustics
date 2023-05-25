#! /usr/bin/env python
# -*- coding: utf-8 -*-

import distro, os, platform, requests, time

pparev = input("ppa revision number: ")
pparev = '-ppa'+str(pparev)

series = os.popen("lsb_release -c").read().split('\t')[1].strip() #input("distro series: ")
#series = os.popen("cat /etc/debian_version").read().split('/')[0].strip() #input("distro series: ")
#publish = input("publish ('y'/'n')?: ")
package = "pychoacoustics"
architecture = os.popen("dpkg --print-architecture").read().strip()
component = "main"

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
buildpath = "../../pkg_build/" + distro.id() + '_' + distro.version() + '_' + platform.uname()[4]

if os.path.exists(buildpath) == False:
    os.makedirs(buildpath)

#copy tarball to the build directory
cmd = "cp " + tarball_path + " " + buildpath
os.system(cmd)

#update debian changelog
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

#move to the build directory
os.chdir(buildpath)

#unpack the tarball
cmd2 = "tar -xvf " + "pychoacoustics-" + ver + ".tar.gz"
os.system(cmd2)

#copy debian files in the package build directory
cmd3 = "cp -R " + "../../pychoacoustics/prep-release/debian/ ./pychoacoustics-" + ver
os.system(cmd3)

#move into package build directory
os.chdir("pychoacoustics-" + ver)
#build the package
#For Debian
os.system("dpkg-buildpackage -F")

#For Launchpad Upload
#os.system("debuild -S -sa")

os.chdir("../")
origdebname = package + "_" + ver +  "_" + architecture + ".deb"
debname = package + "_" + ver + pparev + "~" + series + "_" + architecture + ".deb"
os.system("mv" + " " + origdebname + " " + debname)

# if publish == 1 or publish == "y":
#     print("###############################")
#     print("Publishing")
#     print("###############################")
#     API_KEY = os.environ["BINTRAY_API_KEY"]

#     USERNAME = "sam81"

#     URL = "https://api.bintray.com/content/sam81/hearinglab/"+ package + "/" + ver + "/pool/" + component + "/"+ package[0] + "/" + package + "/" + debname + "?publish=1"
#     parameters = {"publish": "1"}
#     headers = {
#         "X-Bintray-Debian-Distribution": series,
#         "X-Bintray-Debian-Architecture": architecture,
#         "X-Bintray-Debian-Component": component
#     }

#     with open(debname, "rb") as package_fp:
#         response = requests.put(
#             URL, auth=(USERNAME, API_KEY), params=parameters,
#             headers=headers, data=package_fp) 

#     print("status code: " + str(response.status_code))
#     if response.status_code == 201:
#         print("#####################\n Upload successful!")
#     else:
#         print("#####################\n Upload Unsuccessful.")
# else:
#     print("###############################")
#     print("Not Publishing")
#     print("###############################")
    
