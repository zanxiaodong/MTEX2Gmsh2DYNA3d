# MTEX2Gmsh2DYNA3d
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
#### 1. 
Measure your specimen using EBSD machine and input them into MATALB MTEX:
```buildoutcfg
import_wizard('EBSD')
```
For detail, you can see [here](https://mtex-toolbox.github.io/EBSDImport.html).

Or, you can use the EBSD files provided by MTEX, for example: 
```buildoutcfg
mtexdata twins
```
Here is the figure of a very simple EBSD result:
![](https://github.com/MaynotbeGarychan/MTEX2Gmsh2DYNA3d/blob/main/fig/ebsdmtex.JPG)
#### 2.
Process your data via [MTEX](https://github.com/DorianDepriester/MTEX2Gmsh)  and make 2d Mesh(.inp) via [MTEX2Gmsh](https://github.com/DorianDepriester/MTEX2Gmsh) , see 
[MATLAB code](https://github.com/MaynotbeGarychan/MTEX2Gmsh2DYNA3d/blob/main/ebsd2inp.m)
 here:
```buildoutcfg
% import via MTEX
mtexdata twins

% process the grain in ebsd via MTEX
[grains, ebsd('indexed').grainId]=calcGrains(ebsd('indexed'));
ebsd(grains(grains.grainSize<5))=[];

% select region via MTEX
poly = [44 0 4 2];
ebsd = ebsd(inpolygon(ebsd,poly));

% make 2d mesh via MTEX2Gmsh
grains=calcGrains(ebsd('indexed'));
G=gmshGeo(grains);
mesh(G,'test.inp','ElementType','HexOnly','ElementSize',0.2);
exportGrainProps(G,'euler.csv');
```
If you need more details about how to use MTEX2Gmsh 
to make 2d mesh via MATLAB code, 
you can see [here](https://doriandepriester.github.io/MTEX2Gmsh/html/index.html).
They provide a good documentation.

#### 3. 
Make 3d mesh by using my functions, 
see a simple example in
[code](https://github.com/MaynotbeGarychan/MTEX2Gmsh2DYNA3d/blob/main/example.py).

Import the function library of our codes, 
[inp2k](https://github.com/MaynotbeGarychan/MTEX2Gmsh2DYNA3d/blob/main/inp2k.py)
for meshing and [eulerangle](https://github.com/MaynotbeGarychan/MTEX2Gmsh2DYNA3d/blob/main/eulerangle.py)
for process the euler angle by MTEX2Gmsh
:
```buildoutcfg
import eulerangle
import inp2k
```
Specify your working file, mesh from .inp and euler angle from .csv:
```buildoutcfg
inp_dir = r'./test.inp'
euler_dir = r'./euler.csv'
```
Read the data into dataframe from .inp and .csv:
```buildoutcfg
node_df = inp2k.read_node(inp_dir)
elem_df = inp2k.read_element(inp_dir)
grain_df = inp2k.read_grain(inp_dir,len(elem_df))
elemgrain_df = inp2k.read_elemgrain(grain_df)
euler_df = eulerangle.read_euler(euler_dir)
```
In order to make 3d mesh, we have to reorder the dataframe
```buildoutcfg
node_df,elem_df = inp2k.reordering(node_df,elem_df)
```
Make dataframe of 3d mesh based on dataframe of 2d mesh:
```buildoutcfg
num_layers = 5
thick = 0.1
node3d_df, elem3d_df, elemgrain3d_df, grain3d_df = inp2k.kPacking(num_layers,thick,node_df,elem_df,elemgrain_df,grain_df)
```
Output the 3d mesh and euler angle:
```buildoutcfg
inp2k.write_mesh(node3d_df,elem3d_df, grain3d_df, euler_df, elemgrain3d_df)
eulerangle.write_euler(euler_df)
```
Here is the results of 3d mesh:
![](https://github.com/MaynotbeGarychan/MTEX2Gmsh2DYNA3d/blob/main/fig/3dmesh.JPG)
#### Extra:
Also, you can just output the 2d mesh by using:
```buildoutcfg
inp2k.write_mesh(node_df,elem_df, grain_df, euler_df, elemgrain_df)
```
Here is the results of 2d mesh:
![](https://github.com/MaynotbeGarychan/MTEX2Gmsh2DYNA3d/blob/main/fig/2dmesh.JPG)

### Contact:
If you have any problems, you can contact me via:

`
garychan[at]iis[dot]u-tokyo[dot]ac[dot]jp
`
