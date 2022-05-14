clear all;
clc;

%% Global Variables
M = .1;
N = 1000;
h = .1;
Mss = 1; 
tc = 180;

x1_in = 1/6;
x2_in = 2/6;
x3_in = 3/6;
min1 = .001;
min2 = .002;
min2 = .003;
m0 = min1 + min2;


%% Brian Euler Solution 3

y3 = [.333,.333,.333,.333,.333,.333, .333,.333,.333];
ysub1 = ((1/h));
y4(ysub1,:) = y3;
M_Euler = M;
%M = zeros(1,N)

for j = 1:N

  if j == 1 
    sub1 = 1;
    
    
     M_Euler(j) = M_Euler(1);
     %Marray(1) = M;
     m1 = m0;
     Mlast = M_Euler(1);
  else
    sub1 = (((j-1)*10) + 1);
    
    
    %dMdt = (M-Mss)/tc ;
    %M = M - dMdt ;
    %Marray(i) = M;
    %m1 = m0 + dMdt ;
    M_Euler(j) = Mass_Sim(tc, Mss, M_Euler(j-1));
    Mlast = M_Euler(j-1);
  end
  
  sub2 = (((j-1)*10) + 10);
  
  [t, y4] = Euler_3CSTR([.1,1],y4(ysub1, :), h, m0, m1, M_Euler(j),Mlast,Mss, x1_in, x2_in, x3_in); 
  X_tot_Euler_3(j) = y4(10,3) + y4(10,6) + y4(10,9);
  y_plot4(sub1:sub2,:) = y4;
 % y2(:,1:2) = reset;
end



t2 = linspace(h,N,size(y_plot4,1));
figure;
plot(t2,y_plot4(:,3),'r',t2,y_plot4(:,6),'b',t2,y_plot4(:,9),'m')
legend( 'E3');
grid on;
figure;
plot(1:length(M_Euler),M_Euler,'r')
figure;
plot(1:length( X_tot_Euler_3),  X_tot_Euler_3, 'r')    