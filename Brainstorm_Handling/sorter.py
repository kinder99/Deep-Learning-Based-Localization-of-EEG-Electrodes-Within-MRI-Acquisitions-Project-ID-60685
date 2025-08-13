###########################################################################################################
### sorter.py                                                                                           ###
###                                                                                                     ###
### Update given template .txt files according to electrode order used for ICP algorithm application.   ###
###                                                                                                     ###
### Author: Kieran Le Mouël                                                                             ###
### Date: 18/07/2025                                                                                    ###
###########################################################################################################

# Load required modules
import pandas as pd
from io import StringIO
import sys
import argparse

# Recieve command line arguments
# parser = argparse.ArgumentParser("define paths", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
# parser.add_argument("data_path", help="path to data directory", type=str)
# args = vars(parser.parse_args())
path = "C:\\Users\\kiera\\Documents\\Unlimited_Home_Works\\Internship2025\\data\\"
data_path = "C:\\Users\\kiera\\Documents\\Unlimited_Home_Works\\Internship2025\\data\\post_processing\\T1_65\\icp_output\\" #args['data_path']

# List containing the electrodes, sorted according to the order used for ICP.
ref_list = [
    "FT9", "FT10", "TP9", "TP10", "F7",
    "FT7", "T7", "AF7", "Fp1", "AF8",
    "F8", "Fp2", "Fpz", "FT8", "T8",
    "TP7", "TP8", "P7", "P8", "F5",
    "F6", "FC5", "PO7", "AF4", "AF3",
    "PO8", "C5", "FC6", "AFz", "CP5",
    "C6", "O1", "P5", "O2", "CP6",
    "F3", "P6", "Oz", "F4", "FC3",
    "PO3", "C3", "FC4", "CP3", "P3",
    "PO4", "F2", "F1", "Fz", "C4",
    "P4", "CP4", "POz", "FC1", "FC2",
    "P1", "C1", "FCz", "CP1", "P2",
    "C2", "CP2", "Pz", "Cz", "CPz"
]

patchwork_fix = [
    28, 29, 30, 31, 11, 54, 13, 52, 1, 53, 12, 2, 60, 55, 14, 56, 57, 15, 16,
    46, 47, 24, 58, 39, 38, 59, 48, 25, 64, 26, 49, 9, 50, 10, 27, 3, 51, 63,
    4, 40, 5, 41, 42, 7, 45, 33, 32, 17, 6, 8, 43, 42 ,62, 20, 21, 36, 34, 65,
    22, 37, 35, 23, 19, 18, 61
]

def read_file(path: str) -> list[list[float]]:
    """
    Function used to get electrode positions from a .txt file.
    
    Keyword arguments:
    
    path -- path to file to read
    """
    with open(path, 'r') as fi:
        data = fi.read()
    elecs = data.split("\n")
    elecs.pop(-1)
    res = []
    for elec in elecs:
        res.append(elec.split(","))
    return res

def sort(ref_list: list[str], data: list[list[str,float]]) -> list[list[str, float]]:
    """
    Function used to sort a list according to a certain order.
    
    Keyword arguments:
    
    ref_list -- list containing the reference order
    
    data -- list containing the electrode names and their positions
    """
    res = []
    for i in range(0,len(ref_list)):
        for elec in data:
            if(elec[0] == ref_list[i]):
                res.append(elec)
    return res

def patchwork_sort(l):
    res = []
    for i in patchwork_fix:
        res.append(l[i-1])
    return res

def write_file(li: list[list[str, float]], save_path: str) -> None:
    """
    Function used to write a .txt file with sorted electrodes.
    
    Keyword arguments:
    
    li -- sorted list containing electrode names and their positions
    
    save_path -- path to target repository
    """
    for line in li:
        res = StringIO()
        sys.stdout = res
        # print(line[0]+","+float(line[1])+","+float(line[2])+","+float(line[3]))
        print(f'{line[0]},{float(line[1])},{float(line[2])},{float(line[3])}')
        res_str = res.getvalue()
    
        with open(save_path, 'a') as fi:
            fi.write(res_str)
            
def write_file_2(li: list[list[float]], save_path: str) -> None:
    """
    Function used to write a .txt file with sorted electrodes.
    
    Keyword arguments:
    
    li -- sorted list containing electrode names and their positions
    
    save_path -- path to target repository
    """
    for line in li:
        res = StringIO()
        sys.stdout = res
        # print(line[0]+","+float(line[1])+","+float(line[2])+","+float(line[3]))
        print(f'{float(line[0])},{float(line[1])},{float(line[2])}')
        res_str = res.getvalue()
    
        with open(save_path, 'a') as fi:
            fi.write(res_str)

def __main__():
    corr = pd.read_csv(path + 'Correspondancies_ElectrodeDetection_Dataset.csv')
    for index, row in corr.iterrows():
        if row['Set'] == "test":
            id = str(row['Id'])
            id = id.rjust(3,'0')
            
            current_data = read_file(path + "trans\\ID_" + id + ".txt")
            current_res = sort(ref_list, current_data)
            write_file(current_res, path + "trans\\after_sorting\\ID_"+id+"_sorted.txt")
    
    # corr = pd.read_csv(path + 'Correspondancies_ElectrodeDetection_Dataset.csv')
    # for index, row in corr.iterrows():
    #     if row['Set'] == "test":
    #         id = str(row['Id'])
    #         id = id.rjust(3,'0')
            
    #         current_data = read_file(data_path + "Hemisfer_" + id + "_postprocessed_coord.txt")
    #         print(len(patchwork_fix) == len(current_data))
    #         current_res = patchwork_sort(current_data)
    #         write_file_2(current_res, data_path + "\\after_sorting/ID_"+id+"_sorted.txt")
            
__main__()
        
        