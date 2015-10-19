# -*- coding: utf-8 -*-
import os, sys
import numpy as np
sys.path.append(os.path.normpath('../../'))
from pychoacoustics.pysdt import*


def virtualObserver(x, midpoint=0, slope=1, guess=0.5, lapse=0, funType="Logistic", funFit="Linear"):
    if funType == "Logistic":
        if funFit == "Linear":
            probCorr = logisticPsy(x, midpoint,
                                   slope, guess,
                                   lapse)
        elif funFit == "Logarithmic":
            probCorr = logisticPsy(np.log(x), np.log(midpoint),
                                   slope, guess,
                                   lapse)
    elif funType == "Gaussian":
        if funFit == "Linear":
            probCorr = gaussianPsy(x, midpoint,
                                       slope, guess,
                                       lapse)
        elif funFit == "Logarithmic":
            probCorr = gaussianPsy(np.log(x), np.log(midpoint),
                                       slope, guess,
                                       lapse)
    elif funType == "Gumbel":
        if funFit == "Linear":
            probCorr = gumbelPsy(x, midpoint,
                                 slope, guess,
                                 lapse)
        elif funFit == "Logarithmic":
            probCorr = gumbelPsy(np.log(x), np.log(midpoint),
                                 slope, guess,
                                 lapse)
    elif funType == "Weibull":
        if funFit == "Linear":
            probCorr = weibullPsy(x, midpoint,
                                  slope, guess,
                                  lapse)
        elif funFit == "Logarithmic":
            probCorr = weibullPsy(np.log(x), np.log(midpoint),
                                  slope, guess,
                                  lapse)

    resp = np.random.binomial(1, probCorr, 1)[0]
    
    return resp
