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

# This is an implementation of the PSI+ and PSI-marginal method of Prins.
# - Prins, N. (2013). The psi-marginal adaptive method: How to give nuisance parameters the attention they deserve (no more, no less). Journal of Vision, 13, 1–17.
# - Prins, N. (2012). The psychometric function: The lapse rate revisited. Journal of Vision, 12(6), 25–25.

import copy, scipy
import numpy as np
from numpy import arange, exp, linspace, logspace, log, log2, log10, meshgrid, sqrt
from scipy.stats import lognorm, norm
from scipy import stats
from scipy.special import erf
from .pysdt import*
from .stats_utils import gammaShRaFromMeanSD, gammaShRaFromModeSD
eps = np.spacing(1) #add eps to avoid taking log of zero

def setupPSIEstGuessRate(model="Logistic", stimScale="Linear", x0=None, xLim=(-10, 10),
                         xStep=1, alphaLim=(-10,10), alphaStep=1, alphaSpacing="Linear",
                         alphaDist="Uniform", alphaMu=0, alphaSTD=20, betaLim=(0.1,10),
                         betaStep=0.1, betaSpacing="Linear", betaDist="Uniform", betaMu=1,
                         betaSTD=2, gammaLim=(0,0.3), gammaStep=0.05,
                         gammaSpacing="Linear", gammaDist="Uniform", gammaMu=0.1,
                         gammaSTD=0.1, lambdaLim=(0,0.2), lambdaStep=0.01,
                         lambdaSpacing="Linear", lambdaDist="Uniform", lambdaMu=0,
                         lambdaSTD=0.1, marginalize = None):

    
    PSI = {}
    PSI["par"] = {}
    PSI["par"]["model"] = model
    PSI["par"]["x0"] = x0
    PSI["par"]["x"] = {}
    PSI["par"]["x"]["limits"] = xLim
    PSI["par"]["x"]["step"] = xStep
    PSI["par"]["stimScale"] = stimScale
    PSI["par"]["x"]["spacing"] = "Linear"

    PSI["par"]["alpha"] = {}
    PSI["par"]["alpha"]["limits"] = alphaLim
    PSI["par"]["alpha"]["step"] = alphaStep
    #PSI["par"]["alpha"]["scale"] = alphaScale
    PSI["par"]["alpha"]["spacing"] = alphaSpacing
    PSI["par"]["alpha"]["dist"] = alphaDist
    PSI["par"]["alpha"]["mu"] = alphaMu
    PSI["par"]["alpha"]["std"] = alphaSTD

    PSI["par"]["beta"] = {}
    PSI["par"]["beta"]["limits"] = betaLim
    PSI["par"]["beta"]["step"] = betaStep
    #PSI["par"]["beta"]["scale"] = betaScale
    PSI["par"]["beta"]["spacing"] = betaSpacing
    PSI["par"]["beta"]["dist"] = betaDist
    PSI["par"]["beta"]["mu"] = betaMu
    PSI["par"]["beta"]["std"] = betaSTD


    PSI["par"]["lambda"] = {}
    PSI["par"]["lambda"]["limits"] = lambdaLim
    PSI["par"]["lambda"]["step"] = lambdaStep
    PSI["par"]["lambda"]["spacing"] = lambdaSpacing
    PSI["par"]["lambda"]["dist"] = lambdaDist
    PSI["par"]["lambda"]["mu"] = lambdaMu
    PSI["par"]["lambda"]["std"] = lambdaSTD

    PSI["par"]["gamma"] = {}
    PSI["par"]["gamma"]["limits"] = gammaLim
    PSI["par"]["gamma"]["step"] = gammaStep
    PSI["par"]["gamma"]["spacing"] = gammaSpacing
    PSI["par"]["gamma"]["dist"] = gammaDist
    PSI["par"]["gamma"]["mu"] = gammaMu
    PSI["par"]["gamma"]["std"] = gammaSTD

    if stimScale == "Logarithmic":
        PSI["par"]["x"]["limits"] = log(xLim)
        PSI["par"]["x"]["step"] = log(xStep)
        PSI["par"]["alpha"]["limits"] = log(alphaLim)
        PSI["par"]["alpha"]["step"] = log(alphaStep)
        PSI["par"]["alpha"]["mu"] = log(alphaMu)
        PSI["par"]["alpha"]["std"] = log(alphaSTD)
        PSI["par"]["alpha"]["spacing"] = "Linear" #on a log scale
        
    PSI = setP0(PSI)

    
    PSI["x"] = np.array([])
  
    PSI["r"] = np.array([])
    PSI["n"] = 0
    #PSI["gamma"] = gamma
    PSI["lik_corr"] = np.zeros((len(PSI["stims"]), PSI["p"].shape[0], PSI["p"].shape[1], PSI["p"].shape[2], PSI["p"].shape[3]))
    if PSI["par"]["model"] == "Logistic":
        for i in range(len(PSI["stims"])):
            PSI["lik_corr"][i,:,:,:] = logisticPsy(PSI["stims"][i], PSI["a"], PSI["b"], PSI["g"], PSI["l"])
    elif PSI["par"]["model"] == "Gaussian":
        for i in range(len(PSI["stims"])):
            PSI["lik_corr"][i,:,:,:] = gaussianPsy(PSI["stims"][i], PSI["a"], PSI["b"], PSI["g"], PSI["l"])
    elif PSI["par"]["model"] == "Weibull":
        for i in range(len(PSI["stims"])):
            PSI["lik_corr"][i,:,:,:] = weibullPsy(PSI["stims"][i], PSI["a"], PSI["b"], PSI["g"], PSI["l"])
    elif PSI["par"]["model"] == "Gumbel":
        for i in range(len(PSI["stims"])):
            PSI["lik_corr"][i,:,:,:] = gumbelPsy(PSI["stims"][i], PSI["a"], PSI["b"], PSI["g"], PSI["l"])
    PSI["marginalize"] = marginalize

    if x0 == None:
        PSI = PSI_select_next_stim(PSI)
    else:
        PSI["xnext"] = copy.copy(x0)

    return PSI



