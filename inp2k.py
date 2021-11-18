"""
This is the function library for converting .inp to .k
Author: CHEN Jiawei, master student
        Materials forming and processing Lab
        The University of Tokyo
"""
import pandas as pd
import csv
import sys

def read_node(inp_dir):
    # ----------------------------------------
    #   Description:
    #       Read mesh node information from .inp,
    #
    #   Input:      .csv file
    #   Output:     Dataframe node_df
    #               col = [Nodeid, x coor, y coor, z coor]
    # ----------------------------------------
    node_info_columns = ["id", "x", "y", "z"]
    node_df = pd.DataFrame(columns=node_info_columns)
    with open(inp_dir, 'r') as inp:
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
    return node_df



def read_element(inp_dir):
    # ----------------------------------------
    #   Description:
    #       Read mesh element information from .inp,
    #
    #   Input:      .csv file
    #   Output:     Dataframe elem_df
    #               col = ["id", "nodes"]
    # ----------------------------------------
    elem_info_columns = ["id", "nodes"]
    elem_df = pd.DataFrame(columns=elem_info_columns)

    with open(inp_dir, 'r') as inp:
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
    return elem_df



def read_grain(inp_dir,num_elem):
    # ----------------------------------------
    #   Description:
    #       Read mesh grain information from .inp,
    #
    #   Input:      .csv file
    #   Output:     Dataframe grain_df
    #               col = [Grain id,[Element id * n]]
    # ----------------------------------------
    grain_info_columns = ["id", "elements"]
    grain_df = pd.DataFrame(columns=grain_info_columns)
    max_elemid = num_elem
    with open(inp_dir, 'r') as inp:
        line = inp.readline()
        grain_area_flag = False
        id = 1
        vec = []
        while line:
            if line.endswith("*ELSET,ELSET=Grain_1\n"):
                grain_area_flag = True
                line = inp.readline()

            if grain_area_flag == True:
                if line.endswith(f"*ELSET,ELSET=Grain_{id + 1}\n"):
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

    return grain_df



def read_elemgrain(grain_df):
    # ----------------------------------------
    #   Description:
    #       Read mesh grain information from .inp,
    #           for which grain it belongs to
    #
    #   Input:      Dataframe grain_df
    #               col = [Grain id,[Element id * n]]
    #   Output:     Dataframe elemgrain_df
    #               col = ["elementid","grainid"]
    # ----------------------------------------
    elemgrain_df_info_columns = ["elementid", "grainid"]
    elemgrain_df = pd.DataFrame(columns=elemgrain_df_info_columns)

    for i in range(len(grain_df)):
        vec = grain_df.iloc[i]['elements']
        grainid = grain_df.iloc[i]['id']
        for ii in range(len(vec)):
            elemgrain_df = elemgrain_df.append(dict(zip(elemgrain_df.columns, [vec[ii], grainid]))
                                               , ignore_index=True)
            print(f'finding grain for element{vec[ii]}')
    return elemgrain_df



def write_mesh(node_df,elem_df,grain_df,euler_df,elemgrain_df):
    # ----------------------------------------
    #   Description:
    #       write the mesh info in .k file
    #
    #   Input:      Dataframe node_df, col = ["id", "nodes"]
    #               Dataframe elem_df, col = ["id", "nodes"]
    #               Dataframe grain_df, col = [Grain id,[Element id * n]]
    #               Dataframe euler_df, col = ["id","e1","e2","e3"]
    #               Dataframe elemgrain_df, col = ["elementid","grainid"]
    #   Output:     .k file for dyna
    # ----------------------------------------

    kfile_dir = r'./polymesh.k'
    """
    Reading .inp Review
    """
    node_num = len(node_df.index)
    elem_num = len(elem_df.index)
    grain_num = len(grain_df.index)
    grain_num_ebsd = len(euler_df)
    print(f"successfully reading this file, with {grain_num} grains, {elem_num} elements, {node_num} nodes")

    if grain_num_ebsd != grain_num:
        sys.exit("grain num is not match in .csv and .inp")

    """
    Write .k grain
        grain_info_columns = ["id", "elements"]
    """
    with open(kfile_dir, 'w') as k:
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

            pos = elemgrain_df[elemgrain_df.elementid == elem_df.iloc[i]['id']].index.tolist()[0]
            print(pos)
            k.write(f"{elemgrain_df.iloc[pos]['grainid']}".rjust(8))

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

def reordering(node_df,elem_df):
    # ----------------------------------------
    #   Description:
    #       reordering node id by its z,x,y coordinate,
    #       replace the new node id to elem_df
    #
    #   Input:      Dataframe node_df, col = ["id", "nodes"]
    #               Dataframe elem_df, col = ["id", "nodes"]
    #
    #   Output:     Dataframe node_df, col = ["id", "nodes"]
    #               Dataframe elem_df, col = ["id", "nodes"]
    # ----------------------------------------
    node_info_columns = ["id", "x", "y", "z"]
    elem_info_columns = ["id", "nodes"]
    # reordering the node2d
    node_oldid_list = []  # index: newid-1 value: oldid
    node_df_ro = node_df
    node_df_ro.sort_values(by=["z", "x", "y"], inplace=True)
    # make new dataframe with reordering node id
    new_node_df = pd.DataFrame(columns=node_info_columns)
    print("reordering node dataframe")
    for i in range(len(node_df)):
        xcoor = node_df_ro.iloc[i]["x"]
        ycoor = node_df_ro.iloc[i]["y"]
        zcoor = node_df_ro.iloc[i]["z"]
        node_oldid_list.append(int(node_df_ro.iloc[i]["id"]))
        new_node_df = new_node_df.append(dict(zip(node_info_columns, [i + 1, xcoor, ycoor, zcoor])), ignore_index=True)
    # replace the old node id with new node id
    print("reordering element dataframe")
    new_elem_df = pd.DataFrame(columns=elem_info_columns)
    for i in range(len(elem_df)):
        elem_id = elem_df.iloc[i]["id"]
        old_node_list = elem_df.iloc[i]["nodes"]
        vec = []
        for ii in old_node_list:
            old_node_id = int(ii)
            new_node_id = node_oldid_list.index(old_node_id)+1
            vec.append(new_node_id)
        new_elem_df = new_elem_df.append(dict(zip(elem_df.columns, [elem_id, vec])), ignore_index=True)
    print("finish reordering")
    return new_node_df,new_elem_df