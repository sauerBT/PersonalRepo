function [ dydt ] = odefun2(y,C)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here

M0     = C(1);
Xa10   = C(2);
Xb10   = C(3);
ssM    = C(4);
beta   = C(5);
alpha  = C(6);
timeC1 = C(7);
timeC2 = C(8);

timeC1= .001;
alpha = .2;
M0= .0111;
beta = .7;
ssM = 1;
timeC2 = .003;
Xa10 = .5;
Xb10 = 1-Xa10;
m2=beta*M0;


m2=beta*M0
m3=beta*M0 - timeC1*(alpha*(y(1)+y(2)) - y(2))
m1=M0 - timeC2 *(ssM*(1-alpha)-y(1))

dydt =[M0 + m3 - m2 - m1;
       m2 - m3;
       1/y(1)*(M0*Xa10 + m3*y(4) - m2*y(3) - m1*y(3) - y(3)*(M0 + m3 - m2 - m1));
       1/y(2)*(m2*y(3) - m3 * y(4) - y(4)*(m2 - m3));
       1/y(1)*(M0*Xb10 + m3*y(6) - m2*y(5) - m1*y(5) - y(5)*(M0 + m3 - m2 - m1));
       1/y(2)*(m2*y(5) - m3 * y(6) - y(6)*(m2 - m3))];

end
