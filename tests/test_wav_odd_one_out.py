#! /usr/bin/env python 
# -*- coding: utf-8 -*-
import numpy, os, sys, unittest
import pandas as pd
from test_utility_functions import*

rootPath = "../../pychoacoustics_data/test_data/"
dec_n = 4
class TestWAVOddOneOut(unittest.TestCase):

    def testA(self):
        resFileRoot = "res"
        removePreviousResFiles(rootPath + "wav_odd_one_out/"+resFileRoot)

        cmdStr = "PYTHONPATH='/media/ntfsShared/lin_home/auditory/code/pychoacoustics/' python3 ../pychoacoustics/__main__.py -f" + rootPath +  "wav_odd_one_out/wav_odd_one_out.prm -a -q -o --seed 1933 -r" + rootPath + "wav_odd_one_out/"+resFileRoot  + ".txt"
        x = os.system(cmdStr)
        assert(x==0)
        storedRes = pd.read_csv(rootPath + "wav_odd_one_out/results/res_table.csv", sep=";").sort_values("condition")
        currRes = pd.read_csv(rootPath + "wav_odd_one_out/res_table.csv", sep=";").sort_values("condition")
        numpy.testing.assert_array_almost_equal(currRes["dprime_diff_subcnd1"], storedRes["dprime_diff_subcnd1"], decimal=dec_n)
        numpy.testing.assert_array_almost_equal(currRes["dprime_diff_subcnd2"], storedRes["dprime_diff_subcnd2"], decimal=dec_n)
        numpy.testing.assert_array_almost_equal(currRes["dprime_IO_subcnd1"], storedRes["dprime_IO_subcnd1"], decimal=dec_n)
        numpy.testing.assert_array_almost_equal(currRes["dprime_IO_subcnd2"], storedRes["dprime_IO_subcnd2"], decimal=dec_n)

        storedResProc = pd.read_csv(rootPath + "wav_odd_one_out/results/res_table_sess.csv", sep=";").sort_values("condition")
        currResProc = pd.read_csv(rootPath + "wav_odd_one_out/res_table_sess.csv", sep=";").sort_values("condition")
        numpy.testing.assert_array_almost_equal(currRes["dprime_diff_subcnd1"], storedRes["dprime_diff_subcnd1"], decimal=dec_n)
        numpy.testing.assert_array_almost_equal(currRes["dprime_diff_subcnd2"], storedRes["dprime_diff_subcnd2"], decimal=dec_n)
        numpy.testing.assert_array_almost_equal(currRes["dprime_IO_subcnd1"], storedRes["dprime_IO_subcnd1"], decimal=dec_n)
        numpy.testing.assert_array_almost_equal(currRes["dprime_IO_subcnd2"], storedRes["dprime_IO_subcnd2"], decimal=dec_n)



if __name__ == '__main__':
    unittest.main()
