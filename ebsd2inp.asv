%mtexdata forsterite
mtexdata twins

[grains, ebsd('indexed').grainId]=calcGrains(ebsd('indexed'));
ebsd(grains(grains.grainSize<5))=[];

%select region
poly = [44 0 4 2];
ebsd = ebsd(inpolygon(ebsd,poly));

grains=calcGrains(ebsd('indexed'));
G=gmshGeo(grains);
mesh(G,'test.inp','ElementType','HexOnly','ElementSize',1);
exportGrainProps(G,'euler.csv');