TimeVolt = dlmread('F0000MTH.txt');
TimeCurr = dlmread('F0000CH2.txt');

% some Plot defaults
set(0,'defaultlinelinewidth',2);
set(0,'defaultaxeslinewidth',1);

% 2. Provide the number of points that make ONE period!
%
%    Example: If my data was measured with 10 ms/div, and the period of
%    my signals is 16.66ms, the number of points in ONE period is:
%    250 dots / div * 16.66ms / 10ms/div =  417 dots.
N_onePeriod = 417;


% The steps below are automatically done. You don't need to alter these.

% 3. Crop the original data to get only ONE period:
%    I arbitrarily select the first 'N_onePeriod dots'
%    You can keep any you want!


% Full imported versions
t_full      = TimeVolt(:,1);
V_wave_full = TimeVolt(:,2);
I_wave_full = TimeCurr(:,2);

% Crop to keep only ONE period
t      =      t_full(1:N_onePeriod);
V_wave = V_wave_full(1:N_onePeriod);
I_wave = I_wave_full(1:N_onePeriod);



% 4. Use function "fourier_series" to get coefficients and angles
  [V_DC, Vn, V_PHIn, Vrec] = fourier_series(V_wave);
  [I_DC, In, I_PHIn, Irec] = fourier_series(I_wave);
  % Note:
  % Question: Why do I need to find the Fourier series for the voltage
  %           waveform although I know it is a sinusoid?
  % Answer: Because I need to find the angle relative to the
  %         period I decided to extract.

fig = figure(3);
stem(fscale,[I_DC;In]);
title('Magnitude of Fourier coefficients for current (Amps)');
xlabel('Frequency (Hz)');
ylabel('Magnitude (A)');
grid on;
saveas(fig, 'zoomed_current_furier_coefficients.png');