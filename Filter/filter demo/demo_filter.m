%% This code is created by Mayur Gaikwad | 16D100008 for Dual Degree Project
close all;
clear all;
%% program initialisation
fs=1e4;
% time step
dt = 1/fs;

t=0:1/fs:0.2; t=t';
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
v1_var = 40; f=100;
v1 = 5*(2*pi*f)*cos(2*pi*f*t)+v1_var*randn([length(t),1]);
s1 = cumtrapz(t,v1);
s1_var=v1_var/(2*pi*f);
s1 = generate_signal(s1, s1_var);

%     s1 = 5*sin(2*pi*f*t)+s1_var*randn([length(t),1]);
%s1 = generate_signal(s1, s1_var);

% variance of signal 2 (Position Sensor)
s2_var = 0.5; f=100;
s2_theo=5*sin(2*pi*f*t);
s2 = 5*sin(2*pi*f*t)+s2_var*randn([length(t),1]);
s2 = generate_signal(s2, s2_var);

% fusion
for i = 1:n
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


%computing the RMS
RMS_kalman= sqrt(sum((s2_theo-X_arr(:,1)).*(s2_theo-X_arr(:,1)))/n)
RMS_noise= sqrt(sum((s2_theo-s2(:,1)).*(s2_theo-s2(:,1)))/n)
figure
plot(t, [s2(:, 1), s2_theo], 'LineWidth', 1);

figure
plot(t, [X_arr(:, 1), s2_theo], 'LineWidth', 1);

