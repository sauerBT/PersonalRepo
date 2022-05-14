clear all;
clc;

%% Global Variables
M = .1;
N = 10000;
h = .1;
Mss = 5; 
tc = 360;

x1_in = 1/6;
x2_in = 2/6;
x3_in = 3/6;

min1 = .001;
min2 = .002;
min3 = .003;
m0 = min1 + min2 + min3;
%% Paul Euler Solution

M_P = M;
dMdt = (M_P-Mss)/tc;
m1 = m0;



x1 = .333;
x2 = .333;
x3 = .333;

X = x1 + x2 + x3;


i = 1;
j = 1;

for i = 1:N

    dMdt = (M_P-Mss)/tc ;
    M_P = M_P - dMdt ;
    Marray(i) = M_P;
    m1 = m0 + dMdt ;
    
    
    for j = 1:10
    
    dx1dt  = h*((m0 * x1_in - m1 * x1) - x1*(m0 - m1))/M_P ;
    dx2dt  = h*((m0 * x2_in - m1 * x2) - x2*(m0 - m1))/M_P ;
    dx3dt  = h*((m0 * x3_in - m1 * x3) - x3*(m0 - m1))/M_P ;
    x1 = x1 + dx1dt ;
    x2 = x2 + dx2dt ;
    x3 = x3 + dx3dt ;
    X = x1 + x2 + x3;
    y(i) = x1;
    
    end
end

%% Brian Euler Solution 30

y1 = [.333,.333,.333,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
ysub1 = ((1/h));
y2(ysub1,:) = y1;

%M = zeros(1,N)
M_Euler = M;
reset = ones(10,2);
reset(:,1) = reset(:,1)*2;
for j = 1:N

  if j == 1 
    sub1 = 1;
    
    
     M_Euler(j) = M_Euler(1);
     %Marray(1) = M;
     m1 = m0;
  else
    sub1 = (((j-1)*10) + 1);
    
    
    %dMdt = (M-Mss)/tc ;
    %M = M - dMdt ;
    %Marray(i) = M;
    %m1 = m0 + dMdt ;
    M_Euler(j) = Mass_Sim(180, 1, M_Euler(j-1));
    m1 = m0 + (M_Euler(j) - M_Euler(j-1))
  end
  
  sub2 = (((j-1)*10) + 10);
  
  [t, y2] = Euler([.1,1],y2(ysub1, :), h, m0, m1, M_Euler(j), x1_in, x2_in, x3_in); 
  X_tot_Euler(j) = y2(10,1) + y2(10,2) + y2(10,3); 
  y_plot2(sub1:sub2,:) = y2;
 % y2(:,1:2) = reset;
end

%% Brian RK4

y1 = [.333,.333,.333,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
ysub1 = ((1/h));
y2(ysub1,:) = y1;

%M = zeros(1,N)
M_RK4 = M_Euler;
reset = ones(10,2);
reset(:,1) = reset(:,1)*2;
for j = 1:N

  if j == 1 
    sub1 = 1;
    
    
     M_RK4(j) = M_RK4(1);
     %Marray(1) = M;
     m1 = m0;
  else
    sub1 = (((j-1)*10) + 1);
    
    
    %dMdt = (M-Mss)/tc ;
    %M = M - dMdt ;
    %Marray(i) = M;
    %m1 = m0 + dMdt ;
    %%M_RK4(j) = Mass_Sim(180, 1, M_RK4(j-1));
    m1 = m0 + (M_RK4(j) - M_RK4(j-1))
  end
  
  sub2 = (((j-1)*10) + 10);
  
  [t, y2] = RK4_CSTR_S([.1,1],y2(ysub1, :), h, m0, m1, M_RK4(j), x1_in, x2_in, x3_in); 
  X_tot_RK4(j) = y2(10,1) + y2(10,2) + y2(10,3); 
  y_plot3(sub1:sub2,:) = y2;
 % y2(:,1:2) = reset;
end


%% Brian Euler Solution 3

y3 = [.333,.333,.333];
ysub1 = ((1/h));
y4(ysub1,:) = y3;

%M = zeros(1,N)
reset = ones(10,2);
reset(:,1) = reset(:,1)*2;
for j = 1:N

  if j == 1 
    sub1 = 1;
    
    
     M_Euler(j) = M_Euler(1);
     %Marray(1) = M;
     m1 = m0;
  else
    sub1 = (((j-1)*10) + 1);
    
    
    %dMdt = (M-Mss)/tc ;
    %M = M - dMdt ;
    %Marray(i) = M;
    %m1 = m0 + dMdt ;
    %M_Euler(j) = Mass_Sim(180, 1, M_Euler(j-1));
    m1 = m0 + (M_Euler(j) - M_Euler(j-1))
  end
  
  sub2 = (((j-1)*10) + 10);
  
  [t, y4] = Euler_3([.1,1],y4(ysub1, :), h, m0, m1, M_Euler(j), x1_in, x2_in, x3_in); 
  X_tot_Euler_3(j) = y4(10,1) + y4(10,2) + y4(10,3); 
  y_plot4(sub1:sub2,:) = y4;
 % y2(:,1:2) = reset;
end

%% Brian RK4 3
y3 = [.333,.333,.333];
ysub1 = ((1/h));
y4(ysub1,:) = y3;

%M = zeros(1,N)
reset = ones(10,2);
reset(:,1) = reset(:,1)*2;
for j = 1:N

  if j == 1 
    sub1 = 1;
    
    
     M_RK4(j) = M_Euler(1);
     %Marray(1) = M;
     m1 = m0;
  else
    sub1 = (((j-1)*10) + 1);
    
    
    %dMdt = (M-Mss)/tc ;
    %M = M - dMdt ;
    %Marray(i) = M;
    %m1 = m0 + dMdt ;
    %M_Euler(j) = Mass_Sim(180, 1, M_Euler(j-1));
    m1 = m0 + (M_RK4(j) - M_RK4(j-1))
  end
  
  sub2 = (((j-1)*10) + 10);
  
  [t, y4] = Euler_3([.1,1],y4(ysub1, :), h, m0, m1, M_RK4(j), x1_in, x2_in, x3_in); 
  X_tot_Euler_3(j) = y4(10,1) + y4(10,2) + y4(10,3); 
  y_plot5(sub1:sub2,:) = y4;
 % y2(:,1:2) = reset;
end


t1 = linspace(1,N,N);
t2 = linspace(h,N,size(y_plot2,1));
figure;
plot(t1,y,'b',t2,y_plot2(:,1),'r',t2,y_plot3(:,1),'m',t2,y_plot4(:,1),'y',t2,y_plot5(:,1),'k')
legend('Paul', 'E30', 'R30', 'E3', 'R3');
grid on;
figure;
plot(1:length(Marray), Marray,'b',1:length(M_Euler),M_Euler,'r',1:length(M_RK4),M_RK4,'r')
figure;
plot(1:length(X_tot_RK4), X_tot_Euler, 'r',1:length(X_tot_RK4), X_tot_RK4, 'm')    
    