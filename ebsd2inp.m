%% import mtex data
mtexdata alu;

%% % create an EBSD variable containing the data
ebsd=ebsd('indexed');

%% Process the grains
% commonly
%grains=calcGrains(ebsd);
% This one calculate grains by misorientation also give id to grains 
[grains,ebsd.grainId,ebsd.mis2mean] = calcGrains(ebsd('indexed'),'angle',5*degree);

% smooth grains
grains = smooth(grains,5);

% remove small grains
ebsd(grains(grains.grainSize<=5)) = [];
[grains,ebsd.grainId,ebsd.mis2mean] = calcGrains(ebsd('indexed'),'angle',5*degree,'removeQuadruplePoints');

%% plotting the map for this simulation
plot(grains,grains.meanOrientation);
colorKey = ipfColorKey(grains.meanOrientation)
plot(colorKey);

%% MTEX2Gmsh
%G=gmshGeo(grains);
%mesh(G,'test.inp','ElementType','HexOnly','ElementSize',1);
%exportGrainProps(G,'euler.csv');