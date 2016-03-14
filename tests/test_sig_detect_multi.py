#! /usr/bin/env python 
# -*- coding: utf-8 -*-
import numpy, os, sys, unittest
import pandas as pd
from test_utility_functions import*

rootPath = "../../pychoacoustics_data/test_data/"

class TestSigDetectMulti(unittest.TestCase):

    def testA(self):
        resFileRoot = "res"
        removePreviousResFiles(rootPath + "sig_detect_multi/"+resFileRoot)

        cmdStr = "python3 ../pychoacoustics.pyw -f" + rootPath +  "sig_detect_multi/sig_detect_multi.prm -a -q -o --seed 1933 -r" + rootPath + "sig_detect_multi/"+resFileRoot  + ".txt"
        x = os.system(cmdStr)
        assert(x==0)
        storedRes = pd.read_csv(rootPath + "sig_detect_multi/results/res_table.csv", sep=";").sort_values("condition")
        currRes = pd.read_csv(rootPath + "sig_detect_multi/res_table.csv", sep=";").sort_values("condition")
        numpy.testing.assert_array_equal(currRes["dprime_subc1"], storedRes["dprime_subc1"])
        numpy.testing.assert_array_equal(currRes["dprime_subc2"], storedRes["dprime_subc2"])

        storedResProc = pd.read_csv(rootPath + "sig_detect_multi/results/res_table_sess.csv", sep=";").sort_values("condition")
        currResProc = pd.read_csv(rootPath + "sig_detect_multi/res_table_sess.csv", sep=";").sort_values("condition")
        numpy.testing.assert_array_equal(currRes["dprime_subc1"], storedRes["dprime_subc1"])
        numpy.testing.assert_array_equal(currRes["dprime_subc2"], storedRes["dprime_subc2"])



if __name__ == '__main__':
    unittest.main()
