import sys, os
import numpy as np
from virtual_observer import*
sys.path.append(os.path.normpath('../../'))
from pychoacoustics.PSI_method2 import*
import time
t1 = time.time()
rootPath = "../../../pychoacoustics_data/test_data/PSI_method/results/"
np.random.seed(seed=837849)
runChecks = True
decimalTol = 3

marginalize_opts = [None, tuple(np.array([0])), tuple(np.array([1])), tuple(np.array([2])), tuple(np.array([1,2]))]

testN = 0
nTrials = 200
for margOpt in range(len(marginalize_opts)):
     testN = testN+1
     PSI = setupPSI(model="Logistic", stimScale="Linear", x0=None, xLim=(-20, 20), xStep=1, 
                  alphaLim=(-10,10), alphaStep=1, alphaSpacing="Linear", alphaDist="Uniform", alphaMu=0, alphaSTD=20,
                  betaLim=(0.1,10), betaStep=1.1, betaSpacing="Logarithmic", betaDist="Uniform", betaMu=1, betaSTD=2,
                  gamma=0.5,
                  lambdaLim=(0,0.2), lambdaStep=0.01, lambdaSpacing="Linear", lambdaDist="Uniform", lambdaMu=0, lambdaSTD=0.1,
                    marginalize = marginalize_opts[margOpt])
     resps = np.zeros((nTrials))
     for i in range(nTrials):
          resp = virtualObserver(PSI["xnext"], midpoint=0, slope=2, guess=0.5, lapse=0, funType="Logistic", funFit="Linear")
          resps[i] = resp
          PSI = PSI_update(PSI, resp)


     np.savetxt(rootPath+'res_logistic_test'+str(testN)+'.txt', PSI["phi"])
     np.savetxt(rootPath+'resp_logistic_test'+str(testN)+'.txt', resps)

for margOpt in range(len(marginalize_opts)):
     testN = testN+1
     PSI = setupPSI(model="Logistic", stimScale="Logarithmic", x0=None, xLim=(0.05,500), xStep=1.2, 
                  alphaLim=(0.5,50), alphaStep=1.2, alphaSpacing="Linear", alphaDist="Uniform", alphaMu=1, alphaSTD=20,
                  betaLim=(0.1,10), betaStep=1.1, betaSpacing="Logarithmic", betaDist="Uniform", betaMu=1, betaSTD=2,
                  gamma=0.5,
                  lambdaLim=(0,0.2), lambdaStep=0.01, lambdaSpacing="Linear", lambdaDist="Uniform", lambdaMu=0, lambdaSTD=0.1,
                    marginalize = marginalize_opts[margOpt])
     resps = np.zeros((nTrials))
     for i in range(nTrials):
          resp = virtualObserver(exp(PSI["xnext"]), midpoint=log(5), slope=2, guess=0.5, lapse=0, funType="Logistic", funFit="Logarithmic")
          resps[i] = resp
          PSI = PSI_update(PSI, resp)

     PSI["phi"][:,0] = np.exp(PSI["phi"][:,0])
     np.savetxt(rootPath+'res_logistic_test'+str(testN)+'.txt', PSI["phi"])
     np.savetxt(rootPath+'resp_logistic_test'+str(testN)+'.txt', resps)

if runChecks == True:
     for i in range(testN):
          res_pal = np.loadtxt(rootPath+'res_pal_logistic_test'+str(i+1)+'.txt', delimiter=',')
          res_pyth = np.loadtxt(rootPath+'res_logistic_test'+str(i+1)+'.txt')
          np.testing.assert_almost_equal(res_pyth, res_pal, decimal=decimalTol)


t2 = time.time()
print(t2-t1)
