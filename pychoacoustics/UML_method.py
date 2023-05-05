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

# This is a Python port of the UML method of Shen and Richards http://hearlab.ss.uci.edu/UML/uml.html
# - Shen, Y., & Richards, V. (2012). A maximum-likelihood procedure for estimating psychometric functions: Thresholds, slopes, and lapses of attention. The Journal of the Acoustical Society of America, 132, 957–967.
# - Shen, Y., Dai, W., & Richards, V. M. (2014). A MATLAB toolbox for the efficient estimation of the psychometric function using the updated maximum-likelihood adaptive procedure. Behavior Research Methods, 13–26.

import copy, random, scipy
import numpy as np
from numpy import arange, exp, inf, linspace, logspace, log, log10, meshgrid, pi, ravel
from scipy.stats import lognorm, norm #gamma conflicts with gamma variable
from scipy import stats
from scipy.special import erf
from .pysdt import*
from .stats_utils import gammaShRaFromMeanSD, gammaShRaFromModeSD, betaABFromMeanSTD, generalizedBetaABFromMeanSTD


def setupUML(model="Logistic", swptRule="Up-Down", nDown=2, centTend="Mean", stimScale="Linear", x0=None, xLim=(-10, 10), 
             alphaLim=(-10,10), alphaStep=1, alphaSpacing="Linear", alphaDist="Uniform", alphaMu=0, alphaSTD=20,
             betaLim=(0.1,10), betaStep=0.1, betaSpacing="Linear", betaDist="Uniform", betaMu=1, betaSTD=2,
             gamma=0.5,
             lambdaLim=(0,0.2), lambdaStep=0.01, lambdaSpacing="Linear", lambdaDist="Uniform", lambdaMu=0, lambdaSTD=0.1,
             suggestedLambdaSwpt=10, lambdaSwptPC=0.99):

    
    UML = {}
    UML["par"] = {}
    UML["par"]["swptRule"] = swptRule
    UML["par"]["nDown"] = nDown
    UML["par"]["method"] = centTend
    UML["par"]["model"] = model
    UML["par"]["x0"] = x0
    UML["par"]["x"] = {}
    UML["par"]["x"]["limits"] = xLim
    #UML["par"]["x"]["step"] = xStep
    UML["par"]["stimScale"] = stimScale
    UML["par"]["x"]["spacing"] = "Linear"

    UML["par"]["alpha"] = {}
    UML["par"]["alpha"]["limits"] = alphaLim
    UML["par"]["alpha"]["step"] = alphaStep
    #UML["par"]["alpha"]["scale"] = alphaScale
    UML["par"]["alpha"]["spacing"] = alphaSpacing
    UML["par"]["alpha"]["dist"] = alphaDist
    UML["par"]["alpha"]["mu"] = alphaMu
    UML["par"]["alpha"]["std"] = alphaSTD

    UML["par"]["beta"] = {}
    UML["par"]["beta"]["limits"] = betaLim
    UML["par"]["beta"]["step"] = betaStep
    #UML["par"]["beta"]["scale"] = betaScale
    UML["par"]["beta"]["spacing"] = betaSpacing
    UML["par"]["beta"]["dist"] = betaDist
    UML["par"]["beta"]["mu"] = betaMu
    UML["par"]["beta"]["std"] = betaSTD

    #UML["par"]["gamma"] = gamma

    UML["par"]["lambda"] = {}
    UML["par"]["lambda"]["limits"] = lambdaLim
    UML["par"]["lambda"]["step"] = lambdaStep
    #UML["par"]["lambda"]["scale"] = lambdaScale
    UML["par"]["lambda"]["spacing"] = lambdaSpacing
    UML["par"]["lambda"]["dist"] = lambdaDist
    UML["par"]["lambda"]["mu"] = lambdaMu
    UML["par"]["lambda"]["std"] = lambdaSTD

    UML["par"]["suggestedLambdaSwpt"] = suggestedLambdaSwpt
    UML["par"]["lambdaSwptPC"] = lambdaSwptPC
    
    if stimScale == "Logarithmic":
        UML["par"]["x0"] = log(x0)
        UML["par"]["x"]["limits"] = log(xLim)
        UML["par"]["alpha"]["limits"] = log(alphaLim)
        UML["par"]["alpha"]["step"] = log(alphaStep)
        UML["par"]["alpha"]["mu"] = log(alphaMu)
        UML["par"]["alpha"]["std"] = log(alphaSTD)
        UML["par"]["alpha"]["spacing"] = "Linear" #on a log scale
        UML["par"]["suggestedLambdaSwpt"] = log(UML["par"]["suggestedLambdaSwpt"])

    UML = setP0(UML)
    UML["x"] = np.array([])
    UML["xnext"] = copy.copy(UML["par"]["x0"])
    UML["r"] = np.array([])
    #UML["phi"] = np.array([])
    UML["n"] = 0
    UML["gamma"] = gamma

    UML["swpts_idx"] = np.array([], dtype="int32")
    if len(UML["alpha"]) > 1: #alpha is not fixed, estimate it
        UML["swpts_idx"] = np.append(UML["swpts_idx"], 1)
    if len(UML["beta"]) > 1: #beta is not fixed, estimate it
        UML["swpts_idx"] = np.append(UML["swpts_idx"], [0,2])
    if len(UML["lambda"]) > 1: #lambda is not fixed, estimate it
        UML["swpts_idx"] = np.append(UML["swpts_idx"], 3)

    UML["swpts_idx"].sort()
    UML["nsteps"] = len(UML["swpts_idx"])
    UML["step_flag"] = 0
    UML["track_direction"] = 0
    UML["rev_flag"] = np.array([], dtype="int32")
    UML["nrev"] = 0

    if UML["par"]["x0"] == UML["par"]["x"]["limits"][0]:
        UML["current_step"] = 1
    elif UML["par"]["x0"] == UML["par"]["x"]["limits"][1]:
        UML["current_step"] = UML["nsteps"]
    else:
        UML["current_step"] = int(np.ceil(UML["nsteps"]/2))


    return UML


