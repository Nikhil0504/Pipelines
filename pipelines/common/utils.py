import os
from datetime import datetime

import numpy as np

from ..logging.logger_config import setup_logger

logger = setup_logger()


def generate_filename(base_file, extension, output_dir) -> str:
    date_str = datetime.now().strftime('%Y%m%d')
    filename = f'{base_file}_{date_str}.{extension}'

    # create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logger.info(f"Created the output directory {output_dir}")
    
    logger.verbose(f"Generated the filename {filename}")

    return os.path.join(output_dir, filename)


def resample_array(arr, new_length):
    """
    Resample an array to a new length by averaging over bins.
    This function is useful for resampling flux profiles to the same length.
    
    Parameters
    ----------
    arr : array-like
        The array to resample.
        
    new_length : int
        The new length of the array.
    
    Returns
    -------
    new_arr : array-like
        The resampled array.
    """

    logger.verbose(f"Resampling the array to a new length of {new_length}")

    old_length = len(arr)
    bin_size = old_length / new_length
    new_arr = np.array([arr[int(bin_size * i):int(bin_size * (i + 1))].mean() for i in range(new_length)])

    return new_arr
