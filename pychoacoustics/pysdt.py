#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright (C) 2012-2023 Samuele Carcagno <sam.carcagno@gmail.com>
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


def compute_proportions(nCA, nTA, nIB, nTB, corr):
    """
    Compute proportions with optional corrections for extreme proportions.

    Parameters
    ----------
    nCA : float
        Number of correct 'A' trials
    nTA : int
        Number of total 'A' trials
    nIB : float
        Number of incorrect 'B' trials
    nTB : int
        Number of total 'B' trials
    corr : string
        The correction to apply, `none` for no correction, 'loglinear` for the
        log-linear correction, and `2N` for the '2N' correction.

    Returns
    -------
    HR : float
        Hit rate
    FA : float
        False alarm rate

    Examples
    --------
    >>> H,F = compute_proportions(8, 10, 2, 10, "loglinear")
    >>> H,F = compute_proportions(10, 10, 2, 10, "loglinear")
    >>> H,F = compute_proportions(10, 10, 2, 10, "2N")

    References
    ----------
   .. [1] Hautus, M. J. (1995). Corrections for extreme proportions and their biasing effects on estimated values of *d'*. *Behavior Research Methods, Instruments, & Computers, 27(I)*, 46–51. http://doi.org/10.3758/BF03203619
   .. [2] Macmillan, N. A., & Creelman, C. D. (2004). *Detection Theory: A User’s Guide (2nd ed.)*. London: Lawrence Erlbraum Associates.

    
    """
    if corr == "loglinear":
        HR = (nCA+0.5)/(nTA+1)
        FR = (nIB+0.5)/(nTB+1)
    elif corr == "2N":
        if nCA == nTA:
            HR = 1 - 1/(2*nTA)
        elif nCA == 0:
            HR = 1 / (2*nTA)
        else:
            HR = nCA/(nTA)

        if nIB == nTB:
            FR = 1 - 1/(2*nTB)
        elif nIB == 0:
            FR = 1 / (2*nTB)
        else:
            FR = nIB/(nTB)
    else:
        HR = nCA/nTA
        FR = nIB/nTB

    return HR, FR


def dprime_mAFC(Pc, m):
    """
    Compute *d'* corresponding to a certain proportion of correct
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
        *d'* value

    Examples
    --------
    >>> dp = dprime_mAFC(0.7, 3)

    References
    ----------
   .. [1] Green, D. M., & Swets, J. A. (1988). *Signal Detection Theory and Psychophysics*. Los Altos, California: Peninsula Publishing.
   .. [2] Green, D. M., & Dai, H. P. (1991). Probability of being correct with 1 of M orthogonal signals. *Perception & Psychophysics, 49(1)*, 100–101.
    
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



def dprime_ABX(H, FA, meth):
    """
    Compute *d'* for ABX task from 'hit' and 'false alarm' rates.

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
        *d'* value

    Examples
    --------
    >>> dp = dprime_ABX(0.7, 0.2, 'IO')
    >>> dp = dprime_ABX(0.7, 0.2, 'diff')

    References
    ----------
    .. [1] Macmillan, N. A., & Creelman, C. D. (2004). *Detection Theory: A User’s Guide (2nd ed.)*. London: Lawrence Erlbraum Associates.

    """

    if H < 0 or H > 1:
        raise ValueError("H must be between 0 and 1")
    if FA < 0 or FA > 1:
        raise ValueError("FA must be between 0 and 1")

    zdiff = norm.ppf(H) - norm.ppf(FA)
    pcUnb = norm.cdf(zdiff/2)
    if pcUnb < 0.5:
        #raise ValueError("H must be greater than FA")
        dpsign = -1
        zdiff = norm.ppf(FA) - norm.ppf(H)
        pcUnb = norm.cdf(zdiff/2)
    else:
        dpsign = 1

        
    root2 = sqrt(2)
    if meth == "diff":
        root6 = sqrt(6)
        def est_dp2(dp):
            return pcUnb - norm.cdf(dp/root2) * norm.cdf(dp/root6) - norm.cdf(-dp/root2) * norm.cdf(-dp/root6)
        try:
            dprime =  scipy.optimize.brentq(est_dp2, 0, 10)
        except:
            dprime = numpy.nan
    elif meth == "IO":
        def est_dp2(dp):
            return pcUnb - norm.cdf(dp/root2) * norm.cdf(dp/2) - norm.cdf(-dp/root2) * norm.cdf(-dp/2)
        try:
            dprime =  scipy.optimize.brentq(est_dp2, 0, 10)
        except:
            dprime = numpy.nan
    # if H == FA:
    #     dprime = 0
    return dprime*dpsign

def dprime_ABX_from_counts(nCA, nTA, nCB, nTB, meth, corr):
    """
    Compute *d'* for ABX task from counts of correct and total responses.

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
        *d'* value

    Examples
    --------
    >>> dp = dprime_ABX(0.7, 0.2, 'IO')

    References
    ----------
    .. [1] Macmillan, N. A., & Creelman, C. D. (2004). *Detection Theory: A User’s Guide (2nd ed.)*. London: Lawrence Erlbraum Associates.

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

    return dprime_ABX(H=tA, FA=1-tB, meth=meth)

