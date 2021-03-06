% This code computes the Fourier coefficients of a real periodic waveform.
%
% INPUTS:  Samples of ONE period of the waveform  y(t)
%     y : vector of N samples making one period
%
% OUTPUTS: Fourier coefficients
%   Y_DC : DC (average) value of signal y(t). 
%     Yn : magnitude of coefficient, n=1,...,N_half  (column vector)
%   PHIn : phase of coefficient,  n=1,...,N_half (column vector)
%   yrec : reconstructed version of y, from coefficients. (column vec)
%          
% Reconstruction of original signal:
%                   n=N_half  
%        y  =  Y_DC + Sum (Yn*cos(2*pi*n/N + PHIn) 
%              (n=0)  n=1
% 
%  Interpretation of result of FFT, w0 = 2pi/T, T corresponds 
%   to N samples (from 0 to N-1)
% 
%  N odd, eg: N=7
%  [DC, w0, 2w0, 3w0, -3w0, -2w0, -w0], or using f0
% 
%  N even, eg: N=8
%  [DC, w0, 2w0, 3w0, "4w0", -3w0, -2w0, -w0], or using f0
% 
%  The term 4w0 has a vague meaning to me. I will not use it.
%  The term 3w0 is in the position "N_middle"
%  As the input is real, the result has mirror symmetry, thus we only need
%    to consider half the values.


% Author: L.Torres 18.08.2016
% 22.08.2016, enhanced MatLab compatibility.


function [Y_DC, Yn, PHIn, yrec] = fourier_series(y)

  % Fourier analysis
  N = length(y);
  y = reshape(y,N,1); % make columnn vector
  Y_FFT = fft(y);

  % for n = 0: DC term
  Y_DC = 1/N*real(Y_FFT(1));

  % depending whether N is even or odd
  N_middle = (N + mod(N,2))/2;

  % Polar form
  % for n from 1 to N_middle
  Yn   = 2/N*abs(Y_FFT(2:N_middle));
  PHIn =   angle(Y_FFT(2:N_middle));

  % add up
  t = (0:N-1)';  % time axis as sample number (as column vector)
  yrec = Y_DC;
  for n=1:length(Yn)
    yrec = yrec + Yn(n)*cos(2*pi*n*t/N + PHIn(n));
  end

return;



