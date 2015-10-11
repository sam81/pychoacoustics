#! /usr/bin/env python 
# -*- coding: utf-8 -*-

def removePreviousResFiles(fName):
    suffixes = ['.txt', '_res.txt', '_full.txt', '_table.csv', '_table_full.csv', '_table_processed.csv']
    for s in suffixes:
        toRemove = fName + s
        if os.path.exists(toRemove):
            print('Removing', toRemove)
            os.remove(toRemove)
    return

import numpy, os
import pandas as pd

resFileRoot = "res_geometric"
removePreviousResFiles(resFileRoot)

cmdStr = "pychoacoustics-dev -f transformed_up-down_geometric.prm -a -q -c --seed 2033 -r" + resFileRoot  + ".txt"
x = os.system(cmdStr)
if x != 0:
    raise("Test failed!")

storedRes = pd.read_csv("results/res_geometric_table.csv", sep=";")
currRes = pd.read_csv("res_geometric_table.csv", sep=";")
numpy.testing.assert_array_equal(currRes["threshold_geometric"], storedRes["threshold_geometric"])
numpy.testing.assert_array_equal(currRes["SD"], storedRes["SD"])


