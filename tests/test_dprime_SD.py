#! /usr/bin/env python
# -*- coding: utf-8 -*-

import h5py, os, sys, time, unittest
import numpy as np
sys.path.insert(0, os.path.abspath('../')) 
from pychoacoustics.pysdt import*

##t1= time.time()
rootPath = "../../pychoacoustics_data/test_data/pysdt/"

class TestdprimeSD(unittest.TestCase):
    def testA(self):

        fHandle = h5py.File(rootPath+'dp_SD.hdf5','r')

        HR = np.array(fHandle.get('HR'))
        FA = np.array(fHandle.get('FA'))
        dp_diff_R = np.array(fHandle.get('dp_diff'))
        dp_IO_R = np.array(fHandle.get('dp_IO'))

        HR = np.delete(HR, 251)
        FA = np.delete(FA, 251)
        dp_diff_R = np.delete(dp_diff_R, 251)
        dp_IO_R = np.delete(dp_IO_R, 251)
        n = len(HR)
        dp_diff_py = np.zeros(n)
        dp_IO_py = np.zeros(n)

        for cnt in range(n):
            dp_diff_py[cnt] = dprime_SD(HR[cnt], FA[cnt], meth='diff')
            dp_IO_py[cnt] = dprime_SD(HR[cnt], FA[cnt], meth='IO')
            # if np.round(dp_diff_py[cnt], 1) != np.round(dp_diff_R[cnt], 1):
            #     print("#########")
            #     print(HR[cnt])
            #     print(FA[cnt])
            #     print("---------")

        np.testing.assert_array_almost_equal(dp_IO_py, dp_IO_R, decimal=7)
        np.testing.assert_array_almost_equal(dp_diff_py, dp_diff_R, decimal=4)

if __name__ == '__main__':
    unittest.main()

# t2= time.time()
# print(t2-t1)
