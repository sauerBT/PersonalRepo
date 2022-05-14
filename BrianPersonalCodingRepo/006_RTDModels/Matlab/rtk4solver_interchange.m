clear all; clc;
%% Performs the Runge Kutta method on a CSTR with Interchange system of differential equations.
% This specific solver allows for dynamic solving of equations based on a specified tspan
% and the length of your Runge Kutte initialization parameters
% To initialize the numerical solver:
%  1. Define Runge Kutta initialization parameters timeC1, timeC2, alpha, beta, M0, ssM, Xa10, Xb10.
% These parameters may be defines as 1 by x vectors, x being the number of dynamic iterations with new 
% initialization parameters.
%  2. Define you current initial conditions, yinit and yinit_future, of the system.
% See Initial conditions section for descriptions on what each initial condition is.
%  3. Set you current, tspan, and future, tspan_future, prediction time spans as 
% well as your current, ssize, and future, ssize_future, prediciton step sizes.
%
%   Example: You want to run a a prediciton on a system where your Runge Kutta 
% initialization parameters are not changing with time and you want to predict for 200 seconds 
% with a .1 second step size.  This can be solved with two different methods:
%  1. All Runge Kutta initialization parameters are set to 1 by 1 constants.  
% tspan is set to [0,200] and ssize is set to .1.  This method runs the runge kutta method once
% over a time span of 200 seconds.
% 
%  2. All Runge Kutta initialization parameters are set to 1 by 200 vectors and tspan is 
% set to 1 with ssize set to .1.  This method runs the Runge Kutta 200 times on a time span of 1 second
% which allows for Runge Kutta initialization parameters to change over time.
% 
% Future predictions are set up in the same manner and can be used to predict x seconds into the future 
% every second.  figure 3 plots current vs future predictions.
%
% ****NOTE: Method 2 takes much longer for the computer to solve.
%
%
%
 
% Runge Kutta initialization Parameters
timeC1= [.001*ones(1,180)];
alpha = [.2*ones(1,180)];
M0= [1.32*ones(1,180)];
beta = [.7*ones(1,180)];
ssM = [1*ones(1,180)];
timeC2 = [.003*ones(1,180)];
Xa10 = [.9*ones(1,180)];
Xb10 = [.1*ones(1,180)];
M = [3*ones(1,180)];
M1 = M.*alpha;
M2 = M - M1;


% Span and step size for current and future predictions
tspan = [0,1];
ssize = .1;
tspan_future = [0,2];
ssize_future = .1;

last_time = length([tspan(1):ssize:tspan(2)]);
last_time_future = 1/ssize_future;
last_time_future_2 = length([tspan_future(1):ssize_future:tspan_future(2)]);

% Initial conditions for normal and future predictions
yinit = [M1(1), M2(1), .2, .2, .8, .8];
y_future_init = [M1(1), M2(1), .2, .2, .8, .8];
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

i = 1;    
x = [];
x30 = [];
for i = 1:length(M0)  
  if i == 1
    [t,y] = rtk4_interchange('Interchange',tspan,yinit,ssize, M0(i), Xa10(i), Xb10(i), timeC1(i), timeC2(i), ssM(i), alpha(i), beta(i));
    [t30,y_future] = rtk4_interchange('Interchange',tspan_future,y_future_init,ssize_future, M0(i), Xa10(i), Xb10(i), timeC1(i), timeC2(i), ssM(i), alpha(i), beta(i));
  else
    [t,y] = rtk4_interchange('Interchange',tspan,y(last_time,:),ssize, M0(i), Xa10(i), Xb10(i), timeC1(i), timeC2(i), ssM(i), alpha(i), beta(i));
    [t30,y_future] = rtk4_interchange('Interchange',tspan_future,y_future(last_time_future,:),ssize_future, M0(i), Xa10(i), Xb10(i), timeC1(i), timeC2(i), ssM(i), alpha(i), beta(i));
  endif;
  y_future_init = y_future;
  y_init = y;
  
  plot(t+(tspan(2)*(i-1)),y(:,3),'-or',t+(tspan(2)*(i-1)),(y(:,5)),'-ob', t+(tspan(2)*(i-1)),(1 - y(:,3) - y(:,5)),'-ob')
  title('Solution Xa and Xb Interchange Outputs via Runge Kutta');
  xlabel('Time t');
  ylabel('Concentration X');
  legend('Xa','Xb')

  hold on;
  x = [x;
      y(last_time,:);];
  x30 = [x30;
      y_future(last_time_future_2,:);];
endfor;

hold off;
figure;
 plot(t,y(:,1),t,y(:,2));
title('Mass of Big and Little Tanks Over Time');
xlabel('Time t');
ylabel('Mass m');
legend('M1','M2')

t1 = linspace(1,length(x), length(x));
figure;
plot(t1,x(:,3),'-or',t1,x(:,5),'-ob')
title('Current Concentrations VS Predicted Future Concentrations');
xlabel('Time t');
ylabel('Concentration X');
legend('Xa_Current','Xb_Current','Xa_Future', 'Xb_Future')
t30 = linspace(1,length(x30), length(x30));
hold on;
plot(t30,x30(:,3),'-om',t30,x30(:,5),'-oy')






