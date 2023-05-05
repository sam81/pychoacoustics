# -*- coding: utf-8 -*-

#   Copyright (C) 2008-2023 Samuele Carcagno <sam.carcagno@gmail.com>
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

import numpy
from numpy import array, sqrt, log10, mean, sign, sqrt, unique
from scipy.stats.distributions import norm
from scipy.stats.mstats import gmean

def geoMean(vals):
     vals = array(vals)
     if len(unique(sign(vals))) != 1:
          raise ArithmeticError("Sequence of numbers for geometric mean must be all positive or all negative")
     vals = numpy.abs(vals)
     m = gmean(vals)
     return m

def geoSd(vals):
    if len(unique(sign(vals))) != 1:
         raise ArithmeticError("Sequence of numbers for geometric standard deviation must be all positive or all negative")
    vals = numpy.abs(vals)
    res = 10**numpy.std(numpy.log10(vals), ddof=1)
    return res

def geoSe(vals):
    if len(unique(sign(vals))) != 1:
         raise ArithmeticError("Sequence of numbers for geometric standard error must be all positive or all negative")
    vals = numpy.abs(vals)
    n = len(vals)
    standardErr = 10**sqrt(sum((log10(vals) - mean(log10(vals)))**2) / ((n-1)* n))
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

def gammaShRaFromMeanSD(mean, sd):
    if mean <=0:
        raise ValueError("mean must be > 0")
    if sd <= 0:
        raise ValueError("sd must be > 0")
    shape = (mean**2)/(sd**2)
    rate = mean/(sd**2)
    
    return shape, rate

def gammaShRaFromModeSD(mode, sd):
    if mode <=0:
        raise ValueError("mode must be > 0")
    if sd <= 0:
        raise ValueError("sd must be > 0")
    rate = (mode + sqrt(mode**2 + 4 * sd**2)) / (2 * sd**2)
    shape = 1 + mode * rate

    return shape, rate

def betaABFromMeanSTD(mean, std):
  if mean <=0 or mean >= 1:
       raise ValueError("must have 0 < mean < 1")
  if std <= 0:
       raise ValueError("sd must be > 0")
  kappa = mean*(1-mean)/std**2 - 1
  if kappa <= 0:
       raise ValueError("invalid combination of mean and sd")
  a = mean * kappa
  b = (1.0 - mean) * kappa

  return a, b

def betaMeanSTDFromAB(a,b):
     mu = a/(a+b)
     std = sqrt(a*b/((a+b)**2*(a+b+1)))
     #= mu*(1-mu)/(a+b+1)
     return mu, std

def generalizedBetaABFromMeanSTD(mu, std, xmin, xmax):
     lmbd = (((mu-xmin)*(xmax-mu))/std**2)-1
     a = lmbd*((mu-xmin)/(xmax-xmin))
     b = lmbd*((xmax-mu)/(xmax-xmin))

     return a,b

def generalizedBetaMeanSTDFromAB(a,b,xmin,xmax):
     mu = (xmin*b+xmax*a)/(a+b)
     std = sqrt(((a*b)*(xmax-xmin)**2)/((a+b)**2*(1+a+b)))

     return mu, std
     
     
