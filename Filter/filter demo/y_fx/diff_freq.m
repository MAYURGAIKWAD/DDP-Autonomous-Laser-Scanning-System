%% This code is created by Mayur Gaikwad | 16D100008 for Dual Degree Project (filter implementation on real values)
clear all:
clc;
close all;
%% Input parameters (semicircular arc from (0,0) to (2,0)
y_points=20; %scanner frequency
x_points=6;
ty=linspace(0,0.5,y_points+1);
phase=1/y_points/2;
tx=linspace(0,0.5,x_points+1);
%% theoretical values (we look for the values at t1)
%Curve equation = (x-1)^2 + y^2 = 1^2
ytheo=sin(pi*ty);
xtheo=1-sqrt(1-ytheo.*ytheo);
xact=1-cos(pi*tx);
%xarr=[xact; tx];
xfin=ones(1,y_points+1);
%% linear interpolation values of x at each y
%prev=xarr(2,1);
previndex=1;
%next=xarr(2,2);
nextindex=2;
i=1;
while i <=y_points
    if ty(i)>tx(nextindex)
        previndex=nextindex;
        nextindex=nextindex+1;
    elseif ty(i)==tx(previndex)
        xfin(i)=xact(previndex);
        i=i+1;
        
    elseif ty(i)==tx(nextindex)
        xfin(i)=xact(nextindex);
        previndex=nextindex;
        nextindex=nextindex+1;
        i=i+1;
    else
        xfin(i)=((xact(nextindex)-xact(previndex))/(tx(nextindex)-tx(previndex)))*(ty(i)-tx(previndex))+ xact(previndex);
        i=i+1;
    end
end
%y_lin= (y(1:y_points)+y(2:y_points+1))/2;
Rmse_lin= sqrt(sum((xfin-xtheo).^2)/y_points)
figure;
plot (xtheo,ytheo);
hold on;
plot(xfin,ytheo);
title('Linear interpolation for Ny=20, Nx=6, RMSE=0.0044');
xlabel('X');
ylabel('Y');
legend('y-theo vs x', 'y-lin vs x');

