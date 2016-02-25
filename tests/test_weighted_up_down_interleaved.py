#! /usr/bin/env python 
# -*- coding: utf-8 -*-
import numpy, os, sys, unittest
import pandas as pd
from test_utility_functions import*

rootPath = "../../pychoacoustics_data/test_data/"

class TestWeightedUpDown(unittest.TestCase):
    def testGeometric(self):
        resFileRoot = "res_geometric"
        removePreviousResFiles(rootPath + "weighted_up-down_interleaved/"+resFileRoot)

        cmdStr = "python3 ../pychoacoustics.pyw -f" + rootPath + "weighted_up-down_interleaved/weighted_up-down_interleaved_geometric.prm -a -q -o --seed 2033 -r" + rootPath + "weighted_up-down_interleaved/"+resFileRoot  + ".txt"
        x = os.system(cmdStr)
        assert(x==0)
        storedRes = pd.read_csv(rootPath + "weighted_up-down_interleaved/results/res_geometric_table.csv", sep=";")
        currRes = pd.read_csv(rootPath + "weighted_up-down_interleaved/res_geometric_table.csv", sep=";")
        numpy.testing.assert_array_equal(currRes["threshold_geometric_track1"], storedRes["threshold_geometric_track1"])
        numpy.testing.assert_array_equal(currRes["SD_track1"], storedRes["SD_track1"])
        numpy.testing.assert_array_equal(currRes["threshold_geometric_track2"], storedRes["threshold_geometric_track2"])
        numpy.testing.assert_array_equal(currRes["SD_track2"], storedRes["SD_track2"])

        storedResProc = pd.read_csv(rootPath + "weighted_up-down_interleaved/results/res_geometric_table_sess.csv", sep=";")
        currResProc = pd.read_csv(rootPath + "weighted_up-down_interleaved/res_geometric_table_sess.csv", sep=";")

        numpy.testing.assert_array_equal(currResProc["threshold_geometric_track1"], storedResProc["threshold_geometric_track1"])
        numpy.testing.assert_array_equal(currResProc["SE_track1"], storedResProc["SE_track1"])

        numpy.testing.assert_array_equal(currResProc["threshold_geometric_track2"], storedResProc["threshold_geometric_track2"])
        numpy.testing.assert_array_equal(currResProc["SE_track2"], storedResProc["SE_track2"])

    def testArithmetic(self):
        resFileRoot = "res_arithmetic"
        removePreviousResFiles(rootPath + "weighted_up-down_interleaved/"+resFileRoot)

        cmdStr = "python3 ../pychoacoustics.pyw -f" + rootPath +  "weighted_up-down_interleaved/weighted_up-down_interleaved_arithmetic.prm -a -q -o --seed 2033 -r" + rootPath + "weighted_up-down_interleaved/"+resFileRoot  + ".txt"
        x = os.system(cmdStr)
        assert(x==0)
        storedRes = pd.read_csv(rootPath + "weighted_up-down_interleaved/results/res_arithmetic_table.csv", sep=";")
        currRes = pd.read_csv(rootPath + "weighted_up-down_interleaved/res_arithmetic_table.csv", sep=";")
        numpy.testing.assert_array_equal(currRes["threshold_arithmetic_track1"], storedRes["threshold_arithmetic_track1"])
        numpy.testing.assert_array_equal(currRes["SD_track1"], storedRes["SD_track1"])
        numpy.testing.assert_array_equal(currRes["threshold_arithmetic_track2"], storedRes["threshold_arithmetic_track2"])
        numpy.testing.assert_array_equal(currRes["SD_track2"], storedRes["SD_track2"])

        storedResProc = pd.read_csv(rootPath + "weighted_up-down_interleaved/results/res_arithmetic_table_sess.csv", sep=";")
        currResProc = pd.read_csv(rootPath + "weighted_up-down_interleaved/res_arithmetic_table_sess.csv", sep=";")

        numpy.testing.assert_array_equal(currResProc["threshold_arithmetic_track1"], storedResProc["threshold_arithmetic_track1"])
        numpy.testing.assert_array_equal(currResProc["SE_track1"], storedResProc["SE_track1"])

        numpy.testing.assert_array_equal(currResProc["threshold_arithmetic_track2"], storedResProc["threshold_arithmetic_track2"])
        numpy.testing.assert_array_equal(currResProc["SE_track2"], storedResProc["SE_track2"])


if __name__ == '__main__':
    unittest.main()
