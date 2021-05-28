%% This code is created by Mayur Gaikwad| 16D100008 as a part of dual degree project 
clear all;
clc;
%close all;

%% input data
points_per_scan=1280;
% scandata=importdata("Multi_threading_scanner_profile_data.csv");
% t_pos=importdata("time_pos_arr.csv");
% posedata=importdata("Multi_threading_robot_data.csv");
% t_scan=importdata("time_scanner_arr.csv");
%scanlen=size(posedata);
%scanlen=scanlen(1);
%scandata1=scandata(2:scanlen,2:points_per_scan); %excluding the profile numbering

% x=ones(scanlen-1,1);
% y=ones(scanlen-1,1);
% z=ones(scanlen-1,1);

%testing dataset
testdata=readtable("Test data plane.xlsx");
x=table2array(testdata(:,1));
y=table2array(testdata(:,2));
z=table2array(testdata(:,3));

alpha= 0;
beta = 0;
gamma= 0;
N=size(x,1); %total no of points
%% Initialise the form
z_form=0; %plane z=0

%% corrected variables for matching
x_corr= x + alpha;
y_corr= y + beta;
z_corr= z + gamma;
%% squared normal distance of individual point from the plane(form)
d= (z_corr(1) - z_form).^2;

%% Matching problem(Minimisation) (here 1D as the plane to match is Z=0)
obj_init= sum((z_corr-z_form).^2)/N; %objective value to be minimised for form matching(Mean Square error)
gamma_analytical_opt=-1.0*sum(z-z_form)/N;

%final update
z_corr= z + gamma_analytical_opt;
obj_analytical_opt= sum((z_corr-z_form).^2)/N; %objective value to be minimised for form matching(Mean Square error)

%% Gradient descent algorithm for minimisation
max_iter=1000;
l_rate=0.001; %learning rate
gamma=0;
z_corr= z+gamma;
learning=[0 obj_init]; 
for i =1:max_iter
    grad=sum((z_corr-z_form).*2)/N;
    gamma=gamma-l_rate*grad;
    z_corr=z+gamma;
    obj=sum((z_corr-z_form).^2)/N;
    learning=[learning; [i obj]]; 
end
plot(learning(:,1),learning(:,2))
hold on

max_iter=1000;
l_rate=0.01; %learning rate
gamma=0;
z_corr= z+gamma;
learning=[0 obj_init]; 
for i =1:max_iter
    grad=sum((z_corr-z_form).*2)/N;
    gamma=gamma-l_rate*grad;
    z_corr=z+gamma;
    obj=sum((z_corr-z_form).^2)/N;
    learning=[learning; [i obj]]; 
end
plot(learning(:,1),learning(:,2))
hold on
    
max_iter=1000;
l_rate=0.1; %learning rate
gamma=0;
z_corr= z+gamma;
learning=[0 obj_init]; 
for i =1:max_iter
    grad=sum((z_corr-z_form).*2)/N;
    gamma=gamma-l_rate*grad;
    z_corr=z+gamma;
    obj=sum((z_corr-z_form).^2)/N;
    learning=[learning; [i obj]]; 
end
plot(learning(:,1),learning(:,2))

    


