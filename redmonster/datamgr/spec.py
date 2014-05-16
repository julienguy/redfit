from os import environ
from os.path import exists, join
from astropy.io import fits
import numpy as n
from math import ceil, floor
from redmonster.math.misc import flux_check

class Spec:

    def __init__(self, plate=None, mjd=None, fiberid=None, data_range=None):
        self.flux = None
        self.ivar = None
        self.loglambda = None
        self.andmask = None
        self.ormask = None
        self.plugmap = None
        self.skyflux = None
        self.nobj = None
        self.npix = None
        self.coeff0 = None
        self.coeff1 = None
        self.zwarning = n.zeros(len(fiberid))
        try: self.topdir = environ['BOSS_SPECTRO_REDUX']
        except: self.topdir = None
        try: self.run2d = environ['RUN2D']
        except: self.run2d = None
        self.set_plate_mjd(plate=plate, mjd=mjd, fiberid=fiberid, data_range=data_range)
        self.ivar = flux_check(self.flux, self.ivar)
    
    def set_plate_mjd(self, plate=None, mjd=None, fiberid=None, data_range=None):
        self.plate = plate
        self.mjd = mjd
        if self.topdir and self.run2d and self.plate and self.mjd:
            self.platepath = join(self.topdir,self.run2d,"%s" % self.plate,"spPlate-%s-%s.fits" % (self.plate,self.mjd))
            self.set_data()
            if data_range: self.chop_data(data_range)
            if fiberid: self.set_fibers(fiberid)
    
    def set_data(self):
        if self.platepath and exists(self.platepath): hdu = fits.open(self.platepath)
        else: print "Missing path to %r" % self.platepath
        try:
            self.flux = hdu[0].data
            self.ivar = hdu[1].data
            self.loglambda = hdu[0].header['COEFF0'] + n.arange(hdu[0].header['NAXIS1']) * hdu[0].header['COEFF1']
            self.andmask = hdu[2].data
            self.ormask = hdu[3].data
            self.plugmap = hdu[5].data
            self.skyflux = hdu[6].data
            # For plate files before Spectro-2D v5, there are no sky vectors and hdu[6] is something else
            if self.skyflux.shape != self.flux.shape: self.skyflux = 0
            self.nobj = hdu[0].header['NAXIS2']
            self.npix = hdu[0].header['NAXIS1']
            self.coeff0 = hdu[0].header['COEFF0']
            self.coeff1 = hdu[0].header['COEFF1']
        except Exception as e: print "Exception: %r" % e

    def chop_data(self, data_range):
        self.data_range = data_range
        i1 = ceil( (n.log10(data_range[0]) - self.coeff0) / self.coeff1 )
        i2 = floor( (n.log10(data_range[1]) - self.coeff0) / self.coeff1 )
        if i1 >= 0: self.ivar[:,:i1] = 0
        if i2 <= self.npix: self.ivar[:,i2:] = 0
        # CHANGE PRINT STATEMENT TO LOG
        print 'Trim wavelength range to %s' % data_range

    def set_fibers(self, fiberid):
        if min(fiberid) < 0 or max(fiberid) > self.nobj: print 'Invalid value for FIBERID: must be between 0 and %s' % hdu[0].header['NAXIS1'] # CHANGE THIS TO LOG INSTEAD OF PRINT
        else:
            self.fiberid = fiberid
            self.flux = self.flux[fiberid]
            self.ivar = self.ivar[fiberid]
            self.andmask = self.andmask[fiberid]
            self.ormask = self.ormask[fiberid]
            self.plugmap = self.plugmap[fiberid]
            self.nobj = len(fiberid)
            if self.skyflux.shape[0] != 1: self.skyflux = self.skyflux[fiberid]

    def flag_sky_fibers(self):
        flag_val = int('0b1',2) # From BOSS zwarning flag definitions
        for i in xrange(self.plugmap.shape[0]):
            if ( self.plugmap[i]['OBJTYPE'] == 'sky'): self.zwarning = self.zwarning ^ flagval












