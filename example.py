"""
This is the example to use our library
Author: CHEN Jiawei, master student
        Materials forming and processing Lab
        The University of Tokyo
"""
import eulerangle
import inp2k
import ktool
import pandas as pd

# specify the directory of working files
inp_dir = r'./test.inp'
euler_dir = r'./euler.csv'
kfile_dir = r'./polymeshes.k'

# read the data into dataframe
node_df = inp2k.read_node(inp_dir)
elem_df = inp2k.read_element(inp_dir)
grain_df = inp2k.read_grain(inp_dir,len(elem_df))
elemgrain_df = inp2k.read_elemgrain(grain_df)
euler_df = eulerangle.read_euler(euler_dir)

#reordering
node_df,elem_df = inp2k.reordering(node_df,elem_df)
node3d_df, elem3d_df, elemgrain3d_df, grain3d_df = inp2k.kPacking(5,0.2,node_df,elem_df,elemgrain_df,grain_df)


# output the required mesh file and euler angle file
inp2k.write_mesh(kfile_dir,node3d_df,elem3d_df, grain3d_df, euler_df, elemgrain3d_df)
#inp2k.write_mesh(kfile_dir,node_df,elem_df, grain_df, euler_df, elemgrain_df)
eulerangle.write_euler(euler_df)

# write other useful information for lsdyna
ktool.write_boundary(kfile_dir)
ktool.write_database(kfile_dir)
ktool.write_keyword(kfile_dir)
ktool.write_loadcurve(kfile_dir,300,0.2)