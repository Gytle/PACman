# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 11:09:33 2023

@author: Guillaume
"""

import numpy as np
import scipy as sp


def contMI(phi,A,fs,winsize=5.,decim=1,Nbin=16):
    
    winsizeT = np.round(winsize*fs)
    
    winSta = np.arange(A.shape[1]-winsizeT,step=decim,dtype=int)
    
    MIsig = np.zeros((phi.shape[0],A.shape[0],A.shape[1]))
    MIsig[:] = np.nan
    for iSta in np.arange(winSta.shape[0]):
        MIsig[:,:,iSta] = compMI(phi[:,winSta[iSta]+np.arange(winsizeT,dtype=int)],A[:,winSta[iSta]+np.arange(winsizeT,dtype=int)],Nbin=16)
    
    return MIsig

def compMI(phi,A,Nbin=16):
    
    allbins = np.linspace(-np.pi,np.pi,Nbin+1)

    phiSegMI = np.zeros((phi.shape[0],A.shape[0],A.shape[1]))
    phiSegMI[:] = np.nan
    for iBin in np.arange(allbins.shape[0]-1):
        
        indmat = 1*np.multiply(phi>=allbins[iBin],phi<allbins[iBin+1])
        
        indmat2 = np.repeat(np.expand_dims(indmat,axis=1),A.shape[0],axis=1)
        expA = np.repeat(np.expand_dims(A,axis=0),phi.shape[0],axis=0)
        
        phiSegMI[:,:,iBin] = np.divide(np.nansum(np.multiply(expA,indmat2),axis=2),np.nansum(indmat2,axis=2))
    
    regphiSegMI = np.divide(phiSegMI,np.repeat(np.expand_dims(np.nansum(phiSegMI,axis=2),axis=2),phiSegMI.shape[2],axis=2))

    MI = 1+np.nansum(np.multiply(regphiSegMI,np.log(regphiSegMI)),axis=2)/np.log(Nbin)    
    
    return MI
