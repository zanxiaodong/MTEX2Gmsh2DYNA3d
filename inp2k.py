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
    print("reading node info.")
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
                #print(f"reading {info[0]} node info")
            line = inp.readline()
        inp.close()
    print("finish reading node info.")
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
    print("reading elem info.")
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
                    #print(f"reading {info[0]} elem info")
                    id = id + 1
            if line.startswith('*ELSET,ELSET=Grain_1'):
                break
            line = inp.readline()
        inp.close()
    print("finish reading elem info.")
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
    print("reading grain info.")
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
                    #print(f"reading {id} grain info")
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
    print("finish reading grain info.")
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
    print("reading elemgrain info.")
    for i in range(len(grain_df)):
        vec = grain_df.iloc[i]['elements']
        grainid = grain_df.iloc[i]['id']
        for ii in range(len(vec)):
            elemgrain_df = elemgrain_df.append(dict(zip(elemgrain_df.columns, [vec[ii], grainid]))
                                               , ignore_index=True)
            #print(f'finding grain for element{vec[ii]}')
    print("finish reading elemgrain info.")
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
    print("writing grain info into .k")
    with open(kfile_dir, 'w') as k:
        for i in range(len(grain_df)):
            pid = grain_df.iloc[i]["id"]
            #print(f"writing {pid} grain info into .k")
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
        print("writing elem info into .k")
        k.write("*ELEMENT_SOLID\n")
        k.write("$#   eid     pid      n1      n2      n3      n4      n5      n6      n7      n8\n")
        for i in range(elem_num):
            #print(f"writing {elem_df.iloc[i]['id']} elem info into .k")
            k.write(f"{elem_df.iloc[i]['id']}".rjust(8))

            pos = elemgrain_df[elemgrain_df.elementid == elem_df.iloc[i]['id']].index.tolist()[0]
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
            #print(f"writing {node_df.iloc[i]['id']} node into .k")

            k.write(f"{id}".rjust(8))
            k.write(f"{x}".rjust(16))
            k.write(f"{y}".rjust(16))
            k.write(f"{z}".rjust(16))
            k.write("       0")
            k.write("       0")
            k.write('\n')
        k.close()
        print("finish writing meshes into .k.")



def reordering(node_df,elem_df):
    # ----------------------------------------
    #   Description:
    #       reordering node id by its z,x,y coordinate,
    #       replace the new node id to elem_df
    #
    #   Input:      Dataframe node_df, col = ["id", "nodes"]
    #               Dataframe elem_df, col = ["id", "nodes"]
    #
    #   Output:     Reordered dataframe node_df, col = ["id", "nodes"]
    #               Reordered dataframe elem_df, col = ["id", "nodes"]
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


def kPacking(num_layers,thick,node_df,elem_df,elemgrain_df,grain_df):
    # ----------------------------------------
    #   Description:
    #       Make 3d mesh based on 2d mesh info
    #
    #   Input:      num_layer: Number of Meshes layers
    #               thick: thickness of one layer
    #               Reordered dataframe node_df, col = ["id", "x", "y", "z"]
    #               Reordered dataframe elem_df, col = ["id", "nodes"]
    #               Dataframe elemgrain_df, col = ["elementid", "grainid"]
    #               Dataframe grain_df, col = ["id", "elements"]
    #
    #   Output:     [0] : Dataframe node3d_df, col = ["id", "x", "y", "z"]
    #               [1] : Dataframe elem3d_df, col = ["id", "nodes"]
    #               [2] : Dataframe elemgrain3d_df, col = ["elementid", "grainid"]
    #               [3] : Dataframe grain3d_df, col = ["id", "elements"]
    # ----------------------------------------
    #define columns
    node_info_columns = ["id", "x", "y", "z"]
    elem_info_columns = ["id", "nodes"]
    elemgrain_df_info_columns = ["elementid", "grainid"]
    grain_info_columns = ["id", "elements"]

    # make dataframe for 2d node and element
    node2d_df = pd.DataFrame(columns=node_info_columns)
    elem2d_df = pd.DataFrame(columns=elem_info_columns)

    # store data into node2d_df and elem2d_df
    node2d_df = node_df.drop(node_df[node_df['z'] != '0'].index)
    for i in range(len(elem_df)):
        vec = []
        for node in elem_df.iloc[i]['nodes']:
            node = int(node)
            node_id_list = [int(i) for i in node2d_df['id'].tolist()]
            if node in node_id_list:
                vec.append(node)
        elem2d_df = elem2d_df.append(dict(zip(elem2d_df.columns, [i + 1, vec])),
                                     ignore_index=True)

    # make dataframe for 3d node, element, grain
    elem3d_df = pd.DataFrame(columns=elem_info_columns)
    grain3d_df = pd.DataFrame(columns=grain_info_columns)
    # the first layer node and the grain not change
    node3d_df = node2d_df
    elemgrain3d_df = elemgrain_df

    # useful parameter
    elem_num = len(elem_df)
    node2d_num = len(node2d_df)

    # store data into node3d_df, elem3d_df, elemgrain3d_df, grain3d_df
    print("begin to pack 3d meshes.")
    for i in range(len(grain_df)):
        grain_id = int(grain_df.iloc[i]['id'])
        elem_list = [int(elem) for elem in grain_df.iloc[i]['elements']]
        elem_vec = []

        for ii in elem_list:
            top_elem_id = ii
            elem = ii

            top_nodes_list = [int(node) for node in elem2d_df.iloc[ii - 1]['nodes']]

            for iii in range(num_layers):
                upper_nodes_vec = []
                lower_nodes_vec = []
                elem = elem + iii * elem_num
                elem_vec.append(elem)

                for j in top_nodes_list:
                    top_node_id = j
                    upper_node_id = j + node2d_num * iii
                    lower_node_id = j + node2d_num * (iii + 1)
                    upper_nodes_vec.append(upper_node_id)
                    lower_nodes_vec.append(lower_node_id)

                    if lower_node_id not in node3d_df['id'].tolist():
                        # top node coor
                        top_node_x = node2d_df.iloc[top_node_id - 1]['x']
                        top_node_y = node2d_df.iloc[top_node_id - 1]['y']
                        top_node_z = 0.0

                        # lower node coor
                        lower_node_z = top_node_z + thick * (iii + 1)

                        node3d_df = node3d_df.append(dict(zip(node_df.columns,
                                                              [lower_node_id, top_node_x, top_node_y, lower_node_z])),
                                                     ignore_index=True)

                nodes_vec = upper_nodes_vec + lower_nodes_vec
                elem3d_df = elem3d_df.append(dict(zip(elem_df.columns, [elem, nodes_vec])), ignore_index=True)
                elemgrain3d_df = elemgrain3d_df.append(dict(zip(elemgrain_df.columns, [elem, grain_id])),
                                                       ignore_index=True)

        grain3d_df = grain3d_df.append(dict(zip(grain_df.columns, [grain_id, elem_vec])), ignore_index=True)
        print("finish packing 3d meshes.")
    return node3d_df,elem3d_df,elemgrain3d_df,grain3d_df