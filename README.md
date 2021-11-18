# MTEX2Gmsh_dyna
###Author:
        CHEN Jiawei, Master student in Mechnical Engineering,
        Materials Forming and Processing Lab, 
        Institute of Industrial Science,
        The University of Tokyo.
###Short Description:
1. Converting meshing from .inp(Abaqus) to .k(DYNA).
2. Writing 3d polycrystal mesh based on 2d polycrystal mesh
3. Making .csv for input euler angle of UMAT.
### Dependencies:
In order to use my functions, you have to install these in your environment:
1. [MTEX](https://mtex-toolbox.github.io/)
2. [Gmsh](http://gmsh.info/)
3. [MTEX2Gmsh](https://github.com/DorianDepriester/MTEX2Gmsh) 
### How it works:
1. Measure your specimen using EBSD machine and input them into MATALB MTEX:
```buildoutcfg
import_wizard('EBSD')
```
For detail, you can see [here](https://mtex-toolbox.github.io/EBSDImport.html).

Or, you can use the EBSD files provided by MTEX, for example: 
```buildoutcfg
mtexdata twins
```
2. Process your data via MATLAB MTEX, see ![]()
3.  

### Contact:
If you have any problems, you can contact me via:

`
garychan[at]iis[dot]u-tokyo[dot]ac[dot]jp
`