def dprime_oddity(prCorr, meth="diff"):
    """
    Compute *d'* for oddity task from proportion of correct responses.
    Only valid for the case in which there are three presentation intervals.

    Parameters
    ----------
    prCorr : float
        Proportion of correct responses.
    meth : string
        'diff' for differencing strategy or 'IO' for independent observations strategy.

    Returns
    -------
    dprime : float
        *d'* value

    Examples
    --------
    >>> dp = dprime_oddity(0.7)
    >>> dp = dprime_oddity(0.8)

    References
    ----------
    .. [1] Macmillan, N. A., & Creelman, C. D. (2004). *Detection Theory: A User’s Guide (2nd ed.)*. London: Lawrence Erlbraum Associates.
    .. [2] Versfeld, N. J., Dai, H., & Green, D. M. (1996). The optimum decision rules for the oddity task. *Perception & Psychophysics, 58(1)*, 10–21.

    """
    
    if prCorr < 1/3:
        raise ValueError("Only valid for Pc.tri > 1/3")

    if meth == "diff":
        root3 = sqrt(3)
        root2_3 = sqrt(2)/root3
        def est_dp(dp):

            def pr(x):

                out =  2 *(norm.cdf(-x * root3 + dp * root2_3) + norm.cdf(-x * root3 - dp * root2_3)) * norm.pdf(x)

                return out

            out2 = prCorr - quad(pr, 0, Inf)[0] 

            return out2
        try:
            dp_res = scipy.optimize.brentq(est_dp, 0, 10)
        except:
            dp_res = numpy.nan
    elif meth == "IO":
        def est_dp(dp):
            def pr1(x):
                return norm.pdf(x)*norm.cdf(x+dp)**2
            def pr2(x):
                return norm.pdf(x)*(1-norm.cdf(x+dp))**2

            out = prCorr - (norm.cdf(dp/2)**3 + quad(pr1, -Inf, -dp/2)[0] + (1-norm.cdf(dp/2))**3 + quad(pr2, -dp/2, Inf)[0])

            return out

        try:
            dp_res = scipy.optimize.brentq(est_dp, 0, 10)
        except:
            dp_res = numpy.nan

    return dp_res
        



def dprime_SD(H, FA, meth):
    """
    Compute *d'* for one interval same/different task from 'hit' and 'false alarm' rates.

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
        *d'* value

    Examples
    --------
    >>> dp = dprime_SD(0.7, 0.2, 'IO')

    References
    ----------
    .. [1] Macmillan, N. A., & Creelman, C. D. (2004). *Detection Theory: A User’s Guide (2nd ed.)*. London: Lawrence Erlbraum Associates.
    .. [2] Kingdom, F. A. A., & Prins, N. (2010). *Psychophysics: A Practical Introduction*. Academic Press.

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
            if H == FA:
                dprime = 0
            else:
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
    Compute *d'* for one interval same/different task from counts of correct and total responses.

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
        *d'* value

    Examples
    --------
    >>> dp = dprime_SD(0.7, 0.2, 'IO')

    References
    ----------
    .. [1] Macmillan, N. A., & Creelman, C. D. (2004). *Detection Theory: A User’s Guide (2nd ed.)*. London: Lawrence Erlbraum Associates.
    .. [2] Kingdom, F. A. A., & Prins, N. (2010). *Psychophysics: A Practical Introduction*. Academic Press.

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
    Compute *d'* for one interval 'yes/no' type tasks from hits and false alarm rates.

    Parameters
    ----------
    H : float
        Hit rate.
    FA : float
        False alarms rate.

    Returns
    -------
    dprime : float
        *d'* value

    Examples
    --------
    >>> dp = dprime_yes_no(0.7, 0.2)

    References
    ----------
    .. [1] Green, D. M., & Swets, J. A. (1988). *Signal Detection Theory and Psychophysics*. Los Altos, California: Peninsula Publishing.
    .. [2] Macmillan, N. A., & Creelman, C. D. (2004). *Detection Theory: A User’s Guide (2nd ed.)*. London: Lawrence Erlbraum Associates.

    """
    
    if H < 0 or H > 1:
        raise ValueError("H must be between 0 and 1")
    if FA < 0 or FA > 1:
        raise ValueError("FA must be between 0 and 1")

    return norm.ppf(H) - norm.ppf(FA)


