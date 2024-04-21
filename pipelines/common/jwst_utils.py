import numpy as np


def get_pixscl(hdu, ext=0):
    """
    Get the pixel scale from the FITS header.
    
    Parameters:
    hdu : astropy.io.fits.hdu.hdulist.HDUList
        The FITS HDUList object.
    ext : int
        The FITS extension to extract the pixel scale from.
    
    Returns:
    pixscl : float
        The pixel scale in arcseconds.
    """
    pixscl = np.sqrt(abs(hdu[ext].header['CDELT1'] * hdu[ext].header['CDELT2']) - abs(0)) * 60 * 60
    return pixscl