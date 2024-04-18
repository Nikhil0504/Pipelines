from ..logging.logger_config import setup_logger

import numpy as np
import numpy.ma as ma
from astropy.stats import sigma_clip

logger = setup_logger()


def apply_sigma_mask(hdu, ext_img, sigma_lower=3, sigma_upper=3, iters=5):
    """
    Apply a sigma clipping algorithm to mask out outliers in an image using separate upper and lower bounds.
    Handles NaN values and returns statistical information about the clipping process.

    Parameters:
    image_data : numpy.ndarray
        The 2D array of image data.
    sigma_lower : float
        The number of standard deviations for the lower clipping limit.
    sigma_upper : float
        The number of standard deviations for the upper clipping limit.
    iters : int
        The number of iterations to perform clipping.

    Returns:
    masked_image : numpy.ndarray
        The masked image with outliers replaced by NaN.
    stats : dict
        Statistical information about the clipping process.
    """
    logger.verbose(f"Applying sigma clipping of sigma={sigma_lower} to {sigma_upper} to image at extension {ext_img}")

    # handle NaN values
    masked_array = ma.masked_invalid(hdu[ext_img].data)
    clipped_data = sigma_clip(masked_array, sigma_lower=sigma_lower, sigma_upper=sigma_upper, maxiters=iters)

    # Fill masked values with NaN for output
    masked_image = ma.filled(clipped_data, np.nan)

    # get statistical information
    num_clipped = np.count_nonzero(clipped_data.mask)

    stats = {
        'number_of_clipped_pixels': num_clipped,
        'mean_original': np.nanmean(masked_array),
        'mean_clipped': np.nanmean(clipped_data),
        'std_original': np.nanstd(masked_array),
        'std_clipped': np.nanstd(clipped_data),
        'median_original': np.nanmedian(masked_array),
        'median_clipped': np.nanmedian(clipped_data),
    }

    logger.info(f"Sigma clipping applied with {sigma_lower} lower and {sigma_upper} upper bounds. "
                f"Number of pixels clipped: {num_clipped}.")
    
    return masked_image, stats


