
"""
Created on Tue Dec  5 14:24:43 2023

@author: Team PACman

"""
import os
import mne
import pandas as pd
import numpy as np
import neurokit2 as nk
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.signal import hilbert
from scipy import signal
import joblib
from os import makedirs

def ECG_elab(signal,sfreq,mode = "RR"):
    """  
    Input:
    signal = np.array of dimension [1, N], N = time-points, 1-dimensional signal  
    sfreq = sampling frequency
    mode string to select the kind of output: 
        "RR" -> RR series, filtered, resampled at the original sampling frequency, from [https://doi.org/10.1016/j.nlm.2018.12.008]
        "HR" -> Heart rate, at the original sampling frequency
        "HR_avg" -> Heart rate, at the original sampling frequency, smoothed from [https://doi.org/10.3791%2F55863]
    """
    prepro_sample, prepro_info = nk.ecg_process(signal, sampling_rate=sfreq, method='neurokit') #ECG preprocessing
   
    if mode =="RR":
        rr_intervals = prepro_sample['ECG_R_Peaks'] #vector of R peaks (TRUE = R peaks in the corrisponding signal's sample, FLASE = no R peaks in the corresponding signal's sample)
        #Extraction of the timing of the R peaks
        peaks_ts = []
        for idx, peak in enumerate(rr_intervals):
            if peak == 1:
                peaks_ts.append(idx/sfreq)
        differences = np.diff(peaks_ts) # RR series
        
        peaks_ts = peaks_ts[:-1] #removal of last time-values since each RR value is a difference between two peaks
        interpolation_function = interp1d(peaks_ts, differences, kind='cubic', fill_value='extrapolate')#cubic interpolation
        new_time = np.arange(peaks_ts[0], peaks_ts[-1], 1.0 / sfreq) #time-vector
        rr_resample = interpolation_function(new_time) #interpolation of RR serie
        lc = 0.04
        hc = 0.4
        RR_filt = nk.signal_filter(rr_resample, 
                                  sampling_rate = sfreq, 
                                  lowcut =lc, 
                                  highcut=hc, 
                                  method ='butterworth', 
                                  order=2,
                                  show=False
                                  )
        return RR_filt
    
    elif mode == "HR":
        hr_rate = np.array(prepro_sample['ECG_Rate']) #extraction of heart rate
        return hr_rate
    
    if mode == "HR_avg":
        hr_rate = prepro_sample['ECG_Rate'] #extraction of heart rate
        N = int(np.round(4*sfreq)) #Averago in over window of 4seconds, from [https://doi.org/10.3791%2F55863]
        hr_rate_avg = np.convolve(hr_rate, np.ones(N)/N, mode='valid')
        return hr_rate_avg
    
def  Wavelet(data, sfreq, freq_parameters, compute_power = True, compute_phase = True, plot_fig = False):

    """  
    Input:
    data = np.array of dimension [1, N], N = time-points, 1-dimensional signal  
    sfreq = sampling frequency
    freq_parameters = tuple (min freq, max freq, steps), parameters of the frequency analysis: 
    min freq = minimum frequency to analyze, 
    max freq = maximum frequency to analyze, 
    steps minimum = step length between each frequency  
    compute_power = set True to compute the power
    compute_phase = set True to compute the phase
    """
    
    # Select foi and number of cycles per frequency
    freqs = np.arange(freq_parameters[0],freq_parameters[1],freq_parameters[2])
    n_cycles=  np.linspace(2, 10, num= len(freqs))
    
    # compute wavelets 
    Ws= mne.time_frequency.morlet(sfreq, freqs, n_cycles=n_cycles, sigma=None, zero_mean=True)
    
    # Compute tfr 
    data = np.reshape(data, (1,np.size(data)))
    tfr= mne.time_frequency.tfr.cwt(data, Ws, use_fft=True, mode='same', decim=1)
    
    if plot_fig:
        fig, axs = plt.subplots(2)
        a = np.reshape(tfr, (tfr.shape[1], tfr.shape[2]))
        t =  np.arange(0, (np.size(data))/sfreq, 1/sfreq)
        t = np.reshape(t, (np.size(t),1));
        b = np.reshape(data, (np.size(data),1));
        # First subplot
        axs[0].plot(t,b)
        axs[0].set_title("Signal")
        axs[0].set_xlabel("Time (s)")
        axs[0].set_ylabel("Amplitude")

        # Second subplot
        t = np.reshape(t, (1,np.size(t)));
        pcm = axs[1].pcolormesh( t[:], freqs, np.abs(a[:,:]))
        axs[1].set_title("Scalogram")
        plt.axis('tight')
        axs[1].set_xlabel("Time (s)")
        axs[1].set_ylabel("Frequency (Hz)")
        #plt.colorbar(pcm) 
        #plt.yscale("log")

    
    # optional: save tfr results 
    # joblib.dump(tfr, join(out_dir, "wavelets_results"))
    
    # Exctract the power and the phase 
    if compute_power and not(compute_phase):
        power = np.squeeze(np.abs(tfr))
        return power, freqs
    elif compute_phase and not(compute_power): 
        phase = np.squeeze(np.angle(tfr))
        return phase, freqs
    else:
        power = np.squeeze(np.abs(tfr))
        phase = np.squeeze(np.angle(tfr))
        return power, phase, freqs
     
    
    
def Hilbert(data, sfreq, freq_parameters, compute_power = True, compute_phase = True ):
    """  
    Input:
    data = np.array of dimension [1, N], N = time-points, 1-dimensional signal  
    sfreq = sampling frequency
    freq_parameters = tuple (min freq, max freq, steps), parameters of the frequency analysis: 
    min freq = minimum frequency to analyze, 
    max freq = maximum frequency to analyze, 
    steps minimum = step length between each frequency  
    compute_power = set True to compute the power
    compute_phase = set True to compute the phase
    """
   
    freqs = np.arange(freq_parameters[0],freq_parameters[1],freq_parameters[2])
    powers = []
    phases = []
    
    for i in range(np.size(freqs)-1):
        low = freqs[i]
        high = freqs[i+1] 
        filtered_data = nk.signal_filter(data, 
                                  sampling_rate = sfreq, 
                                  lowcut =low, 
                                  highcut=high, 
                                  method ='butterworth', 
                                  order=5,
                                  show=False
                                  )
        
        analytic = hilbert(filtered_data)        
        
        if compute_power and not(compute_phase):
            power = np.abs(analytic)
            powers.append(power)
            #powers = np.vstack((powers, power))
            
        elif compute_phase and not(compute_power): 
            phase = np.angle(analytic)
            phases.append(phase)
            
        else:
            power = np.abs(analytic)
            phase = np.angle(analytic)
            
            powers.append(power)
            phases.append(phase)

        
    if compute_power and not(compute_phase):
        power = np.squeeze(np.array(powers))
        return power, freqs
        
    elif compute_phase and not(compute_power): 
        phases = np.squeeze(np.array(phases))
        return phase, freqs
    else:
        power = np.squeeze(np.array(powers))
        phases = np.squeeze(np.array(phases))
        return power, phase, freqs
        
        
    
    
