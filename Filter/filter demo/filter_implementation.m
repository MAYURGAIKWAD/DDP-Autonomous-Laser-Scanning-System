%% This code is created by Mayur Gaikwad | 16D100008 for Dual Degree Project (filter implementation on real values)
clear all:
clc;
close all;
%% Input values from laser scanner data (1000_1280_is14.csv)
scanner_freq=100;
end_eff_vel= 0.001;
y_res= end_eff_vel/scanner_freq;
points_per_scan=1280;
a=importdata("Multi_threading_scanner_profile_data.csv");
size_a=size(a);
%N_scan= size_a(1)/2;
N_scan=1000;
Y=linspace(y_res,N_scan*y_res,N_scan);
Y_pts=linspace(y_res/2,N_scan*y_res+y_res/2,N_scan+1); % actual sensor data
%size(Y)
lambda=y_res*10;    % Noise factor in y
Y_noise= Y_pts+lambda*(-1+2*rand(N_scan+1,1))';
Y_lin= (Y_noise(1:N_scan)+Y_noise(2:N_scan+1))/2;

%% Plotting the data 
% plotting a singe line
%scatter3(a(1,:),ones(points_per_scan, 1)'*Y(1), a(2,:))

%% Plot for the base case: assumed to be true (indexing based)
% for i = 1:N_scan
%     scatter3(a(2*i-1,:),ones(points_per_scan, 1)'*Y(i), a(2*i,:));
%     hold on;
% end

%% Plotting y_theo vs after noise additions
% plot (1:N_scan,Y)
% hold on
% plot (1:N_scan,Y_lin)

%% Scatter plot for linearly interpolated values
for i = 1:N_scan/4
    scatter3(a(2*i-1,:),ones(points_per_scan, 1)'*Y_lin(i), a(2*i,:));
    hold on;
end

% ynoise ylin ykalman
%cance1

%% kalman filter results

%% program initialisation
fs=1e4;
% time step
dt = 1/fs;
dt=y_res/10;

t=0:y_res:0.2; t=t';
n = numel(t);

% state matrix
X = zeros(2,1);

% covariance matrix
P = zeros(2,2);

% kalman filter output through the whole time
X_arr = zeros(n, 2);

% system noise
Q = [0.04 0;
    0 1];

% transition matrix
F = [1 dt;
    0 1];

% observation matrix
H = [1 0];

% variance of signal 1 (Velocity Sensor)
v1_var = 0.040; 
% v1 = 5*(2*pi*f)*cos(2*pi*f*t)+v1_var*randn([length(t),1]);
% v1=0.001
v1=ones(n,1)*0.001+v1_var*randn([n,1]);
s1 = cumtrapz(t,v1);
%s1_var=v1_var/(2*pi*f);
s1_var=v1_var;
s1 = generate_signal(s1, s1_var);

%     s1 = 5*sin(2*pi*f*t)+s1_var*randn([length(t),1]);
%s1 = generate_signal(s1, s1_var);

% variance of signal 2 (Position Sensor)
s2_var = y_res; f=100;
s2_theo=Y';
% s2 = 5*sin(2*pi*f*t)+s2_var*randn([length(t),1]);
s2=Y_noise';
s2 = generate_signal(s2, s2_var);

% fusion
for i = 1:N_scan
    if (i == 1)
        [X, P] = init_kalman(X, s1(i, 1)); % initialize the state using the 1st sensor
    else
        [X, P] = prediction(X, P, Q, F);
        
        [X, P] = update(X, P, s1(i, 1), s1(i, 2), H);
        [X, P] = update(X, P, s2(i, 1), s2(i, 2), H);
    end
    
    X_arr(i, :) = X;
end
% figure;
% plot(t, [s1(:, 1), s2(:, 1),X_arr(:, 1)], 'LineWidth', 1);
% set(gca,'FontSize',12);
% grid on;
% legend('signal 1', 'signal 2', 'Kalman Filter');
% figure;
% plot(t, X_arr(:, 1), 'LineWidth', 1);

SMA5=(Y_noise(1:N_scan-10)+Y_noise(2:N_scan-9)+Y_noise(3:N_scan-8)+Y_noise(4:N_scan-7)+Y_noise(5:N_scan-6))/5;
%computing the RMS
% RMS_kalman= sqrt(sum((s2_theo-X_arr(:,1)).*(s2_theo-X_arr(:,1)))/n)
% RMS_noise= sqrt(sum((s2_theo-s2(:,1)).*(s2_theo-s2(:,1)))/n)
figure
% plot([ s2_theo(1:90),Y_noise(1:90)', Y_lin(1:90)',X_arr(1:90, 1), SMA10'], 'LineWidth', 1);
plot([ s2_theo(1:90),Y_noise(1:90)', Y_lin(1:90)',SMA5'], 'LineWidth', 1);
legend('theoretical', 'noisy raw data','Linear Interpolation', 'Kalman filter')
% figure
% plot(t, [X_arr(:, 1), s2_theo], 'LineWidth', 1);

