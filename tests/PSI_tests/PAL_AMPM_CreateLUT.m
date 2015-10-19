
%modified version of the same file from Palamedes to use slope on normal coordinates
function PFLookUpTable = PAL_AMPM_CreateLUT(priorAlphaValues, priorBetaValues, priorGammaValues, priorLambdaValues, StimLevels, PF, gammaEQlambda)
    
[a, b, g, l, x] = ndgrid(priorAlphaValues, priorBetaValues, priorGammaValues, priorLambdaValues, StimLevels);
params.alpha = a;
%params.beta = 10.^b;
params.beta = b;
params.gamma = g;
params.lambda = l;

if gammaEQlambda
    params.gamma = l;
end

PFLookUpTable = PF(params, x);