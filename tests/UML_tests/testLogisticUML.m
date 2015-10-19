% 

%test logistic linear coordinates 
addpath(genpath('../../../UML_method/UML_ver2.2/')) 
rootPath = '../../../pychoacoustics_data/test_data/UML_method/results/';

%test 1
par.model = 'logit';
par.ndown = 2;  % the parameter for the up-down sweetpoint selection rule
par.method = 'mean';   
par.x0 = 0;    % the initial signal strength
par.x_lim = [-20 20];   % the limits to the signal strength

par.alpha = struct(...
    'limits',[-10 10],...       %range of the parameter space for alpha
    'N',21,...                %number of alpha values. If this value is set to 1, then the first element of alpha.limits would be the assumed alpha and the alpha parameter is not estimated.
    'scale','lin',...         %the linear or log spacing. Choose between 'lin' and 'log'.
    'dist','flat',...         %prior distribution of the alpha parameter. Choose between 'norm' and 'flat'.
    'mu',0,...                %mean of the prior distribution.
    'std',20 ...              %standard deviation of the prior distribution.  
    );

par.beta = struct(...
    'limits',[.1 9.70172338],...      %range of the parameter space for beta
    'N',49,...                %number of beta values. If this value is set to 1, then the first element of beta.limits would be the assumed beta and the beta parameter is not estimated.
    'scale','log',...         %the linear or log spacing. Choose between 'lin' and 'log'.
    'dist','flat',...         %prior distribution of the beta parameter. Choose between 'norm' and 'flat'.
    'mu',0,...                %mean of the prior distribution.
    'std',2 ...               %standard deviation of the prior distribution.
    );

par.gamma = 0.5;

par.lambda = struct(...
    'limits',[0 0.2],...      %range of the parameter space for lambda
    'N',21,...                 %number of lambda values. If this value is set to 1, then the first element of lambda.limits would be the assumed lambda and the lambda parameter is not estimated.
    'scale','lin',...         %the linear or log spacing. Choose between 'lin' and 'log'.
    'dist','flat',...         %prior distribution of the lambda parameter. Choose between 'norm' and 'flat'.
    'mu',0,...                %mean of the prior distribution.
    'std',0.1 ...             %standard deviation of the prior distribution.  
    );


resps = load(strcat(rootPath, 'resp_logistic_test1.txt'));
uml = UML(par);

for i=1:length(resps)
    uml.update(resps(i));
end

res = uml.phi;
dlmwrite(strcat(rootPath, 'res_shen_logistic_test1.txt'), res)


%test 2
par.model = 'logit';
par.ndown = 3;  % the parameter for the up-down sweetpoint selection rule
par.method = 'mean';   
par.x0 = 0;    % the initial signal strength
par.x_lim = [-20 20];   % the limits to the signal strength

par.alpha = struct(...
    'limits',[-10 10],...       %range of the parameter space for alpha
    'N',21,...                %number of alpha values. If this value is set to 1, then the first element of alpha.limits would be the assumed alpha and the alpha parameter is not estimated.
    'scale','lin',...         %the linear or log spacing. Choose between 'lin' and 'log'.
    'dist','flat',...         %prior distribution of the alpha parameter. Choose between 'norm' and 'flat'.
    'mu',0,...                %mean of the prior distribution.
    'std',20 ...              %standard deviation of the prior distribution.  
    );

par.beta = struct(...
    'limits',[.1 9.70172338],...      %range of the parameter space for beta
    'N',49,...                %number of beta values. If this value is set to 1, then the first element of beta.limits would be the assumed beta and the beta parameter is not estimated.
    'scale','log',...         %the linear or log spacing. Choose between 'lin' and 'log'.
    'dist','flat',...         %prior distribution of the beta parameter. Choose between 'norm' and 'flat'.
    'mu',0,...                %mean of the prior distribution.
    'std',2 ...               %standard deviation of the prior distribution.
    );

par.gamma = 0.5;

par.lambda = struct(...
    'limits',[0 0.2],...      %range of the parameter space for lambda
    'N',21,...                 %number of lambda values. If this value is set to 1, then the first element of lambda.limits would be the assumed lambda and the lambda parameter is not estimated.
    'scale','lin',...         %the linear or log spacing. Choose between 'lin' and 'log'.
    'dist','flat',...         %prior distribution of the lambda parameter. Choose between 'norm' and 'flat'.
    'mu',0,...                %mean of the prior distribution.
    'std',0.1 ...             %standard deviation of the prior distribution.  
    );


resps = load(strcat(rootPath, 'resp_logistic_test2.txt'));
uml = UML(par);

for i=1:length(resps)
    uml.update(resps(i));