def dprime_yes_no_from_counts(nCA, nTA, nCB, nTB, corr):
    """
    Compute *d'* for one interval 'yes/no' type tasks from counts of correct and total responses.

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
        *d'* value

    Examples
    --------
    >>> dp = dprime_yes_no_from_counts(nCA=70, nTA=100, nCB=80, nTB=100, corr=True)

    References
    ----------
    .. [1] Green, D. M., & Swets, J. A. (1988). *Signal Detection Theory and Psychophysics*. Los Altos, California: Peninsula Publishing.
    .. [2] Macmillan, N. A., & Creelman, C. D. (2004). *Detection Theory: A User’s Guide (2nd ed.)*. London: Lawrence Erlbraum Associates.

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
    Compute the logistic psychometric function.

    Parameters
    ----------
    x : 
        Stimulus level(s).
    alphax:
        Mid-point(s) of the psychometric function.
    betax:
        The slope of the psychometric function.
    gammax:
        Lower limit of the psychometric function (guess rate).
    lambdax:
        The lapse rate.

    Returns
    -------
    pc :
         Proportion correct at the stimulus level(s) `x`.

    References
    ----------- 
    .. [1] Kingdom, F. A. A., & Prins, N. (2010). *Psychophysics: A Practical Introduction*. Academic Press.

    """
    
    out = gammax + (1-gammax-lambdax) *(1/(1+exp(betax*(alphax-x))))
    return out

def logisticPsyWd(x, alphax, width, gammax, lambdax, perc=90):
    """
    Compute the logistic psychometric function
    parametrized in terms of width.

    Parameters
    ----------
    x : 
        Stimulus level(s).
    alphax:
        Mid-point(s) of the psychometric function.
    width:
        The width of the psychometric function.
    gammax:
        Lower limit of the psychometric function (guess rate).
    lambdax:
        The lapse rate.
    perc:
        The percentage of the psychometric function covered
        by the width. For example, if `perc` is 90, the width
        goes from 5% to 95% of the probability range covered by
        the psychometric function.

    Returns
    -------
    pc :
         Proportion correct at the stimulus level(s) `x`.

    References
    ----------- 
    .. [1] Kingdom, F. A. A., & Prins, N. (2010). *Psychophysics: A Practical Introduction*. Academic Press.

    .. [2] Alcalá-Quintana, R., & García-Pérez, M. A. (2004). The Role of Parametric Assumptions in Adaptive Bayesian Estimation. Psychological Methods, 9(2), 250–271. https://doi.org/10.1037/1082-989X.9.2.250

    .. [3] Kuss, M., Jäkel, F., & Wichmann, F. A. (2005). Bayesian inference for psychometric functions. Journal of Vision, 5(5), 8. https://doi.org/10.1167/5.5.8

    """
    
    betax = psychWidthToSlope(width, perc, sigmoid="logistic")
    out = logisticPsy(x, alphax, betax, gammax, lambdax)
    
    return out


def invLogisticPsy(p, alphax, betax, gammax, lambdax):
    """
    Compute the inverse logistic psychometric function.

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

    Returns
    -------
    x :
         Stimulus level at which proportion correct equals `p`
         for the listener specified by the function.
    
    References
    ----------- 
    .. [1] Kingdom, F. A. A., & Prins, N. (2010). *Psychophysics: A Practical Introduction*. Academic Press.
    
    """

    x = alphax - (1/betax)*log((1-gammax-lambdax)/(p-gammax) - 1)
    return x

