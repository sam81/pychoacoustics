#! /usr/bin/env python 
# -*- coding: utf-8 -*-
import numpy, os, sys, unittest
import pandas as pd
from test_utility_functions import*

rootPath = "../../pychoacoustics_data/test_data/"
dec_IO = 7
dec_diff = 4
class TestWAVSameDifferent(unittest.TestCase):

    def testA(self):
        resFileRoot = "res"
        removePreviousResFiles(rootPath + "wav_same-different/"+resFileRoot)

        cmdStr = "PYTHONPATH='/media/ntfsShared/lin_home/auditory/code/pychoacoustics/' python3 ../pychoacoustics/__main__.py -f" + rootPath +  "wav_same-different/wav_same-different.prm -a -q -o --seed 1933 -r" + rootPath + "wav_same-different/"+resFileRoot  + ".txt"
        x = os.system(cmdStr)
        assert(x==0)
        storedRes = pd.read_csv(rootPath + "wav_same-different/results/res_table.csv", sep=";").sort_values("condition")
        currRes = pd.read_csv(rootPath + "wav_same-different/res_table.csv", sep=";").sort_values("condition")
        numpy.testing.assert_array_almost_equal(currRes["dprime_diff_pair1"], storedRes["dprime_diff_pair1"], decimal=dec_diff)
        numpy.testing.assert_array_almost_equal(currRes["dprime_diff_pair2"], storedRes["dprime_diff_pair2"], decimal=dec_diff)
        numpy.testing.assert_array_almost_equal(currRes["dprime_IO_pair1"], storedRes["dprime_IO_pair1"], decimal=dec_IO)
        numpy.testing.assert_array_almost_equal(currRes["dprime_IO_pair2"], storedRes["dprime_IO_pair2"], decimal=dec_IO)

        storedResProc = pd.read_csv(rootPath + "wav_same-different/results/res_table_sess.csv", sep=";").sort_values("condition")
        currResProc = pd.read_csv(rootPath + "wav_same-different/res_table_sess.csv", sep=";").sort_values("condition")
        numpy.testing.assert_array_almost_equal(currRes["dprime_diff_pair1"], storedRes["dprime_diff_pair1"], decimal=dec_diff)
        numpy.testing.assert_array_almost_equal(currRes["dprime_diff_pair2"], storedRes["dprime_diff_pair2"], decimal=dec_diff)
        numpy.testing.assert_array_almost_equal(currRes["dprime_IO_pair1"], storedRes["dprime_IO_pair1"], decimal=dec_IO)
        numpy.testing.assert_array_almost_equal(currRes["dprime_IO_pair2"], storedRes["dprime_IO_pair2"], decimal=dec_IO)



if __name__ == '__main__':
    unittest.main()


# rootPath = "../../pychoacoustics_data/test_data/"

# class TestWAVSameDifferent(unittest.TestCase):

#     def testA(self):
#         resFileRoot = "res"
#         removePreviousResFiles(rootPath + "wav_same-different/"+resFileRoot)

#         cmdStr = "PYTHONPATH='/media/ntfsShared/lin_home/auditory/code/pychoacoustics_exp/:/media/ntfsShared/lin_home/auditory/code/pychoacoustics/' python3 ../pychoacoustics/__main__.py -f" + rootPath +  "wav_same-different/wav_same-different.prm -a -q -o --seed 1933 -r" + rootPath + "wav_same-different/"+resFileRoot  + ".txt"
#         x = os.system(cmdStr)
#         assert(x==0)
#         storedRes = pd.read_csv(rootPath + "wav_same-different/results/res_table.csv", sep=";").sort_values("condition")
#         currRes = pd.read_csv(rootPath + "wav_same-different/res_table.csv", sep=";").sort_values("condition")
#         numpy.testing.assert_array_equal(currRes["dprime_diff_pair1"], storedRes["dprime_diff_pair1"])
#         numpy.testing.assert_array_equal(currRes["dprime_diff_pair2"], storedRes["dprime_diff_pair2"])
#         numpy.testing.assert_array_equal(currRes["dprime_IO_pair1"], storedRes["dprime_IO_pair1"])
#         numpy.testing.assert_array_equal(currRes["dprime_IO_pair2"], storedRes["dprime_IO_pair2"])

#         storedResProc = pd.read_csv(rootPath + "wav_same-different/results/res_table_sess.csv", sep=";").sort_values("condition")
#         currResProc = pd.read_csv(rootPath + "wav_same-different/res_table_sess.csv", sep=";").sort_values("condition")
#         numpy.testing.assert_array_equal(currRes["dprime_diff_pair1"], storedRes["dprime_diff_pair1"])
#         numpy.testing.assert_array_equal(currRes["dprime_diff_pair2"], storedRes["dprime_diff_pair2"])
#         numpy.testing.assert_array_equal(currRes["dprime_IO_pair1"], storedRes["dprime_IO_pair1"])
#         numpy.testing.assert_array_equal(currRes["dprime_IO_pair2"], storedRes["dprime_IO_pair2"])



# if __name__ == '__main__':
#     unittest.main()
