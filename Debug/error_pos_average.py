from io import StringIO
import numpy as np
import pandas as pd

path_NAS = "/home/klemouel/NAS_EMPENN/share/users/klemouel/Stage/"
path_proc = path_NAS + "post_processing/petra_65/pos_errors/"
path_CSV = path_NAS + "Correspondancies_ElectrodeDetection_Dataset.csv"

corr = pd.read_csv(path_CSV)

with open(path_proc + "007_err.txt",'r') as f:
    data = f.read()

def get_err_values(data: str):
    tmp = data.split("\n")
    tmp.pop(-1)
    l = []
    for i in tmp:
        haha = i.split(" ")
        l.append(float(haha[1]))
    return l

def avg(li):
    res = 0
    for i in range(0, len(li)):
        res += li[i]
    return res/len(li)

count = 0
res = 0
for index, row in corr.iterrows():
    if(row['Set'] == "test"):
        id = str(row['Id'])
        id = id.rjust(3,'0')

        with open(path_proc + id +"_err.txt", 'r') as f:
            data = f.read()
        
        count += 1
        res += avg(get_err_values(data))

print(res/count)