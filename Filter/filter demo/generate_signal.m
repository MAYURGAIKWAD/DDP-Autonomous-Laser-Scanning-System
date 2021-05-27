function [s] = generate_signal(signal, var)
%     noise = randn(size(signal)).*sqrt(var);

    s(:, 1) = signal;
    s(:, 2) = var; 
end