import os
import shutil
import pandas as pd
import gzip
import argparse

p_NAS = "/home/klemouel/NAS_EMPENN/share/users/klemouel/Stage/"
p_gt_mod = p_NAS + "temp_imgs/"
p_target = p_NAS + "nnUNet/nnUNet_raw/Dataset000_Petra_1class/labelsTr/"

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

for id in ids:
    shutil.copy2(p_gt_mod + "Hemisfer_"+id+".nii",p_target+"Hemisfer_"+id+".nii")

    with open(p_target + "Hemisfer_"+id+".nii", 'rb') as f_in:
        with gzip.open(p_target + "Hemisfer_"+id+".nii"+".gz", 'wb') as f_out:
            shutil.copyfileobj(f_in,f_out)
    os.remove(p_target + "Hemisfer_"+id+".nii")