#Builds a nnUNet dataset following the csv file with the subjects correspondancies of HEMISFER dataset on it

import os #System files manipulations
import shutil #copying files
import pandas as pd #reading the csv correspondancies 
import gzip #Creating .nii.gz files

#Names
mod = "EDT1" #name of the dataset
e = "Hemisfer"#Name of the experiment
p = e + "_" #Prefix of the file name
s = "_0000.nii" #Suffix of the file name
s_gt = ".nii" #Suffix of the ground truth file
name = "rT1.nii" #name of the images in the folders

#Paths definition 
# TODO : change the paths to allow current configuration to work
p_NAS = "/home/mgeorgea/NAS_EMPENN/share/users/mgeorgea/Electrode_Detection/"
p_dat = p_NAS + "Raw Data/" #Data location
p_gt = p_NAS + "Raw Data/GroundTruth/"#path to ground truths
p_csv = p_NAS + "nnUNet/nnUNet_raw/Correspondancies_ElectrodeDetection_Dataset.csv"#CSV file with correspondencies between subject Ids and nnUNet Ids
p_Tr = p_NAS + "nnUNet/nnUNet_raw/Dataset005_T1_R/imagesTr/" #path to the train set
p_Ts = p_NAS + "nnUNet/nnUNet_raw/Dataset005_T1_R/imagesTs/" #path to the test set
p_lTr = p_NAS + "nnUNet/nnUNet_raw/Dataset005_T1_R/labelsTr/" #path to the ground truths associated with the train set images

#Reading the CSV
corr = pd.read_csv(p_csv)

#Sorting, copying, and compressing the files into the right folders
for index,row in corr.iterrows():
    
    id = str(row['Id'])
    id = id.rjust(3,'0')
    
    f = p + id + s
    f_gt = p + id + s_gt
    
    s_dir = p_dat + row['Folder'] + "/" + row['Name'] + "/" + row['Quality'] + "/" + name #Source directory (name of the file)
    gt_dir = p_gt + row['Folder'] + "/" + row['Name'] + "/" + row['Quality'] + "/gt_seg.nii"#Ground truth directory
    
    if(row['Set'] == "train"):
        
        t_dir = p_Tr + f #Target directory
        l_dir = p_lTr + f_gt #Target directory for the ground truth (label)
        
        #Debug
        print(os.path.isfile(s_dir), " | ",os.path.isfile(gt_dir))
        print("Source Directory : ", s_dir, " | Target Directory : ", t_dir, " | Ground Truth Directory : ", gt_dir, " | Label Directory : ", l_dir)
        
        #Copying the files then compressing them, using gzip, for both files
        shutil.copy2(s_dir,t_dir) #copy2 keeps de metadata
        
        with open(t_dir, 'rb') as f_in:
            with gzip.open(t_dir + ".gz", 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(t_dir)
        
        shutil.copy2(gt_dir,l_dir)
        
        with open(l_dir, 'rb') as f_in:
            with gzip.open(l_dir + ".gz", 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(l_dir)
    else:
        
        t_dir = p_Ts + f #Target directory for the train set
        
        #Debug
        print(os.path.isfile(s_dir))
        print("Source Directory : ", s_dir, " | Target Directory : ", t_dir)
        
        #Copying the files then compressing them, using gzip, for both files
        shutil.copy2(s_dir, t_dir)
        with open(t_dir, 'rb') as f_in:
            with gzip.open(t_dir + ".gz", 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(t_dir)    
    print("====================")