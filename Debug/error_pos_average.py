import numpy as np
import pandas as pd

path_NAS = "/home/klemouel/NAS_EMPENN/share/users/klemouel/Stage/"
path_proc = path_NAS + "post_processing/T1_65/pos_errors/"
path_CSV = path_NAS + "Correspondancies_ElectrodeDetection_Dataset.csv"

corr = pd.read_csv(path_CSV)
database = []
l = []

def load_all_data():
    for i, row in corr.iterrows():
        if(row['Set'] == "test"):
            id = str(row['Id'])
            id = id.rjust(3,'0')

            with open(path_proc + id +"_err.txt", 'r') as f:
                data = f.read()
                database.append(data)

def get_err_values(data: str):
    tmp = data.split("\n")
    tmp.pop(-1)
    l = []
    for i in tmp:
        haha = i.split(" ")
        l.append(float(haha[1]))
    return l

def get_values_dict(data: str):
    tmp = data.split("\n")
    tmp.pop(-1)
    d = {}
    for i in tmp:
        hehe = i.split(" ")
        d[float(hehe[0])] = float(hehe[1])
    return d

def avg(li):
    res = 0
    for i in range(0, len(li)):
        res += li[i]
    return res/len(li)

def count_average():
    res = 0
    for data in database:
        res += avg(get_err_values(data))
    return res/len(database)

# print(count_average())

def __main__():
    sorted_list = []
    vals = []
    for data in database:
        d = get_values_dict(data)
        sorted_list = sorted(d)
        tmp = []
        for i in sorted_list:
            tmp.append(d[i])
        vals.append(tmp)

    for m in range(0, len(sorted_list)-1):
        res = []
        for n in range(0, len(vals)-1):
            res.append(vals[n][m])
        l.append(res)
    return None

__main__()

print(l)