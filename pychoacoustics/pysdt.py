#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright (C) 2012-2015 Samuele Carcagno <sam.carcagno@gmail.com>
#   This file is part of pysdt

#    pysdt is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    pysdt is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with pysdt.  If not, see <http://www.gnu.org/licenses/>.

"""
A module for computing signal detection theory measures.
Some of the functions in this module have been ported to
python from the 'psyphy' R package of Kenneth Knoblauch
http://cran.r-project.org/web/packages/psyphy/index.html
"""

from scipy.stats import norm
from scipy.integrate import quad
from scipy.special import erf, erfinv
from scipy import Inf
import numpy, scipy
from numpy import exp, log, log10, sign, sqrt
import numpy as np
#from numpy.lib.scimath import logn #log with arbitrary base




def dprime_mAFC(Pc, m):
    """
    Compute d' corresponding to a certain proportion of correct
    responses in m-AFC tasks.

    Parameters
    ----------
    Pc : float
        Proportion of correct responses.
    m : int
        Number of alternatives.

    Returns
    -------
    dprime : float
        d' value

    Examples
    --------
    >>> dp = dprime_mAFC(0.7, 3)

    """

    if Pc < 0 or Pc > 1:
        raise ValueError("Pc must be between 0 and 1")
    if isinstance(m, int) == False:
        raise TypeError("m must be an int")
    
    def est_dp(dp):

        def pr(x):
            return (norm.pdf(x-dp) * (norm.cdf(x)**(m-1)))
        
        return (Pc - quad(pr, -Inf, Inf)[0])
    try:
        dprime = scipy.optimize.brentq(est_dp, -10, 10)#scipy.optimize.newton(est_dp, 1)
    except:
        dprime = numpy.nan
    
    return dprime


def dprime_SD(H, FA, meth):
    """
    Compute d' for one interval same/different task from 'hit' and 'false alarm' rates.

    Parameters
    ----------
    H : float
        Hit rate.
    FA : float
        False alarms rate.
    meth : string
        'diff' for differencing strategy or 'IO' for independent observations strategy.

    Returns
    -------
    dprime : float
        d' value

    Examples
    --------
    >>> dp = dprime_SD(0.7, 0.2, 'IO')

    """

    if H < 0 or H > 1:
        raise ValueError("H must be between 0 and 1")
    if FA < 0 or FA > 1:
        raise ValueError("FA must be between 0 and 1")
    
    if meth == "diff":
        k = sqrt(2) * norm.ppf(FA/2)
        def est_dp2(dp):
            return H - norm.cdf((k+dp)/sqrt(2)) - norm.cdf((k-dp)/sqrt(2))
        #dprime =  scipy.optimize.newton(est_dp2, 1)
        try:
            dprime =  scipy.optimize.brentq(est_dp2, 0, 10)
        except:
            dprime = numpy.nan
    elif meth == "IO":
        zdiff = norm.ppf(H) - norm.ppf(FA)
        pcMax = norm.cdf(zdiff/2)
        dp_sign = sign(pcMax - 0.5)
        if pcMax < 0.5:
            val = 2 * norm.ppf(0.5 * (1 + sqrt(2 * (1 - pcMax) - 1)))
        else:
            val = 2 * norm.ppf(0.5 * (1 + sqrt(2 * pcMax - 1)))
        dprime = dp_sign*val
    return dprime


def dprime_SD_from_counts(nCA, nTA, nCB, nTB, meth, corr):
    """
    Compute d' for one interval same/different task from counts of correct and total responses.

    Parameters
    ----------
    nCA : int
        Number of correct responses in 'same' trials.
    nTA : int
        Total number of 'same' trials.
    nCB : int
        Number of correct responses in 'different' trials.
    nTB : int
        Total number of 'different' trials.
    meth : string
        'diff' for differencing strategy or 'IO' for independent observations strategy.
    corr : logical
         if True, apply the correction to avoid hit and false alarm rates of 0 or one.

    Returns
    -------
    dprime : float
        d' value

    Examples
    --------
    >>> dp = dprime_SD(0.7, 0.2, 'IO')

    """

    if nCA > nTA:
        raise ValueError("nCA must be <= than nTA")
    if nCB > nTB:
        raise ValueError("nCB must be <= than nTB")
    
    if corr == True:
        if nCA == nTA:
            tA = 1 - 1/(2*nTA)
        elif nCA == 0:
            tA = 1 / (2*nTA)
        else:
            tA = nCA/(nTA)

        if nCB == nTB:
            tB = 1 - 1/(2*nTB)
        elif nCB == 0:
            tB = 1 / (2*nTB)
        else:
            tB = nCB/(nTB)
    else:
        tA = nCA/nTA
        tB = nCB/nTB

    return dprime_SD(H=tA, FA=1-tB, meth=meth)


