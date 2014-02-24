#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, shutil

fls = os.listdir("../dist")
fls.sort()
latest_ver = fls[-1].split("-")[1].split(".z")[0]
print("Latest available version is: ", latest_ver)
decis = input("Do you want to upload this one (1) or another version (2): ")

if decis == "1":
    upload_ver = latest_ver
else:
    upload_ver = input("Enter version number to upload: ")

print("Uploading Version: ", upload_ver)

pack_prefixes = ["pychoacoustics-", "pychoacoustics-", "pychoacoustics_"]
pack_suffixes = [".tar.gz", ".zip", "_amd64.deb"]
pack_names = []
for i in range(len(pack_prefixes)):
    pack_names.append(pack_prefixes[i]+upload_ver+pack_suffixes[i])

for i in range(2):
    shutil.copyfile("../dist/"+pack_names[i], "../../../../dc/devel/xoom-website/xoom/pychoacoustics/pych_builds/"+pack_names[i])

shutil.copyfile("../../pkg_build/debian_7.4_x86_64/"+pack_names[2], "../../../../dc/devel/xoom-website/xoom/pychoacoustics/pych_builds/"+pack_names[2])


#doc
#cleanup previous doc
shutil.rmtree("../../../../dc/devel/xoom-website/xoom/pychoacoustics/doc-latest")
shutil.rmtree("../../../../dc/devel/xoom-website/xoom/pychoacoustics/doc-dev")

shutil.copytree("../pychoacoustics/doc/_build/html/", "../../../../dc/devel/xoom-website/xoom/pychoacoustics/doc-dev")

olddir = os.getcwd()
os.chdir("../../../../dc/devel/xoom-website/xoom/pychoacoustics/pych_builds/")
cmd2 = "tar -xvf " + "pychoacoustics-" + upload_ver + ".tar.gz"
os.system(cmd2)
shutil.copytree("pychoacoustics-"+upload_ver+"/pychoacoustics/doc/_build/html/", "../doc-latest")
shutil.rmtree("pychoacoustics-"+upload_ver)
os.chdir(olddir)

f = open("../../../../dc/devel/xoom-website/xoom/pychoacoustics/pychoacoustics.html", "r")
l = f.readlines()
f.close()
#get the line where current html version is stored
idx = l.index("<!--Version-->\n")
#previos version was
oldver = l[idx+1].split("--")[1]
l[idx+1] = "<!--"+upload_ver+"-->\n"

idx = l.index('<li> <a href="pych_builds/pychoacoustics-0.2.63.tar.gz">pychoacoustics-0.2.63.tar.gz<a> Linux/UNIX source package</li>\n')
l[idx] = l[idx].replace(oldver, upload_ver)

idx = l.index('<li> <a href="pych_builds/pychoacoustics-0.2.63.zip">pychoacoustics-0.2.63.zip</a> Windows source package</li>\n')
l[idx] = l[idx].replace(oldver, upload_ver)

idx = l.index('<li> <a href="pych_builds/pychoacoustics_0.2.63_amd64.deb">pychoacoustics_0.2.63_amd64.deb</a> 64-bit Debian Wheezy package</li>\n')
l[idx] = l[idx].replace(oldver, upload_ver)

f = open("../../../../dc/devel/xoom-website/xoom/pychoacoustics/pychoacoustics.html", "w")
l = f.writelines(l)
f.close()
