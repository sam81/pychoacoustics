#! /usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

###########################
# sndlib tests
import sndlib_default_tests
import write_sndlib_examples_code
import sndlib_examples_code
from sndlib_unittest import*

#############################
# pysdt tests
from test_dprime_ABX import*
from test_dprime_mAFC import*
from test_dprime_oddity_diff import*
from test_dprime_SD import*

###########################
# paradigm tests
from test_constant_1_interval_2_alternatives import*
from test_constant_1_pair_same_different import*
from test_constant_m_intervals_n_alternatives import*
from test_multiple_constants_m_intervals_n_alternatives import*
from test_transformed_up_down import*
from test_transformed_up_down_interleaved import*
from test_weighted_up_down import*
from test_weighted_up_down_interleaved import*
from test_PEST import*
from test_PSI import*
from test_UML import*

###########################
# experiment tests
from test_wav_ABX import*
from test_wav_odd_one_out import*
from test_wav_same_different import*
from test_sig_detect_multi import*


if __name__ == "__main__":
    unittest.main()
