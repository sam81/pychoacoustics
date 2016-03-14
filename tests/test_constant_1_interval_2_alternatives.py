#! /usr/bin/env python 
# -*- coding: utf-8 -*-
import numpy, os, sys, unittest
import pandas as pd
from test_utility_functions import*

rootPath = "../../pychoacoustics_data/test_data/"

class TestConstantMIntervalsNAlternatives(unittest.TestCase):

    def testA(self):
        resFileRoot = "res"
        removePreviousResFiles(rootPath + "constant_1-interval_2-alternatives/"+resFileRoot)

        cmdStr = "python3 ../pychoacoustics.pyw -f" + rootPath +  "constant_1-interval_2-alternatives/constant_1-interval_2-alternatives.prm -a -q -o --seed 1933 -r" + rootPath + "constant_1-interval_2-alternatives/"+resFileRoot  + ".txt"
        x = os.system(cmdStr)
        assert(x==0)
        storedRes = pd.read_csv(rootPath + "constant_1-interval_2-alternatives/results/res_table.csv", sep=";").sort_values("condition")
        currRes = pd.read_csv(rootPath + "constant_1-interval_2-alternatives/res_table.csv", sep=";").sort_values("condition")
        numpy.testing.assert_array_equal(currRes["dprime"], storedRes["dprime"])

        storedResProc = pd.read_csv(rootPath + "constant_1-interval_2-alternatives/results/res_table_sess.csv", sep=";").sort_values("condition")
        currResProc = pd.read_csv(rootPath + "constant_1-interval_2-alternatives/res_table_sess.csv", sep=";").sort_values("condition")

        numpy.testing.assert_array_equal(currResProc["dprime"], storedResProc["dprime"])


if __name__ == '__main__':
    unittest.main()