def setP0(UML):
    UML["alpha"] = setParSpace(UML["par"]["alpha"])
    UML["beta"] = setParSpace(UML["par"]["beta"])
    UML["lambda"] = setParSpace(UML["par"]["lambda"])

    (UML["a"], UML["b"], UML["l"]) = meshgrid(UML["alpha"], UML["beta"], UML["lambda"], indexing='ij')

    A = setPrior(UML["a"], UML["par"]["alpha"])
    B = setPrior(UML["b"], UML["par"]["beta"])
    L = setPrior(UML["l"], UML["par"]["lambda"])

    UML["p"] = log(prepare_prob(A*B*L))

    return UML

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
            #m = s["mu"]; st=s["std"]
            #p0 = lognorm.pdf(phi, scale=log(m/sqrt(1+st**2/m**2)), s=sqrt(log(1+st**2/m**2)))
            p0  = norm.pdf(log(phi), loc=log(s["mu"]), scale=log(s["std"]))
    elif s["dist"] == "Uniform":
        p0 = np.ones(phi.shape)
    elif s["dist"] == "Gamma":
        gShape, gRate = gammaShRaFromModeSD(s["mu"], s["std"])
        if s["spacing"] == "Linear":
            p0 = stats.gamma.pdf(phi, gShape, loc=0, scale=1/gRate)
        elif s["spacing"] == "Logarithmic":
            p0 = stats.gamma.pdf(log(phi), gShape, loc=0, scale=1/gRate)
    elif s["dist"] == "Beta":
        if s["spacing"] == "Linear":
            a,b=betaABFromMeanSTD(s["mu"], s["std"])
            p0  = stats.beta.pdf(phi, a=a, b=b)
        elif s["spacing"] == "Logarithmic":
            a,b=betaABFromMeanSTD(log(s["mu"]), log(s["std"]))
            p0  = stats.beta.pdf(phi, a=a, b=b)
        #p0[np.isinf(p0)] = scipy.stats.beta.pdf(np.finfo(0.1).eps, a, b)
        #p0[np.isneginf(p0)] = scipy.stats.beta.pdf(np.finfo(0.1).eps, a, b)
    elif s["dist"] == "Generalized Beta":
        if s["spacing"] == "Linear":
            a,b=generalizedBetaABFromMeanSTD(s["mu"], s["std"], s["limits"][0], s["limits"][1])
            p0  = stats.beta.pdf(phi, a=a, b=b, loc=s["limits"][0], scale=s["limits"][1]-s["limits"][0])
        elif s["spacing"] == "Logarithmic":
            a,b=generalizedBetaABFromMeanSTD(log(s["mu"]), log(s["std"]), log(s["limits"][0]), log(s["limits"][1]))
            p0  = stats.beta.pdf(phi, a=a, b=b, loc=log(s["limits"][0]), scale=log(s["limits"][1])-log(s["limits"][0]))
        #p0[np.isinf(p0)] = scipy.stats.beta.pdf(np.finfo(0.1).eps, a, b)
        #p0[np.isneginf(p0)] = scipy.stats.beta.pdf(np.finfo(0.1).eps, a, b)
    elif s["dist"] == "t":
        if s["spacing"] == "Linear":
            p0  = stats.t.pdf(phi, loc=s["mu"], scale=s["std"], df=1)
        elif s["spacing"] == "Logarithmic":
            p0  = stats.t.pdf(log(phi), loc=log(s["mu"]), scale=log(s["std"]), df=1)
            
    return p0


