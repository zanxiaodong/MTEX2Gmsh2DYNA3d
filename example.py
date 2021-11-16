import eulerangle
import inp2k

# specify the directory of working files
inp_dir = r'./test.inp'
euler_dir = r'./euler.csv'

# read the data into dataframe
node_df = inp2k.read_node(inp_dir)
elem_df = inp2k.read_element(inp_dir)
grain_df = inp2k.read_grain(inp_dir,len(elem_df))
elemgrain_df = inp2k.read_elemgrain(grain_df)
euler_df = eulerangle.read_euler(euler_dir)

# output the required mesh file and euler angle file
inp2k.write_mesh(node_df,elem_df, grain_df, euler_df, elemgrain_df)
eulerangle.write_euler(euler_df)