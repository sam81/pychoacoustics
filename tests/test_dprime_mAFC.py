#! /usr/bin/env python
# -*- coding: utf-8 -*-

import h5py, os, sys, time, unittest
import numpy as np
sys.path.insert(0, os.path.abspath('../')) 
from pychoacoustics.pysdt import*
rootPath = "../../pychoacoustics_data/test_data/pysdt/"
#t1= time.time()
class TestdprimemAFC(unittest.TestCase):

    def testA(self):
        fHandle = h5py.File(rootPath+'dp_mAFC.hdf5','r')

        PR = np.array(fHandle.get('PR'))
        nAlts = np.array(fHandle.get('Alt'), dtype=np.int32)
        dp_R = np.array(fHandle.get('dp'))


        n = len(PR)
        dp_py = np.zeros(n)


        for cnt in range(n):
            dp_py[cnt] = dprime_mAFC(PR[cnt], int(nAlts[cnt]))

        np.testing.assert_array_almost_equal(dp_py, dp_R, decimal=4)

if __name__ == '__main__':
    unittest.main()


# t2= time.time()
# print(t2-t1)
