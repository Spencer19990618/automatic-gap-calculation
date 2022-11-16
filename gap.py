import argparse
import os
import statistics as stc
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('-i', "--ip_path", help="the directory where the xlsx files are in", type=str)
parser.add_argument('-o', "--op_path", help="the directory to save the outcome", type=str)
args = parser.parse_args()

def remove_ds_store(lst):
    """remove mac specific file if present"""
    if '.DS_Store' in lst:
        lst.remove('.DS_Store')
    return lst

def main():
    ip_path = args.ip_path
    op_path  = args.op_path
    file_list = os.listdir(ip_path)
    file_list = remove_ds_store(file_list)

    name_list = []
    max_list = []
    min_list = []
    mid_list = []
    mean_list = []

    for file in file_list:
        file_path = os.path.join(ip_path, file)
        df = pd.read_excel(file_path, index_col=0)
        start = np.array(df['Start'])
        end = np.array(df['End'])

        file_name = file[-23:-16]
        gap = []
        for i in range(len(start)-1):
            gap.append(start[i+1]-end[i])

        name_list.append(file_name)
        min_list.append(np.min(gap))
        max_list.append(np.max(gap))
        mid_list.append(stc.median(gap))
        mean_list.append(np.mean(gap))
        
    
    outcome = pd.DataFrame({'file': name_list, 'min': min_list, 'max': max_list, 'mid':mid_list, 'mean':mean_list})
    op_path = os.path.join(op_path,'output.csv')
    outcome.to_csv(op_path)  


if __name__=='__main__':
    main()