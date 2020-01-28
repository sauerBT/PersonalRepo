function ret = CSTR_S_3(t, y, m0, m1, M, x1_in, x2_in, x3_in)
%UNTITLED2 Summary of this function goes here
%   y(1)  = x1
%   y(2) = x2
%   y(3) = x3

ret = [((m0 * x1_in - m1 * y(1)) - y(1)*(m0 - m1))/M ;
        ((m0 * x2_in - m1 * y(2)) - y(2)*(m0 - m1))/M ;
        ((m0 * x3_in - m1 * y(3)) - y(3)*(m0 - m1))/M ;
        ]
end