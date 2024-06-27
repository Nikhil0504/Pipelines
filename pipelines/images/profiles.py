from astropy.io import fits
from astropy.wcs import WCS
from photutils.aperture import SkyRectangularAperture
import numpy as np

from ..logging.logger_config import setup_logger
from ..images.img_utils import flatten_array

logger = setup_logger()


def get_flux_profiles(filters, img_dict, apertures, axis=0, crop=slice(None, None), crop2=slice(None, None)):
    """
    Gets the flux profiles of the data for a given set of filters and apertures.

    Parameters
    ----------
    filters : list
        List of filters to get the profiles for.
    img_dict : dict
        Dictionary with the paths to the images for each filter.
        It will be in the form of {filter: path}.
    apertures : list[SkyRectangularAperture]
        List of apertures to get the profiles for. It should be in the form of
        [SkyRectangularAperture(...), ...]. We will need the WCS to convert the
        apertures to pixel coordinates.
    axis : int
        Axis to sum the data along. Default is 0.
    
    Returns
    -------
    data_prof : dict
        Dictionary with the profiles of the data for each filter and aperture.
        It will be in the form of {filter: [profile1, profile2, ...]}.
    """
    # make a empty dictionary to store the data of the profiles with each filter as key
    data_prof = {filter: [] for filter in filters}

    for filt in filters:
        logger.verbose(f"Getting flux profiles for filter {filt}")

        img_path = img_dict[filt]
        hdul = fits.open(img_path)

        data = hdul[0].data
        wcs = WCS(hdul[0].header)

        for aperture in apertures:
            if not isinstance(aperture, SkyRectangularAperture):
                logger.error("The apertures should be of type SkyRectangularAperture.")
                raise TypeError("The apertures should be of type SkyRectangularAperture.")

            ap_pix = aperture.to_pixel(wcs)
            mask = ap_pix.to_mask(method='exact')

            cutout_data = mask.multiply(data)
            cutout_data = np.rot90(cutout_data, k=1)
            cutout_data = flatten_array(cutout_data)
            cutout_data = cutout_data[crop, crop2]
            cutout_data = np.clip(cutout_data, 0, None)

            # append to the data dictionary
            profile = np.average(cutout_data, axis=axis)
            data_prof[filt].append(profile)

    return data_prof