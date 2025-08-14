clear
close all
clc
%% Translate channel file into readable txt file

cd('C:\Users\kiera\Documents\Unlimited_Home_Works\Internship2025\data\T1_test_dataset_data_brainstorm\')

id = '004';

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
res(:,1) = r{2};
res(:,2) = r{3};
res(:,3) = r{4};

%% load brainstorm coordinates

cd('C:\Users\kiera\Documents\Unlimited_Home_Works\Internship2025\data\post_processing\T1_65\coords_gt_output\')

fid = fopen(strcat('Hemisfer_',id,'_coords.txt'));
r = textscan(fid, '%n %n %n','delimiter',',');
fclose(fid);

target = [];
% res_labels = r{1};
target(:,1) = r{1};
target(:,2) = r{2};
target(:,3) = r{3};

%% load brainstorm coordinates

cd('C:\Users\kiera\Documents\Unlimited_Home_Works\Internship2025\data\post_processing\T1_65\icp_output\')

fid = fopen(strcat('after_sorting\ID_',id,'_sorted.txt'));
r = textscan(fid, '%n %n %n','delimiter',',');
fclose(fid);

icp = [];
icp(:,1) = r{1};
icp(:,2) = r{2};
icp(:,3) = r{3};

%% convert coordinate system
cd('C:\Users\kiera\Documents\Unlimited_Home_Works\Internship2025\data\post_processing\T1_65\brainstorm_mris\')

temp = load(strcat(id,'.mat'));

P = cs_convert(temp, 'scs', 'voxel', res);

cd('C:\Users\kiera\Documents\Unlimited_Home_Works\Internship2025\data\trans\after_convert\')

writematrix(P, strcat('ID_',id,'_converted.txt'))

%% mesh
icp_labels = ["TP10" "TP9" "FT10" "FT9" "TP8" "P8" "T8" "PO8" "O1" "O2" "PO7" "P7" "OZ" "TP7" "T7" "FT8" "FT7" "F8" "F7" "P6" "P5" "AF8" "CP6" "PO3" "PO4" "C6" "AF7" "POZ" "CP5" "FC6" "C5" "FP2" "F6" "FP1" "FC5" "FPZ" "F5" "P4" "P3" "CP4" "AF4" "C4" "P2" "AF3" "CP3" "FC4" "F4" "P1" "PZ" "C3" "F3" "FC3" "AFZ" "CP2" "CP1" "F2" "C2" "FC2" "CPZ" "F1" "C1" "FC1" "FZ" "CZ" "FCZ"];
icp_labels = icp_labels';

verts = test_mesh.Vertices;
verts(:,1) = verts(:,1);
verts(:,2) = verts(:,2);
verts_mod = cs_convert(temp, 'scs', 'voxel', verts);

PlotSurf(verts_mod, test_mesh.Faces, [.5 .5 .5]);

% mesh = boundary(verts_mod(:,1),verts_mod(:,2),verts_mod(:,3));
% trisurf(mesh,verts_mod(:,1),verts_mod(:,2),verts_mod(:,3),'FaceAlpha',0.3);
hold on;

plot3(P(:,1),P(:,2),P(:,3),'s','MarkerEdgeColor','red',...
    'MarkerFaceColor',[.6 .1 .1]);
plot3(target(:,1),target(:,2),target(:,3),'o','MarkerEdgeColor','yellow',...
    'MarkerFaceColor',[.2 .2 .2]); %,res(:,1),res(:,2),res(:,3),'g+'
% plot3(icp(:,1),icp(:,2),icp(:,3),'s','MarkerEdgeColor','cyan',...
%     'MarkerFaceColor',[.1 .6 .6]);
for n = 1:65
    % text(P(n,1),P(n,2),P(n,3),target_labels(n));
    text(target(n,1),target(n,2),target(n,3),icp_labels(n));
    text(P(n,1),P(n,2),P(n,3),res_labels(n));
end
axis('equal');
legend({'Scalp','Brainstorm','GT Point'}, 'Location', 'southwest', ...
        'FontSize', 15)
    
hold off;