def prepare_prob(p):
    p = p*(1-1e-10)
    p = p/p.sum()

    return p


def UML_update(UML, r):
    UML["n"] = UML["n"] +1
    UML["x"] = np.append(UML["x"], UML["xnext"])
    UML["r"] = np.append(UML["r"], r)

    if UML["par"]["model"] == "Logistic":
        UML["p"] = UML["p"] + \
                   log(prepare_prob(logisticPsy(UML["xnext"], UML["a"], UML["b"], UML["gamma"], UML["l"]))**r) + \
                   log(prepare_prob(1-logisticPsy(UML["xnext"], UML["a"], UML["b"], UML["gamma"], UML["l"]))**(1-r))
    elif UML["par"]["model"] == "Gaussian":
        UML["p"] = UML["p"] + \
                   log(prepare_prob(gaussianPsy(UML["xnext"], UML["a"], UML["b"], UML["gamma"], UML["l"]))**r) + \
                   log(prepare_prob(1-gaussianPsy(UML["xnext"], UML["a"], UML["b"], UML["gamma"], UML["l"]))**(1-r))
    elif UML["par"]["model"] == "Weibull":
        UML["p"] = UML["p"] + \
                   log(prepare_prob(weibullPsy(UML["xnext"], UML["a"], UML["b"], UML["gamma"], UML["l"]))**r) + \
                   log(prepare_prob(1-weibullPsy(UML["xnext"], UML["a"], UML["b"], UML["gamma"], UML["l"]))**(1-r))


    UML["p"] = UML["p"]-np.max(np.max(np.max(UML["p"])))
  
    if UML["par"]["method"] == "Mode":
        # idx = np.where(UML["p"] == np.max(UML["p"]))
        # if UML["n"] < 2:
        #     UML["phi"] = np.array([UML["a"][idx[0][0], idx[1][0], idx[2][0]], UML["b"][idx[0][0], idx[1][0], idx[2][0]], UML["gamma"], UML["l"][idx[0][0], idx[1][0], idx[2][0]]], ndmin=2)
        # else:
        #     UML["phi"] = np.concatenate((UML["phi"], np.array([UML["a"][idx[0][0]], UML["b"][idx[0][0], idx[1][0], idx[2][0]], UML["gamma"], UML["l"][idx[0][0], idx[1][0], idx[2][0]]], ndmin=2)), axis=0)
        
        idx = np.argmax(UML["p"])
        if UML["n"] < 2:
            UML["phi"] = np.array([ravel(UML["a"])[idx], ravel(UML["b"])[idx], UML["gamma"], ravel(UML["l"])[idx]], ndmin=2)
        else:
            UML["phi"] = np.concatenate((UML["phi"], np.array([ravel(UML["a"])[idx], ravel(UML["b"])[idx], UML["gamma"], ravel(UML["l"])[idx]], ndmin=2)), axis=0)
    elif UML["par"]["method"] == "Mean":
        pdf_tmp = np.exp(UML["p"])
        pdf_tmp = pdf_tmp/pdf_tmp.sum()
        alpha_est_tmp = np.sum(pdf_tmp*UML["a"])
        beta_est_tmp = np.sum(pdf_tmp*UML["b"])
        lambda_est_tmp = np.sum(pdf_tmp*UML["l"])

        if UML["n"] < 2:
            UML["phi"] = np.array([alpha_est_tmp, beta_est_tmp, UML["gamma"], lambda_est_tmp], ndmin=2)
        else:
            UML["phi"] = np.concatenate((UML["phi"], np.array([alpha_est_tmp, beta_est_tmp, UML["gamma"], lambda_est_tmp], ndmin=2)), axis=0)

    if UML["par"]["stimScale"] == "Logarithmic":
        UML["est_midpoint"] = exp(UML["phi"][UML["phi"].shape[0]-1, 0])
    else:
        UML["est_midpoint"] = UML["phi"][UML["phi"].shape[0]-1, 0]
    UML["est_slope"] = UML["phi"][UML["phi"].shape[0]-1, 1]
    UML["est_lapse"] = UML["phi"][UML["phi"].shape[0]-1, 3]

    if UML["par"]["model"] == "Logistic":
        swpt = logit_sweetpoints(UML["phi"][-1,:])
    elif UML["par"]["model"] == "Gaussian":
        swpt = gaussian_sweetpoints(UML["phi"][-1,:])
    elif UML["par"]["model"] == "Weibull":
        swpt = weibull_sweetpoints(UML["phi"][-1,:])

    est_alpha = UML["phi"][UML["phi"].shape[0]-1, 0] #if scale is Logarithmic this needs to stay in log coordinates
    if UML["par"]["model"] == "Logistic":
        xCeiling = invLogisticPsy(UML["par"]["lambdaSwptPC"]-UML["est_lapse"], est_alpha, UML["est_slope"], UML["gamma"], UML["est_lapse"])
    elif UML["par"]["model"] == "Gaussian":
        xCeiling = invGaussianPsy(UML["par"]["lambdaSwptPC"]-UML["est_lapse"], est_alpha, UML["est_slope"], UML["gamma"], UML["est_lapse"])
    elif UML["par"]["model"] == "Weibull":
        xCeiling = invWeibullPsy(UML["par"]["lambdaSwptPC"]-UML["est_lapse"], est_alpha, UML["est_slope"], UML["gamma"], UML["est_lapse"])
   
    lmbdSwpt = min(max(UML["par"]["suggestedLambdaSwpt"], xCeiling), UML["par"]["x"]["limits"][1])
    
    #swpt = np.append(swpt, UML["par"]["x"]["limits"][1])
    swpt = np.append(swpt, lmbdSwpt)
    UML["swpt"] = swpt
    swpt = np.maximum(np.minimum(swpt[UML["swpts_idx"]], UML["par"]["x"]["limits"][1]), UML["par"]["x"]["limits"][0])#; % limit the sweet points to be within the stimulus space

    if UML["par"]["swptRule"] == "Up-Down":
        UML["rev_flag"] = np.append(UML["rev_flag"], 0)
        if r >= 0.5:
            if UML["step_flag"] == UML["par"]["nDown"]-1:
                UML["current_step"] = np.maximum(UML["current_step"]-1,1)
                newx = swpt[UML["current_step"]-1]
                UML["step_flag"] = 0
                if UML["track_direction"] == 1:
                    UML["rev_flag"] = np.append(UML["rev_flag"], 1)
                    UML["nrev"] = UML["nrev"] +1
                UML["track_direction"] = -1
            elif UML["step_flag"] < UML["par"]["nDown"]-1:
                newx = swpt[UML["current_step"]-1]
                UML["step_flag"] = UML["step_flag"]+1
        elif r <= 0.5:
            UML["current_step"] = np.minimum(UML["current_step"]+1, UML["nsteps"])
            newx = swpt[UML["current_step"]-1]
            UML["step_flag"] = 0
            if UML["track_direction"] == -1:
                UML["rev_flag"] = np.append(UML["rev_flag"], 1)
                UML["nrev"] = UML["nrev"]+1
            UML["track_direction"] = 1
    elif UML["par"]["swptRule"] == "Random":
        newx = swpt[random.choice([0,1,2,3])]

    if UML["n"] < 2:
        UML["swpts"] = np.array(swpt, ndmin=2)
    else:
        UML["swpts"] = np.concatenate((UML["swpts"], np.array(swpt, ndmin=2)), axis=0)
    UML["xnext"] = newx

    if UML["par"]["stimScale"] == "Logarithmic":
        UML["xnextLinear"] = exp(UML["xnext"])
    else:
        UML["xnextLinear"] = UML["xnext"]

    # print('Est Midpoint: ', UML["est_midpoint"])
    # print('Est Slope: ', UML["est_slope"])
    # print('Est Lapse: ', UML["est_lapse"])
    # print('Next level: ', UML["xnextLinear"])
    # if UML["par"]["stimScale"] == "Logarithmic":
    #     print('xCeiling: ', exp(xCeiling))
    #     print('Lambda Swpt: ', exp(lmbdSwpt))
    # else:
    #     print('xCeiling: ', xCeiling)
    #     print('Lambda Swpt: ', lmbdSwpt)
        
    return UML

