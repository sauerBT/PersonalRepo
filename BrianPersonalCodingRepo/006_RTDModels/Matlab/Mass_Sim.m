function [ Mnew ] = Mass_Sim(tc,Mss,M0)

noise = -.009 + (.009 + .009) * rand(1);

dM = ((M0-Mss)/tc);
Mnew = M0 - dM;
end 