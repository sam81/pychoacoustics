#! /usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

###########################
# sndlib tests
import sndlib_default_tests
import write_sndlib_examples_code
import sndlib_examples_code
from sndlib_unittest import*

###########################
# paradigm tests
from test_transformed_up_down import*
from test_transformed_up_down_interleaved import*
from test_weighted_up_down import*
from test_weighted_up_down_interleaved import*
from test_PEST import*
from test_PSI import*
from test_UML import*

if __name__ == "__main__":
    unittest.main()