def logit_sweetpoints(phi):

    def alphavar_est(x):

        term1 = exp(2*beta*(alpha-x))
        term2 = (1+exp(beta*(x-alpha)))**2
        term3 = -gamma+(lambdax-1)*exp(beta*(x-alpha))
        term4 = 1-gamma+lambdax*exp(beta*(x-alpha))
        term5 = beta**2*(-1+gamma+lambdax)**2

        sigmaalphasq = -term1*term2*term3*term4/term5

        return sigmaalphasq


    def betavar_est1(x):

        term1 = exp(2*beta*(alpha-x))
        term2 = (1+exp(beta*(x-alpha)))**2
        term3 = -gamma+(lambdax-1)*exp(beta*(x-alpha))
        term4 = 1-gamma+lambdax*exp(beta*(x-alpha))
        term5 = (x-alpha)**2*(-1+gamma+lambdax)**2

        sigmabetasq = (-term1*term2*term3*term4/term5) +(x>=alpha)*1e10

        return sigmabetasq

    def betavar_est2(x):

        term1 = exp(2*beta*(alpha-x))
        term2 = (1+exp(beta*(x-alpha)))**2
        term3 = -gamma+(lambdax-1)*exp(beta*(x-alpha))
        term4 = 1-gamma+lambdax*exp(beta*(x-alpha))
        term5 = (x-alpha)**2*(-1+gamma+lambdax)**2

        sigmabetasq = (-term1*term2*term3*term4/term5) +(x<=alpha)*1e10

        return sigmabetasq

    alpha = phi[0]
    beta = phi[1]
    gamma = phi[2]
    lambdax = phi[3]

    swpts = np.zeros(3)

    swpts[0] = scipy.optimize.fmin(betavar_est1, x0=alpha-10, disp=False)
    swpts[2] = scipy.optimize.fmin(betavar_est2, x0=alpha+10, disp=False)
    swpts[1] = scipy.optimize.fmin(alphavar_est, x0=alpha, disp=False)
    swpts.sort()

    return swpts