def invLogisticPsyWd(p, alphax, width, gammax, lambdax, perc=90):
    """
    Compute the inverse logistic psychometric function
    parametrized by width.

    Parameters
    ----------
    p : 
        Proportion correct on the psychometric function.
    alphax:
        Mid-point(s) of the psychometric function.
    width:
        The width of the psychometric function.
    gammax:
        Lower limit of the psychometric function.
    lambdax:
        The lapse rate.
    perc:
        The percentage of the psychometric function covered
        by the width. For example, if `perc` is 90, the width
        goes from 5% to 95% of the probability range covered by
        the psychometric function.

    Returns
    -------
    x :
         Stimulus level at which proportion correct equals `p`
         for the listener specified by the function.
    
    References
    ----------- 
    .. [1] Kingdom, F. A. A., & Prins, N. (2010). *Psychophysics: A Practical Introduction*. Academic Press.

    .. [2] Alcalá-Quintana, R., & García-Pérez, M. A. (2004). The Role of Parametric Assumptions in Adaptive Bayesian Estimation. Psychological Methods, 9(2), 250–271. https://doi.org/10.1037/1082-989X.9.2.250

    .. [3] Kuss, M., Jäkel, F., & Wichmann, F. A. (2005). Bayesian inference for psychometric functions. Journal of Vision, 5(5), 8. https://doi.org/10.1167/5.5.8
    
    """
    
    betax = psychWidthToSlope(width, perc, sigmoid="logistic")
    out = invLogisticPsy(p, alphax, betax, gammax, lambdax)
    
    return out


def logisticLikelihood(lev, response, alphax, betax, gammax, lambdax):

    p = logistic(lev, alphax, betax, gammax, lambdax)
    if response == 1:
        ll = log(p)
    elif response == 0:
        ll = log(1-p)
    

    return ll


def gaussianPsy(x, alphax, betax, gammax, lambdax):
    """
    Compute the gaussian psychometric function.

    Parameters
    ----------
    x : 
        Stimulus level(s).
    alphax:
        Mid-point(s) of the psychometric function.
    betax:
        The slope of the psychometric function.
    gammax:
        Lower limit of the psychometric function (guess rate).
    lambdax:
        The lapse rate.

    Returns
    -------
    pc :
         Proportion correct at the stimulus level(s) `x`.

    References
    ----------- 
    .. [1] Kingdom, F. A. A., & Prins, N. (2010). *Psychophysics: A Practical Introduction*. Academic Press.
    
    """
    # as in UML toolbox
    out = gammax+(1-gammax-lambdax)*(1+erf((x-alphax)/sqrt(2*betax**2)))/2
    return out

def invGaussianPsy(p, alphax, betax, gammax, lambdax):
    """
    Compute the inverse gaussian psychometric function.

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

    Returns
    -------
    x :
         Stimulus level at which proportion correct equals `p`
         for the listener specified by the function.

    References
    ----------- 
    .. [1] Kingdom, F. A. A., & Prins, N. (2010). *Psychophysics: A Practical Introduction*. Academic Press.
    
    """
    out = alphax + sqrt(2*betax**2)*erfinv(2*(p-gammax)/(1-gammax-lambdax)-1)
    return out

def weibullPsy(x, alphax, betax, gammax, lambdax):
    """
    Compute the weibull psychometric function.

    Parameters
    ----------
    x : 
        Stimulus level(s).
    alphax:
        Mid-point(s) of the psychometric function.
    betax:
        The slope of the psychometric function.
    gammax:
        Lower limit of the psychometric function (guess rate).
    lambdax:
        The lapse rate.

    Returns
    -------
    pc :
         Proportion correct at the stimulus level(s) `x`.

    References
    ----------- 
    .. [1] Kingdom, F. A. A., & Prins, N. (2010). *Psychophysics: A Practical Introduction*. Academic Press.
    
    """
    out = gammax+(1-gammax-lambdax)*(1-numpy.exp(-(x/alphax)**betax))
    return out

