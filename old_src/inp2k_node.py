import pandas as pd

inp_dir = r"./brick.inp"

node_info_columns = ["id", "x", "y", "z"]
node_df = pd.DataFrame(columns = node_info_columns)

with open(inp_dir,'r') as inp:
    line = inp.readline()
    node_area_flag = False
    while line:
        if line.startswith('*NODE'):
            line = inp.readline()
            node_area_flag = True
        if line.startswith('******* E L E M E N T S *************'):
            break
        if node_area_flag == True:
            info = line.replace(" ", "").replace("\n", "").split(',')
            node_df = node_df.append(dict(zip(node_df.columns, [info[0], info[1], info[2], info[3]])),
                                     ignore_index=True)
            print(f"processing line:{line}")
        line = inp.readline()
    inp.close()

print(node_df)
