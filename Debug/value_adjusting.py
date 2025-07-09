###########################################################################################################
### value_adjusting.py                                                                                  ###
###                                                                                                     ###
### Script used to modify incorrect labeling in NIfTI volumes.                                          ###
###                                                                                                     ###
### Author: Kieran Le Mouël                                                                             ###
### Date: 7/06/2025                                                                                     ###
###########################################################################################################

# Various imports
import nibabel as nib
import numpy as np
import pandas as pd
import tqdm

# Array containing all the ids for which the labeling is incorrect
wrong_ids = ["028",
            "033",
            "035",
            "042",
            "044",
            "046",
            "048",
            "027",
            "041",
            "043",
            "034",
            "032",
            "045",
            "047",
            "049",
            "050",
            "054",
            "056",
            "052",
            "058",
            "051",
            "053",
            "057"]

# Paths definition
nas_path = "/home/klemouel/NAS_EMPENN/share/users/klemouel/Stage/"
gt_path = nas_path + "Data/Ground_Truths/"
csv_path = nas_path + "Correspondancies_ElectrodeDetection_Dataset.csv"
temp_path = nas_path + "temp_imgs/"

# Read the CSV
corr = pd.read_csv(csv_path)

# Iterate on the rows of the CSV
for index, row in tqdm.tqdm(corr.iterrows()):
    id = str(row['Id'])
    id = id.rjust(3,'0')

    # Check if labeling is incorrect for this id
    if id in wrong_ids:
        s_dir = gt_path + row['Folder'] + "/" + row['Name'] + "/" + row['Quality'] + "/" + "gt.nii"
        img = nib.load(s_dir) # Load original image using nibabel
        img_data = img.get_fdata()
        img_header = img.header
        img_affine = img.affine

        # Counter
        c = 0

        # Iterate over all the volume
        for i in range(0,len(img_data)-1):
            for j in range(0,len(img_data[i])-1):
                for k in range(0,len(img_data[i][j])-1):
                    if(img_data[i][j][k] == 32767):
                        c += 1
                        img_data[i][j][k] = 1 # Replace erronous label with correct value
        print("Current id : "+ id +", Number of voxels modified : ", c)

        # Define and save replacement NIfTI volume
        temp_img = nib.Nifti1Image(img_data, affine=img_affine, header=img_header)
        nib.save(temp_img, temp_path + "Hemisfer_"+id+".nii")