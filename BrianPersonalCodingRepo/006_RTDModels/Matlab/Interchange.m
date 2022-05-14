function [ dydt ] = Interchange(t,y)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here

%m1 = mass flow entering big tank
%m3 = mass flow leaving big tank
%m2 = mass flow entering little tank
%m4 = mass flow leaving little tank

%y(1) = mass tank 1
%y(2) = mass tank 2
%y(3) = concentration of a in big tank (X11)
%y(4) = concentration of a in little tank (X12)
%y(5) = concentration of b in big tank
%y(6) = concentration of b in little tank

m1 = .004;
Xa10 = .25;
Xb10 = .75;
%timeC1 = 180;
%timeC2 = 360;
ssM = 2;
alpha = .2; 
beta = 0.5; 


%M1 := '^/M' * (1 - alpha);  rem Initial Mass in Tank 1
%M2 := '^/M'*alpha; rem Initial Mass in Tank 2
timeC1 = (ssM * (1 - alpha))/(m1);
timeC2 = (ssM*alpha)/(beta*m1);



m2=beta*m1;
m4=beta*m1 - (alpha*(y(1)+y(2)) - y(2))/timeC2;
m3=m1 - (ssM*(1-alpha)-y(1))/timeC1;

dydt =[m1 + m4 - m2 - m3;
       m2 - m4;
       (1/y(1))*(m1*Xa10 + m4*y(4) - m2*y(3) - m3*y(3) - y(3)*(m1 + m4 - m2 - m3));
       (1/y(2))*(m2*y(3) - m4*y(4) - y(4)*(m2 - m4));
       (1/y(1))*(m1*Xb10 + m4*y(6) - m2*y(5) - m3*y(5) - y(5)*(m1 + m4 - m2 - m3));
       (1/y(2))*(m2*y(5) - m4*y(6) - y(6)*(m2 - m4))];
end

  % m2=beta*M0;
  % m3=beta*M0 - (alpha*(y(1)+y(2)) - y(2))/timeC2;
  % m1=M0 - (ssM*(1-alpha)-y(1))/timeC1;
  % 1/y(1)*(M0*Xa10 + m3*y(4) - m2*y(3) - m1*y(3) - y(3)*(M0 + m3 - m2 - m1));
  % 1/y(2)*(m2*y(3) - m3 * y(4) - y(4)*(m2 - m3));
  % 1/y(1)*(M0*Xb10 + m3*y(6) - m2*y(5) - m1*y(5) - y(5)*(M0 + m3 - m2 - m1));
  % 1/y(2)*(m2*y(5) - m3 * y(6) - y(6)*(m2 - m3))];
