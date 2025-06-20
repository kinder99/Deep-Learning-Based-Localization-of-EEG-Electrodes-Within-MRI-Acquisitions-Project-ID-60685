#########################################################################################################
### ground_truth_infodump.py
###
### Script used to compare ground truth metadata between binary and labeled datasets.
###
### Author : Kieran Le Mouël
### Date : 20/06/2025
#########################################################################################################

# Various imports
import nibabel as nib
import numpy as np
import SimpleITK as sitk
import pandas as pd
from io import StringIO
import sys
import os

# Paths definitions
path_NAS = "/home/klemouel/NAS_EMPENN/share/users/klemouel/Stage/"
path_CSV = path_NAS + "Correspondancies_ElectrodeDetection_Dataset.csv"
path_binary_gt = path_NAS + "nnUNet/nnUNet_raw/Dataset000_Petra_1class/labelsTr/"
path_labels_gt = path_NAS + "nnUNet/nnUNet_raw/Dataset005_Petra_65/labelsTr/"
path_SAVE = path_NAS + "temp_gt_compare/"

prefix = "Hemisfer_"
suffix = ".nii.gz"

# Read the CSV
corr = pd.read_csv(path_CSV)


def write_metadata(bin_image, lab_image):
    """
    Function used to read image metadata and write it into .txt files.

    Keywords arguments:
    bin_image -- ground truth image for binary classes (background and electrodes)
    lab_image -- ground truth image for labeled classes (background and 65 electrode classes)
    """
    for k in bin_image.GetMetaDataKeys(): # Iterate over all keys in the metadata
        data = bin_image.GetMetaData(k)

        # Get standard output as string
        res = StringIO() 
        sys.stdout = res 
        print(f'({k}) = = "{data}"')
        res_str = res.getvalue()

        # Write .txt file with read data
        with open(path_SAVE + "binary/bin_" + str(id) + ".txt", "a") as fi:
            fi.write(res_str + "\n")

    for kk in lab_image.GetMetaDataKeys(): # Iterate over all keys in the metadata, again
        data = lab_image.GetMetaData(kk)

        # Get standard output as string, again
        res2 = StringIO()
        sys.stdout = res2
        print(f'({kk}) = = "{data}"')
        res2_str = res2.getvalue()

        # Write .txt file with read data
        with open(path_SAVE + "labels/lab_" + str(id) + ".txt", "a") as fi:
            fi.write(res2_str + "\n")

def compare_metadata_dict(bin_image, lab_image):
    """
    Function used to create a dictionary comparing the metadata of a binary and a labeled ground truth.

    Keyword arguments:
    bin_image -- ground truth image for binary classes (background and electrodes)
    lab_image -- ground truth image for labeled classes (background and 65 electrode classes)
    """

    # Initialize empty dictionnary
    res = {}
    
    # For all keys in the metadata
    for k in bin_image.GetMetaDataKeys():
        bin_data = bin_image.GetMetaData(k)
        lab_data = lab_image.GetMetaData(k)
        res[k] = bin_data == lab_data # Values of the keys is a test between values of binary and labeled metadata

    return res

def compare_metadata_file(bin_file, lab_file):
    """
    Function used to compare the contents of two files.

    Keyword arguments:
    bin_file -- file (containing the binary metadata probably)
    lab_file -- file (containing the labeled metadata probably)
    """

    # Read binary metadata file
    with open(bin_file, "r") as file:
        bin_data = file.read()
    
    # Read labeled metadata file
    with open(lab_file, "r") as file2:
        lab_data = file2.read()

    # Compare both files
    return bin_data == lab_data

# Initialize empty array to list all the ids where a discrepancy is present
issues_id = []

# Iterate over all rows of the CSV
for index, row in corr.iterrows():
    id = str(row['Id']) # Get id from current row
    id = id.rjust(3,'0') # Add padding with character '0' to the left if id, until id is of length 3

    if row['Set'] == "train": # Check if image belongs to the train set
        
        # Define source paths for the ground truths files
        source_path_binary = path_binary_gt + prefix + id + suffix
        source_path_labels = path_labels_gt + prefix + id + suffix

        # Load ground truth images using SimpleITK
        bin_image = sitk.ReadImage(source_path_binary, sitk.sitkUInt8)
        lab_image = sitk.ReadImage(source_path_labels, sitk.sitkUInt8)

        # Exact same information for all cases, commented to save computation time
        # bin_proportion = (np.count_nonzero(binary) * 100) / binary.size
        # bin_components = sitk.ConnectedComponentImageFilter()
        # bin_electrodes = bin_components.Execute(bin_image)
        # print("Proportion of non zero voxels : " + str(bin_proportion) + ", Number of electrodes : " + str(bin_components.GetObjectCount()))

        # lab_proportion = (np.count_nonzero(labels) * 100) / labels.size
        # lab_components = sitk.ConnectedComponentImageFilter()
        # lab_electrodes = lab_components.Execute(lab_image)
        # print("Proportion of non zero voxels : " + str(lab_proportion) + ", Number of electrodes : " + str(lab_components.GetObjectCount()))

        # Check if the write repositories are empty, if they aren't, don't write
        if len(os.listdir(path_SAVE + "binary/")) == 0 and len(os.listdir(path_SAVE + "labels/")) == 0 :
            print("writing dataset metadata")
            write_metadata(bin_image, lab_image)

        # Compute comparing dictionary
        dict = compare_metadata_dict(bin_image, lab_image)

        # Check if writing repository is empty, if it isn't, don't write
        if len(os.listdir(path_SAVE + "compare/")) == 0 :
            print("writing comparasion files")
            for k in dict: # Iterate over all keys in metadata

                # Get standard output as string, again, again 
                res2 = StringIO()
                sys.stdout = res2
                print(f'{id} : ({k}) = = "{dict[k]}"')
                res2_str = res2.getvalue()

                # Write output .txt file
                with open(path_SAVE + "compare/compare_"+str(id)+".txt", "a") as fi:
                    fi.write(res2_str + "\n")

        # Check if metadata testing shows an issue
        if not compare_metadata_file(path_SAVE + "binary/" + "bin_"+str(id)+".txt", path_SAVE + "labels/" + "lab_"+str(id)+".txt"):
            issues_id.append(str(id)) # Add id to the array
            print("this id has a problem : " + str(id))

# Array containing the ids for which the label values were wrong in binary ground truths
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
        
issues_id.sort()
wrong_ids.sort()

# Check if id arrays are the same
print("are the erronous ids the same ? " + str(issues_id == wrong_ids))