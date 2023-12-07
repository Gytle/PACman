# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 11:30:34 2023

@author: Guillaume
"""

import numpy as np


def contMI(phi,A,fs,winsize=5.,decim=1):
    
    zn = np.multiply(np.repeat(np.expand_dims(A,axis=0),phi.shape[0],axis=0),np.exp(1j*np.repeat(np.expand_dims(phi,axis=1),A.shape[0],axis=1)))

    kernel = np.ones(np.int64(np.round(fs*winsize)))

    MIsig = abs((np.apply_along_axis(
    lambda mi_: np.convolve(mi_, kernel, mode="valid"), 
    axis=-1, arr=zn))/len(kernel))   
    
    return MIsig[:,:,np.arange(MIsig.shape[2],step=decim,dtype=int)]
    
    