import nibabel as nib
import numpy as np
import pandas as pd
import tqdm

nas_path = "/home/klemouel/NAS_EMPENN/share/users/klemouel/Stage/"
gt_path = nas_path + "nnUNet/nnUNet_raw/Dataset000_Petra_1class/labelsTr/"
csv_path = nas_path + "Correspondancies_ElectrodeDetection_Dataset.csv"

corr = pd.read_csv(csv_path)

for index, row in tqdm.tqdm(corr.iterrows()):
    id = str(row['Id']) #get id from current row 
    id = id.rjust(3,'0') #add padding with character 0 to the left of id, until id is of length 3

    if(row['Set'] == "train"):
        labels = nib.load(gt_path + "Hemisfer_" + id + ".nii.gz").get_fdata()
        img = nib.load(gt_path + "Hemisfer_" + id + ".nii.gz")
        print(img.header)
        #print(labels)
        # proportion = (np.count_nonzero(labels) * 100) / labels.size # compute percentage of non zero voxels in volume
        # print("Proportion of labeled pixels for Hemisfer_"+id+".nii.gz : ",proportion)