# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 12:06:26 2023

@author: Guillaume
"""

# %% Import modules
import mne
from os.path import join, exists
import numpy as np
import joblib
from os import makedirs

# %% Find data and upload eeg data
# Set the Path (input and output dir)
data_path= 'eeg'
out_dir= 'results/F3A2'
if not exists(out_dir):
    makedirs(out_dir)

# Select subject id
subject_id= "Subject_n1_eeg.set"
subject_annot= "Subject_n1_annot.fif"

# Load Data from .set file to MNE
raw = mne.io.read_raw_eeglab(join(data_path, subject_id), preload= True)
annot = mne.read_annotations(join(data_path, subject_annot))
raw.set_annotations(annot)

# Extract data from 1 channel
channel= 'F3A2'
X = raw.get_data(picks= channel)


# %% Extract phase and amplitude of eeg signal
# This part will be replaced with the modules extracting phase and amplitude with different methods
# Wavelet convolution, bandpass-hilbert transform...

# Select foi and number of cycles per frequency
freqs= np.arange(0.5, 16.5, 0.5)
n_cycles=  np.linspace(2, 10, num= len(freqs))
sfreq= raw.info['sfreq']

# compute wavelets 
Ws= mne.time_frequency.morlet(sfreq, freqs, n_cycles=n_cycles, sigma=None, zero_mean=True)

# Compute tfr 
tfr= mne.time_frequency.tfr.cwt(X, Ws, use_fft=True, mode='same', decim=1)

# optional: save tfr results 
# joblib.dump(tfr, join(out_dir, "wavelets_results"))

# Exctract the power and the phase 
power= np.squeeze(np.abs(tfr))
phase= np.squeeze(np.angle(tfr))

# %% Let select only a part of the signal

# We define a starting time for the small epoch we want to extract and try phase-amplitude coupling
startTime = 3500 # in seconds
epochlen = 600 # in seconds

A = power[:,startTime+np.arange(10*60*256,dtype=int)]
phi = phase[:,startTime+np.arange(10*60*256,dtype=int)]

# %% Let's compute the MI over time with different methods

