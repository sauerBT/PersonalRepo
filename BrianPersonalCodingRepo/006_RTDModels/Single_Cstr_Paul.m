function [ ret] = Single_Cstr_Paul(t, y, m0, M)
%UNTITLED2 Summary of this function goes here
%   y(1)  = x1
%   y(2) = x2
%   y(3) = x3
tc = 180; Mss = 1;
%m1 = ((Mss - M)/tc);
x1_in = (y(1)*m0)/m0;
x2_in = (y(2)*m0)/m0;
x3_in = (y(3)*m0)/m0;
ret = [((m0 * x1_in - m1 * y(1)) - y(1)*(m0 - m1))/M ;
        ((m0 * x2_in - m1 * y(2)) - y(2)*(m0 - m1))/M ;
        ((m0 * x3_in - m1 * y(3)) - y(3)*(m0 - m1))/M ;];
end