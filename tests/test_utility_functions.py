#! /usr/bin/env python 
# -*- coding: utf-8 -*-

import os

def removePreviousResFiles(fName):
    suffixes = ['.txt', '_sess.txt', '_trial.txt', '_table.csv', '_table_trial.csv', '_table_sess.csv']
    for s in suffixes:
        toRemove = fName + s
        if os.path.exists(toRemove):
            print('Removing', toRemove)
            os.remove(toRemove)
    return 
