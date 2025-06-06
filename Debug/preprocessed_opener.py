import numpy as np
import pickle
import matplotlib.pyplot as plt

path_preprocessed = "/home/klemouel/NAS_EMPENN/share/users/klemouel/Stage/nnUNet/nnUNet_preprocessed/Dataset005_T1_R/nnUNetPlans_3d_fullres/"

def open_preprocessed(path):
    with open(path,'rb') as f: 
        data = pickle.load(f)
    
    return data

data = open_preprocessed(path_preprocessed + "Hemisfer_001.pkl")
classes = data['class_locations']

print(classes)