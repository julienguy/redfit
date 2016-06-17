#!/usr/bin/env python

import pyfits
import sys
import numpy as np
import os.path

#for ifilename in ['../templates/ndArch-ssp_em_galaxy-v000.fits','../templates/ndArch-spEigenStar-55734.fits','../templates/ndArch-QSO-V003.fits'] :
for ifilename in ['../templates/ndArch-QSO-V003.fits'] :

    h=pyfits.open(ifilename)
    h.info()

    # Number of templates    
    nbtemp = h[0].shape[0]
    print '%d templates found'%nbtemp

    # First, exlude templates with negative flux
    index, = np.where(np.sum(h[0].data<0.,axis=1)==0)

    # Builds wavelength grid
    w = np.arange(h[0].header['CRVAL1'],h[0].header['CRVAL1']+h[0].header['CDELT1']*h[0].header['NAXIS1'],h[0].header['CDELT1'])
    w=10**w
    dw = (w[1]-w[0])
    
    # Assume snr of 0.1 per angtroems
    snr=0.1*np.sqrt(dw)

    # Keep templates with chi2 > chi2_cut
    chi2_cut = 1.
    
    bad=list()
    valid=list(index)
    for i in range(index.size):
        for j in range(index.size):
            chi2 = np.sum((h[0].data[index[j]]-h[0].data[index[i]])**2.)*(snr**2.)
            if ((chi2 < chi2_cut) & (chi2 != 0.)): 
                try:
                    bad=valid.pop(int(np.where(valid == valid[index[j]])[0]))
                except:
                    pass
    
    print "Keeping %d templates with non-zero values and chi2 diff. greater than %f"%(len(valid),chi2_cut)

    
    if (False):
        import pylab as pl
        for i in valid:
            pl.plot(w,h[0].data[i,:])
        pl.show()
    
    # Write new list of templates in fits file
    h[0].data = h[0].data[valid,:]
    print h[0].shape
    ofilename=os.path.basename(ifilename)
    h.writeto(ofilename,clobber=True)
    print "wrote",ofilename
