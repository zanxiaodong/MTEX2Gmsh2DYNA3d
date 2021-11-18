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
1. Measure your specimen using EBSD machine and input them into MATALB MTEX:
```buildoutcfg
import_wizard('EBSD')
```
For detail, you can see [here](https://mtex-toolbox.github.io/EBSDImport.html).

Or, you can use the EBSD files provided by MTEX, for example: 
```buildoutcfg
mtexdata twins
```
2. Process your data via [MTEX](https://github.com/DorianDepriester/MTEX2Gmsh)  and make 2d Mesh(.inp) via [MTEX2Gmsh](https://github.com/DorianDepriester/MTEX2Gmsh) , see 
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
Here is the figure of a very simple mesh result in 2D:
!()[]

### Contact:
If you have any problems, you can contact me via:

`
garychan[at]iis[dot]u-tokyo[dot]ac[dot]jp
`