def weibull_sweetpoints(phi):

    k = phi[0]
    beta = phi[1]
    gamma = phi[2]
    lambdax = phi[3]

    def kvar_est(x):

        term1 = k**2*(x/k)**(-2*beta)
        term2 = -1+gamma-exp((x/k)**beta)*(-1+lambdax)+lambdax
        term3 = -1+gamma+lambdax-exp((x/k)**beta)*lambdax
        term4 = beta**2*(-1+gamma+lambdax)**2

        sigmaksq = -term1*term2*term3/term4
        return sigmaksq

    def betavar_est1(x):

        term1 = (x/k)**(-2*beta)
        term2 = -1+gamma-exp((x/k)**beta)*(-1+lambdax)+lambdax
        term3 = -1+gamma+lambdax-exp((x/k)**beta)*lambdax
        term4 = (-1+gamma+lambdax)**2*log(x/k)**2

        sigmabetasq = -term1*term2*term3/term4 + (x>=k)*1e10
        return sigmabetasq

    def betavar_est2(x):

        term1 = (x/k)**(-2*beta)
        term2 = -1+gamma-exp((x/k)**beta)*(-1+lambdax)+lambdax
        term3 = -1+gamma+lambdax-exp((x/k)**beta)*lambdax
        term4 = (-1+gamma+lambdax)**2*log(x/k)**2

        sigmabetasq = -term1*term2*term3/term4 + (x<=k)*1e10
        return sigmabetasq

    # swpts[0] = fminsearch(@(x) betavar_est(x,k,beta,gamma,lambdax)+(x>=k)*1e10,k/2,opt)
    # swpts[2] = fminsearch(@(x) betavar_est(x,k,beta,gamma,lambdax)+(x<=k)*1e10,k*2,opt)
    # swpts[1] = fminsearch(@(x) kvar_est(x,k,beta,gamma,lambdax),k,opt)
    
    swpts = np.zeros(3)
    swpts[0] = scipy.optimize.fmin(betavar_est1, x0=k/2, disp=False)
    swpts[2] = scipy.optimize.fmin(betavar_est2, x0=k*2, disp=False)
    swpts[1] = scipy.optimize.fmin(kvar_est, x0=k, disp=False)
    swpts = np.maximum(np.sort(swpts), 0)

    return swpts

