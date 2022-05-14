function ret = CSTR3(t, y, m0, m1, M, Mlast, Mss, x1_in, x2_in, x3_in)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here

Ncstr = 3;
M0=m0;
X1_11 = x1_in;
X2_11 = x2_in;
X3_11 = x3_in;
Mcstr = M/Ncstr;
q = 0;
dM = M - Mlast;

m31 = (M0 + (dM/Ncstr))/(1-q);
m41 = m31*q;
m32 = (m31 - m41 + (dM/Ncstr))/(1-q);
m42 = m32*q;
m33 = (m32 - m42 + (dM/Ncstr));
ret = [(1/Mcstr).*(M0.*X1_11 - m31.*y(1) + m41.*y(2) - y(1).*(M0 + m41 - m31));
        (1/Mcstr).*(m31.*y(1) + m42.*y(3) - m32.*y(2) - m41.*y(2) - y(2).*(m31 + m42 - m32 - m41));
        (1/Mcstr).*(m32.*y(2) - m33.*y(3) - m42.*y(3) - y(3).*(m32 - m33 - m42));
        (1/Mcstr).*(M0.*X2_11 + m41.*y(5) - m31.*y(4) - y(4).*(M0 + m41 - m31));
        (1/Mcstr).*(m31.*y(4) + m42.*y(6) - m32.*y(5) - m41.*y(5) - y(5).*(m31 + m42 - m32 - m41));
        (1/Mcstr).*(m32.*y(5) - m33.*y(6) - m42.*y(6) - y(6).*(m32 - m33 - m42));
        (1/Mcstr).*(M0.*X3_11 + m41.*y(8) - m31.*y(7) - y(7).*(M0 + m41 - m31));
        (1/Mcstr).*(m31.*y(7) + m42.*y(9) - m32.*y(8) - m41.*y(8) - y(8).*(m31 + m42 - m32 - m41));
        (1/Mcstr).*(m32.*y(8) - m33.*y(9) - m42.*y(9) - y(9).*(m32 - m33 - m42));
        ];

end




% y(7) = (1 - y(1) + y(4))
% y(8) = (1 - y(2) + y(5))
% y(9) = (1 - y(3) + y(6))
%ret = [(1/Mcstr).*(M0.*X1_11 - m31.*y(1) + m41.*y(2) - y(1).*(M0 + m41 - m31));
%        (1/Mcstr).*(m31.*y(1) + m42.*y(3) - m32.*y(2) - m41.*y(2) - y(2).*(m31 + m42 - m32 - m41));
%        (1/Mcstr).*(m32.*y(2) - m33.*y(3) - m42.*y(3) - y(3).*(m32 - m33 - m42));
%        (1/Mcstr).*(M0.*X2_11 + m41.*y(5) - m31.*y(4) - y(4).*(M0 + m41 - m31));
%        (1/Mcstr).*(m31.*y(4) + m42.*y(6) - m32.*y(5) - m41.*y(5) - y(5).*(m31 + m42 - m32 - m41));
%        (1/Mcstr).*(m32.*y(5) - m33.*y(6) - m42.*y(6) - y(6).*(m32 - m33 - m42));
%        (1/Mcstr).*(M0.*X3_11 + m41.*y(8) - m31.*y(7) - y(7).*(M0 + m41 - m31));
%        (1/Mcstr).*(m31.*y(7) + m42.*y(9) - m32.*y(8) - m41.*y(8) - y(8).*(m31 + m42 - m32 - m41));
%        (1/Mcstr).*(m32.*y(8) - m33.*y(9) - m42.*y(9) - y(9).*(m32 - m33 - m42));
%        ];