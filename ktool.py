"""
This is the function library for writing .k by scripting
Author: CHEN Jiawei, master student
        Materials forming and processing Lab
        The University of Tokyo
"""
def write_loadcurve(kfile_dir, total_time, velocity):
    # ----------------------------------------
    #   Description:
    #       write the load info in .k file
    #
    #   Input:      kfile_dir: keyword file directory
    #               total_time: total load time
    #               velocity: loading velocity for nodes
    #   Output:     .k file for dyna
    # ----------------------------------------
    print("writing load curve info into .k")
    with open(kfile_dir, mode='a') as k:
        k.write("*CONTROL_TERMINATION\n")
        k.write(f"{format(total_time,'.1f')}".rjust(8))
        k.write("         0       0.0       0.01.000000E8         0\n")
        k.write("*DEFINE_CURVE\n")
        k.write("         1         0       1.0       1.0       0.0       0.0         0         0\n")
        k.write("                 0.0                 0.0\n")
        k.write("               0.001")
        k.write(f"{velocity}\n".rjust(20))
        k.write(f"{total_time+0.01}".rjust(20))
        k.write(f"{velocity}\n".rjust(20))
        k.close()

def write_keyword(kfile_dir):
    # ----------------------------------------
    #   Description:
    #       write the keyword card info into .k file
    #       also write other header info into .k file
    #       write energy control info into .k file
    #
    #
    #   Input:      kfile_dir: keyword file directory
    # ----------------------------------------
    print("writing keyword card info into .k")
    with open(kfile_dir, mode='a') as k:
        k.write("$# LS-DYNA Keyword file created by LS-PrePost(R) V4.8.8 - 08Jan2021\n")
        k.write("$# Created on Nov-20-2021 (15:10:53)\n")
        k.write("*KEYWORD MEMORY=1000000000 MEMORY2=1000000000 NCPU=8\n")
        k.write("*TITLE\n")
        k.write("$#                                                                         title\n")
        k.write("*CONTROL_ENERGY\n")
        k.write("         2         2         2         1         2\n")
        k.close()

def write_database(kfile_dir):
    # ----------------------------------------
    #   Description:
    #       write the database card info into .k file
    #        (Define the output file .d3plot, .ndout, etc..)
    #
    #   Input:      kfile_dir: keyword file directory
    # ----------------------------------------
    print("writing keyword card info into .k")
    with open(kfile_dir, mode='a') as k:
        k.write("*DATABASE_BNDOUT\n")
        k.write("       0.0         0         0         1\n")
        k.write("*DATABASE_ELOUT\n")
        k.write("       2.0         0         0         1       270         0         0         0\n")
        k.write("*DATABASE_GLSTAT\n")
        k.write("       0.0         0         0         1\n")
        k.write("*DATABASE_MATSUM\n")
        k.write("       0.0         0         0         1\n")
        k.write("*DATABASE_NODFOR\n")
        k.write("       2.0         3         0         1\n")
        k.write("*DATABASE_NODOUT\n")
        k.write("       2.0         3         0         1       0.0         0\n")
        k.write("*DATABASE_RCFORC\n")
        k.write("       0.0         3         0         1\n")
        k.write("*DATABASE_BINARY_D3PLOT\n")
        k.write("       2.0         0         0         0         0\n")
        k.write("         0       0.0       0.0       0.0         0         0\n")
        k.write("*DATABASE_EXTENT_BINARY\n")
        k.write("       270         0         3         3         1         1         1         1\n")
        k.write("         0         0         0         1         1         1         2         1\n")
        k.write("         0         0       1.0         0         0         0                    \n")
        k.write("         0         0         0         0         0\n")
        k.write("*DATABASE_NODAL_FORCE_GROUP\n")
        k.write("         1         0\n")
        k.write("*DATABASE_HISTORY_NODE_SET\n")
        k.write("         2         0         0         0         0         0         0         0\n")
        k.close()

def write_boundary(kfile_dir):
    # ----------------------------------------
    #   Description:
    #       write the boundary card info into .k file
    #        (Define constrain and load boundary conditions)
    #
    #   Input:      kfile_dir: keyword file directory
    # ----------------------------------------
    print("writing boundary card info into .k")
    with open(kfile_dir, mode='a') as k:
        k.write("*BOUNDARY_PRESCRIBED_MOTION_SET\n")
        k.write("         2         1         0         1       1.0         01.00000E28       0.0\n")
        k.write("*BOUNDARY_SPC_SET\n")
        k.write("         1         0         1         0         0         0         0         0\n")
        k.close()

