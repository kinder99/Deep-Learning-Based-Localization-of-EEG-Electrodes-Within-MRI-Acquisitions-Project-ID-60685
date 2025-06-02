% USAGE : Adapt paths until *** END USAGE *** 

% Add the path where libs are
addpath C:\Users\User\Desktop\Stage_Caroline\TED\Code\Matlab\Librairies\NIfTI_Librairy
 
% Include the path where your functions are
addpath C:\Users\User\Desktop\Stage_Caroline\TED\Code\Matlab\Functions

%% Creation of the template EEG cap

% TEMPLATE
filename = 'C:\Users\User\Desktop\Stage_Caroline\TED\Results_Predictions\Post-Processed\template_petra.txt';
delimiterIn = ' ';
headerlinesIn = 0;
pt_templ = importdata(filename, delimiterIn, headerlinesIn);
pt_templ_untouched = importdata(filename, delimiterIn, headerlinesIn);


%% Loading of the detected coordinates

% PETRA 
nii = load_untouch_nii('C:\Users\User\Desktop\Stage_Caroline\TED\Data\UTE\S_8\15K\rUTE.nii');

% PRED Coordinates (from coord.py or any other extractor)
filename = 'C:\Users\User\Desktop\Stage_Caroline\TED\Results_Predictions\Brut\Pred_UTE_V2\Hemisfer_120_coord.txt';
delimiterIn = ' ';
headerlinesIn = 0;
pt_detec = importdata(filename,delimiterIn,headerlinesIn);

scoord = 'Hemisfer_120_postprocessed_coord.txt'; % optional : name
s = 'Hemisfer_120_postprocessed.nii'; % optional : name

