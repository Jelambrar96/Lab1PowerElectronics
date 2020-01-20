# % This code computes the Fourier coefficients of a real periodic waveform.
# %
# % INPUTS:  Samples of ONE period of the waveform  y(t)
# %     y : vector of N samples making one period
# %
# % OUTPUTS: Fourier coefficients
# %   Y_DC : DC (average) value of signal y(t). 
# %     Yn : magnitude of coefficient, n=1,...,N_half  (column vector)
# %   PHIn : phase of coefficient,  n=1,...,N_half (column vector)
# %   yrec : reconstructed version of y, from coefficients. (column vec)
# %          
# % Reconstruction of original signal:
# %                   n=N_half  
# %        y  =  Y_DC + Sum (Yn*cos(2*pi*n/N + PHIn) 
# %              (n=0)  n=1
# % 
# %  Interpretation of result of FFT, w0 = 2pi/T, T corresponds 
# %   to N samples (from 0 to N-1)
# % 
# %  N odd, eg: N=7
# %  [DC, w0, 2w0, 3w0, -3w0, -2w0, -w0], or using f0
# % 
# %  N even, eg: N=8
# %  [DC, w0, 2w0, 3w0, "4w0", -3w0, -2w0, -w0], or using f0
# % 
# %  The term 4w0 has a vague meaning to me. I will not use it.
# %  The term 3w0 is in the position "N_middle"
# %  As the input is real, the result has mirror symmetry, thus we only need
# %    to consider half the values.
#
# 
# % Author: L.Torres 18.08.2016
# % 22.08.2016, enhanced MatLab compatibility.

import numpy as np


def fourier_series(y):

    y = y.flatten()
    Y_FFT = np.fft.fft(y)

    N = y.shape[0]
    # % for n = 0: DC term
    Y_DC = 1 / N * np.real(Y_FFT[0])

    # % depending whether N is even or odd
    N_middle = (N + np.mod(N , 2)) // 2
    
    # % Polar form
    # % for n from 1 to N_middle
    Yn = 2 / N * np.abs(Y_FFT[1:N_middle])
    PHIn = np.angle(Y_FFT[1:N_middle])

    # % add up
    # t = (0:N-1)';  % time axis as sample number (as column vector)
    t = np.arange(N)
    # yrec = Y_DC;
    # for n=1:length(Yn)
    # yrec = yrec + Yn(n)*cos(2*pi*n*t/N + PHIn(n));
    
    yrec = 0 # Y_DC
    # for i, item in enumerate(Yn):
    #     yrec = np.sum(yrec, item * np.cos(2 * np.pi * (i + 1) * t / N + PHIn[i]))
    
    for ind, item in enumerate(Yn):
        # print(type(i))
        # print(item)
        yrec = yrec + item * np.cos(2 * np.pi * ind * t / N + PHIn[ind])
        # pass
    
    # print(yrec.shape)
    
    yrec = np.fft.ifft(np.real(np.fft.fft(y)))

    return Y_DC, Yn, PHIn, yrec

