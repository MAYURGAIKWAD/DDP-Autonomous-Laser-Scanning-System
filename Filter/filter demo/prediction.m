function [X, P] = prediction(X, P, Q, F)
    X = F*X;
    P = F*P*F' + Q;
end
