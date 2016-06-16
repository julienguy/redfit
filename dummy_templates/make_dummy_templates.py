#!/usr/bin/env python

import pyfits
import sys
import numpy as np
import os.path

reduction=30

for ifilename in ['../templates/ndArch-ssp_em_galaxy-v000.fits','../templates/ndArch-spEigenStar-55734.fits','../templates/ndArch-QSO-V003.fits'] :
    h=pyfits.open(ifilename)
    h.info()
    
    nparamdim=len(h[0].data.shape)-1
    print nparamdim
    red=(np.power(reduction,1./nparamdim))
    nshape=h[0].data.shape
    for d in range(len(h[0].data.shape)-1) :
        nsize=max(1,int(h[0].data.shape[d]/red))
        print "%d -> %d"%(h[0].data.shape[d],nsize)
        if d==0 :
            h[0].data=h[0].data[:nsize]
        elif d==1 :
            h[0].data=h[0].data[:,:nsize]
        elif d==2 :
            h[0].data=h[0].data[:,:,:nsize]
        elif d==3 :
            h[0].data=h[0].data[:,:,:,:nsize]
        else :
            print "stop here"
            break
    print h[0].data.shape
    ofilename=os.path.basename(ifilename)
    h.writeto(ofilename,clobber=True)
    print "wrote",ofilename

    