def invWeibullPsy(p, alphax, betax, gammax, lambdax):
    """
    Compute the inverse weibull psychometric function.

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

    Returns
    -------
    x :
         Stimulus level at which proportion correct equals `p`
         for the listener specified by the function.

    References
    ----------- 
    .. [1] Kingdom, F. A. A., & Prins, N. (2010). *Psychophysics: A Practical Introduction*. Academic Press.
    
    """
    out = alphax * (np.power(-log(1-(p-gammax)/(1-gammax-lambdax)), 1/betax))
    return out
    
def gumbelPsy(x, alphax, betax, gammax, lambdax):
    """
    Compute the gumbel psychometric function.

    Parameters
    ----------
    x : 
        Stimulus level(s).
    alphax:
        Mid-point(s) of the psychometric function.
    betax:
        The slope of the psychometric function.
    gammax:
        Lower limit of the psychometric function (guess rate).
    lambdax:
        The lapse rate.

    Returns
    -------
    pc :
         Proportion correct at the stimulus level(s) `x`.

    References
    ----------- 
    .. [1] Kingdom, F. A. A., & Prins, N. (2010). *Psychophysics: A Practical Introduction*. Academic Press.
    
    """
    out = gammax + (1-gammax-lambdax) * (1-numpy.exp(-10**(betax*(x-alphax))))
    return out

def invGumbelPsy(p, alphax, betax, gammax, lambdax):
    """
    Compute the inverse gumbel psychometric function.

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

    Returns
    -------
    x :
         Stimulus level at which proportion correct equals `p`
         for the listener specified by the function.

    References
    ----------- 
    .. [1] Kingdom, F. A. A., & Prins, N. (2010). *Psychophysics: A Practical Introduction*. Academic Press.
    
    """
    out = alphax + (log10(-log(1 - (p-gammax)/(1-gammax-lambdax))))/betax
    return out


def psychSlopeToWidth(sl, perc=90, sigmoid="logistic"):
    """
    Convert psychometric function slope to width. Currently
    works only for a logistic psychometric function.

    Parameters
    ----------
    sl : 
        Psychometric function slope.
    perc:
        The percentage of the psychometric function covered
        by the width. For example, if `perc` is 90, the width
        goes from 5% to 95% of the probability range covered by
        the psychometric function.
    sigmoid:
        The psychometric function shape. Currently only
        logistic psychometric functions are accepted.

    Returns
    -------
    width :
         The psychometric function width.

    References
    ----------- 
    .. [1] Alcalá-Quintana, R., & García-Pérez, M. A. (2004). The Role of Parametric Assumptions in Adaptive Bayesian Estimation. Psychological Methods, 9(2), 250–271. https://doi.org/10.1037/1082-989X.9.2.250

    .. [2] Kuss, M., Jäkel, F., & Wichmann, F. A. (2005). Bayesian inference for psychometric functions. Journal of Vision, 5(5), 8. https://doi.org/10.1167/5.5.8
    
    """
    pTail = (1-perc/100)/2
    
    if sigmoid == "logistic":
        out = (2*log(1/pTail-1)) / sl
    
    return out

def psychWidthToSlope(wd, perc=90, sigmoid="logistic"):
    """
    Convert psychometric function width to slope. Currently
    works only for a logistic psychometric function.

    Parameters
    ----------
    wd : 
        Psychometric function width.
    perc:
        The percentage of the psychometric function covered
        by the width. For example, if `perc` is 90, the width
        goes from 5% to 95% of the probability range covered by
        the psychometric function.
    sigmoid:
        The psychometric function shape. Currently only
        logistic psychometric functions are accepted.

    Returns
    -------
    slope :
         The psychometric function slope.

    References
    ----------- 
    .. [1] Alcalá-Quintana, R., & García-Pérez, M. A. (2004). The Role of Parametric Assumptions in Adaptive Bayesian Estimation. Psychological Methods, 9(2), 250–271. https://doi.org/10.1037/1082-989X.9.2.250

    .. [2] Kuss, M., Jäkel, F., & Wichmann, F. A. (2005). Bayesian inference for psychometric functions. Journal of Vision, 5(5), 8. https://doi.org/10.1167/5.5.8
    
    """
    pTail = (1-perc/100)/2
    
    if sigmoid == "logistic":
        out = (2*log(1/pTail-1)) / wd
    
    return out

