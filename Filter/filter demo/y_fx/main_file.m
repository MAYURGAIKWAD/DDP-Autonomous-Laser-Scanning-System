%% This code is created by Mayur Gaikwad | 16D100008 for Dual Degree Project (filter implementation on real values)
clear all:
clc;
close all;
%% Input parameters (semicircular arc from (0,0) to (2,0)
N_points=100;
t=linspace(0,1,N_points+1);
phase=1/N_points/2;
t1=t+phase;
%% theoretical values (we look for the values at t1)
%Curve equation = (x-1)^2 + y^2 = 1^2
x= 1-cos(pi*t1(1:N_points));
ytheo= sqrt(1-(x-1).^2);
y=sin(pi*t);

%% linear interpolation values of y at t1
y_lin= (y(1:N_points)+y(2:N_points+1))/2;
Rmse_lin= sqrt(sum((y_lin-ytheo).^2)/N_points)
figure;
plot (x,ytheo);
hold on;
plot(x,y_lin);
title('Linear interpolation for N=100, RMSE=8.7234e-05')
xlabel('X');
ylabel('Y');
legend('y-theo vs x', 'y-lin vs x');

