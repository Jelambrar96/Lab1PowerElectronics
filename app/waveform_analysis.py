#

import numpy as np
from matplotlib import pyplot as plt

from fourier import fourier_series

class WaveAnalizer(object):

    def __init__(self, voltage_array, current_array, time_array, nperiod):

        self._string_out= ""
        self._output_dict = {}

        self._voltage_array = voltage_array
        self._current_array = current_array
        self._time_array = time_array
        self._nperiod = nperiod

        self._voltage_wave = self._voltage_array[0:nperiod]
        self._current_wave = self._current_array[0:nperiod]
        self._time_wave = self._time_array[0:nperiod]

        self._computed = False

        self._fscale = None
        self._T = None
        self._f0 = None

        self._V_DC, self._Vn, self._V_PHIn, self._Vrec = None, None, None, None
        self._I_DC, self._In, self._I_PHIn, self._Irec = None, None, None, None
        


        
    def compute(self):
        
        V_DC, Vn, V_PHIn, Vrec = fourier_series(self._voltage_wave)
        I_DC, In, I_PHIn, Irec = fourier_series(self._current_wave)

        self._V_DC, self._Vn, self._V_PHIn, self._Vrec = V_DC, Vn, V_PHIn, Vrec
        self._I_DC, self._In, self._I_PHIn, self._Irec = I_DC, In, I_PHIn, Irec

        #  % Plot the magnitude of Fourier coefficients for current and voltage   
        N = 1 + self._In.shape[0]
        Ts = self._time_wave[1] - self._time_wave[0] # % sampling period
        self._T = Ts * self._nperiod # ; %period chosen 
        self._f0 = 1 / self._T # ; %fundamental frequency
        # fscale = (0:length(In))' * f0; %(as column vector)
        self._fscale = np.arange(N) * self._f0

        self._computed = True
        
        self._Vrms = np.sqrt(np.mean(np.square(self._voltage_wave))) #  % in Volts
        self._Irms = np.sqrt(np.mean(np.square(self._current_wave))) #  % in Amps 

        S = self._Vrms * self._Irms     
        self._S = S

        # % Definition of P and Q for general case:
        # %
        # %    infty           infty
        # % P = Sum  Pn ,   Q = Sum  Qn 
        # %     n=0             n=0
        # %
        # %  where
        # %  Pn = Vn*In/2 * cos(Angle_Volt_n - Angle_Curr_n);
        # %  Qn = Vn*In/2 * sin(Angle_Volt_n - Angle_Curr_n);
        # %
        # %  For the case of pure sinusoidal voltage, only the 
        # %  powers at DC and the fundamental frequency remain:
        # %  P = P0 + P1,   and  Q = Q1

        P0   = V_DC * I_DC;
        Q0   = 0
        # % or equivalently,
        P_DC = V_DC * I_DC;
        Q_DC = 0
     
        # % Other terms:
        Pn = Vn * In / 2 * np.cos(V_PHIn - I_PHIn);
        Qn = Vn * In / 2 * np.sin(V_PHIn - I_PHIn);

        # % Total active and reactive powers, P and Q: 
        P = P0 + np.sum(Pn);
        self._P = P
        Q = 0  + np.sum(Qn);
        self._Q = Q
        # %Alternatively for P you can apply the definition,
        # % the mean value of the instantaneous power:
        P_wave = self._voltage_wave * self._current_wave; # %instantaneous
        Pavg = np.mean(P_wave); 
        self._Pavg = Pavg
        
        # %S^2 = P^2 + Q^2 + D^2
        D_fast = np.sqrt(S**2 - P**2 - Q**2);
        self._D_fast = D_fast

        # % Long (and slow) method, in terms of components
        D2 = 0;
        D  = 0;
        V_0n = np.hstack((V_DC, Vn))
        V_PHI0n = np.hstack((0, V_PHIn));
        I_0n = np.hstack((I_DC, In));
        I_PHI0n = np.hstack((0, I_PHIn));
        N = V_0n.shape[0];
        # tic();
        
        # for idxN = 1:N
        # for idxM = 1:N
        #  if (idxN ~= idxM)
        #    D2 = D2 + 1/4*V_0n(idxN)^2*I_0n(idxM)^2 - 1/4*V_0n(idxN)*V_0n(idxM)*I_0n(idxN)*I_0n(idxM)*cos((V_PHI0n(idxN)-V_PHI0n(idxM))-(I_PHI0n(idxN)-I_PHI0n(idxM)));
        # end
        # end
        # end

        for idxN in range(N):
            for idxM in range(N):
                if idxN != idxM:
                    D2 += V_0n[idxN]**2 * I_0n[idxM] ** 2 / 4
                    D2 -= V_0n[idxN] * V_0n[idxM] * I_0n[idxN] * I_0n[idxM] * np.cos(V_PHI0n[idxN]-V_PHI0n[idxM]- I_PHI0n[idxN] + I_PHI0n[idxM]) / 4
                    
        self._D = np.sqrt(D2);


        # % Power Factor
        self._PF = P / S;

        # % Definition of THD of signal y(t)
        # %            
        # %  THD^2 =  1/(Y_1)^2 * (Y_DC^2 + sum (Y_n)^2). 
        # %                                 n > 1
        # % Note: Total harmonic distortion measures how much a 
        # %       waveform differs from the sinusoid whose period
        # %       corresponds to the length of the (cropped) data vector
        self._THD_V = np.sqrt( (V_DC**2 + np.sum( np.square(Vn[1:])) ) / Vn[0]**2 );
        self._THD_I = np.sqrt( (I_DC**2 + np.sum( np.square(In[1:])) ) / In[0]**2 );
        
        str_output = ""
        str_output = str_output + 'T      = {0:10.4f} s (one period)\n'.format(self._T)
        str_output = str_output + 'f0     = {0:10.4f} Hz (fundamental frequency)\n'.format(self._f0)
        str_output = str_output + 'Vrms   = {0:10.4f} V\n'.format(self._Vrms)
        str_output = str_output + 'Irms   = {0:10.4f} A\n'.format(self._Irms)
        str_output = str_output + 'S      = {0:10.4f} VA\n'.format(self._S)
        str_output = str_output + 'Pavg   = {0:10.4f} W (directly using definition)\n'.format(self._Pavg)
        str_output = str_output + 'P      = {0:10.4f} W (based on Fourier series)\n'.format(self._P)
        str_output = str_output + 'Q      = {0:10.4f} VAR (based on Fourier series)\n'.format(self._Q)
        str_output = str_output + 'D_fast = {0:10.4f} VA (distortion power, fast, easy from S^2)\n'.format(self._D_fast)
        str_output = str_output + 'D      = {0:10.4f} VA (distortion power, slow, full computation)\n'.format(self._D)
        str_output = str_output + 'PF     = {0:10.4f} (power factor)\n'.format(self._PF)
        str_output = str_output + 'TDH_V  = {0:10.4f} %\n'.format(self._THD_V * 100)
        str_output = str_output + 'TDH_I  = {0:10.4f} %\n'.format(self._THD_I * 100)
        
        self._string_out = str_output
        
        self._output_dict = {
            'T': self._T,
            'f0': self._f0,
            'Vrms': self._Vrms,
            'Irms': self._Irms,
            'S': self._S,
            'Pavg': self._Pavg,
            'P': self._P,
            'Q': self._Q,
            'D': self._D,
            'D_fast': self._D_fast,
            'TDH_V': self._THD_V,
            'TDH_I': self._THD_I
        }


    def getOutputString(self):
        return self._string_out

    def getOutputDict(self):
        return self._output_dict
    
    def plot(self):
        
        if not self._computed:
            print('ERROR: No computed data.')
            return
    
        plt.figure()
        plt.plot(self._time_array, self._voltage_array, 'b', label='Voltage (V)')
        plt.plot(self._time_array, self._current_array * 1000, 'r', label='Current (mA)')
        plt.grid(True)
        plt.title('Original waveforms (full length), Volts, milliAmps');
        plt.xlabel('Times(s)');
        plt.ylabel('Amplitude');
        plt.legend(loc='upper right', shadow=False)
        

        plt.figure()
        plt.plot(self._time_wave, self._voltage_wave, 'b', label='Voltage(V)')
        plt.plot(self._time_wave, self._current_wave * 1000, 'r', label='Current (mA)')
        plt.grid(True)
        plt.title('Cropped waveforms (ONE period), Volts, milliAmps');
        plt.xlabel('Times(s)');
        plt.ylabel('Amplitude');
        plt.legend(loc='upper right', shadow=False)
        
        
        plt.figure()
        plt.stem(self._fscale, np.hstack((self._I_DC, self._In)), use_line_collection=True, basefmt=" ");
        plt.title('Magnitude of Fourier coefficients for current (Amps)');
        plt.xlabel('Frequency (Hz)'); 
        plt.ylabel('Magnitude (A)');
        plt.grid(True);  
        
        plt.figure()
        plt.stem(self._fscale, np.hstack((self._V_DC, self._Vn)), use_line_collection = True, basefmt=" ");
        plt.xlabel('Frequency (Hz)');
        plt.ylabel('Magnitude (V)');
        plt.title('Magnitude of Fourier coefficients for Voltage (Volts)');
        plt.grid(True)  
        
        plt.figure()
        plt.plot(self._time_wave, self._Vrec, 'b', label='Voltage(V)')
        plt.plot(self._time_wave, self._Irec * 1000, 'r', label='Current (mA)')
        plt.title('Reconstructed versions of voltage (V) and current (mA)');
        plt.xlabel('Time (s)');
        plt.ylabel('Amplitude'); 
        plt.grid(True);
        plt.legend(loc='upper right', shadow=False)
        
        plt.show()
        
        
