"""
This is the function library for multi layers of meshes
Author: CHEN Jiawei, master student
        Materials forming and processing Lab
        The University of Tokyo
"""

import pandas as pd

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
    return node3d_df,elem3d_df,elemgrain3d_df,grain3d_df