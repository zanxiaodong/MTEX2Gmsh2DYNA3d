
"""
Input dir
    Please specify it every time
"""
inp_dir = r"./du.inp"
euler_dir = r'./du_euler.csv'

"""
Output dir
    Please specify it every time
"""
euler_angle_dir = r'.\Euler_angle_du.csv'
kfile_dir = r'.\EBSD_mesh_du.k'


"""
Node from .inp to .k
    DataStructure: [Nodeid, x coor, y coor, z coor]
"""
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
            print(f"reading {info[0]} node info")
        line = inp.readline()
    inp.close()

"""
Element from .inp to .k
    DataStructure: [Element id,[Node id * 8]]
"""
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
                print(f"reading {info[0]} elem info")
                id = id + 1
        if line.startswith('*ELSET,ELSET=Grain_1'):
            break
        line = inp.readline()
    inp.close()

"""
Grain from .inp to .k
    grain_df: DataStructure: [Grain id,[Element id * n]]
    elemgrain_df: DataStructure: [elementid,grainid]
"""
grain_info_columns = ["id", "elements"]
grain_df = pd.DataFrame(columns = grain_info_columns)
max_elemid = len(elem_df.index)
with open(inp_dir,'r') as inp:
    line = inp.readline()
    grain_area_flag = False
    id = 1
    vec = []
    while line:
        if line.endswith("*ELSET,ELSET=Grain_1\n"):
            grain_area_flag = True
            line = inp.readline()

        if grain_area_flag == True:
            if line.endswith(f"*ELSET,ELSET=Grain_{id+1}\n"):
                grain_df = grain_df.append(dict(zip(grain_df.columns, [id, vec]))
                                           , ignore_index=True)
                print(f"reading {id} grain info")
                vec = []
                id = id + 1
                line = inp.readline()

            info = line.replace("\n", "").replace(" ", "").split(',')[:-1]
            vec += info

        if vec[-1:] == [f'{max_elemid}']:
            grain_df = grain_df.append(dict(zip(grain_df.columns, [id, vec]))
                                       , ignore_index=True)

        line = inp.readline()
    inp.close()


elemgrain_df_info_columns = ["elementid","grainid"]
elemgrain_df = pd.DataFrame(columns = elemgrain_df_info_columns)

for i in range(len(grain_df)):
    vec = grain_df.iloc[i]['elements']
    grainid = grain_df.iloc[i]['id']
    for ii in range(len(vec)):
        elemgrain_df = elemgrain_df.append(dict(zip(elemgrain_df.columns, [vec[ii], grainid]))
                                           , ignore_index=True)
        print(f'finding grain for element{vec[ii]}')

print(elemgrain_df)

"""
Reading euler angle
    Data Structure: ["id","e1","e2","e3"]
"""
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


"""
Reading .inp Review
"""
node_num = len(node_df.index)
elem_num = len(elem_df.index)
grain_num = len(grain_df.index)
grain_num_ebsd = len(euler_df)
print(f"successfully reading this file, with {grain_num} grains, {elem_num} elements, {node_num} nodes")

if grain_num_ebsd!=grain_num:
    sys.exit("grain num is not match in .csv and .inp")

"""
Write .k grain
    grain_info_columns = ["id", "elements"]
"""
with open(kfile_dir,'w') as k:
    for i in range(len(grain_df)):
        pid = grain_df.iloc[i]["id"]
        print(f"writing {pid} grain info into .k")
        k.write("*PART\n")
        k.write("$#                                                                         title\n")
        k.write(f"boxsolid_{pid}\n")
        k.write("$#     pid     secid       mid     eosid      hgid      grav    adpopt      tmid\n")
        k.write(f"{pid}".rjust(10))
        k.write(f"1".rjust(10))
        k.write(f"{pid}".rjust(10))
        k.write("         0         0         0         0         0\n")
        k.write("*MAT_USER_DEFINED_MATERIAL_MODELS_TITLE\n")
        k.write(f"umat43_{pid}\n")
        k.write("$#     mid        ro        mt       lmc       nhv    iortho     ibulk        ig\n")
        k.write(f"{pid}".rjust(10))
        k.write(f"0.027".rjust(10))
        k.write("        43        16       270         0         3         4\n")
        k.write("$#   ivect     ifail    itherm    ihyper      ieos      lmca    unused    unused\n")
        k.write("         0         0         0         1         0         0                    \n")
        k.write("$#      p1        p2        p3        p4        p5        p6        p7        p8\n")
        k.write("     70000       0.3  58333.33  26923.08     0.001      42.0      0.02     240.0\n")
        k.write("$#      p1        p2        p3        p4        p5        p6        p7        p8\n")
        k.write("      78.0       0.0       1.4       0.1       0.0       0.0")
        k.write(f"{pid}.0".rjust(10))
        k.write("       0.0\n")

    """
    Write .k element
        elem_info_columns = ["id", "nodes"]
        elemgrain_df_info_columns = ["elementid","grainid"]
    """
    k.write("*ELEMENT_SOLID\n")
    k.write("$#   eid     pid      n1      n2      n3      n4      n5      n6      n7      n8\n")
    for i in range(elem_num):
        print(f"writing {elem_df.iloc[i]['id']} elem info into .k")
        k.write(f"{elem_df.iloc[i]['id']}".rjust(8))
        k.write(f"{elemgrain_df.iloc[i]['grainid']}".rjust(8))
        for nodeid in range(len(elem_df.iloc[i]['nodes'])):
            k.write(f"{elem_df.iloc[i]['nodes'][nodeid]}".rjust(8))
        k.write('\n')
    """
    Write .k node
        node_info_columns = ["id", "x", "y", "z"]
    """
    print("writing node info into .k")
    k.write("*NODE\n")
    k.write("$#   nid               x               y               z      tc      rc  \n")
    for i in range(node_num):
        id = node_df.iloc[i]['id']
        x = node_df.iloc[i]['x']
        x = '%s' % float('%.6g' % float(x))
        y = node_df.iloc[i]['y']
        y = '%s' % float('%.6g' % float(y))
        z = node_df.iloc[i]['z']
        z = '%s' % float('%.5g' % float(z))
        print(f"writing {node_df.iloc[i]['id']} node into .k")

        k.write(f"{id}".rjust(8))
        k.write(f"{x}".rjust(16))
        k.write(f"{y}".rjust(16))
        k.write(f"{z}".rjust(16))
        k.write("       0")
        k.write("       0")
        k.write('\n')
    k.close()

"""
Writing euler angle
"""
with open(euler_angle_dir, 'w',newline='') as csvfile:
    csvwriter = csv.writer(csvfile,delimiter=',')

    for i in range(len(euler_df)):
        csvwriter.writerow(euler_df[['e1','e2','e3']].iloc[i])
        print(f'Writing euler angle {euler_df.iloc[i]}')

    csvfile.close()