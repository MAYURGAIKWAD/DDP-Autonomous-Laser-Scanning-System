%% code for homogenous transformation of laser scan to homogenous coordinate system
clc;
clear all;
close all;
%% input data
points_per_scan=1280;
scandata=importdata("Multi_threading_scanner_profile_data1.csv");
%t_pos=importdata("time_pos_arr.csv");
posedata=importdata("Multi_threading_robot_data_1.xlsx");
%t_scan=importdata("time_scanner_arr.csv");
scanlen=size(posedata);
scanlen=scanlen(1);
scandata1=scandata(2:scanlen,2:points_per_scan); %excluding the profile numbering
%% transformations to global reference frame for visualisation
% for each profile y remains same only x and z change
for i =1:scanlen/1
    x1=posedata(i,1);
    y1=posedata(i,2);
    z1=posedata(i,3);
    %scatter3(scandata(2*i-1,:)+ones(points_per_scan, 1)'.*y1, ones(points_per_scan, 1)'.*x1 , ones(points_per_scan, 1)'.*z1- scandata(2*i-1,:));
    scatter3(ones(points_per_scan, 1)'.*x1, ones(points_per_scan, 1)'.*y1- scandata(2*i-1,:) , ones(points_per_scan, 1)'.*z1- scandata(2*i-1,:));
    hold on;
end
    

