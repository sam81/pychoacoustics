#! /usr/bin/env python 
# -*- coding: utf-8 -*-
import numpy, os, sys, unittest
import pandas as pd
from test_utility_functions import*

rootPath = "../../pychoacoustics_data/test_data/"

class TestConstantMIntervalsNAlternatives(unittest.TestCase):

    def testA(self):
        resFileRoot = "res"
        removePreviousResFiles(rootPath + "constant_1_pair_same-different/"+resFileRoot)

        cmdStr = "python3 ../pychoacoustics.pyw -f" + rootPath +  "constant_1_pair_same-different/constant_1_pair_same-different.prm -a -q -o --seed 1933 -r" + rootPath + "constant_1_pair_same-different/"+resFileRoot  + ".txt"
        x = os.system(cmdStr)
        assert(x==0)
        storedRes = pd.read_csv(rootPath + "constant_1_pair_same-different/results/res_table.csv", sep=";").sort_values("condition")
        currRes = pd.read_csv(rootPath + "constant_1_pair_same-different/res_table.csv", sep=";").sort_values("condition")
        numpy.testing.assert_array_equal(currRes["dprime_diff"], storedRes["dprime_diff"])
        numpy.testing.assert_array_equal(currRes["dprime_IO"], storedRes["dprime_IO"])

        storedResProc = pd.read_csv(rootPath + "constant_1_pair_same-different/results/res_table_sess.csv", sep=";").sort_values("condition")
        currResProc = pd.read_csv(rootPath + "constant_1_pair_same-different/res_table_sess.csv", sep=";").sort_values("condition")

        numpy.testing.assert_array_equal(currResProc["dprime_diff"], storedResProc["dprime_diff"])
        numpy.testing.assert_array_equal(currResProc["dprime_IO"], storedResProc["dprime_IO"])


if __name__ == '__main__':
    unittest.main()
