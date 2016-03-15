#! /usr/bin/env python
# -*- coding: utf-8 -*-

import h5py, os, sys, time, unittest
import numpy as np
sys.path.insert(0, os.path.abspath('../')) 
from pychoacoustics.pysdt import*

rootPath = "../../pychoacoustics_data/test_data/pysdt/"

#t1= time.time()
class TestdprimeOddity(unittest.TestCase):

    def testA(self):
        fHandle = h5py.File(rootPath+'dp_oddity.hdf5','r')

        PR = np.array(fHandle.get('PR'))
        dp_diff_R = np.array(fHandle.get('dp_diff'))


        n = len(PR)
        dp_diff_py = np.zeros(n)


        for cnt in range(n):
            dp_diff_py[cnt] = dprime_oddity(PR[cnt], meth='diff')

        np.testing.assert_array_almost_equal(dp_diff_py, dp_diff_R, decimal=4)

if __name__ == '__main__':
    unittest.main()
    
# t2= time.time()
# print(t2-t1)
