#########################################################################################################
### ground_truth_proportion.py
###
### Script used to compute the total percentage of voxels making up the electrodes in each ground truth.
###
### Author : Kieran Le Mouël
### Date : 7/06/2025
#########################################################################################################

# Various imports
import nibabel as nib
import numpy as np
import pandas as pd
import tqdm

# Paths definitions
nas_path = "/home/klemouel/NAS_EMPENN/share/users/klemouel/Stage/"
gt_path = nas_path + "nnUNet/nnUNet_raw/Dataset000_Petra_1class/labelsTr/"
csv_path = nas_path + "Correspondancies_ElectrodeDetection_Dataset.csv"

# Read the CSV
corr = pd.read_csv(csv_path)

# Iterate for all rows in the CSV
for index, row in tqdm.tqdm(corr.iterrows()):
    id = str(row['Id']) # Get id from current row 
    id = id.rjust(3,'0') # Add padding with character 0 to the left of id, until id is of length 3

    if(row['Set'] == "train"): # Check if image belongs to train set or not; test images have no ground truth
        labels = nib.load(gt_path + "Hemisfer_" + id + ".nii.gz").get_fdata()
        proportion = (np.count_nonzero(labels) * 100) / labels.size # Compute percentage of non zero voxels in volume
        print("Proportion of labeled pixels for Hemisfer_"+id+".nii.gz : ",proportion)