% OUTPUT PATH
%cd('C:\Users\User\Desktop\Stage_Caroline\TED\Results_Predictions\Post-Processed\PostProcessed_UTE_V2\');
cd('C:\Users\User\Desktop\');

%*** END USAGE *** 

figure
    %subplot(211)
    plot3(pt_detec(:,1),pt_detec(:,2),pt_detec(:,3),'bo',pt_templ(:,1),pt_templ(:,2),pt_templ(:,3),'r*');
    axis('equal');
    legend({'Detected Point','Template Point'}, 'Location', 'southwest', ...
        'FontSize', 15)
    title('Coord' ,'FontSize',18,...      %Titre du tracé
           'FontWeight','bold','FontName',...
           'Times New Roman','Color','k')

%% Suppr obvious outliers at the border of the image

index_list = [];

for index = 1:size(pt_detec,1)
    if (pt_detec(index,1) < 15) || (pt_detec(index,2) < 15) || (pt_detec(index,3) < 15) || (pt_detec(index,1) > 305) || (pt_detec(index,2) > 305) || (pt_detec(index,3) > 305)
        index_list = [index_list,index];
    end
end

for index2 = 1:size(index_list,1)
    pt_detec(index_list,:) = [];
end

%%
%% Method 1 : too much detected coordinates
%%

if size(pt_detec,1) >= 65
    
    disp('Method 1')
    %% ICP

    %[pt_recal , ~ ] = ICP_affine(pt_detec, pt_templ,1000,100);
    
    pt_templ_ptcloud = pointCloud(pt_templ);
    pt_detec_ptcloud = pointCloud(pt_detec);
    error = 1000;
                    
    for x = -50:10:50
        for y = -50:10:50
            for z = -50:10:50
                    M = [1, 0, 0, 0;
                        0, 1, 0, 0;
                        0, 0, 1, 0;
                        x, y, z, 1];
                    tform_init = affine3d(M);
                    [tform,pt_recal_ptcloud,rmse] = pcregistericp(pt_templ_ptcloud,pt_detec_ptcloud,'MaxIterations',100,'InitialTransform',tform_init);
                    if (rmse < error)
                        error = rmse;
                        pt_recal = pt_recal_ptcloud.Location; 
                        best_tform = tform;
                        disp('Best ICP1 :')
                        disp(rmse)
                    end  
            end
        end
    end

    figure
    %subplot(211)
    plot3(pt_detec(:,1),pt_detec(:,2),pt_detec(:,3),'bo',pt_recal(:,1),pt_recal(:,2),pt_recal(:,3),'r*');
    axis('equal');
    legend({'Detected Point','Template Point'}, 'Location', 'southwest', ...
        'FontSize', 15)
    title('ICP 1' ,'FontSize',18,...      %Titre du tracé
           'FontWeight','bold','FontName',...
           'Times New Roman','Color','k')
   
   
    %% Remove false positives

    pt_detec2 = [];

    for i = 1:size(pt_recal,1)

        max_dist = 1000;

        % For each template electrode, associate the closest point from the detected
        for j = 1:size(pt_detec,1)
            if ( abs(pt_recal(i,1)-pt_detec(j,1)) + abs(pt_recal(i,2)-pt_detec(j,2)) + abs(pt_recal(i,3)-pt_detec(j,3)) < max_dist )
                max_dist = sqrt((pt_recal(i,1)-pt_detec(j,1)).^2 + (pt_recal(i,2)-pt_detec(j,2)).^2 + (pt_recal(i,3)-pt_detec(j,3)).^2);
                closest_recal = j;
                
            end
        end

        % Add the associated point in order to keep only the complementary points
        if (max_dist*0.9375) < 15
            pt_detec2 = [pt_detec2;pt_detec(closest_recal,:)];
        end

    end

    figure
    %subplot(211)
    plot3(pt_detec2(:,1),pt_detec2(:,2),pt_detec2(:,3),'bo');
    axis('equal');
    legend({'Detected Point','Template Point'}, 'Location', 'southwest', ...
        'FontSize', 15)
    title('Remove false positives ' ,'FontSize',18,...      %Titre du tracé
           'FontWeight','bold','FontName',...
           'Times New Roman','Color','k')
   
    %% ICP 2

    %[pt_recal , ~ ] = ICP_affine(pt_detec2, pt_templ,1000,100);
    
    pt_templ_ptcloud = pointCloud(pt_templ);
    pt_detec_ptcloud = pointCloud(pt_detec2);
    error = 1000;
                    
    for x = -50:10:50
        for y = -50:10:50
            for z = -50:10:50
                    M = [1, 0, 0, 0;
                        0, 1, 0, 0;
                        0, 0, 1, 0;
                        x, y, z, 1];
                    tform_init = affine3d(M);
                    [tform,pt_recal_ptcloud,rmse] = pcregistericp(pt_templ_ptcloud,pt_detec_ptcloud,'MaxIterations',100,'InitialTransform',tform_init);
                    if (rmse < error)
                        error = rmse;
                        pt_recal = pt_recal_ptcloud.Location; 
                        best_tform = tform;
                        disp('Best ICP2 :')
                        disp(rmse)
                    end  
            end
        end
    end

    figure
    %subplot(211)
    plot3(pt_detec2(:,1),pt_detec2(:,2),pt_detec2(:,3),'bo',pt_recal(:,1),pt_recal(:,2),pt_recal(:,3),'r*');
    axis('equal');
    legend({'Detected Point','Template Point'}, 'Location', 'southwest', ...
        'FontSize', 15)
    title('ICP 2 ' ,'FontSize',18,...      %Titre du tracé
           'FontWeight','bold','FontName',...
           'Times New Roman','Color','k')

   
    %% Add to the detected points the coordinates from the template when missing

    for i = 1:size(pt_detec2,1)
        
        max_dist = 1000;

        % For each detected electrode, associate the closest point from the template
        for j = 1:size(pt_recal,1)
            if ( abs(pt_detec2(i,1)-pt_recal(j,1)) + abs(pt_detec2(i,2)-pt_recal(j,2)) + abs(pt_detec2(i,3)-pt_recal(j,3)) < max_dist )
                max_dist = sqrt((pt_detec2(i,1)-pt_recal(j,1)).^2 + (pt_detec2(i,2)-pt_recal(j,2)).^2 + (pt_detec2(i,3)-pt_recal(j,3)).^2);
                closest_recal = j;
                
            end
        end
        % Suppr the associated point in order to keep only the complementary points
        pt_recal(closest_recal,:) = [];

    end

    % Final positions for the 65 electrodes
    pt_detec2 = [pt_detec2;pt_recal];

    figure
    %subplot(211)
    plot3(pt_detec2(:,1),pt_detec2(:,2),pt_detec2(:,3),'bo',pt_recal(:,1),pt_recal(:,2),pt_recal(:,3),'r.');
    axis('equal');
    legend({'Detected Point','Template Point'}, 'Location', 'southwest', ...
        'FontSize', 15)
    title('Add the missing electrodes ' ,'FontSize',18,...      %Titre du tracé
           'FontWeight','bold','FontName',...
           'Times New Roman','Color','k')
    
%%
%% Method 2 : not enough detected coordinates
%%
else
    disp('Method 2')
    %% ICP

%     [pt_recal , ~ ] = ICP_affine(pt_templ, pt_detec,1000,100);

%     T = [0.997019266142096, 0.0641697552888403, -0.0428348625263036, 0;
%         -0.0510697800502303, 0.965053880648330, 0.257027012220933, 0;
%         0.0578313107848861, -0.254073316095510, 0.965454447160058, 0;
%         -4.91579192234647, 56.3198125280031, -39.5718399834604, 1];
% 
% 
%     M = [1, 0, 0, 0;
%         0, 1, 0, 0;
%         0, 0, 1, 0;
%         0, 0, -20, 1];
%     
%     tform_init = affine3d(M);
%     
%     pt_recal = movepoints(M',pt_detec);
%     
%     figure
%     %subplot(211)
%     plot3(pt_recal(:,1),pt_recal(:,2),pt_recal(:,3),'bo',pt_templ(:,1),pt_templ(:,2),pt_templ(:,3),'r.');
%     axis('equal');
%     legend({'Detected Point','Template Point'}, 'Location', 'southwest', ...
%         'FontSize', 15)
%     title('ICP 1' ,'FontSize',18,...      %Titre du tracé
%            'FontWeight','bold','FontName',...
%            'Times New Roman','Color','k')
    pt_templ_ptcloud = pointCloud(pt_templ);
    pt_detec_ptcloud = pointCloud(pt_detec);
    error = 1000;
                    
    for x = -50:10:50
        for y = -50:10:50
            for z = -50:10:50
                    M = [1, 0, 0, 0;
                        0, 1, 0, 0;
                        0, 0, 1, 0;
                        x, y, z, 1];
                    tform_init = affine3d(M);
                    [tform,pt_recal_ptcloud,rmse] = pcregistericp(pt_detec_ptcloud,pt_templ_ptcloud,'MaxIterations',100,'InitialTransform',tform_init);
                    if (rmse < error)
                        error = rmse;
                        pt_recal = pt_recal_ptcloud.Location; 
                        best_tform = tform;
                        disp('Best ICP1 :')
                        disp(rmse)
                    end  
                    %disp('ICP1 :')
                    %disp(rmse)
            end
        end
    end

%     pt_templ_ptcloud = pointCloud(pt_templ);
%     pt_detec_ptcloud = pointCloud(pt_detec);
%     [tform,pt_recal_ptcloud,rmse] = pcregistericp(pt_detec_ptcloud,pt_templ_ptcloud,'MaxIterations',100,'InitialTransform',tform_init);
%     pt_recal = pt_recal_ptcloud.Location;    
%     disp('ICP1 :')
%     disp(rmse)
    
    figure
    %subplot(211)
    plot3(pt_recal(:,1),pt_recal(:,2),pt_recal(:,3),'bo',pt_templ(:,1),pt_templ(:,2),pt_templ(:,3),'r.');
    axis('equal');
    legend({'Detected Point','Template Point'}, 'Location', 'southwest', ...
        'FontSize', 15)
    title('ICP 1' ,'FontSize',18,...      %Titre du tracé
           'FontWeight','bold','FontName',...
           'Times New Roman','Color','k')
       
    %% Compute the rotation matrix

    pt_detec_absor = transpose(pt_detec);
    pt_recal_absor = transpose(pt_recal);

    [regParams , Bfit , ErrorStats] = absor(pt_recal_absor,pt_detec_absor, 'doScale', true, 'doTrans', true);

%     disp('R :')
%     disp(regParams.R)
%     disp('t :')
%     disp(regParams.t)
%     disp('s :')
%     disp(regParams.s)

    Rotation = regParams.R;
    Translation = regParams.t;
    Scale = regParams.s;
      
    %% Remove false positives

    pt_detec2 = [];

    for i = 1:size(pt_templ,1)

        max_dist = 1000;

        % For each template electrode, associate the closest point from the detected
        for j = 1:size(pt_recal,1)
            if ( abs(pt_templ(i,1)-pt_recal(j,1)) + abs(pt_templ(i,2)-pt_recal(j,2)) + abs(pt_templ(i,3)-pt_recal(j,3)) < max_dist )
                max_dist = sqrt((pt_templ(i,1)-pt_recal(j,1)).^2 + (pt_templ(i,2)-pt_recal(j,2)).^2 + (pt_templ(i,3)-pt_recal(j,3)).^2);
                closest_recal = j;
                
            end
        end

        % Add the associated point in order to keep only the complementary points
        if (max_dist*0.9375) < 20
            pt_detec2 = [pt_detec2;pt_recal(closest_recal,:)];
        end

    end

    figure
    %subplot(211)
    plot3(pt_detec2(:,1),pt_detec2(:,2),pt_detec2(:,3),'bo',pt_templ(:,1),pt_templ(:,2),pt_templ(:,3),'r.');
    axis('equal');
    legend({'Detected Point','Template Point'}, 'Location', 'southwest', ...
        'FontSize', 15)
    title('Remove false positives ' ,'FontSize',18,...      %Titre du tracé
           'FontWeight','bold','FontName',...
           'Times New Roman','Color','k')
       
%% ICP 2

%     [pt_recal , ~ ] = ICP_affine(pt_templ, pt_detec2,1000,100);
%     pt_templ_ptcloud = pointCloud(pt_templ);
%     pt_detec_ptcloud = pointCloud(pt_detec2);
%     [tform,pt_recal_ptcloud,rmse] = pcregistericp(pt_detec_ptcloud,pt_templ_ptcloud);
%     pt_recal = pt_recal_ptcloud.Location;
%     disp('ICP2 :')
%     disp(rmse)
    
    pt_templ_ptcloud = pointCloud(pt_templ);
    pt_detec_ptcloud = pointCloud(pt_detec2);
    error = 1000;
                    
    for x = -50:10:50
        for y = -50:10:50
            for z = -50:10:50
                    M = [1, 0, 0, 0;
                        0, 1, 0, 0;
                        0, 0, 1, 0;
                        x, y, z, 1];
                    tform_init = affine3d(M);
                    [tform,pt_recal_ptcloud,rmse] = pcregistericp(pt_detec_ptcloud,pt_templ_ptcloud,'MaxIterations',100,'InitialTransform',tform_init);
                    if (rmse < error)
                        error = rmse;
                        pt_recal = pt_recal_ptcloud.Location; 
                        best_tform = tform;
                        disp('Best ICP2 :')
                        disp(rmse)
                    end  
            end
        end
    end
    
    figure
    %subplot(211)
    plot3(pt_recal(:,1),pt_recal(:,2),pt_recal(:,3),'bo',pt_templ(:,1),pt_templ(:,2),pt_templ(:,3),'r.');
    axis('equal');
    legend({'Detected Point','Template Point'}, 'Location', 'southwest', ...
        'FontSize', 15)
    title('ICP 2 ' ,'FontSize',18,...      %Titre du tracé
           'FontWeight','bold','FontName',...
           'Times New Roman','Color','k')
       
%% Compute the rotation matrix 2

    pt_detec_absor2 = transpose(pt_detec2);
    pt_recal_absor2 = transpose(pt_recal);

    [regParams2 , Bfit2 , ErrorStats2] = absor(pt_recal_absor2,pt_detec_absor2, 'doScale', true, 'doTrans', true);

%     disp('R :')
%     disp(regParams2.R)
%     disp('t :')
%     disp(regParams2.t)
%     disp('s :')
%     disp(regParams2.s)

    Rotation2 = regParams2.R;
    Translation2 = regParams2.t;
    Scale2 = regParams2.s;
    
    pt_detec2 = pt_recal;
       
    %% Add to the detected points the coordinates from the template when missing

    for i = 1:size(pt_detec2,1)

        max_dist = 1000;

        % For each detected electrode, associate the closest point from the template
        for j = 1:size(pt_templ,1)
            if ( abs(pt_detec2(i,1)-pt_templ(j,1)) + abs(pt_detec2(i,2)-pt_templ(j,2)) + abs(pt_detec2(i,3)-pt_templ(j,3)) < max_dist )
                max_dist = sqrt((pt_detec2(i,1)-pt_templ(j,1)).^2 + (pt_detec2(i,2)-pt_templ(j,2)).^2 + (pt_detec2(i,3)-pt_templ(j,3)).^2);
                closest_recal = j;
               
            end
        end
        % Suppr the associated point in order to keep only the complementary points
        pt_templ(closest_recal,:) = [];

    end

    % Final positions for the 65 electrodes
    pt_detec2 = [pt_detec2;pt_templ];

    figure
    %subplot(211)
    plot3(pt_detec2(:,1),pt_detec2(:,2),pt_detec2(:,3),'bo',pt_templ(:,1),pt_templ(:,2),pt_templ(:,3),'r.');
    axis('equal');
    legend({'Detected Point','Template Point'}, 'Location', 'southwest', ...
        'FontSize', 15)
    title('Add missing electrodes ' ,'FontSize',18,...      %Titre du tracé
           'FontWeight','bold','FontName',...
           'Times New Roman','Color','k')
       
    %% ICP INVERSE
    
    M2 = creation_mat_transformation(Scale2*Rotation2 , Translation2);

    pt_detec2 = movepoints(M2,pt_detec2);

    M = creation_mat_transformation(Scale*Rotation , Translation);

    pt_detec2 = movepoints(M,pt_detec2);

    figure
    %subplot(211)
    plot3(pt_detec2(:,1),pt_detec2(:,2),pt_detec2(:,3),'bo',pt_detec(:,1),pt_detec(:,2),pt_detec(:,3),'r.');
    axis('equal');
    legend({'Detected Point','Template Point'}, 'Location', 'southwest', ...
        'FontSize', 15)
    title('Move to original coordinates' ,'FontSize',18,...      %Titre du tracé
           'FontWeight','bold','FontName',...
           'Times New Roman','Color','k')
    
end
    
    

%% Save

%cd('C:\Users\User\Desktop\Stage_Caroline\TED\Results_Predictions\Post-Processed\PostProcessed_UTE_V3\');
disp('Sauvegarde des coordonn�es');
dlmwrite(scoord,pt_detec2)

%% Sort electrodes for labeling

%[pt_templ_label , ~ ] = ICP_affine(pt_detec2, pt_templ_untouched,1000,100);

    pt_templ_ptcloud = pointCloud(pt_templ_untouched);
    pt_detec_ptcloud = pointCloud(pt_detec2);
    error = 1000;
                    
    for x = -50:10:50
        for y = -50:10:50
            for z = -50:10:50
                    M = [1, 0, 0, 0;
                        0, 1, 0, 0;
                        0, 0, 1, 0;
                        x, y, z, 1];
                    tform_init = affine3d(M);
                    [tform,pt_recal_ptcloud,rmse] = pcregistericp(pt_templ_ptcloud,pt_detec_ptcloud,'MaxIterations',100,'InitialTransform',tform_init);
                    if (rmse < error)
                        error = rmse;
                        pt_templ_label = pt_recal_ptcloud.Location; 
                        best_tform = tform;
                    end  
            end
        end
    end

figure
    %subplot(211)
    plot3(pt_detec2(:,1),pt_detec2(:,2),pt_detec2(:,3),'bo',pt_templ_label(:,1),pt_templ_label(:,2),pt_templ_label(:,3),'r.');
    axis('equal');
    legend({'Detected Point','Template Point'}, 'Location', 'southwest', ...
        'FontSize', 15)
    title('Move to original coordinates' ,'FontSize',18,...      %Titre du tracé
           'FontWeight','bold','FontName',...
           'Times New Roman','Color','k')

pt_detec_sort = [];

for i = 1:size(pt_templ_label,1)
    max_dist = 1000;
    for j = 1:size(pt_detec2,1)
        if ( abs(pt_templ_label(i,1)-pt_detec2(j,1)) + abs(pt_templ_label(i,2)-pt_detec2(j,2)) + abs(pt_templ_label(i,3)-pt_detec2(j,3)) < max_dist )
            max_dist = sqrt((pt_templ_label(i,1)-pt_detec2(j,1)).^2 + (pt_templ_label(i,2)-pt_detec2(j,2)).^2 + (pt_templ_label(i,3)-pt_detec2(j,3)).^2);
            closest_recal = j;
        end
    end
    pt_detec_sort = [pt_detec_sort;pt_detec2(closest_recal,:)];
end



%% Segmentation map

coords = pt_detec_sort;
n = 320 ; 
[T , U, V] = ndgrid(1:n , 1:n, 1:n);
t = coords(:,1); u = coords(:,2); v = coords(:,3);
radius = 3;

F  = zeros(n,n,n);
% for electrode=1:length(t)
%     disp(electrode)
%     E  = ((sqrt(((T-t(electrode)).^2)+((U-u(electrode)).^2)+(V-v(electrode)).^2)) <= radius)*1000000;
%     F = F + E ;
%     
% % Uncomment for gt_seg.nii
%     
%     for i = 1:n
%         for j = 1:n
%             for k = 1:n
%                 if F(i,j,k)==1000000
%                     %disp(F(i,j,k))
%                     F(i,j,k) = electrode;
%                 end
%             end
%         end
%     end
%     
% end

radius2 = radius*radius;
for electrode=1:length(t)
    F(((T-t(electrode)).^2+(U-u(electrode)).^2+(V-v(electrode)).^2) <= radius2) = electrode ;
end

% Uncomment for gt.nii
%F = F>0 ;

disp('Sauvegarde des spheres');
nii.img = F; 

save_untouch_nii(nii , s);
gzip(s) % this will return niftifilename.nii.gz