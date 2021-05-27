%% This code is created by Mayur Gaikwad | 16D100008 for Dual Degree Project
clear all
clc
close all
%% Input parameters
N=100; %no of points
lambda=5; %noise factor
t1=0;
t2=2*pi;
t=linspace(t1,t2,N);
y1=t+lambda*(-1+2*rand(N,1))'*(t2-t1)/N;
s1=t;
s1=sin(t)
% y=s1;
v=1 %velocity of the
s2=sin(t)+lambda*(-1+2*rand(N,1))'*(t2-t1)/N;
% s2=t+lambda*(-1+2*rand(N,1))'*(t2-t1)/N;
%% initialising measured and actual values
y_meas=s2(1:2:N);
t_meas= t(1:2:N);
y_act=s2(2:2:N-1);
t_act=t(2:2:N-1);

%% Prediction branch 
%linear interpolation
y_pred = (y_meas(1:N/2-1)+y_meas(2:N/2))/2 ;
%% RMS error
% rmse=sum((y_pred-y_meas(1:N/2-1)).*(y_pred-y_meas(1:N/2-1)))/(N/2-1)
Rmse=sum((y_pred-s1(2:2:N-1)).*(y_pred-s1(2:2:N-1)))/(N/2-1)

%% Plots functions
plot(t_meas,y_meas,'o')
hold on
plot(t_act,y_pred,'x')
plot(t_act,y_act,'*')
plot(t,s1)
xlabel('Time (t)')
ylabel('Time (t)')
title('Variation of position vs time (with random noise)')
legend('measured values','predicted values', 'actual values', 'expected path')
hold off
% figure
% plot(t,s1)
% hold on 
% plot(t,s2,'x')