def setP0(PSI):
    PSI["alpha"] = setParSpace(PSI["par"]["alpha"])
    PSI["beta"] = setParSpace(PSI["par"]["beta"])
    PSI["gamma"] = setParSpace(PSI["par"]["gamma"])
    PSI["lambda"] = setParSpace(PSI["par"]["lambda"])
    PSI["stims"] = setParSpace(PSI["par"]["x"])

    (PSI["a"], PSI["b"], PSI["g"], PSI["l"]) = meshgrid(PSI["alpha"], PSI["beta"], PSI["gamma"], PSI["lambda"], indexing='ij')

    A = setPrior(PSI["a"], PSI["par"]["alpha"])
    B = setPrior(PSI["b"], PSI["par"]["beta"])
    G = setPrior(PSI["g"], PSI["par"]["gamma"])
    L = setPrior(PSI["l"], PSI["par"]["lambda"])

    PSI["p"] = (A*B*G*L)
    PSI["p"]=PSI["p"]/PSI["p"].sum()

    #5-D probability distributions for each stimulus level and psychometric function in case of a correct
    # and in case of an incorrect response in the next trial
    PSI["pCorrNextNorm"] = np.zeros((len(PSI["stims"]), PSI["p"].shape[0], PSI["p"].shape[1], PSI["p"].shape[2], PSI["p"].shape[3]))
    PSI["pIncorrNextNorm"] = np.zeros((len(PSI["stims"]), PSI["p"].shape[0], PSI["p"].shape[1], PSI["p"].shape[2], PSI["p"].shape[3]))
    #probability of a correct and of an incorrect response at each stimulus level across 
    #also serves to scale the pdf to sum to one
    PSI["pCorrNextScaler"] = np.zeros(len(PSI["stims"]))
    PSI["pIncorrNextScaler"] = np.zeros(len(PSI["stims"]))
    #entropy for each possible stimulus level in case of a correct and an incorrect response
    PSI["entrCorr"] = np.zeros(len(PSI["stims"]))
    PSI["entrIncorr"] = np.zeros(len(PSI["stims"]))
    

    return PSI

def setParSpace(s):
    if s["spacing"] == "Linear":
        space = np.arange(s["limits"][0], s["limits"][1]+s["step"], s["step"])
    elif s["spacing"] == "Logarithmic":
        space = 10**(arange(log10(s["limits"][0]), log10(s["limits"][1]), log10(s["step"])))

    return space

def setPrior(phi, s):
    if s["dist"] == "Normal":
        if s["spacing"] == "Linear":
            p0  = norm.pdf(phi, loc=s["mu"], scale=s["std"])
        elif s["spacing"] == "Logarithmic":
            #p0  = norm.pdf(log10(phi), loc=s["mu"], scale=s["std"])
            #p0 = lognorm.pdf(phi, scale=exp(s["mu"]), s=s["std"], loc=0)
            #this is the MATLAB equivalent of
            #p0 =  lognpdf(phi, s["mu"], s["std"])
            m = s["mu"]; st=s["std"]
            #p0 = lognorm.pdf(x, scale=log(m/sqrt(1+st**2/m**2)), s=sqrt(log(1+st**2/m**2)))
            p0  = norm.pdf(log(phi), loc=log(s["mu"]), scale=log(s["std"]))
    elif s["dist"] == "Uniform":
        p0 = np.ones(phi.shape)
    elif s["dist"] == "Gamma":
        gShape, gRate = gammaShRaFromModeSD(s["mu"], s["std"])
        if s["spacing"] == "Linear":
            p0 = stats.gamma.pdf(phi, gShape, loc=0, scale=1/gRate)
        elif s["spacing"] == "Logarithmic":
            p0 = stats.gamma.pdf(log(phi), gShape, loc=0, scale=1/gRate)

    return p0


def PSIEstGuessRate_update(PSI, r):
    PSI = PSI_update_posterior(PSI, r)
    PSI = PSI_select_next_stim(PSI)
    return PSI

