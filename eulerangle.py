
import pandas as pd
import csv

euler_dir = r'C:\Users\Gary\Desktop\polycrystalline modelling\MTEX2Gmsh\euler.csv'
euler_info_columns = ["id","e1","e2","e3"]
euler_df = pd.DataFrame(columns = euler_info_columns)

with open(euler_dir,'r') as euler:

    title_str = 'GrainID\tPhase\tphi1\tPhi\tphi2'
    raw_euler_df = pd.read_csv(euler)[title_str]

    for i in range(len(raw_euler_df)):
        info = raw_euler_df[i].split('\t')
        euler_df.at[i, 'id'] = info[0]
        euler_df.at[i, 'e1'] = info[2]
        euler_df.at[i, 'e2'] = info[3]
        euler_df.at[i, 'e3'] = info[4]
        print(f'Reading euler angle {info[0]}')
    euler.close()

euler_angle_dir = r'.\Euler_angle.csv'
with open(euler_angle_dir, 'w',newline='') as csvfile:
    csvwriter = csv.writer(csvfile,delimiter=',')

    for i in range(len(euler_df)):
        csvwriter.writerow(euler_df[['e1','e2','e3']].iloc[i])
        print(f'Writing euler angle {euler_df.iloc[i]}')

    csvfile.close()





