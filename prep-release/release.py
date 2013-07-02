#! /usr/bin/env python
# -*- coding: utf-8 -*-

import getopt, datetime, os, subprocess, sys
os.chdir('../')

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "m:", ["message="])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-m", "--message"):
            message = arg
    major_v = 0
    minor_v = 2

    #read minor minor release number
    f = open('prep-release/minor_minor_number.txt', 'r')
    ln = f.readlines()
    f.close()
    minor_minor_v = int(ln[0].strip()) + 1
    #write incremented minor minor release number
    f = open('prep-release/minor_minor_number.txt', 'w')
    f.write(str(minor_minor_v))
    f.close()
    builddate = datetime.datetime.now().strftime("%d-%b-%Y %H:%M")
    #set git tag
    gittag = str(major_v) + '.' + str(minor_v) + '.' + str(minor_minor_v)
    
    f = open('setup.py', 'r')
    ln = f.readlines()
    f.close()
    for i in range(len(ln)):
        if ln[i].strip().split('=')[0].strip() == "version":
            ln[i] = '    version="' + gittag +'",\n'

    f = open('setup.py', 'w')
    f.writelines(ln)
    f.close()

    #version specific build
    for i in range(len(ln)):
        if ln[i].strip().split('=')[0].strip() == "name":
            ln[i] = '    name="pychoacoustics' + gittag.replace(".", "-") +'",\n'
        if ln[i].strip().split('=')[0].strip() == "scripts":
            ln[i] = '    scripts=["pychoacoustics' + gittag.replace(".", "-") + '.pyw"], \n'
    f = open('setup_ver.py', 'w')
    f.writelines(ln)
    f.close()
    

    f = open('pychoacoustics_pack/_version_info.py', 'r')
    ln = f.readlines()
    f.close()
    for i in range(len(ln)):
        if ln[i].strip().split('=')[0].strip() == "pychoacoustics_version":
            ln[i] = 'pychoacoustics_version = "' + gittag +'"\n'
        if ln[i].strip().split('=')[0].strip() == "pychoacoustics_builddate":
            ln[i] = 'pychoacoustics_builddate = "' + builddate +'"\n'

    f = open('pychoacoustics_pack/_version_info.py', 'w')
    f.writelines(ln)
    f.close()


    f = open('doc/conf.py', 'r')
    ln = f.readlines()
    f.close()
    for i in range(len(ln)):
        if ln[i].strip().split('=')[0].strip() == "version":
            ln[i] = 'version = "' + gittag +'",\n'
        if ln[i].strip().split('=')[0].strip() == "release":
            ln[i] = 'release = "' + gittag + '",\n'

    f = open('doc/conf.py', 'w')
    f.writelines(ln)
    f.close()

 
    subprocess.call('git commit -a -m"' + message+'"', shell=True)
    #tag the commit so that it can be easily retrieved
    subprocess.call('git tag -a "' + gittag +'"' + ' -m "' + gittag +'"', shell=True)
    
if __name__ == "__main__":
    main(sys.argv[1:])
