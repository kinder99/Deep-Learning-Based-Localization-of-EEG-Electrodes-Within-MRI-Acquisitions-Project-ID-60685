#########################################################################################################
### COORD
###
### Compute the center position of connected components.
###
### Author : Caroline Pinte
### Date : 27/08/2020
#########################################################################################################


# Load the required modules
import numpy as np
import SimpleITK as sitk
import math

# Read the Prediction image
predict_image = sitk.ReadImage('c:/Users/User/Desktop/Stage_Caroline/TED/Results_Predictions/Brut/Pred_PETRA_FEWDATA2/Hemisfer_004.nii.gz')


# Compute the connected components 
predict_components = sitk.ConnectedComponentImageFilter()
predict_label = predict_components.Execute( predict_image )
predict_nbObjects = predict_components.GetObjectCount()
print('Prediction : Number of connected components = {0}'.format(predict_nbObjects))

# Compute the image statistics and find the center of each sphere 
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

# Save
with open('c:/Users/User/Desktop/Stage_Caroline/TED/Results_Predictions/Brut/Pred_PETRA_FEWDATA2/Hemisfer_004_coord.txt', 'w') as f:
    for coord in predict_centers :
        f.write('{0} {1} {2}\n'.format(coord[0],coord[1],coord[2]))

