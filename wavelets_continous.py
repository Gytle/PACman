# %%
import mne
from os.path import join, exists
import numpy as np
import joblib
from os import makedirs

# Set the Path (input and output dir)
data_path= 'eeg'
out_dir= 'results/F3A2'
if not exists(out_dir):
    makedirs(out_dir)

# Select subject id
subject_id= "Subject_n1_eeg.set"

# Load Data from .set file to MNE
raw= mne.io.read_raw_eeglab(join(data_path, subject_id), preload= True)

# Extract data from 1 channel
channel= 'F3A2'
X= raw.get_data(picks= channel)

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