def dprime_yes_no(H, FA):
    """
    Compute d' for one interval 'yes/no' type tasks from hits and false alarm rates.

    Parameters
    ----------
    H : float
        Hit rate.
    FA : float
        False alarms rate.

    Returns
    -------
    dprime : float
        d' value

    Examples
    --------
    >>> dp = dprime_yes_no(0.7, 0.2)

    """
    
    if H < 0 or H > 1:
        raise ValueError("H must be between 0 and 1")
    if FA < 0 or FA > 1:
        raise ValueError("FA must be between 0 and 1")

    return norm.ppf(H) - norm.ppf(FA)


def dprime_yes_no_from_counts(nCA, nTA, nCB, nTB, corr):
    """
    Compute d' for one interval 'yes/no' type tasks from counts of correct and total responses.

    Parameters
    ----------
    nCA : int
        Number of correct responses in 'signal' trials.
    nTA : int
        Total number of 'signal' trials.
    nCB : int
        Number of correct responses in 'noise' trials.
    nTB : int
        Total number of 'noise' trials.
    corr : logical
         if True, apply the correction to avoid hit and false alarm rates of 0 or one.

    Returns
    -------
    dprime : float
        d' value

    Examples
    --------
    >>> dp = dprime_yes_no_from_counts(nCA=70, nTA=100, nCB=80, nTB=100, corr=True)

    """
    
    if nCA > nTA:
        raise ValueError("nCA must be <= than nTA")
    if nCB > nTB:
        raise ValueError("nCB must be <= than nTB")

    if corr == True:
        if nCA == nTA:
            tA = 1 - 1/(2*nTA)
        elif nCA == 0:
            tA = 1 / (2*nTA)
        else:
            tA = nCA/(nTA)

        if nCB == nTB:
            tB = 1 - 1/(2*nTB)
        elif nCB == 0:
            tB = 1 / (2*nTB)
        else:
            tB = nCB/(nTB)
    else:
        tA = nCA/nTA
        tB = nCB/nTB

    return norm.ppf(tA) - norm.ppf(1-tB)

def logisticPsy(x, alphax, betax, gammax, lambdax):
    """
    Compute the logistic function

    Parameters
    ----------
    x : 
        Stimulus level(s).
    alphax:
        Mid-point(s) of the psychometric function.
    betax:
        The slope of the psychometric function.
    gammax:
        Lower limit of the psychometric function.
    lambdax:
        The lapse rate.
    
    """
    
    out = gammax + (1-gammax-lambdax) *(1/(1+exp(betax*(alphax-x))))
    return out

def invLogisticPsy(p, alphax, betax, gammax, lambdax):
    """
    Compute the inverse of the logistic function

    Parameters
    ----------
    p : 
        Proportion correct on the psychometric function.
    alphax:
        Mid-point(s) of the psychometric function.
    betax:
        The slope of the psychometric function.
    gammax:
        Lower limit of the psychometric function.
    lambdax:
        The lapse rate.
    
    """

    x = alphax - (1/betax)*log((1-gammax-lambdax)/(p-gammax) - 1)
    return x

def logisticLikelihood(lev, response, alphax, betax, gammax, lambdax):

    p = logistic(lev, alphax, betax, gammax, lambdax)
    if response == 1:
        ll = log(p)
    elif response == 0:
        ll = log(1-p)
    

    return ll


def gaussianPsy(x, alphax, betax, gammax, lambdax):
    # as in UML toolbox
    out = gammax+(1-gammax-lambdax)*(1+erf((x-alphax)/sqrt(2*betax**2)))/2
    return out

def invGaussianPsy(p, alphax, betax, gammax, lambdax):
    out = alphax + sqrt(2*betax**2)*erfinv(2*(p-gammax)/(1-gammax-lambdax)-1)
    return out

def weibullPsy(x, alphax, betax, gammax, lambdax):
    out = gammax+(1-gammax-lambdax)*(1-numpy.exp(-(x/alphax)**betax))
    return out

def invWeibullPsy(p, alphax, betax, gammax, lambdax):
    out = alphax * (np.power(-log(1-(p-gammax)/(1-gammax-lambdax)), 1/betax))
    return out
    
def gumbelPsy(x, alphax, betax, gammax, lambdax):
    out = gammax + (1-gammax-lambdax) * (1-numpy.exp(-10**(betax*(x-alphax))))
    return out

def invGumbelPsy(p, alphax, betax, gammax, lambdax):
    out = alphax + (log10(-log(1 - (p-gammax)/(1-gammax-lambdax))))/betax
    return out
