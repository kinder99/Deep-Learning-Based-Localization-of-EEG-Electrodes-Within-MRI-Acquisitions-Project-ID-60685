clear
close all
clc
%% Translate channel file into readable txt file and adapt contents to current scale

cd('C:\Users\kiera\Documents\Unlimited_Home_Works\Internship2025\data\T1_test_dataset_data_brainstorm\')

name = 'ID_060';

channel = load(strcat(name, '\@intra\channel.mat'));
data = channel.Channel;

coords = [];
for i = 1:65
    dat = data(i).Loc * 1000;
    res = [ convertCharsToStrings(data(i).Name) dat' ];
    coords = [ coords; res ];
end

cd('C:\Users\kiera\Documents\Unlimited_Home_Works\Internship2025\data\trans\')

writematrix(coords,strcat(name,'.txt'))
%% compute transformation matrix using absor 

cd('C:\Users\kiera\Documents\Unlimited_Home_Works\Internship2025\data\trans\')

fid = fopen('template_positions.txt');
s = textscan(fid, '%s %n %n %n','delimiter',',');
fclose(fid);

sauce_labels = s{1};
sauce(:,1) = s{2};
sauce(:,2) = s{3};
sauce(:,3) = s{4};

fid = fopen('../EEG_template.txt');
t = textscan(fid, '%s %n %n %n','delimiter',',');
fclose(fid);

target_labels = t{1};
target(:,1) = t{2};
target(:,2) = t{3};
target(:,3) = t{4};

addpath 'C:\Users\kiera\Documents\Unlimited_Home_Works\Internship2025\data\code\matlab\Functions'

[ regParams, BFit, ErrorStats ] = absor(sauce', target', 'doScale', true, 'doTrans', true);
%% get subject data

cd('C:\Users\kiera\Documents\Unlimited_Home_Works\Internship2025\data\trans\')

fid = fopen(strcat('after_sorting/',name,'_sorted.txt'));
r = textscan(fid, '%s %n %n %n','delimiter',',');
fclose(fid);

res = [];
res_labels = r{1};
res(:,1) = r{2};
res(:,2) = r{3};
res(:,3) = r{4};

resed = regParams.R * res' + regParams.t;

resed = resed';
%% plot

plot3(resed(:,1),resed(:,2),resed(:,3),'bo',target(:,1),target(:,2),target(:,3),'r*');
for n = 1:65
    text(resed(n,1),resed(n,2),resed(n,3),res_labels(n));
    text(target(n,1),target(n,2),target(n,3),target_labels(n));
end
axis('equal');
legend({'ICP Point','Brainstorm Point'}, 'Location', 'southwest', ...
        'FontSize', 15)
%% saving

cd('C:\Users\kiera\Documents\Unlimited_Home_Works\Internship2025\data\trans\after_matrix\')

dlmwrite(strcat(name,'_sorted_trans.txt'), resed, ' ');
%% compute and save distances

dis = [];
for i = 1:65
    res_point = [resed(i,1) resed(i,2) resed(i,3)];
    tar_point = [target(i,1) target(i,2) target(i,3)];
    dis = [dis norm(res_point - tar_point)];
end
dis = dis';

cd('C:\Users\kiera\Documents\Unlimited_Home_Works\Internship2025\data\trans\distances\')

dlmwrite(strcat(name,'_distances.txt'),dis)