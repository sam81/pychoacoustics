#! /usr/bin/env python 
# -*- coding: utf-8 -*-
import numpy, os, sys, unittest
import pandas as pd
from test_utility_functions import*

class TestTransformedUpDown(unittest.TestCase):
    def testGeometric(self):
        resFileRoot = "res_geometric"
        removePreviousResFiles("transformed_up-down/"+resFileRoot)

        cmdStr = "python3 ../pychoacoustics.pyw -f transformed_up-down/transformed_up-down_geometric.prm -a -q -c --seed 2033 -r" + "transformed_up-down/"+resFileRoot  + ".txt"
        x = os.system(cmdStr)
        if x != 0:
            raise("Test failed!")

        storedRes = pd.read_csv("transformed_up-down/results/res_geometric_table.csv", sep=";")
        currRes = pd.read_csv("transformed_up-down/res_geometric_table.csv", sep=";")
        numpy.testing.assert_array_equal(currRes["threshold_geometric"], storedRes["threshold_geometric"])
        numpy.testing.assert_array_equal(currRes["SD"], storedRes["SD"])

        storedResProc = pd.read_csv("transformed_up-down/results/res_geometric_table_processed.csv", sep=";")
        currResProc = pd.read_csv("transformed_up-down/res_geometric_table_processed.csv", sep=";")

        numpy.testing.assert_array_equal(currResProc["threshold_geometric"], storedResProc["threshold_geometric"])
        numpy.testing.assert_array_equal(currResProc["SE"], storedResProc["SE"])

    def testArithmetic(self):
        resFileRoot = "res_arithmetic"
        removePreviousResFiles("transformed_up-down/"+resFileRoot)

        cmdStr = "python3 ../pychoacoustics.pyw -f transformed_up-down/transformed_up-down_arithmetic.prm -a -q -c --seed 2033 -r" + "transformed_up-down/"+resFileRoot  + ".txt"
        x = os.system(cmdStr)
        if x != 0:
            raise("Test failed!")

        storedRes = pd.read_csv("transformed_up-down/results/res_arithmetic_table.csv", sep=";")
        currRes = pd.read_csv("transformed_up-down/res_arithmetic_table.csv", sep=";")
        numpy.testing.assert_array_equal(currRes["threshold_arithmetic"], storedRes["threshold_arithmetic"])
        numpy.testing.assert_array_equal(currRes["SD"], storedRes["SD"])

        storedResProc = pd.read_csv("transformed_up-down/results/res_arithmetic_table_processed.csv", sep=";")
        currResProc = pd.read_csv("transformed_up-down/res_arithmetic_table_processed.csv", sep=";")

        numpy.testing.assert_array_equal(currResProc["threshold_arithmetic"], storedResProc["threshold_arithmetic"])
        numpy.testing.assert_array_equal(currResProc["SE"], storedResProc["SE"])


if __name__ == '__main__':
    unittest.main()
