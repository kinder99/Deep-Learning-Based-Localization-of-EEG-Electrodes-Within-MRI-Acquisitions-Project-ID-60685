clear
close all
clc
%% Translate channel file into readable txt file

cd('C:\Users\kiera\Documents\Unlimited_Home_Works\Internship2025\data\T1_test_dataset_data_brainstorm\')

id = '039';

channel = load(strcat('ID_',id, '\@intra\channel.mat'));
data = channel.Channel;

coords = [];
for i = 1:65
    dat = data(i).Loc;
    res = [ convertCharsToStrings(data(i).Name) dat' ];
    coords = [ coords; res ];
end

cd('C:\Users\kiera\Documents\Unlimited_Home_Works\Internship2025\data\trans\')

writematrix(coords,strcat('ID_',id,'.txt'))
%% load brainstorm coordinates

cd('C:\Users\kiera\Documents\Unlimited_Home_Works\Internship2025\data\trans\')

fid = fopen(strcat('after_sorting/ID_',id,'_sorted.txt'));
r = textscan(fid, '%s %n %n %n','delimiter',',');
fclose(fid);

res = [];
res_labels = r{1};
res(:,1) = -r{2};
res(:,2) = -r{3};
res(:,3) = r{4};

%% convert coordinate system
cd('C:\Users\kiera\Documents\Unlimited_Home_Works\Internship2025\data\post_processing\T1_65\brainstorm_mris\')

temp = load(strcat(id,'.mat'));

P = cs_convert(temp, 'scs', 'voxel', res);

cd('C:\Users\kiera\Documents\Unlimited_Home_Works\Internship2025\data\trans\after_convert\')

writematrix(P, strcat('ID_',id,'_converted.txt'))

%% plotting

% plot3(P(:,1),P(:,2),P(:,3),'bo',target(:,1),target(:,2),target(:,3),'r*'); %,res(:,1),res(:,2),res(:,3),'g+'
% for n = 1:65
%     text(P(n,1),P(n,2),P(n,3),target_labels(n));
%     text(target(n,1),target(n,2),target(n,3),target_labels(n));
%     % text(res(n,1),res(n,2),res(n,3),res_labels(n));
% end
% axis('equal');
% legend({'Modified Brainstorm','ICP Point','Brainstorm Point'}, 'Location', 'southwest', ...
%         'FontSize', 15)