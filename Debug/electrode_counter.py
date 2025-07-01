###########################################################################################################
### ground_truth_proportion.py                                                                          ###
###                                                                                                     ###
### Script used to compute the total percentage of voxels making up the electrodes in given volume.     ###
### Also able to count the number of individual electrodes in a volume.                                 ###
###                                                                                                     ###
### Author: Kieran Le Mouël                                                                             ###
### Date: 7/06/2025                                                                                     ###
###########################################################################################################

# Various imports
import nibabel as nib
import numpy as np
import pandas as pd
import argparse
import SimpleITK as sitk

# Command line argument handling
parser = argparse.ArgumentParser("check for mode", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("path", help="path to repository of images to work on, starts from root internship repo", type=str)
parser.add_argument("mode", help="Whether train mode is enabled or not (1 = True, 0 = False)", type=int)
args = vars(parser.parse_args())
inf_path = args['path']
mode = args['mode']

# Paths definitions
nas_path = "/home/klemouel/NAS_EMPENN/share/users/klemouel/Stage/"
gt_path = nas_path + "nnUNet/nnUNet_raw/Dataset005_Petra_65/labelsTr/"
res_path = nas_path + inf_path + "/"
csv_path = nas_path + "Correspondancies_ElectrodeDetection_Dataset.csv"

# Read the CSV
corr = pd.read_csv(csv_path)

# Iterate for all rows in the CSV
for index, row in corr.iterrows():
    id = str(row['Id']) # Get id from current row 
    id = id.rjust(3,'0') # Add padding with character 0 to the left of id, until id is of length 3

    if(mode == 0):
        if(row['Set'] == "train"): # Check if image belongs to train set or not; test images have no ground truth
            labels = nib.load(gt_path + "Hemisfer_" + id + ".nii.gz").get_fdata()
            proportion = (np.count_nonzero(labels) * 100) / labels.size # Compute percentage of non zero voxels in volume
            print("Proportion of labeled pixels for Hemisfer_"+id+".nii.gz : ",proportion)

            gt_image = sitk.ReadImage(gt_path + "Hemisfer_" + id + ".nii.gz", sitk.sitkUInt8) # Load ground truth volume with SimpleITK
            gt_components = sitk.ConnectedComponentImageFilter() # Initialize default connected components filter
            gt_labels = gt_components.Execute(gt_image) # Filter the ground truth volume to get the number of connected components (electrodes)
            print("Number of found electrodes according to SimpleITK : " + str(gt_components.GetObjectCount()))

    if(mode == 1):
        if(row['Set'] == "test"): # Check if image belongs to train set or not; test images have no ground truth
            labels = nib.load(res_path + "Hemisfer_" + id + ".nii.gz").get_fdata()
            proportion = (np.count_nonzero(labels) * 100) / labels.size # Compute percentage of non zero voxels in volume
            print("Proportion of labeled pixels for Hemisfer_"+id+".nii.gz : ",proportion)

            predicted_image = sitk.ReadImage(res_path + "Hemisfer_" + id + ".nii.gz", sitk.sitkUInt8) # Load predicted volume with SimpleITK
            predicted_components = sitk.ConnectedComponentImageFilter() # Initialize default connected components filter
            predicted_labels = predicted_components.Execute(predicted_image) # Filter the predicted volume to get the connected components (eletrodes) 
            print("Number of found electrodes according to SimpleITK : " + str(predicted_components.GetObjectCount()))