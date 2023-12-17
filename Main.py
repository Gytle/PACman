# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 14:14:56 2023

@author: PACman team
"""
#%%  #Import packages
import Mod1
import Mod2

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
from os.path import join, exists

#%% # Load data ECG
datapath = "C:\\Users\\Utente\\Desktop\\PACman-main\\ecg-20231205T111854Z-001\\ecg"
samples = os.listdir(datapath)
sub_one_path = os.path.join(datapath, samples[2])  #Import .set data

sig_start = 3382*256  # [n° of sample]
sig_end = (3382+50)*256  # [n° of sample]

sample = mne.io.read_raw_eeglab(sub_one_path) #Import EEGlab
sfreq = sample.info["sfreq"]
ecg_data = sample[0][0]
ecg_data = ecg_data[0][sig_start:sig_end]

#%% # Load data EEG

# Select subject id
datapath = "C:\\Users\\Utente\\Desktop\\PACman-main\\eeg"
subject_id= "Subject_n1_eeg.set"

# Load Data from .set file to MNE
raw = mne.io.read_raw_eeglab(join(datapath, subject_id), preload= True)

# Extract data from 1 channel
channel= 'F3A2'
eeg_data = raw.get_data(picks= channel)
eeg_data = eeg_data[0][sig_start:sig_end]

#%% # Preprocess ECG

RR_ecg = Mod1.ECG_elab(ecg_data,sfreq,mode = "RR")
    
#%% # Alignment EEG-RR
eeg_data = eeg_data[0:len(RR_ecg)]

t =  np.arange(0, (len(RR_ecg))/sfreq, 1/sfreq)
fig,  axs = plt.subplots(3)
axs[0].plot(t,ecg_data[0:len(RR_ecg)])
axs[0].set_title("Original signal ECG")
axs[0].set_xlabel("Time (s)")
axs[1].plot(t, RR_ecg)
axs[1].set_title("RR serie")
axs[1].set_xlabel("Time (s)")
axs[2].plot(t, eeg_data)
axs[2].set_title("EEG")
axs[2].set_xlabel("Time (s)")

#%% # Extraction of phase and power
freq_parameters_ecg = (0.04, 0.4, 0.02)
freq_parameters_eeg = (1,13,1)
phase_ECG, freqs_ECG =  Mod1.Wavelet(RR_ecg, sfreq, freq_parameters_ecg, compute_power = False, compute_phase = True, plot_fig = True)
phase_EEG, power_EEG, freqs_EEG =  Mod1.Wavelet(eeg_data, sfreq, freq_parameters_eeg, compute_power = True, compute_phase = True, plot_fig = True)

#phase_ECG, freqs_ECG = Mod1.Hilbert(RR_ecg, sfreq, freq_parameters_ecg, compute_power = False, compute_phase = True ) 
#phase_EEG, power_EEG, freqs_EEG = Mod1.Hilbert(eeg_data, sfreq, freq_parameters_eeg, compute_power = True, compute_phase = True )

#%% MI vector
mi_vect_ECG_EEG = Mod2.contMI_vectorized(phase_ECG,power_EEG,sfreq,winsize=5.,decim=1)
mi_vect_EEG_EEG = Mod2.contMI_vectorized(phase_EEG,power_EEG,sfreq,winsize=5.,decim=1)

mi_ent_ECG_EEG = Mod2.contMI_entropy(phase_ECG,power_EEG,sfreq,winsize=5.,decim=1,Nbin=16)
mi_ent_EEG_EEG = Mod2.contMI_entropy(phase_EEG,power_EEG,sfreq,winsize=5.,decim=1,Nbin=16)