def gaussian_sweetpoints(phi):
    
    def psycfunc(x, phi):
        mu = phi[0]
        sigma = phi[1]
        gamma = phi[2]
        lambdax = phi[3]
        p = gamma+((1-gamma-lambdax)/2)*(1+erf((x-mu)/sqrt(2*sigma**2)))
        return p

    def psycfunc_derivative_mu(x, phi):
        mu = phi[0]
        sigma = phi[1]
        gamma = phi[2]
        lambdax = phi[3]
        dpdm = -(1-gamma-lambdax)/(sqrt(2*pi)*sigma)*exp(-(x-mu)**2/(2*sigma**2))
        return dpdm

    def psycfunc_derivative_sigma(x, phi):
        mu = phi[0]
        sigma = phi[1]
        gamma = phi[2]
        lambdax = phi[3]
        dpds = -(1-gamma-lambdax)*(x-mu)/(sqrt(2*pi)*sigma**2)*exp(-(x-mu)**2/(2*sigma**2))
        return dpds

    #sigma2_mu = @(x) psycfunc(x,phi)*(1-psycfunc(x,phi))/ (psycfunc_derivative_mu(x,phi))**2
    
    #sigma2_sigma = @(x) psycfunc(x,phi)*(1-psycfunc(x,phi))/ (psycfunc_derivative_sigma(x,phi))**2

    def sigma2_mu(x):
        out = psycfunc(x, phi)*(1-psycfunc(x, phi))/ (psycfunc_derivative_mu(x, phi))**2
        return out
    def sigma2_sigma(x):
        out = psycfunc(x, phi)*(1-psycfunc(x, phi))/ (psycfunc_derivative_sigma(x, phi))**2
        return out
    
    # swpt_mu = fminsearch(sigma2_mu, phi(1))
    # swpt_sigma_L = fminsearch(sigma2_sigma, phi(1)-10)
    # swpt_sigma_H = fminsearch(sigma2_sigma, phi(1)+10)

    swpt_mu = scipy.optimize.fmin(sigma2_mu, x0=phi[0], disp=False)
    swpt_sigma_L = scipy.optimize.fmin(sigma2_sigma, x0=phi[0]-10, disp=False)
    swpt_sigma_H = scipy.optimize.fmin(sigma2_sigma, x0=phi[0]+10, disp=False)
    swpts = np.array([swpt_sigma_L, swpt_mu, swpt_sigma_H])

    return swpts
