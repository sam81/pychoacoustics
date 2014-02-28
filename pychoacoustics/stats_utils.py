# -*- coding: utf-8 -*-

#   Copyright (C) 2008-2014 Samuele Carcagno <sam.carcagno@gmail.com>
#   This file is part of pychoacoustics

#    pychoacoustics is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    pychoacoustics is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with pychoacoustics.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, unicode_literals
import numpy
from numpy import sqrt, log10, mean, sqrt
from scipy.stats.distributions import norm
def geoMean(vals):
     n = float(len(vals))
     m = numpy.prod(vals)**(1/n)
     return m
def geoSd(vals):
    vals = numpy.abs(vals)
    res = 10**numpy.std(numpy.log10(vals), ddof=1)
    return res
def geoSe(vals):
    n = len(vals)
    standardErr = 10**sqrt(sum((log10(vals) - mean(log10(vals)))**2) / float(((n-1)* n)))
    return(standardErr)
def se(vals):
    standardDev = numpy.std(vals, ddof=1)
    standardErr = standardDev / sqrt(len(vals))
    return(standardErr)

def getdprime(A_correct, A_total, B_correct, B_total, corrected):
    if corrected == True:
        if A_correct == A_total:
            tA = 1 - 1/(2*A_total)
        elif A_correct == 0:
            tA = 1 / (2*A_total)
        else:
            tA = A_correct/(A_total)
        
        if B_correct == B_total:
            tB = 1 - 1/(2*B_total)
        elif B_correct == 0:
            tB = 1 / (2*B_total)
        else:
            tB = B_correct/(B_total)
    else:
        tA = A_correct/(A_total)
        tB = B_correct/(B_total)
    dp = norm.ppf(tA) - norm.ppf(1-(tB))
    return dp
