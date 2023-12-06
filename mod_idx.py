#%%
import numpy as np

def mod_idx(tfr, raw_x, sfreq=256, sp_in_sec=3382, timing=50, window_length=5, 
            freqs= np.arange(0.5, 16.5, 0.5), freq_1=2, freq_2=13):

    # Extract power and phase
    power_1= np.squeeze(np.abs(tfr))
    phase_1= np.squeeze(np.angle(tfr))

    # Take first 50 sec
    starting_point= sp_in_sec*sfreq
    ending_point= starting_point + timing*sfreq

    power= power_1[:, starting_point:ending_point]
    phase= phase_1[:, starting_point:ending_point]

    #  Compute Modulation Index (MI)    

    zeta_all = []

    for pow in power:
        z_all = []

        for ph in phase:
            z = pow * (np.exp(1j * ph))
            z_all.append(z)

        zeta_all.append(np.asarray(z_all))

    zn = np.asarray(zeta_all)

    kernel = np.ones(sfreq*window_length)
  
    # Calculate the sum of z[n] by convolving with the kernel
    mi = abs((np.apply_along_axis(
    lambda mi_: np.convolve(mi_, kernel, mode="valid"), 
    axis=-1, arr=zn))/len(kernel))

    couple= np.squeeze(mi[np.where(freqs==freq_1),
           np.where(freqs==freq_2),:])
    
    starting_point= (sp_in_sec*sfreq + window_length*sfreq)
    ending_point= (starting_point + timing*sfreq - window_length*sfreq)

    raw_signal= np.squeeze(raw_x[:, starting_point:ending_point])

    return mi, raw_signal, couple


# ax = plt.gca()
# ax.plot(stats.zscore(couple), color='r')
# ax.plot(stats.zscore(raw_signal), color='b')
# ax.legend(["PAC", "Raw"])
# plt.xlabel('Time (ms)')
# plt.ylabel('z-scores')
# plt.title('Channel F3A2 (freq 2-13 Hz)')
