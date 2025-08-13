#########################################################################################################
### COORD
###
### Compute the center position of connected components.
###
### Author: Caroline Pinte, Kieran Le Mouël
### Date: 27/08/2020, Modified: 30/06/2025 
#########################################################################################################

# Load the required modules
import numpy as np
import SimpleITK as sitk
import math
import pandas as pd
import argparse

# Receive command line arguments
# parser = argparse.ArgumentParser("define paths", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
# parser.add_argument("gt_path", help="path to ground truths repository", type=str)
# #parser.add_argument("inf_path", help="path to inferences repository", type=str)
# parser.add_argument("out_path", help="path to output repository", type=str)
# args = vars(parser.parse_args())

# Read the Prediction image
# gt_path = args['gt_path']
nas_path = "C:\\Users\\kiera\\Documents\\Unlimited_Home_Works\\Internship2025\\data\\"
# inf_path = nas_path + args['inf_path']
csv_path = nas_path + "Correspondancies_ElectrodeDetection_Dataset.csv"
out_path = nas_path + "post_processing\\T1_65\\coords_gt_output\\"

corr = pd.read_csv(csv_path)

for index, row in corr.iterrows():
    id = str(row['Id'])
    id = id.rjust(3, '0')

    if(row['Set'] == "test"):
        # predict_image = sitk.ReadImage(inf_path + "Hemisfer_" + id + ".nii.gz")
        predict_image = sitk.ReadImage(nas_path + "Results_GroundTruth\\" + row['Folder'] + "\\" + row['Name'] + "\\" + row['Quality'] + "\\gt_seg.nii")

        # Compute the connected components
        predict_components = sitk.ConnectedComponentImageFilter()
        predict_label = predict_components.Execute(predict_image)
        predict_nbObjects = predict_components.GetObjectCount()
        print('Prediction : Number of connected components = {0}'.format(predict_nbObjects))

        # Compute the image statistics and find the center of each sphere
        predict_stats = sitk.LabelStatisticsImageFilter()
        predict_stats.Execute(predict_image, predict_label)

        predict_centers = []
        for i in range(1,predict_nbObjects+1) :
            bb = predict_stats.GetBoundingBox(i)
            x = math.ceil((bb[0] + bb[1]+1) / 2)
            y = math.ceil((bb[2] + bb[3]+1) / 2)
            z = math.ceil((bb[4] + bb[5]+1) / 2)
            center = (x,y,z)
            predict_centers.append(center)

        # Save
        with open(out_path + "Hemisfer_" + id + "_coords.txt", 'a') as f:
            for coord in predict_centers :
                f.write('{0} {1} {2}\n'.format(coord[0],coord[1],coord[2]))