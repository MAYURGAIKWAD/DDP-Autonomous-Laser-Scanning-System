%% code for homogenous transformation of laser scan to homogenous coordinate system
clc;
clear all;
close all;
format long;
%% input data
points_per_scan=1280;
scandata=importdata("Multi_threading_scanner_profile_data.csv");
t_pos=importdata("time_pos_arr.csv");
posedata=importdata("Multi_threading_robot_data.csv");
t_scan=importdata("time_scanner_arr.csv");
scanlen=size(posedata);
scanlen=scanlen(1);
scandata1=scandata(2:scanlen,2:points_per_scan); %excluding the profile numbering
x_lin=ones(scanlen-1,1);
y_lin=ones(scanlen-1,1);
z_lin=ones(scanlen-1,1);

x_kal=ones(scanlen-1,1);
v=1.295558011;

%% Linear interpolation based
%currently only x, y & z changes

for i =1:scanlen-1
    x_lin(i)=((posedata(i+1,1)-posedata(i,1))/(t_pos(i+1)-t_pos(i)))*(t_scan(i)-t_pos(i))+ posedata(i,1);
    y_lin(i)=((posedata(i+1,2)-posedata(i,2))/(t_pos(i+1)-t_pos(i)))*(t_scan(i)-t_pos(i))+ posedata(i,2);
    z_lin(i)=((posedata(i+1,3)-posedata(i,3))/(t_pos(i+1)-t_pos(i)))*(t_scan(i)-t_pos(i))+ posedata(i,3);
    
end

% Kalman filter without noise
for i=1: scanlen-1
    x_kal(i)= posedata(i,1)+v*(t_scan(i)-t_pos(i));
end

%% transformations to global reference frame for visualisation
% for each profile y remains same only x and z change
% for i =1:scanlen-1
%     x1=posedata(i,1);
%     y1=posedata(i,2);
%     z1=posedata(i,3);
%     %scatter3(scandata(2*i-1,:)+ones(points_per_scan, 1)'.*y1, ones(points_per_scan, 1)'.*x1 , ones(points_per_scan, 1)'.*z1- scandata(2*i-1,:));
%     scatter3(ones(points_per_scan, 1)'.*x1, ones(points_per_scan, 1)'.*y1- scandata(2*i-1,:) , ones(points_per_scan, 1)'.*z1- scandata(2*i,:));
%     xlabel('X')
%     ylabel('Y')
%     zlabel('Z')
%     hold on;
% end

%linear interpolation based
% for i =1:scanlen-1
%     x1=x_lin(i);
%     y1=y_lin(i);
%     z1=z_lin(i);
%     %scatter3(scandata(2*i-1,:)+ones(points_per_scan, 1)'.*y1, ones(points_per_scan, 1)'.*x1 , ones(points_per_scan, 1)'.*z1- scandata(2*i-1,:));
%     scatter3(ones(points_per_scan, 1)'.*x1, ones(points_per_scan, 1)'.*y1- scandata(2*i-1,:) , ones(points_per_scan, 1)'.*z1- scandata(2*i,:));
%     hold on;
% end
% xlabel('X')
% ylabel('Y')
% zlabel('Z')

%Kalman filter visualisation
%  for i =1:scanlen-1
%     x1=x_kal(i,1);
%     y1=posedata(i,2);
%     z1=posedata(i,3);
%     %scatter3(scandata(2*i-1,:)+ones(points_per_scan, 1)'.*y1, ones(points_per_scan, 1)'.*x1 , ones(points_per_scan, 1)'.*z1- scandata(2*i-1,:));
%     scatter3(ones(points_per_scan, 1)'.*x1, ones(points_per_scan, 1)'.*y1- scandata(2*i-1,:) , ones(points_per_scan, 1)'.*z1- scandata(2*i,:));   
%     hold on;
%  end
plot(t_scan(1:306), posedata(1:306));
hold on;
plot(t_scan(1:306), x_lin(1:306));
plot(t_scan(1:306), x_kal(1:306));

xlabel('X')
ylabel('Y')
zlabel('Z')
legend('without correction','linear interpolation', 'kalman based interpolation')

title('visualisation based on kalman filter')
hold off

% figure
% plot
