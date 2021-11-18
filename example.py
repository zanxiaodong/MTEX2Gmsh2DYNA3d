import eulerangle
import inp2k
import pandas as pd

# specify the directory of working files
inp_dir = r'./test.inp'
euler_dir = r'./euler.csv'

# read the data into dataframe
node_df = inp2k.read_node(inp_dir)
elem_df = inp2k.read_element(inp_dir)
grain_df = inp2k.read_grain(inp_dir,len(elem_df))
elemgrain_df = inp2k.read_elemgrain(grain_df)
euler_df = eulerangle.read_euler(euler_dir)

#reordering
node_df,elem_df = inp2k.reordering(node_df,elem_df)

# begin new cod
node_info_columns = ["id", "x", "y", "z"]
elem_info_columns = ["id", "nodes"]
elemgrain_df_info_columns = ["elementid","grainid"]
grain_info_columns = ["id", "elements"]
# make 2d node2d_df,elem2d_df
node2d_df = pd.DataFrame(columns = node_info_columns)
elem2d_df = pd.DataFrame(columns= elem_info_columns)

node2d_df = node_df.drop(node_df[node_df['z']=='1'].index)

for i in range(len(elem_df)):
    #print(elem_df.iloc[i]['nodes'])
    vec = []
    for node in elem_df.iloc[i]['nodes']:
        node = int(node)
        node_id_list = [int(i) for i in node2d_df['id'].tolist()]
        if node in node_id_list:
            vec.append(node)
    elem2d_df = elem2d_df.append(dict(zip(elem2d_df.columns, [i+1, vec])),
                                 ignore_index=True)

# make 3d dataframe
node3d_df = pd.DataFrame(columns = node_info_columns)
node3d_df = node2d_df
elem3d_df = pd.DataFrame(columns= elem_info_columns)
grain3d_df = pd.DataFrame(columns= grain_info_columns)
elemgrain3d_df = pd.DataFrame(columns= elemgrain_df_info_columns)
elemgrain3d_df = elemgrain_df

num_layers = 5
thick = 0.2
elem_num = len(elem_df)
node2d_num = len(node2d_df)

for i in range(len(grain_df)):
    grain_id = int(grain_df.iloc[i]['id'])
    elem_list = [int(elem) for elem in grain_df.iloc[i]['elements']]
    elem_vec = []

    for ii in elem_list:
        top_elem_id = ii
        elem = ii

        top_nodes_list = [int(node) for node in elem2d_df.iloc[ii-1]['nodes']]

        for iii in range(num_layers):
            upper_nodes_vec = []
            lower_nodes_vec = []
            elem = elem + iii * elem_num
            elem_vec.append(elem)

            for j in top_nodes_list:
                top_node_id = j
                upper_node_id = j +node2d_num*iii
                lower_node_id = j + node2d_num*(iii+1)
                upper_nodes_vec.append(upper_node_id)
                lower_nodes_vec.append(lower_node_id)

                if lower_node_id not in node3d_df['id'].tolist():

                    # top node coor
                    top_node_x = node2d_df.iloc[top_node_id - 1]['x']
                    top_node_y = node2d_df.iloc[top_node_id - 1]['y']
                    top_node_z = node2d_df.iloc[top_node_id - 1]['z']

                    # lower node coor
                    lower_node_z = float(top_node_z) + thick * (iii+1)

                    node3d_df = node3d_df.append(dict(zip(node_df.columns,
                    [lower_node_id, top_node_x, top_node_y, lower_node_z])),ignore_index=True)

            nodes_vec = upper_nodes_vec + lower_nodes_vec
            elem3d_df = elem3d_df.append(dict(zip(elem_df.columns, [elem, nodes_vec])), ignore_index=True)
            elemgrain3d_df = elemgrain3d_df.append(dict(zip(elemgrain_df.columns, [elem, grain_id])), ignore_index=True)

    grain3d_df = grain3d_df.append(dict(zip(grain_df.columns, [grain_id, elem_vec])), ignore_index=True)

#print(elemgrain3d_df)

# reordering the elem3d, elemgrain3d, grain3d

# output the required mesh file and euler angle file
inp2k.write_mesh(node3d_df,elem3d_df, grain3d_df, euler_df, elemgrain3d_df)
#inp2k.write_mesh(node_df,elem_df, grain_df, euler_df, elemgrain_df)
#eulerangle.write_euler(euler_df)