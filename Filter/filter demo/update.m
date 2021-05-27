function [X, P] = update(X, P, y, R, H)
    Inn = y - H*X;
    S = H*P*H' + R;
    K = P*H'/S;

    X = X + K*Inn;
    P = P - K*H*P;
end