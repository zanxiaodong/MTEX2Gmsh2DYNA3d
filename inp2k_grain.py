import pandas as pd

inp_dir = r"./brick.inp"

grain_info_columns = ["id", "elements"]
grain_df = pd.DataFrame(columns = grain_info_columns)

with open(inp_dir,'r') as inp:
    line = inp.readline()
    grain_area_flag = False
    id = 1
    vec = []
    while line:
        if line.startswith(f'*ELSET,ELSET=Grain_{id}'):
            if id != 1:
                grain_df = grain_df.append(dict(zip(grain_df.columns, [id-1, vec]))
                                           , ignore_index=True)
            id = id +1
            vec = []
            print(f"processing grain:{line}")
            line = inp.readline()
        info = line.replace("\n", "").replace(" ", "").split(',')[:-1]
        vec += info
        line = inp.readline()
    inp.close()

print(grain_df)