import sys, os
import numpy as np
from virtual_observer import*
sys.path.append(os.path.normpath('../../'))
from pychoacoustics.UML_method import*

rootPath = "../../../pychoacoustics_data/test_data/UML_method/results/"
np.random.seed(seed=54126)
runChecks = True
decimalTol = 3

ruleOpts = [2,3,4]

testN = 0
nTrials = 200
for ruleOpt in range(len(ruleOpts)):
     testN = testN+1
     UML = setupUML(model="Logistic",
                    swptRule="Up-Down",
                    nDown = ruleOpts[ruleOpt],
                    centTend = "Mean",
                    stimScale="Linear",
                    x0=0,
                    xLim=(-20, 20),
                    alphaLim=(-10,10),
                    alphaStep=1,
                    alphaSpacing="Linear",
                    alphaDist="Uniform",
                    alphaMu=0,
                    alphaSTD=20,
                    betaLim=(0.1,10),
                    betaStep=1.1,
                    betaSpacing="Logarithmic",
                    betaDist="Uniform",
                    betaMu=1,
                    betaSTD=2,
                    gamma=0.5,
                    lambdaLim=(0,0.2),
                    lambdaStep=0.01,
                    lambdaSpacing="Linear",
                    lambdaDist="Uniform",
                    lambdaMu=0,
                    lambdaSTD=0.1,
                    suggestedLambdaSwpt=20,
                    lambdaSwptPC=0.99)
     resps = np.zeros((nTrials))
     for i in range(nTrials):
          resp = virtualObserver(UML["xnext"], midpoint=0, slope=2, guess=0.5, lapse=0, funType="Logistic", funFit="Linear")
          resps[i] = resp
          UML = UML_update(UML, resp)


     np.savetxt(rootPath+'res_logistic_test'+str(testN)+'.txt', UML["phi"])
     np.savetxt(rootPath+'resp_logistic_test'+str(testN)+'.txt', resps)


for ruleOpt in range(len(ruleOpts)):
     testN = testN+1
     UML = setupUML(model="Logistic",
                    swptRule="Up-Down",
                    nDown = ruleOpts[ruleOpt],
                    centTend = "Mean",
                    stimScale="Logarithmic",
                    x0=20,
                    xLim=(0.05, 500),
                    alphaLim=(0.5,50),
                    alphaStep=1.1,
                    alphaSpacing="Linear",
                    alphaDist="Uniform",
                    alphaMu=0,
                    alphaSTD=20,
                    betaLim=(0.1,10),
                    betaStep=1.1,
                    betaSpacing="Logarithmic",
                    betaDist="Uniform",
                    betaMu=1,
                    betaSTD=2,
                    gamma=0.5,
                    lambdaLim=(0,0.2),
                    lambdaStep=0.01,
                    lambdaSpacing="Linear",
                    lambdaDist="Uniform",
                    lambdaMu=0,
                    lambdaSTD=0.1,
                    suggestedLambdaSwpt=500,
                    lambdaSwptPC=0.99)
     resps = np.zeros((nTrials))
     for i in range(nTrials):
          resp = virtualObserver(exp(UML["xnext"]), midpoint=log(5), slope=2, guess=0.5, lapse=0, funType="Logistic", funFit="Logarithmic")
          resps[i] = resp
          UML = UML_update(UML, resp)


     np.savetxt(rootPath+'res_logistic_test'+str(testN)+'.txt', UML["phi"])
     np.savetxt(rootPath+'resp_logistic_test'+str(testN)+'.txt', resps)


if runChecks == True:
     for i in range(testN):
          res_shen = np.loadtxt(rootPath+'res_shen_logistic_test'+str(i+1)+'.txt', delimiter=',')
          res_pyth = np.loadtxt(rootPath+'res_logistic_test'+str(i+1)+'.txt')
          np.testing.assert_almost_equal(res_pyth, res_shen, decimal=decimalTol)


