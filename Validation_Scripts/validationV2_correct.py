#########################################################################################################
### VALIDATION V2
###
### Compare the ground truth segmentation with the predicted segmentation for the second model.
###
### Author : Caroline Pinte
### Date : 10/08/2020
#########################################################################################################

# Load the required modules
import numpy as np
import SimpleITK as sitk
import math

###################### UTILISATION ######################
### Read the Ground Truth image and the Prediction image
gTruth_image = sitk.ReadImage('c:/Users/User/Desktop/Stage_Caroline/TED/Results_GroundTruth/UTE/S_8/15K/gt_seg.nii')

### BRUT
#predict_image = sitk.ReadImage('c:/Users/User/Desktop/Stage_Caroline/TED/Results_Predictions/Brut/Pred_UTE_V2/Hemisfer_101.nii.gz')

### Post-Processed
predict_image = sitk.ReadImage('c:/Users/User/Desktop/Stage_Caroline/TED/Results_Predictions/Post-Processed/PostProcessed_UTE_V2_newICP/Hemisfer_120_postprocessed.nii.gz')

# Optionnal 
s = 'c:/Users/User/Desktop/Stage_Caroline/TED/Results_Predictions/Post-Processed/PostProcessed_UTE_V2_newICP/Hemisfer_120_poserror.txt'
######################### FIN #########################

### 1. Compute the connected components of both images

## Ground Truth
gTruth_components = sitk.ConnectedComponentImageFilter()
gTruth_label = gTruth_components.Execute( gTruth_image )
gTruth_nbObjects = gTruth_components.GetObjectCount()
print('Ground Truth : Number of connected components = {0}'.format(gTruth_nbObjects))

## Prediction
predict_components = sitk.ConnectedComponentImageFilter()
predict_label = predict_components.Execute( predict_image )
predict_nbObjects = predict_components.GetObjectCount()
print('Prediction : Number of connected components = {0}'.format(predict_nbObjects))


### 2. Compute the image statistics and find the center of each sphere for both images

## Ground Truth
gTruth_stats = sitk.LabelStatisticsImageFilter()
gTruth_stats.Execute( gTruth_image , gTruth_label )

gTruth_centers = []
for i in range(1,gTruth_nbObjects+1) :
    bb = gTruth_stats.GetBoundingBox(i)
    x = math.ceil((bb[0] + bb[1]+1) / 2)
    y = math.ceil((bb[2] + bb[3]+1) / 2)
    z = math.ceil((bb[4] + bb[5]+1) / 2)
    center = (x,y,z)
    gTruth_centers.append(center)

## Prediction
predict_stats = sitk.LabelStatisticsImageFilter()
predict_stats.Execute( predict_image , predict_label )

predict_centers = []
for i in range(1,predict_nbObjects+1) :
    bb = predict_stats.GetBoundingBox(i)
    x = math.ceil((bb[0] + bb[1]+1) / 2)
    y = math.ceil((bb[2] + bb[3]+1) / 2)
    z = math.ceil((bb[4] + bb[5]+1) / 2)
    center = (x,y,z)
    predict_centers.append(center)


### 3. Compute the association between the corresponding centers and position error

corresponding_gTruth_centers = []
position_error = []
pixel2mm = 0.9375 # voxel size
nbMislabeled = 0
mislabeled = []
position_error_label = []

for i in range(0, len(predict_centers)) :
    max_dist = 1000
    p_x = predict_centers[i][0]
    p_y = predict_centers[i][1]
    p_z = predict_centers[i][2]
    p_value = predict_image.GetPixel(p_x-1,p_y-1,p_z-1)
        
    for j in range(0, len(gTruth_centers)) :
        g_x = gTruth_centers[j][0]
        g_y = gTruth_centers[j][1]
        g_z = gTruth_centers[j][2]

        if ( (abs(p_x-g_x) + abs(p_y-g_y) + abs(p_z-g_z)) < max_dist ) :
            max_dist = math.sqrt((p_x-g_x)**2 + (p_y-g_y)**2 + (p_z-g_z)**2)
            corresponding_center = gTruth_centers[j]
            g_value = gTruth_image.GetPixel(g_x-1,g_y-1,g_z-1)

    corresponding_gTruth_centers.append(corresponding_center)
    position_error_mm = max_dist*pixel2mm
    position_error.append(position_error_mm)
    if (p_value != g_value) :
            nbMislabeled = nbMislabeled + 1
            mislabeled.append((p_value,g_value))

    print('Composante {0} : {1} corresponding to {2}, position error = {3} mm, label {4}-{5}'.format(i+1, predict_centers[i], corresponding_gTruth_centers[i], position_error[i], p_value, g_value))
    position_error_label.append((g_value,position_error[i]))

### 4. Some statistics

nbTotal = 0
sumTotal = 0
maxPE = 0
nbOutliers = 0
nbDoubles = 0
nbOutlierAndDoubles = 0

for index in range(0, len(position_error)) :
    # Mean PE
    nbTotal = nbTotal + 1
    sumTotal = sumTotal + position_error[index]
    # Maximum PE
    if (position_error[index] > maxPE) :
        maxPE = position_error[index]
    # Outliers
    if (position_error[index] > 10) :
        nbOutliers = nbOutliers + 1
        print('Outlier : {0} {1}'.format(predict_centers[index], position_error[index]))


for coord1 in range(0, len(corresponding_gTruth_centers)) :
    double = 0
    for others in range(0, len(corresponding_gTruth_centers)) :
        if (corresponding_gTruth_centers[coord1] == corresponding_gTruth_centers[others]) :
            if (predict_centers[coord1] != predict_centers[others]) :
                nbDoubles = nbDoubles + 1
                print('Double : {0} et {1}'.format(predict_centers[coord1], predict_centers[others]))

meanPE = sumTotal / nbTotal
stdPE = np.std(position_error)
true_positives = predict_nbObjects - nbOutliers
ppv = (true_positives / predict_nbObjects)*100
nbDoubles = nbDoubles / 2 # compted twice for each

print('Mean PE : {0} mm'.format(meanPE))
print('Std PE : {0} mm'.format(stdPE))
print('Max PE : {0} mm'.format(maxPE))
print('Outlier(s) : {0}'.format(nbOutliers))
print('Double(s) : {0}'.format(nbDoubles))
print('PPV : {0} %'.format(ppv))
print('True Positives : {0}'.format(true_positives))
print('Mislabeled : {0} -> {1}'.format(nbMislabeled, mislabeled))

with open(s, 'w') as f:
    for coord in position_error_label :
        f.write('{0} {1}\n'.format(coord[0],coord[1]))