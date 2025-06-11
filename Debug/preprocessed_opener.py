#########################################################################################################
### preprocessed_opener.py
###
### Script used to try and open NIfTI volumes preprocessed by nnUNer. Somewhat useless.
###
### Author : Kieran Le Mouël
### Date : 7/06/2025
#########################################################################################################

# Various imports
import numpy as np
import pickle
import matplotlib.pyplot as plt

# Path to preprocessed images
path_preprocessed = "/home/klemouel/NAS_EMPENN/share/users/klemouel/Stage/nnUNet/nnUNet_preprocessed/Dataset005_T1_R/nnUNetPlans_3d_fullres/"

# Load data using pickle
def open_preprocessed(path):
    with open(path,'rb') as f: 
        data = pickle.load(f)
    
    return data

# Various tests
data = open_preprocessed(path_preprocessed + "Hemisfer_001.pkl")
classes = data['class_locations']

# for key in classes:
#     print(classes[key])

print(classes[1].shape)

