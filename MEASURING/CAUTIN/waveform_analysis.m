function [] = waveform_analysis(TimeVolt, TimeCurr)
% Analysis of a waveform captured by an oscilloscope.
%
% 1. Import files from oscilloscope
% 2. Provide the number of points that make ONE period.
% 3. Crop the original data to keep ONE period.
% 4. Use function "fourier_series" to get coefficients
% 5. Do some plots.
% 6. Compute
%    S:   apparent power
%    P:   active power
%    Q:   reactive power
%    D:   volt-amp distorsion power
%    THD: total harmonic distorsion
%
% Author: L.Torres 18.08.2016
% 22.08.2016, enhanced Matlab compatibility.

% 1. Import files from oscilloscope:
%   - This may change for different oscilloscope models.
%   - Here we assume that in each file there are two columns:
%     The FIRST column is the time of each sample (horizontal axis),
%     and the SECOND column is the voltage (or current, the vertical axis).
%     Provide your file names!
%TimeVolt = dlmread('F0000MTH.txt');
%TimeCurr = dlmread('F0000CH2.txt');

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



% 5. Do some plots.
  % Plot the acquired waves, scale current (I) to milliamps
    fig = figure(1);
    plot(t_full,[V_wave_full, 1000*I_wave_full]);
    title('Original waveforms (full length), Volts, milliAmps');
    xlabel('Times(s)');
    ylabel('Amplitude');
    legend('Voltage (V)', 'Current (mA)');
    grid on;
    saveas(fig, 'original_waveform.png');


  % Plot the cropped waves, scale current (I) to milliamps
    fig = figure(2);
    plot(t,[V_wave, 1000*I_wave]);
    title('Cropped waveforms (ONE period), Volts, milliAmps');
    legend('Voltage (V)', 'Current (mA)');
    grid on;
    axis('tight');
    xlabel('Time (s)');
    ylabel('Amplitude');
    axLim=axis(gca);
    saveas(fig, 'cropped_waveform.png');

  % Plot the magnitude of Fourier coefficients for current and voltage
    N = 1 + length(In);
    Ts = t(2)-t(1); % sampling period
    T = Ts*N_onePeriod; %period chosen
    f0 = 1/T; %fundamental frequency
    fscale = (0:length(In))' * f0; %(as column vector)

    fig = figure(3);
    stem(fscale,[I_DC;In]);
    title('Magnitude of Fourier coefficients for current (Amps)');
    xlabel('Frequency (Hz)');
    ylabel('Magnitude (A)');
    grid on;
    saveas(fig, 'current_furier_coefficients.png');

    fig = figure(4);
    stem(fscale,[V_DC;Vn]);
    xlabel('Frequency (Hz)');
    ylabel('Magnitude (V)');
    title('Magnitude of Fourier coefficients for Voltage (Volts)');
    grid on;
    saveas(fig, 'voltage_furier_coefficients.png');

  % Plot the reconstructed version of voltage and current
  % scale current (I) to milliamps
    fig = figure(5);
    plot(t,[Vrec,1000*Irec]);
    axis(gca,axLim);
    title('Reconstructed versions of voltage (V) and current (mA)');
    xlabel('Time (s)');
    ylabel('Amplitude');
    grid on;
    saveas(fig, 'reconstructed_voltage_current.png');    
    