end

res = uml.phi;
dlmwrite(strcat(rootPath, 'res_shen_logistic_test2.txt'), res)


%test 3
par.model = 'logit';
par.ndown = 4;  % the parameter for the up-down sweetpoint selection rule
par.method = 'mean';   
par.x0 = 0;    % the initial signal strength
par.x_lim = [-20 20];   % the limits to the signal strength

par.alpha = struct(...
    'limits',[-10 10],...       %range of the parameter space for alpha
    'N',21,...                %number of alpha values. If this value is set to 1, then the first element of alpha.limits would be the assumed alpha and the alpha parameter is not estimated.
    'scale','lin',...         %the linear or log spacing. Choose between 'lin' and 'log'.
    'dist','flat',...         %prior distribution of the alpha parameter. Choose between 'norm' and 'flat'.
    'mu',0,...                %mean of the prior distribution.
    'std',20 ...              %standard deviation of the prior distribution.  
    );

par.beta = struct(...
    'limits',[.1 9.70172338],...      %range of the parameter space for beta
    'N',49,...                %number of beta values. If this value is set to 1, then the first element of beta.limits would be the assumed beta and the beta parameter is not estimated.
    'scale','log',...         %the linear or log spacing. Choose between 'lin' and 'log'.
    'dist','flat',...         %prior distribution of the beta parameter. Choose between 'norm' and 'flat'.
    'mu',0,...                %mean of the prior distribution.
    'std',2 ...               %standard deviation of the prior distribution.
    );

par.gamma = 0.5;

par.lambda = struct(...
    'limits',[0 0.2],...      %range of the parameter space for lambda
    'N',21,...                 %number of lambda values. If this value is set to 1, then the first element of lambda.limits would be the assumed lambda and the lambda parameter is not estimated.
    'scale','lin',...         %the linear or log spacing. Choose between 'lin' and 'log'.
    'dist','flat',...         %prior distribution of the lambda parameter. Choose between 'norm' and 'flat'.
    'mu',0,...                %mean of the prior distribution.
    'std',0.1 ...             %standard deviation of the prior distribution.  
    );


resps = load(strcat(rootPath, 'resp_logistic_test3.txt'));
uml = UML(par);

for i=1:length(resps)
    uml.update(resps(i));
end

res = uml.phi;
dlmwrite(strcat(rootPath, 'res_shen_logistic_test3.txt'), res)


%test 4
par.model = 'logit';
par.ndown = 2;  % the parameter for the up-down sweetpoint selection rule
par.method = 'mean';   
par.x0 = log(20);    % the initial signal strength
par.x_lim = [log(0.05) log(500)];   % the limits to the signal strength

par.alpha = struct(...
    'limits', [log(0.5) log(53.359478589578345)],...       %range of the parameter space for alpha
    'N',50,...                %number of alpha values. If this value is set to 1, then the first element of alpha.limits would be the assumed alpha and the alpha parameter is not estimated.
    'scale','lin',...         %the linear or log spacing. Choose between 'lin' and 'log'.
    'dist','flat',...         %prior distribution of the alpha parameter. Choose between 'norm' and 'flat'.
    'mu',0,...                %mean of the prior distribution.
    'std',20 ...              %standard deviation of the prior distribution.  
    );

par.beta = struct(...
    'limits',[.1 9.70172338],...      %range of the parameter space for beta
    'N',49,...                %number of beta values. If this value is set to 1, then the first element of beta.limits would be the assumed beta and the beta parameter is not estimated.
    'scale','log',...         %the linear or log spacing. Choose between 'lin' and 'log'.
    'dist','flat',...         %prior distribution of the beta parameter. Choose between 'norm' and 'flat'.
    'mu',0,...                %mean of the prior distribution.
    'std',2 ...               %standard deviation of the prior distribution.
    );

par.gamma = 0.5;

par.lambda = struct(...
    'limits',[0 0.2],...      %range of the parameter space for lambda
    'N',21,...                 %number of lambda values. If this value is set to 1, then the first element of lambda.limits would be the assumed lambda and the lambda parameter is not estimated.
    'scale','lin',...         %the linear or log spacing. Choose between 'lin' and 'log'.
    'dist','flat',...         %prior distribution of the lambda parameter. Choose between 'norm' and 'flat'.
    'mu',0,...                %mean of the prior distribution.
    'std',0.1 ...             %standard deviation of the prior distribution.  
    );


resps = load(strcat(rootPath, 'resp_logistic_test4.txt'));
uml = UML(par);

for i=1:length(resps)
    uml.update(resps(i));
end

res = uml.phi;
dlmwrite(strcat(rootPath, 'res_shen_logistic_test4.txt'), res)