def PSI_update_posterior(PSI, r):
    PSI["n"] = PSI["n"] +1
    PSI["x"] = np.append(PSI["x"], PSI["xnext"])
    PSI["r"] = np.append(PSI["r"], r)

    if r == 1:
        #PSI["p"] = PSI["p"] * PSI["lik_corr"][np.where(PSI["stims"] == PSI["xnext"])[0][0],:,:,:]
        PSI["p"] = PSI["p"] * PSI["lik_corr"][np.where(abs(PSI["stims"] - PSI["xnext"]) == min(abs(PSI["stims"] - PSI["xnext"])))[0][0],:,:,:,:]
        
    elif r == 0:
        #PSI["p"] = PSI["p"] * (1-PSI["lik_corr"][np.where(PSI["stims"] == PSI["xnext"])[0][0],:,:,:])
        PSI["p"] = PSI["p"] * (1-PSI["lik_corr"][np.where(abs(PSI["stims"] - PSI["xnext"]) == min(abs(PSI["stims"] - PSI["xnext"])))[0][0],:,:,:,:])
    PSI["p"]=PSI["p"]/PSI["p"].sum()

    alpha_est = np.sum(PSI["p"]*PSI["a"])
    beta_est = np.sum(PSI["p"]*PSI["b"])
    gamma_est = np.sum(PSI["p"]*PSI["g"])
    lambda_est = np.sum(PSI["p"]*PSI["l"])
    if PSI["n"] == 1:
        PSI["phi"] = np.array([alpha_est, beta_est, gamma_est, lambda_est], ndmin=2)
    else:
        PSI["phi"] =  np.concatenate((PSI["phi"], np.array([alpha_est, beta_est, gamma_est, lambda_est], ndmin=2)), axis=0)
    if PSI["par"]["stimScale"] == "Logarithmic":
        PSI["est_midpoint"] = exp(alpha_est)
    else:
        PSI["est_midpoint"] = alpha_est
    PSI["est_slope"] = beta_est
    PSI["est_lapse"] = lambda_est
    PSI["est_guess"] = gamma_est

    return PSI

def PSI_select_next_stim(PSI):

    #5-D probability distributions for each stimulus level and psychometric function in case of a correct
    # and in case of an incorrect response in the next trial
    pCorrNextNorm = PSI["pCorrNextNorm"]
    pIncorrNextNorm = PSI["pIncorrNextNorm"]
    #probability of a correct and of an incorrect response at each stimulus level across 
    #also serves to scale the pdf to sum to one
    pCorrNextScaler = PSI["pCorrNextScaler"]
    pIncorrNextScaler = PSI["pIncorrNextScaler"]
    #entropy for each possible stimulus level in case of a correct and an incorrect response
    entrCorr = PSI["entrCorr"]
    entrIncorr = PSI["entrIncorr"]
    for i in range(len(PSI["stims"])):
        pCorrNextRaw = (PSI["p"] * PSI["lik_corr"][i,:,:,:,:])
        pIncorrNextRaw = (PSI["p"] * (1-PSI["lik_corr"][i,:,:,:,:]))
        pCorrNextScaler[i] = pCorrNextRaw.sum()
        pIncorrNextScaler[i]=pIncorrNextRaw.sum()
        pCorrNextNorm[i,:,:,:,:] = pCorrNextRaw / pCorrNextScaler[i]
        pIncorrNextNorm[i,:,:,:,:] = pIncorrNextRaw / pIncorrNextScaler[i]
        if PSI["marginalize"] != None:
            pCorrNextNormMarg = np.sum(pCorrNextNorm[i,:,:,:,:], axis=PSI["marginalize"])
            pIncorrNextNormMarg = np.sum(pIncorrNextNorm[i,:,:,:,:], axis=PSI["marginalize"])
            entrCorr[i] =  -((pCorrNextNormMarg*log2(pCorrNextNormMarg+eps)).sum())
            entrIncorr[i] = -((pIncorrNextNormMarg*log2(pIncorrNextNormMarg+eps)).sum())
        else:
            entrCorr[i] =  -((pCorrNextNorm[i]*log2(pCorrNextNorm[i]+eps)).sum())
            entrIncorr[i] = -((pIncorrNextNorm[i]*log2(pIncorrNextNorm[i]+eps)).sum())
    PSI["pCorrNextNorm"] =  pCorrNextNorm
    #Estimate the expected entropy for each test intensity x.
    PSI["entrTot"] = entrCorr*pCorrNextScaler + entrIncorr*pIncorrNextScaler
    #Find the test intensity that has the minimum expected entropy
    stimIdx = np.argmin(PSI["entrTot"])#np.where(PSI["entrTot"] == np.min(PSI["entrTot"]))
   
    PSI["xnext"] = PSI["stims"][stimIdx]
    if PSI["par"]["stimScale"] == "Logarithmic":
        PSI["xnextLinear"] = exp(PSI["xnext"])
    else:
        PSI["xnextLinear"] = PSI["xnext"]

    print('Est Midpoint: ', PSI["est_midpoint"])
    print('Est Guess: ', PSI["est_guess"])
    print('Est Slope: ', PSI["est_slope"])
    print('Est Lapse: ', PSI["est_lapse"])
    print('Next level: ', PSI["xnextLinear"])
  
    return PSI



