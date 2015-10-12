#! /usr/bin/env python 
# -*- coding: utf-8 -*-

import numpy, os, sys, unittest
import pandas as pd
from test_utility_functions import*

rootPath = "../../pychoacoustics_data/test_data/"

class TestUML(unittest.TestCase):
    def testGeometric(self):
        resFileRoot = "res_geometric"
        removePreviousResFiles(rootPath + "UML/"+resFileRoot)

        cmdStr = "python3 ../pychoacoustics.pyw -f" + rootPath + "UML/UML_geometric.prm -a -q -o --seed 2033 -r" + rootPath + "UML/"+resFileRoot  + ".txt"
        x = os.system(cmdStr)
        assert(x==0)
        storedRes = pd.read_csv(rootPath + "UML/results/res_geometric_table.csv", sep=";")
        currRes = pd.read_csv(rootPath + "UML/res_geometric_table.csv", sep=";")
        numpy.testing.assert_array_equal(currRes["threshold"], storedRes["threshold"])
        numpy.testing.assert_array_equal(currRes["slope"], storedRes["slope"])
        numpy.testing.assert_array_equal(currRes["lapse"], storedRes["lapse"])


    def testArithmetic(self):
        resFileRoot = "res_arithmetic"
        removePreviousResFiles(rootPath + "UML/"+resFileRoot)

        cmdStr = "python3 ../pychoacoustics.pyw -f" + rootPath + "UML/UML_arithmetic.prm -a -q -o --seed 2033 -r" + rootPath + "UML/"+resFileRoot  + ".txt"
        x = os.system(cmdStr)
        assert(x == 0)
        storedRes = pd.read_csv(rootPath + "UML/results/res_arithmetic_table.csv", sep=";")
        currRes = pd.read_csv(rootPath + "UML/res_arithmetic_table.csv", sep=";")
        numpy.testing.assert_array_equal(currRes["threshold"], storedRes["threshold"])
        numpy.testing.assert_array_equal(currRes["slope"], storedRes["slope"])
        numpy.testing.assert_array_equal(currRes["lapse"], storedRes["lapse"])

       


if __name__ == '__main__':
    unittest.main()
