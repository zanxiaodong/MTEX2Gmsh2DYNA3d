import pandas as pd

inp_dir = r"./brick.inp"

elem_info_columns = ["id", "nodes"]
elem_df = pd.DataFrame(columns = elem_info_columns)

with open(inp_dir,'r') as inp:
    line = inp.readline()
    elem_area_flag = False
    id = 1
    while line:
        if line.startswith('******* E L E M E N T S *************'):
            elem_area_flag = True
        if elem_area_flag == True:
            if line.startswith(f'{id}'):
                info = line.replace(" ", "").replace("\n", "").split(',')
                elem_df = elem_df.append(dict(zip(elem_df.columns, [info[0], info[1:]])),
                                         ignore_index=True)
                print(f"processing line:{line}")
                id = id + 1
        if line.startswith('*ELSET,ELSET=Grain_1'):
            break
        line = inp.readline()

print(elem_df)