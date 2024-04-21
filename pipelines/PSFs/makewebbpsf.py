import webbpsf
from astropy import time
from astropy.io import fits

from pipelines.common.jwst_utils import get_pixscl
from pipelines.images.rotate import imrotate

from ..logging.logger_config import setup_logger

webbpsf.setup_logging()
logger = setup_logger()

def generate_webbpsf(filter, img_hdu, ext, pixscl, oversample, fov_pixels, fov_arcsec):
    """ Generate a WebbPSF for the given filter.
    
    Parameters:
    filter : str
        The filter to generate the WebbPSF for.
    img_hdu : astropy.io.fits.hdu.hdulist.HDUList
        The image HDUList object.
    ext : int
        The FITS extension to extract the pixel scale from.
    pixscl : float
        The pixel scale for the WebbPSF.
    oversample : int
        The oversampling factor for the WebbPSF.
    fov_pixels : int
        The field of view in pixels for the WebbPSF.
    fov_arcsec : float
        The field of view in arcseconds for the WebbPSF.
    
    Returns:
    psf : astropy.io.fits.hdu.hdulist.HDUList
        The WebbPSF HDUList object.
    """
    logger.verbose(f"Generating WebbPSF for filter {filter}")

    try:
        nc = webbpsf.NIRCam()
        nc.filter = filter
        nc.pixelscale = pixscl if pixscl else get_pixscl(img_hdu, ext)

        t = time.Time(img_hdu[ext].header['MJD-AVG'], format='mjd')
        nc.load_wss_opd_by_date(t.iso.replace(' ', 'T'))

        # output format
        nc.options['output_mode'] = 'both'

        psf = nc.calc_psf(oversample=oversample, fov_pixels=fov_pixels, fov_arcsec=fov_arcsec)
        
        logger.info(f"WebbPSF generated for filter {filter}")
        logger.info(f"Pixscale for the oversampled PSF: {psf['OVERSAMP'].header['PIXELSCL']}")
        logger.info(f"Pixscale for the detector-sampled PSF: {psf['DET_SAMP'].header['PIXELSCL']}")

        return psf
    
    except Exception as e:
        logger.error(f"Failed to generate WebbPSF for filter {filter}: {e}", exc_info=True)
        return None
    

def rotate_webbpsf(psf, img_hdu=None, ext=None, pa=None):
    """ Rotate the WebbPSF by the given position angle.
    
    Parameters:
    psf : astropy.io.fits.hdu.hdulist.HDUList
        The WebbPSF HDUList object.
    img_hdu : astropy.io.fits.hdu.hdulist.HDUList
        The image HDUList object.
    ext : int
        The FITS extension to extract the pixel scale from.
    pa : float
        The position angle in degrees.
        
    Returns:
    psf : astropy.io.fits.hdu.hdulist.HDUList
        The rotated WebbPSF HDUList object.
    """

    try:
        angle = pa if pa else img_hdu[ext].header['PA_APER']
        logger.verbose(f"Rotating WebbPSF by PA={angle}")
        rotated_psf_oversamp = imrotate(psf['OVERSAMP'].data, angle, reshape=False)
        rotated_psf_detsamp = imrotate(psf['DET_SAMP'].data, angle, reshape=False)

        # add these two files to the hdu list
        psf.append(fits.ImageHDU(data=rotated_psf_oversamp, name='ROTATED_OVERSAMP', header=psf['OVERSAMP'].header.copy()))
        psf.append(fits.ImageHDU(data=rotated_psf_detsamp, name='ROTATED_DET_SAMP', header=psf['DET_SAMP'].header.copy()))

        # copy the header from the input image HDU to the rotated PSF HDU and add a comment about the rotation
        psf['ROTATED_OVERSAMP'].header['COMMENT'] = f"Rotated by PA={angle} degrees"
        psf['ROTATED_DET_SAMP'].header['COMMENT'] = f"Rotated by PA={angle} degrees"

        return psf
    except Exception as e:
        logger.error(f"Failed to rotate WebbPSF by PA={angle}: {e}", exc_info=True)
        return None