% 6. Compute assuming general case
%    S:   apparent power
%    P:   active power
%    Q:   reactive power
%    D:   volt-amp distorsion power
%    THD: total harmonic distorsion

     Vrms = sqrt(mean(V_wave.^2));  % in Volts
     Irms = sqrt(mean(I_wave.^2));  % in Amps

     S = Vrms*Irms;

     % Definition of P and Q for general case:
     %
     %    infty           infty
     % P = Sum  Pn ,   Q = Sum  Qn
     %     n=0             n=0
     %
     %  where
     %  Pn = Vn*In/2 * cos(Angle_Volt_n - Angle_Curr_n);
     %  Qn = Vn*In/2 * sin(Angle_Volt_n - Angle_Curr_n);
     %
     %  For the case of pure sinusoidal voltage, only the
     %  powers at DC and the fundamental frequency remain:
     %  P = P0 + P1,   and  Q = Q1

     P0   = V_DC*I_DC;
     Q0   = 0;
     % or equivalently,
     P_DC = V_DC*I_DC;
     Q_DC = 0;

     % Other terms:
     Pn = Vn.*In/2 .* cos(V_PHIn - I_PHIn);
     Qn = Vn.*In/2 .* sin(V_PHIn - I_PHIn);

     % Total active and reactive powers, P and Q:
     P = P0 + sum(Pn);
     Q = 0  + sum(Qn);
     %Alternatively for P you can apply the definition,
     % the mean value of the instantaneous power:
     P_wave = V_wave.*I_wave; %instantaneous
     Pavg = mean(P_wave);

     % S^2 = P^2 + Q^2 + D^2
     D_fast = sqrt(S^2 - P^2 - Q^2);

     % Long (and slow) method, in terms of components
     D2 = 0;
     D  = 0;
     V_0n = [V_DC; Vn];
     V_PHI0n = [0; V_PHIn];
     I_0n = [I_DC; In];
     I_PHI0n = [0; I_PHIn];
     N = length(V_0n);
     tic();
     for idxN = 1:N
       for idxM = 1:N
         if (idxN ~= idxM)
           D2 = D2 + 1/4*V_0n(idxN)^2*I_0n(idxM)^2 - 1/4*V_0n(idxN)*V_0n(idxM)*I_0n(idxN)*I_0n(idxM)*cos((V_PHI0n(idxN)-V_PHI0n(idxM))-(I_PHI0n(idxN)-I_PHI0n(idxM)));
         end
       end
     end
     elapsed_time = toc()
     %Finally, we take square root
     D = sqrt(D2);


     % Power Factor
     PF = P/S;

     % Definition of THD of signal y(t)
     %
     %  THD^2 =  1/(Y_1)^2 * (Y_DC^2 + sum (Y_n)^2).
     %                                 n > 1
     % Note: Total harmonic distortion measures how much a
     %       waveform differs from the sinusoid whose period
     %       corresponds to the length of the (cropped) data vector
     THD_V = sqrt( (V_DC^2 + sum(Vn(2:end).^2) ) / Vn(1)^2 );
     THD_I = sqrt( (I_DC^2 + sum(In(2:end).^2) ) / In(1)^2 );

     % printf values
     fileID = fopen('output.txt', 'w');
     fprintf(fileID, 'T     = %10.4f s (one period)\n',T);
     fprintf(fileID, 'f0    = %10.4f Hz (fundamental frequency)\n',f0);
     fprintf(fileID, 'Vrms  = %10.4f V\n',Vrms);
     fprintf(fileID, 'Irms  = %10.4f A\n',Irms);
     fprintf(fileID, 'S     = %10.4f VA\n',S);
     fprintf(fileID, 'Pavg  = %10.4f W (directly using definition)\n',Pavg);
     fprintf(fileID, 'P     = %10.4f W (based on Fourier series)\n',P);
     fprintf(fileID, 'Q     = %10.4f VAR (based on Fourier series)\n',Q);
     fprintf(fileID, 'D_fast= %10.4f VA (distortion power, fast, easy from S^2)\n',D_fast);
     fprintf(fileID, 'D     = %10.4f VA (distortion power, slow, full computation)\n',D);
     fprintf(fileID,'PF    = %10.4f (power factor)\n',PF);
     fprintf(fileID, 'THD_V = %10.4f %%\n',THD_V*100);
     fprintf(fileID, 'THD_I = %10.4f %%\n',THD_I*100);
     fclose(fileID);
 end
