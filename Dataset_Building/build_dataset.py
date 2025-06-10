#Builds a nnUNet dataset following the csv file with the subjects correspondancies of HEMISFER dataset on it

import os #System files manipulations
import shutil #copying files
import pandas as pd #reading the csv correspondancies 
import gzip #Creating .nii.gz files
import argparse

parser = argparse.ArgumentParser("check for mode", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("mode", type=bool, help="whether petra mode is enabled or not")

args = vars(parser.parse_args())

#Names
mod = "EDT1" #name of the dataset
e = "Hemisfer"#Name of the experiment
p = e + "_" #Prefix of the file name
s = "_0000.nii" #Suffix of the file namepen
s_gt = ".nii" #Suffix of the ground truth file
name = "rT1.nii" #name of the images in the folders

mode_petra = args['mode']

#Paths definition
p_NAS = "/home/klemouel/NAS_EMPENN/share/users/klemouel/Stage/"
p_dat = p_NAS + "Data/Raw/" #Data location
p_gt = p_NAS + "Data/Ground_Truths/"#path to ground truths
p_csv = p_NAS + "Correspondancies_ElectrodeDetection_Dataset.csv" #CSV file with correspondencies between subject Ids and nnUNet Ids
p_dataset = "nnUNet/nnUNet_raw/Dataset000_Petra_1class/"
p_Tr = p_NAS + p_dataset + "imagesTr/" #path to the train set
p_Ts = p_NAS + p_dataset + "imagesTs/" #path to the test set
p_lTr = p_NAS + p_dataset + "labelsTr/" #path to the ground truths associated with the train set images

#Reading the CSV
corr = pd.read_csv(p_csv)   

#Sorting, copying, and compressing the files into the right folders
for index,row in corr.iterrows():
    
    id = str(row['Id']) #get id from current row 
    id = id.rjust(3,'0') #add padding with character 0 to the left of id, until id is of length 3
    
    f = p + id + s #set name according to nomenclature : Hemisfer_id_0000.nii
    f_gt = p + id + s_gt #set name of segmented image : Hemisfer_id.nii

    if(mode_petra):
        if(row["Quality"] == "30K"):
            name = "PETRA_30K.nii"
        if(row["Quality"] == "30Kbis"):
            name = "PETRA_30K.nii"
        if(row["Quality"] == "60K"):
            name = "PETRA_60K.nii"
        if(row["Quality"] == "60Kbis"):
            name = "PETRA_60K.nii"
        if(row["Quality"] == "60Kbisbis"):
            name = "PETRA_60K.nii"
    
    s_dir = p_dat + row['Folder'] + "/" + row['Name'] + "/" + row['Quality'] + "/" + name #Source directory (name of the file)
    gt_dir = p_gt + row['Folder'] + "/" + row['Name'] + "/" + row['Quality'] + "/gt.nii" #Ground truth directory
    
    # print("chmod s_dir : " + (str)(os.stat(s_dir).st_mode))

    if(row['Set'] == "train"):
        
        t_dir = p_Tr + f #Target directory
        l_dir = p_lTr + f_gt #Target directory for the ground truth (label)

        #Debug
        print(os.path.isfile(s_dir), " | ", os.path.isfile(t_dir)," | ",os.path.isfile(gt_dir))
        print("Source Directory : ", s_dir, "\nTarget Directory : ", t_dir, "\nGround Truth Directory : ", gt_dir, "\nLabel Directory : ", l_dir)

        #Copying the files then compressing them, using gzip, for both files

        shutil.copy2(s_dir, t_dir) #copy2 keeps the metadata
        
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
        print("Source Directory : ", s_dir, "\nTarget Directory : ", t_dir)
        
        #Copying the files then compressing them, using gzip, for both files
        shutil.copy2(s_dir, t_dir)
        with open(t_dir, 'rb') as f_in:
            with gzip.open(t_dir + ".gz", 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(t_dir)    
    print("====================")