#! /usr/bin/env python 
# -*- coding: utf-8 -*-

import os

def removePreviousResFiles(fName):
    suffixes = ['.txt', '_res.txt', '_full.txt', '_table.csv', '_table_full.csv', '_table_processed.csv']
    for s in suffixes:
        toRemove = fName + s
        if os.path.exists(toRemove):
            print('Removing', toRemove)
            os.remove(toRemove)
    return 
