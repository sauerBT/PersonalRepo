clear all; clc;
M = 2;
alpha = .2; 
MB = M * (1 - alpha);
ML = M*alpha;
% Equation Parameters
y=[MB, ML, .5, .5, .5, .5]; 
y2 = ones(10,6);
h = .1;
h2 = .1;
time = 360;
ysub1 = ((1/h));
y2(ysub1,:) = y

%y(1) = mass tank 1
%y(2) = mass tank 2
%y(3) = concentration of a in big tank
%y(4) = concentration of a in little tank
%y(5) = concentration of b in big tank
%y(6) = concentration of b in little tank

%m0 = mass flow entering big tank
%m1 = mass flow leaving big tank
%m2 = mass flow entering little tank
%m3 = mass flow leaving little tank


%M0 = [ones(1, 100)*1];
%X1_11 = [.2*ones(1,50),.8*ones(1,50)];
%X2_11 = [.8*ones(1,50),.2*ones(1,50)];
%X3_11 = [0*ones(1,100)];


y_plot2 = ones(((1/h)*time), length(y))

[t,y] = rk4('Interchange',[1,time],y,h2);

reset = ones(10,2);
reset(:,1) = reset(:,1)*MB;
reset(:,2) = reset(:,2)*ML;
i = 1;
while i <= (time)
  if i == 1 
    sub1 = 1;
  else
    sub1 = (((i-1)*10) + 1)
  end
  sub2 = (((i-1)*10) + 10)
  [t,y2] = rk4('Interchange',[.1,1],y2(ysub1, :),h);
  X_tot_RK4(i) = y2(10,3) + y2(10,5);
  y_plot2(sub1:sub2,:) = y2;
  y2(:,1:2) = reset;
  i = i + 1;
end








t1 = linspace(h,time, time*10);
t3 = linspace(h2, time, length(y));
figure;
plot(t3,y(:,3),'-r',t3,y(:,5),'-b', t1,y_plot2(:,3),'-m',t1,y_plot2(:,5),'-y')
title('Big Tank');
xlabel('Time t');
ylabel('Solution X');
legend('Xa Matlab','Xb1 Matlab','Xa2 Matlab Iteration','Xb2 Matlab Iteration');
figure;
plot(t3,y(:,4),'-r',t3,y(:,6),'-b',t1,y_plot2(:,4),'-m',t1,y_plot2(:,6),'-y')
title('Little Tank');
xlabel('Time t');
ylabel('Solution X');
legend('Xa Matlab','Xb1 Matlab','Xa2 DeltaV','Xb2 DeltaV');

figure;
plot(t3,y(:,1),'-r',t3,y(:,2),'-b',t1,y_plot2(:,1),'-m',t1,y_plot2(:,2),'-y')
title('Mass');
xlabel('Time t');
ylabel('Solution X');
legend('MB Matlab','ML Matlab','MB2 DeltaV Simulation','ML2 DeltaV Simulation');
figure;
plot(1:length( X_tot_RK4),  X_tot_RK4, 'r')    
%figure;
%plot(t,y(:,3),'-o',t,y(:,5),'-o')
%title('Solution X1_3_2 and X2_3_2 via Runge Kutta');
%xlabel('Time t');
%ylabel('Solution X');
%legend('X1_3_2', 'X2_3_2')


%figure;
%plot(t,y(:,4),'-o',t,y(:,6),'-o')
%title('Solution X1_3_3 and X2_3_3 via Runge Kutta');
%xlabel('Time t');
%ylabel('Solution X');
%legend('X1_3_3', 'X2_3_3')
 

