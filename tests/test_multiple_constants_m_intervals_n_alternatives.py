#! /usr/bin/env python 
# -*- coding: utf-8 -*-
import numpy, os, sys, unittest
import pandas as pd
from test_utility_functions import*

rootPath = "../../pychoacoustics_data/test_data/"

class TestMultiple_ConstantsMIntervalsNAlternatives(unittest.TestCase):

    def testA(self):
        resFileRoot = "res"
        removePreviousResFiles(rootPath + "multiple_constants_m-intervals_n-alternatives/"+resFileRoot)

        cmdStr = "python3 ../pychoacoustics.pyw -f" + rootPath +  "multiple_constants_m-intervals_n-alternatives/multiple_constants_m-intervals_n-alternatives.prm -a -q -o --seed 1933 -r" + rootPath + "multiple_constants_m-intervals_n-alternatives/"+resFileRoot  + ".txt"
        x = os.system(cmdStr)
        assert(x==0)
        storedRes = pd.read_csv(rootPath + "multiple_constants_m-intervals_n-alternatives/results/res_table.csv", sep=";").sort_values("condition")
        currRes = pd.read_csv(rootPath + "multiple_constants_m-intervals_n-alternatives/res_table.csv", sep=";").sort_values("condition")
        numpy.testing.assert_array_equal(currRes["dprime_subc1"], storedRes["dprime_subc1"])
        numpy.testing.assert_array_equal(currRes["perc_corr_subc1"], storedRes["perc_corr_subc1"])
        numpy.testing.assert_array_equal(currRes["dprime_subc2"], storedRes["dprime_subc2"])
        numpy.testing.assert_array_equal(currRes["perc_corr_subc2"], storedRes["perc_corr_subc2"])

        storedResProc = pd.read_csv(rootPath + "multiple_constants_m-intervals_n-alternatives/results/res_table_sess.csv", sep=";").sort_values("condition")
        currResProc = pd.read_csv(rootPath + "multiple_constants_m-intervals_n-alternatives/res_table_sess.csv", sep=";").sort_values("condition")

        numpy.testing.assert_array_equal(currResProc["dprime_subc1"], storedResProc["dprime_subc1"])
        numpy.testing.assert_array_equal(currResProc["perc_corr_subc1"], storedResProc["perc_corr_subc1"])
        numpy.testing.assert_array_equal(currResProc["dprime_subc2"], storedResProc["dprime_subc2"])
        numpy.testing.assert_array_equal(currResProc["perc_corr_subc2"], storedResProc["perc_corr_subc2"])


if __name__ == '__main__':
    unittest.main()
