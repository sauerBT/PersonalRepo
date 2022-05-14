function ret = CSTR_1(t,y, M0, X1_11, X2_11, X3_11)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
M = 1;
Ncstr = 1;
Tc= 60;
%M0= 1.32;
Mss = 79.2;
%X1_11 = .5;
%X2_11 = .25;
%X3_11 = .25;
Mcstr = M/Ncstr;
q = 0;

m31 = (M0 - (Mss - M)/Tc)/(1-q);
m41 = m31.*q;

ret = [(1/Mcstr).*(M0.*X1_11 - m31.*y(1) - y(1).*(M0 + m41 - m31));
        (1/Mcstr).*(M0.*X2_11 - m31.*y(2) - y(2).*(M0 + m41 - m31));
        (1/Mcstr).*(M0.*X3_11 - m31.*y(3) - y(3).*(M0 + m41 - m31));];
 
end
