%% This code is created by Mayur Gaikwad| 16D100008 as a part of dual degree project 
clear all;
clc;
close all;

%% initialise the surface to perform the error estimate
%lets try for a ripple surface centered at origin
grid_res=0.0001;
d=0.1 ; %Damping factor
[X,Y] = meshgrid(-1:grid_res:1, -1:grid_res:1);
k=10; %initial amplitude for ripple
r=sqrt(X.*X + Y.*Y);
ripple=k*exp(-1.0*d*r).*cos(deg2rad(r));
surf(X,Y,ripple)
res= [grid_res mean(mean(ripple))];

%% Matching check by fitting a plane parallel to XY i.e z= contant ==> will geometrically be z avg
for i=2:10
    [X1,Y1] = meshgrid(-2:grid_res*i:2, -2:grid_res*i:2);
    r1=sqrt((X1).^2 + (Y1).^2);
    Z1=k*exp(-1.0*d*r1).*cos(r1);
    res=[res;[grid_res*i  mean(mean(Z1))]];
end
figure;
plot(res(:,1),res(:,2))

% [X,Y] = meshgrid(-2:0.1:2, -2:0.1:2);
