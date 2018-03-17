% This code generates typical waveforms for voltage and current.

% some Plot defaults
set(0,"defaultlinelinewidth",2);
set(0,"defaultaxeslinewidth",1);

% Typically, in a digital oscilloscope there are 2500 horizontal points. 
% Oscilloscopes have 10 main horizontal divisions, each with 250 points. 
% The screen capture will produce a file (a vector) of 2500 values. 

% We assume the circuits are mains-powered (120 VAC @ 60 Hz)

% The voltage is in Volts
% The current is in milliamps. 



V_rms = 117; % rms voltage
theta = 0.3*pi; %relative phase of voltage in the screen 
secDiv = 0.005; % 2 ms/div : seconds per division

% computed:
Ts = secDiv / 250; % sampling time
Freq = 60; % fundamental frequency 
V_ampl = V_rms*sqrt(2);
t = (0:2499)'*Ts;


%%% GENERATE TYPICAL VOLTAGE %%%%%

% generate the voltage source
V_wave_pure = V_ampl*sin(2*pi*Freq*t + theta);  

% apply some small noise
V_wave = V_wave_pure + 0.02*V_rms*rand(size(V_wave_pure));


%%% GENERATE TYPICAL CURRENT %%%%
thres = 0.96;

base1 = sin(2*pi*Freq*t + theta);
I_base1 = max(0,base1-thres)+min(0,base1+thres);

base2 = sin(2*pi*Freq*t + theta + 5*pi/16);
I_base2 = max(0,base2-thres)+min(0,base2+thres);

base3 = sin(2*pi*Freq*t + theta - 5*pi/16);
I_base3 = max(0,base3-thres)+min(0,base3+thres);

% make current in amps
I_wave_pure = 10^(-3)*20*V_ampl*(I_base1 -.3*I_base2 -.1*I_base3);
I_rms = sqrt(mean(I_wave_pure.^2));

% apply some small noise
I_wave = I_wave_pure + 0.1*I_rms*rand(size(I_wave_pure));

% to plot current together with voltage, express current in milliamps

figure(1);
plot(t,[V_wave, 10^3*I_wave]);  % voltage in volts, current in milliamps
grid on;

% store waveforms
dlmwrite('data_voltage.txt',[t, V_wave]);
dlmwrite('data_current.txt',[t, I_wave]);



