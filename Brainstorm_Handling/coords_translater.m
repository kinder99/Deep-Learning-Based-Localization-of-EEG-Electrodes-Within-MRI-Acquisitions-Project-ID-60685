clear
close all
clc

%% Translate channel file into readable txt file and adapt contents to current scale

cd('C:\Users\kiera\Documents\Unlimited_Home_Works\Internship2025\data\T1_test_dataset_data_brainstorm\')

name = 'ID_060';

channel = load(strcat(name, '\@intra\channel.mat'));
data = channel.Channel;

ID_060 = [];
for i = 1:65
    dat = data(i).Loc * 1000;
    res = [ convertCharsToStrings(data(i).Name) dat' ];
    ID_060 = [ ID_060; res ];
end

cd('C:\Users\kiera\Documents\Unlimited_Home_Works\Internship2025\data\trans\')

writematrix(ID_060)

% do it from templated brainstorm positions to nnunet useable coordinates

% best case for nnunet is the petra template so getting accurate brainstorm
% coordinates for it would be ideal

% absor could then compute the transformation matrix between the
% coordinates set which could then be used to transform the brainstorm
% dataset for validation
% 
% source = readmatrix(strcat(name,'.txt')); % template brainstorm positions
% source(:,1) = [];
% source = source';
% 
% trans = regParams.R * source + regParams.t;
% 
% cd('C:\Users\kiera\Documents\Unlimited_Home_Works\Internship2025\data\trans\after_matrix\')
% 
% trans = trans';
% 
% dlmwrite(strcat(name,'_trans.txt'), trans, ' ');

%% Write matrix

cd('C:\Users\kiera\Documents\Unlimited_Home_Works\Internship2025\data\trans\')

writematrix(ID_060)

% do it from templated brainstorm positions to nnunet useable coordinates

% best case for nnunet is the petra template so getting accurate brainstorm
% coordinates for it would be ideal

% absor could then compute the transformation matrix between the
% coordinates set which could then be used to transform the brainstorm
% dataaset for validation

source = readmatrix(strcat(name,'.txt')); % template brainstorm positions
source(:,1) = [];
source = source';

%% absor

cd('C:\Users\kiera\Documents\Unlimited_Home_Works\Internship2025\data\trans\')
sauce = readmatrix('template_positions.txt');
sauce(:,1) = [];
sauce = sauce';

target = readmatrix('../EEG_template.txt');
target(:,1) = [];
target = target';

% use absor to compute transformation matrix
addpath 'C:\Users\kiera\Documents\Unlimited_Home_Works\Internship2025\data\code\matlab\Functions'

% pay attention to template formatting, must be using commas as separators
% and also po*
[ regParams, BFit, ErrorStats ] = absor(sauce, target, 'doScale', true, 'doTrans', true);

%%

cd('C:\Users\kiera\Documents\Unlimited_Home_Works\Internship2025\data\trans\after_sorting\')

name = 'ID_060_sorted';

source = readmatrix(strcat(name,'.txt')); % template brainstorm positions
source(:,1) = [];
source = source';

trans = regParams.R * source + regParams.t;

cd('C:\Users\kiera\Documents\Unlimited_Home_Works\Internship2025\data\trans\after_matrix\')

trans = trans';

dlmwrite(strcat(name,'_trans.txt'), trans, ' ');

%%

cd ('C:\Users\kiera\Documents\Unlimited_Home_Works\Internship2025\data\')

icp = readmatrix('post_processing\T1_65\icp_output\Hemisfer_003_postprocessed_coord.txt');
brainstorm = readmatrix('trans\after_matrix\ID_003_sorted_trans.txt');

sauce = readmatrix('trans\ID_003.txt');
sauce(:,1) = [];
sauce = sauce';

sauced = regParams.R * sauce + regParams.t;

sauced = sauced';
target = target';

plot3(sauced(:,1),sauced(:,2),sauced(:,3),'bo',target(:,1),target(:,2),target(:,3),'r*');
axis('equal');
legend({'ICP Point','Brainstorm Point'}, 'Location', 'southwest', ...
        'FontSize', 15)
    
% [res, fit, err] = absor(brainstorm', icp', 'doScale', true, 'doTrans', true);
% 
% brainstorm_mod = res.R * brainstorm' + res.t;
% brainstorm_mod = brainstorm_mod';
% 
% plot3(icp(:,1),icp(:,2),icp(:,3),'bo',brainstorm_mod(:,1),brainstorm_mod(:,2),brainstorm_mod(:,3),'r*');
% axis('equal');
% legend({'ICP Point','Brainstorm Mod Point'}, 'Location', 'southwest', ...
%         'FontSize', 15)