#########################################################################################################
### add_to_dataset.py
###
### Script used to move NIfTI volumes from temporary repository to nnUNet dataset repository, 
### and compress them.
###
### Author: Kieran Le Mouël
### Date: 11/06/2025
#########################################################################################################

# Various imports
import os
import shutil
import pandas as pd
import gzip

# Path definitions
p_NAS = "/home/klemouel/NAS_EMPENN/share/users/klemouel/Stage/"
p_gt_mod = p_NAS + "temp_imgs/"
p_target = p_NAS + "nnUNet/nnUNet_raw/Dataset000_Petra_1class/labelsTr/"

# Array containing all the ids for which the labeling was wrong
ids = ["028",
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

# Iterate over all ids in array
for id in ids:
    shutil.copy2(p_gt_mod + "Hemisfer_"+id+".nii", p_target+"Hemisfer_"+id+".nii") # Copy temp image to target directory while keeping metadata

    with open(p_target + "Hemisfer_"+id+".nii", 'rb') as f_in:
        with gzip.open(p_target + "Hemisfer_"+id+".nii"+".gz", 'wb') as f_out:
            shutil.copyfileobj(f_in,f_out) # Compress NIfTI volume
    os.remove(p_target + "Hemisfer_"+id+".nii") # Remove temporary image