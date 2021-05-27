%% This code is created by Mayur Gaikwad | 16D100008 for Dual Degree Project (filter implementation on real values)
clear all:
clc;
close all;
%% Input parameters (semicircular arc from (0,0) to (2,0)
y_points=20; %scanner frequency
x_points=6;
ty=linspace(0,10,y_points+1);
phase=1/y_points/2;
tx=linspace(0,10,x_points+1);
%% theoretical values (we look for the values at t1)
%Curve equation = y=x^2
ytheo= ty;
xtheo=(ytheo.*ytheo).*ytheo;
xact=tx.*tx.*tx;
xlin=ones(1,y_points+1);
xkal=xlin;
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
        xlin(i)=xact(previndex);
        xkal(i)=xlin(i);
        i=i+1;
        
    elseif ty(i)==tx(nextindex)
        xlin(i)=xact(nextindex);
        xkal(i)=xlin(i);
        previndex=nextindex;
        nextindex=nextindex+1;
        i=i+1;
    else
        deltat=ty(i)-tx(previndex);
        xkal(i)=xact(previndex)+(3*tx(previndex)*tx(previndex)*deltat + 0.5*6*tx(previndex)*deltat*deltat);
        xlin(i)=((xact(nextindex)-xact(previndex))/(tx(nextindex)-tx(previndex)))*(ty(i)-tx(previndex))+ xact(previndex);
        i=i+1;
    end
end
%y_lin= (y(1:y_points)+y(2:y_points+1))/2;
Rmse_lin= sqrt(sum((xlin(1:end-1)-xtheo(1:end-1)).^2)/y_points)
Rmse_kal= sqrt(sum((xkal(1:end-1)-xtheo(1:end-1)).^2)/y_points)

max_abs_error_lin=max(abs(xlin(1:end-1)-xtheo(1:end-1)))
max_abs_error_kal=max(abs(xkal(1:end-1)-xtheo(1:end-1)))

figure;
plot (xtheo(1:end-1),ytheo(1:end-1));
hold on;
plot(xlin(1:end-1),ytheo(1:end-1));
title('Case 2: x=y^3;  for N_y=20, N_x=6');
plot(xkal(1:end-1),ytheo(1:end-1));
xlabel('X');
ylabel('Y');
legend('y-theo vs x', 'y-lin vs x', 'y-kal vs x');
deltax= mean(abs(xact(1:end-1)-xact(2:end)))

% %% Kalman filter based
% 
% fs=1e4;
% % time step
% dt = 1/fs;
% 
% t=0:1/fs:0.5; t=t';
% t=tx';
% n = numel(t);
% 
% % state matrix
% X = zeros(2,1);
% 
% % covariance matrix
% P = zeros(2,2);
% 
% % kalman filter output through the whole time
% X_arr = zeros(n, 2);
% 
% % system noise
% Q = [0.04 0;
%     0 1];
% 
% % transition matrix
% F = [1 dt;
%     0 1];
% 
% % observation matrix
% H = [1 0];
% 
% % variance of signal 1 (Velocity Sensor)
% v1_var = 40; f=100;
% v1 = (pi)*sin(pi*tx)+v1_var*randn([length(tx),1]);
% s1 = cumtrapz(t,v1);
% %s1_var=v1_var/(2*pi*f);
% s1_var=0.001;
% s1 = generate_signal(s1, s1_var);
% 
% %     s1 = 5*sin(2*pi*f*t)+s1_var*randn([length(t),1]);
% %s1 = generate_signal(s1, s1_var);
% 
% % variance of signal 2 (Position Sensor)
% s2_var = 0.5; f=100;
% %s2_theo=5*sin(2*pi*f*t);
% s2_theo=xact;
% s2 = 1-cos(pi*tx)+s2_var*randn([length(tx),1]);
% s2 = generate_signal(s2, s2_var);
% 
% % fusion
% for i = 1:n
%     if (i == 1) 
%         [X, P] = init_kalman(X, s1(i, 1)); % initialize the state using the 1st sensor
%     else
%         [X, P] = prediction(X, P, Q, F);
%         
%         [X, P] = update(X, P, s1(i, 1), s1(i, 2), H);
%         [X, P] = update(X, P, s2(i, 1), s2(i, 2), H);
%     end
%     
%     X_arr(i, :) = X;
% end
% % figure;
% % plot(t, [s1(:, 1), s2(:, 1),X_arr(:, 1)], 'LineWidth', 1);
% % set(gca,'FontSize',12);
% % grid on;
% % legend('signal 1', 'signal 2', 'Kalman Filter');
% % figure;
% % plot(t, X_arr(:, 1), 'LineWidth', 1);
% 
% 
% %computing the RMS
% RMS_kalman= sqrt(sum((s2_theo-X_arr(:,1)).*(s2_theo-X_arr(:,1)))/n)
% RMS_noise= sqrt(sum((s2_theo-s2(:,1)).*(s2_theo-s2(:,1)))/n)
% figure
% plot(t, [s2(:, 1), s2_theo], 'LineWidth', 1);
% 
% figure
% plot(t, [X_arr(:, 1), s2_theo], 'LineWidth', 1);
% 
