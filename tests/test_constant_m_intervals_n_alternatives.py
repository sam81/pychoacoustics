#! /usr/bin/env python 
# -*- coding: utf-8 -*-
import numpy, os, sys, unittest
import pandas as pd
from test_utility_functions import*

rootPath = "../../pychoacoustics_data/test_data/"

class TestConstantMIntervalsNAlternatives(unittest.TestCase):

    def testA(self):
        resFileRoot = "res"
        removePreviousResFiles(rootPath + "constant_m-intervals_n-alternatives/"+resFileRoot)

        cmdStr = "python3 ../pychoacoustics.pyw -f" + rootPath +  "constant_m-intervals_n-alternatives/constant_m-intervals_n-alternatives.prm -a -q -o --seed 1933 -r" + rootPath + "constant_m-intervals_n-alternatives/"+resFileRoot  + ".txt"
        x = os.system(cmdStr)
        assert(x==0)
        storedRes = pd.read_csv(rootPath + "constant_m-intervals_n-alternatives/results/res_table.csv", sep=";").sort_values("condition")
        currRes = pd.read_csv(rootPath + "constant_m-intervals_n-alternatives/res_table.csv", sep=";").sort_values("condition")
        numpy.testing.assert_array_equal(currRes["dprime"], storedRes["dprime"])
        numpy.testing.assert_array_equal(currRes["perc_corr"], storedRes["perc_corr"])

        storedResProc = pd.read_csv(rootPath + "constant_m-intervals_n-alternatives/results/res_table_sess.csv", sep=";").sort_values("condition")
        currResProc = pd.read_csv(rootPath + "constant_m-intervals_n-alternatives/res_table_sess.csv", sep=";").sort_values("condition")

        numpy.testing.assert_array_equal(currResProc["dprime"], storedResProc["dprime"])
        numpy.testing.assert_array_equal(currResProc["perc_corr"], storedResProc["perc_corr"])


if __name__ == '__main__':
    unittest.main()
