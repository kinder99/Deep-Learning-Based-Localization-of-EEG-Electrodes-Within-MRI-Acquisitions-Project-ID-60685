from io import StringIO
import sys
import os
import numpy as np
import re

path_NAS = "/home/klemouel/NAS_EMPENN/share/users/klemouel/Stage/"

# path_log = path_NAS + "nnUNet/nnUNet_results/Dataset001_T1_65/nnUNetTrainerDiceCELoss_noSmooth__nnUNetPlans__3d_fullres/fold_0/"
path_log = path_NAS + "training_log_2025_6_30_15_17_03.txt"

with open(path_log, 'r') as f:
    data = f.read()

electrodes = {
    1: "FP2", 2: "FPZ", 3: "FP1", 4: "AF7", 5: "AF3", 6: "AFZ", 7: "AF4", 8: "AF8", 9: "F8", 10: "F6",
    11: "F4", 12: "F2", 13: "FZ", 14: "F1", 15: "F3", 16: "F5", 17: "F7", 18: "FT9", 19: "FT7", 20: "FC5",
    21: "FC3", 22: "FC1", 23: "FCZ", 24: "FC2", 25: "FC4", 26: "FC6", 27: "FT8", 28: "FT10", 29: "T8", 30: "C6",
    31: "C4", 32: "C2", 33: "CZ", 34: "C1", 35: "C3", 36: "C5", 37: "T7", 38: "TP9", 39: "TP7", 40: "CP5",
    41: "CP3", 42: "CP1", 43: "CPZ", 44: "CP2", 45: "CP4", 46: "CP6", 47: "TP8", 48: "TP10", 49: "P8", 50: "P6",
    51: "P4", 52: "P2", 53: "PZ", 54: "P1", 55: "P3", 56: "P5", 57: "P7", 58: "PO7", 59: "PO3", 60: "POZ",
    61: "PO4", 62: "PO8", 63: "O2", 64: "OZ", 65: "O1"
}

epochs = re.findall(r"\[.*?\]", data)

dices = []

for epo in epochs:
    dices.append(re.findall(r"\(.*?\)", epo))

print(len(dices[0]))
