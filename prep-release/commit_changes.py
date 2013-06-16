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
    subprocess.call('bzr version-info > prep-release/versioninfo.txt', shell=True)
    f = open('prep-release/versioninfo.txt', 'r')
    ln = f.readlines()
    f.close()
    revno = int(ln[3].strip().split(':')[1]) + 1
    builddate = datetime.datetime.now().strftime("%d-%b-%Y %H:%M")

    f = open('prep-release/minor_minor_number.txt', 'r')
    ln = f.readlines()
    f.close()
    minor_minor_v = int(ln[0].strip()) + 1
    f = open('prep-release/minor_minor_number.txt', 'w')
    f.write(str(minor_minor_v))
    f.close()

    f = open('setup.py', 'r')
    ln = f.readlines()
    f.close()
    for i in range(len(ln)):
        if ln[i].strip().split('=')[0].strip() == "version":
            ln[i] = '    version="' + str(major_v) + '.' + str(minor_v) + '.' + str(minor_minor_v)+'",\n'

    f = open('setup.py', 'w')
    f.writelines(ln)
    f.close()

    f = open('pychoacoustics_pack/_version_info.py', 'w')
    f.write("# -*- coding: utf-8 -*-\n\n")
    f.write('pychoacoustics_version = "' + str(major_v) + '.' + str(minor_v) + '.' + str(minor_minor_v)+'"\n')
    f.write('pychoacoustics_revno = ' + str(revno) + '\n')
    f.write('pychoacoustics_builddate = "' + builddate + '"\n')
    f.close()

    f = open('doc/source/conf.py', 'r')
    ln = f.readlines()
    f.close()
    for i in range(len(ln)):
        if ln[i].strip().split('=')[0].strip() == "version":
            ln[i] = 'version = "' + str(major_v) + '.' + str(minor_v) + '.' + str(minor_minor_v)+'",\n'
        if ln[i].strip().split('=')[0].strip() == "release":
            ln[i] = 'release = "' + str(major_v) + '.' + str(minor_v) + '.' + str(minor_minor_v)+'",\n'

    f = open('doc/source/conf.py', 'w')
    f.writelines(ln)
    f.close()

    f = open('pychoacoustics.desktop', 'r')
    ln = f.readlines()
    f.close()
    for i in range(len(ln)):
        if ln[i].strip().split('=')[0].strip() == "Version":
            ln[i] = 'Version = ' + str(major_v) + '.' + str(minor_v) + '.' + str(minor_minor_v)+'\n'

    f = open('pychoacoustics.desktop', 'w')
    f.writelines(ln)
    f.close()

    subprocess.call('bzr commit -m"' + message+'"', shell=True)
if __name__ == "__main__":
    main(sys.argv[1:])
