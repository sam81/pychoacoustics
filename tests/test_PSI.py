#! /usr/bin/env python 
# -*- coding: utf-8 -*-

import numpy, os, sys, unittest
import pandas as pd
from test_utility_functions import*
rootPath = "../../pychoacoustics_data/test_data/"
class TestPSI(unittest.TestCase):
    def testGeometric(self):
        resFileRoot = "res_geometric"
        removePreviousResFiles(rootPath+"PSI/"+resFileRoot)

        cmdStr = "python3 ../pychoacoustics.pyw -f"+ rootPath+ "PSI/PSI_geometric.prm -a -q -o --seed 2033 -r" + rootPath + "PSI/"+ resFileRoot  + ".txt"
        x = os.system(cmdStr)
        assert(x==0)
        storedRes = pd.read_csv(rootPath + "PSI/results/res_geometric_table.csv", sep=";")
        currRes = pd.read_csv(rootPath + "PSI/res_geometric_table.csv", sep=";")
        numpy.testing.assert_array_equal(currRes["threshold"], storedRes["threshold"])
        numpy.testing.assert_array_equal(currRes["slope"], storedRes["slope"])
        numpy.testing.assert_array_equal(currRes["lapse"], storedRes["lapse"])


    def testArithmetic(self):
        resFileRoot = "res_arithmetic"
        removePreviousResFiles(rootPath + "PSI/"+resFileRoot)

        cmdStr = "python3 ../pychoacoustics.pyw -f" + rootPath + "PSI/PSI_arithmetic.prm -a -q -o --seed 2033 -r" + rootPath + "PSI/"+resFileRoot  + ".txt"
        x = os.system(cmdStr)
        assert(x==0)
        storedRes = pd.read_csv(rootPath + "PSI/results/res_arithmetic_table.csv", sep=";")
        currRes = pd.read_csv(rootPath + "PSI/res_arithmetic_table.csv", sep=";")
        numpy.testing.assert_array_equal(currRes["threshold"], storedRes["threshold"])
        numpy.testing.assert_array_equal(currRes["slope"], storedRes["slope"])
        numpy.testing.assert_array_equal(currRes["lapse"], storedRes["lapse"])

       


if __name__ == '__main__':
    unittest.main()
