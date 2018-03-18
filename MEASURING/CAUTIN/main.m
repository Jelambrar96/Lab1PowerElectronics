TimeVolt = dlmread('F0000MTH.txt');
TimeCurr = dlmread('F0000CH2.txt');

waveform_analysis(TimeVolt, TimeCurr)

fig = figure(3);
stem(fscale,[I_DC;In]);
title('Magnitude of Fourier coefficients for current (Amps)');
xlabel('Frequency (Hz)');
ylabel('Magnitude (A)');
grid on;
saveas(fig, 'current_furier_coefficients.png');