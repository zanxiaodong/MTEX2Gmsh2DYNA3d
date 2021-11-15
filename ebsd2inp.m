%mtexdata forsterite
mtexdata twins
[grains, ebsd('indexed').grainId]=calcGrains(ebsd('indexed'));
ebsd(grains(grains.grainSize<5))=[];
grains=calcGrains(ebsd('indexed'));
mesh(G,'twins.inp','ElementType','HexOnly','ElementSize',1);
exportGrainProps(G,'euler.csv');