%test 5
par.model = 'logit';
par.ndown = 3;  % the parameter for the up-down sweetpoint selection rule
par.method = 'mean';   
par.x0 = log(20);    % the initial signal strength
par.x_lim = [log(0.05) log(500)];   % the limits to the signal strength

par.alpha = struct(...
    'limits', [log(0.5) log(53.359478589578345)],...       %range of the parameter space for alpha
    'N',50,...                %number of alpha values. If this value is set to 1, then the first element of alpha.limits would be the assumed alpha and the alpha parameter is not estimated.
    'scale','lin',...         %the linear or log spacing. Choose between 'lin' and 'log'.
    'dist','flat',...         %prior distribution of the alpha parameter. Choose between 'norm' and 'flat'.
    'mu',0,...                %mean of the prior distribution.
    'std',20 ...              %standard deviation of the prior distribution.  
    );

par.beta = struct(...
    'limits',[.1 9.70172338],...      %range of the parameter space for beta
    'N',49,...                %number of beta values. If this value is set to 1, then the first element of beta.limits would be the assumed beta and the beta parameter is not estimated.
    'scale','log',...         %the linear or log spacing. Choose between 'lin' and 'log'.
    'dist','flat',...         %prior distribution of the beta parameter. Choose between 'norm' and 'flat'.
    'mu',0,...                %mean of the prior distribution.
    'std',2 ...               %standard deviation of the prior distribution.
    );

par.gamma = 0.5;

par.lambda = struct(...
    'limits',[0 0.2],...      %range of the parameter space for lambda
    'N',21,...                 %number of lambda values. If this value is set to 1, then the first element of lambda.limits would be the assumed lambda and the lambda parameter is not estimated.
    'scale','lin',...         %the linear or log spacing. Choose between 'lin' and 'log'.
    'dist','flat',...         %prior distribution of the lambda parameter. Choose between 'norm' and 'flat'.
    'mu',0,...                %mean of the prior distribution.
    'std',0.1 ...             %standard deviation of the prior distribution.  
    );


resps = load(strcat(rootPath, 'resp_logistic_test5.txt'));
uml = UML(par);

for i=1:length(resps)
    uml.update(resps(i));
end

res = uml.phi;
dlmwrite(strcat(rootPath, 'res_shen_logistic_test5.txt'), res)


%test 6
par.model = 'logit';
par.ndown = 4;  % the parameter for the up-down sweetpoint selection rule
par.method = 'mean';   
par.x0 = log(20);    % the initial signal strength
par.x_lim = [log(0.05) log(500)];   % the limits to the signal strength

par.alpha = struct(...
    'limits', [log(0.5) log(53.359478589578345)],...       %range of the parameter space for alpha
    'N',50,...                %number of alpha values. If this value is set to 1, then the first element of alpha.limits would be the assumed alpha and the alpha parameter is not estimated.
    'scale','lin',...         %the linear or log spacing. Choose between 'lin' and 'log'.
    'dist','flat',...         %prior distribution of the alpha parameter. Choose between 'norm' and 'flat'.
    'mu',0,...                %mean of the prior distribution.
    'std',20 ...              %standard deviation of the prior distribution.  
    );

par.beta = struct(...
    'limits',[.1 9.70172338],...      %range of the parameter space for beta
    'N',49,...                %number of beta values. If this value is set to 1, then the first element of beta.limits would be the assumed beta and the beta parameter is not estimated.
    'scale','log',...         %the linear or log spacing. Choose between 'lin' and 'log'.
    'dist','flat',...         %prior distribution of the beta parameter. Choose between 'norm' and 'flat'.
    'mu',0,...                %mean of the prior distribution.
    'std',2 ...               %standard deviation of the prior distribution.
    );

par.gamma = 0.5;

par.lambda = struct(...
    'limits',[0 0.2],...      %range of the parameter space for lambda
    'N',21,...                 %number of lambda values. If this value is set to 1, then the first element of lambda.limits would be the assumed lambda and the lambda parameter is not estimated.
    'scale','lin',...         %the linear or log spacing. Choose between 'lin' and 'log'.
    'dist','flat',...         %prior distribution of the lambda parameter. Choose between 'norm' and 'flat'.
    'mu',0,...                %mean of the prior distribution.
    'std',0.1 ...             %standard deviation of the prior distribution.  
    );


resps = load(strcat(rootPath, 'resp_logistic_test6.txt'));
uml = UML(par);

for i=1:length(resps)
    uml.update(resps(i));
end

res = uml.phi;
dlmwrite(strcat(rootPath, 'res_shen_logistic_test6.txt'), res)

