#! /usr/bin/env python 
# -*- coding: utf-8 -*-
import numpy, os, sys, unittest
import pandas as pd
from test_utility_functions import*

rootPath = "../../pychoacoustics_data/test_data/"

class TestPEST(unittest.TestCase):
    def testGeometric(self):
        resFileRoot = "res_geometric"
        removePreviousResFiles(rootPath + "PEST/"+resFileRoot)

        cmdStr = "python3 ../pychoacoustics.pyw -f" + rootPath + "PEST/PEST_geometric.prm -a -q -o --seed 2033 -r" + rootPath + "PEST/"+resFileRoot  + ".txt"
        x = os.system(cmdStr)
        assert(x==0)
        storedRes = pd.read_csv(rootPath + "PEST/results/res_geometric_table.csv", sep=";")
        currRes = pd.read_csv(rootPath + "PEST/res_geometric_table.csv", sep=";")
        numpy.testing.assert_array_equal(currRes["threshold_geometric"], storedRes["threshold_geometric"])


        storedResProc = pd.read_csv(rootPath + "PEST/results/res_geometric_table_sess.csv", sep=";")
        currResProc = pd.read_csv(rootPath + "PEST/res_geometric_table_sess.csv", sep=";")

        numpy.testing.assert_array_equal(currResProc["threshold_geometric"], storedResProc["threshold_geometric"])
        numpy.testing.assert_array_equal(currResProc["SE"], storedResProc["SE"])

    def testArithmetic(self):
        resFileRoot = "res_arithmetic"
        removePreviousResFiles(rootPath + "PEST/"+resFileRoot)

        cmdStr = "python3 ../pychoacoustics.pyw -f" + rootPath +  "PEST/PEST_arithmetic.prm -a -q -o --seed 2033 -r" + rootPath + "PEST/"+resFileRoot  + ".txt"
        x = os.system(cmdStr)
        assert(x==0)
        storedRes = pd.read_csv(rootPath + "PEST/results/res_arithmetic_table.csv", sep=";")
        currRes = pd.read_csv(rootPath + "PEST/res_arithmetic_table.csv", sep=";")
        numpy.testing.assert_array_equal(currRes["threshold_arithmetic"], storedRes["threshold_arithmetic"])

        storedResProc = pd.read_csv(rootPath + "PEST/results/res_arithmetic_table_sess.csv", sep=";")
        currResProc = pd.read_csv(rootPath + "PEST/res_arithmetic_table_sess.csv", sep=";")

        numpy.testing.assert_array_equal(currResProc["threshold_arithmetic"], storedResProc["threshold_arithmetic"])
        numpy.testing.assert_array_equal(currResProc["SE"], storedResProc["SE"])


if __name__ == '__main__':
    unittest.main()
