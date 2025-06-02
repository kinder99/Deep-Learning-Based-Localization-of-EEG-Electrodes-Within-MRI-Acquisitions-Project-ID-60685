#########################################################################################################
### TEMPLATE_CREATION
###
### Compute a template based on multiple data.
###
### Author : Caroline Pinte
### Date : 27/08/2020
#########################################################################################################

# Load the required modules
import numpy as np
import SimpleITK as sitk
import math

# # Read the Ground Truth image 
# gTruth_image = sitk.ReadImage('c:/Users/User/Desktop/Stage_Caroline/TED/Results_GroundTruth/UTE/S_11/60K/gt_seg.nii')

# # Compute the connected components
# gTruth_components = sitk.ConnectedComponentImageFilter()
# gTruth_label = gTruth_components.Execute( gTruth_image )
# gTruth_nbObjects = gTruth_components.GetObjectCount()
# print('Ground Truth : Number of connected components = {0}'.format(gTruth_nbObjects))

# # Compute the image statistics and find the center of each sphere 
# gTruth_stats = sitk.LabelStatisticsImageFilter()
# gTruth_stats.Execute( gTruth_image , gTruth_label )

# gTruth_centers = []
# for i in range(1,gTruth_nbObjects+1) :
#     bb = gTruth_stats.GetBoundingBox(i)
#     x = math.ceil((bb[0] + bb[1]+1) / 2)
#     y = math.ceil((bb[2] + bb[3]+1) / 2)
#     z = math.ceil((bb[4] + bb[5]+1) / 2)
#     center = (x,y,z)
#     seg_value = gTruth_image.GetPixel(x,y,z)
        
#     gTruth_centers.append((seg_value,center))

# # Tri
# gTruth_centers_sort = sorted(gTruth_centers, key=lambda gTruth: gTruth[0])   
# print(gTruth_centers_sort)

# # # Save
# # with open('tpl_data_9.txt', 'w') as f:
# #     for coord in gTruth_centers_sort :
# #         f.write('{0} {1} {2}\n'.format(coord[1][0],coord[1][1],coord[1][2]))

# # Normalize
# x_values = []
# y_values = []
# z_values = []

# for electrode in gTruth_centers_sort :
#     x_values.append(electrode[1][0])
#     y_values.append(electrode[1][1])
#     z_values.append(electrode[1][2])

# x_mean = np.mean(x_values)
# y_mean = np.mean(y_values)
# z_mean = np.mean(z_values)

# gTruth_centers_norm = []
# for electrode_index in range(0,65) :
#     electrode_position = (x_values[electrode_index]-x_mean, y_values[electrode_index]-y_mean, z_values[electrode_index]-z_mean)
#     print(electrode_position)
#     gTruth_centers_norm.append(electrode_position)

# # Save
# with open('tpl_data_9_norm.txt', 'w') as f:
#     for coord in gTruth_centers_norm :
#         f.write('{0} {1} {2}\n'.format(coord[0],coord[1],coord[2]))

####################################################################################

data1 = np.loadtxt('tpl_data_1_norm.txt', skiprows=0)
data2 = np.loadtxt('tpl_data_2_norm.txt', skiprows=0)
data3 = np.loadtxt('tpl_data_3_norm.txt', skiprows=0)
data4 = np.loadtxt('tpl_data_4_norm.txt', skiprows=0)
data5 = np.loadtxt('tpl_data_5_norm.txt', skiprows=0)
data6 = np.loadtxt('tpl_data_6_norm.txt', skiprows=0)
data7 = np.loadtxt('tpl_data_7_norm.txt', skiprows=0)
data8 = np.loadtxt('tpl_data_8_norm.txt', skiprows=0)
data9 = np.loadtxt('tpl_data_9_norm.txt', skiprows=0)

template = []

for electrode_index in range(0,65) :
    x = (data1[electrode_index][0] + data2[electrode_index][0] + data3[electrode_index][0] + data4[electrode_index][0] + data5[electrode_index][0] + data6[electrode_index][0] + data7[electrode_index][0] + data8[electrode_index][0] + data9[electrode_index][0]) / 9.0
    y = (data1[electrode_index][1] + data2[electrode_index][1] + data3[electrode_index][1] + data4[electrode_index][1] + data5[electrode_index][1] + data6[electrode_index][1] + data7[electrode_index][1] + data8[electrode_index][1] + data9[electrode_index][1]) / 9.0
    z = (data1[electrode_index][2] + data2[electrode_index][2] + data3[electrode_index][2] + data4[electrode_index][2] + data5[electrode_index][2] + data6[electrode_index][2] + data7[electrode_index][2] + data8[electrode_index][2] + data9[electrode_index][2]) / 9.0
    avg_coord = (x,y,z)
    
    template.append(avg_coord)

print(template)

with open('template_ute_norm.txt', 'w') as f:
    for coord in template :
        f.write('{0} {1} {2}\n'.format(coord[0],coord[1],coord[2]))