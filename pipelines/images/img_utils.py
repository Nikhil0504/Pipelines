from scipy.ndimage import rotate, median_filter
import numpy as np
import numpy.ma as ma


def imrotate(image, angle, interp_order=1, reshape=False):
    """
    Rotate an image from North to East given an angle in degrees

    Parameters
    ----------
    image : `numpy.ndarray`
        Input data array
    angle : float
        Angle in degrees
    interp_order : int, optional
        Spline interpolation order [0, 5] (default 1: linear)

    Returns
    -------
    output : `numpy.ndarray`
        Rotated data array

    """
    return rotate(image, -1.0 * angle,
                  order=interp_order, reshape=reshape, prefilter=False)



def create_mask(image, mask_above, exclude_adjacent: bool):
    """
    Creates a mask for all pixels in `image` that are above the `mask_above` value.
    If `exclude_adjacent` is True, it also masks the pixels adjacent to the pixels
    being masked.
    """
    # Mask all pixels above the given level
    mask = ma.masked_greater(image, mask_above).mask
    if not exclude_adjacent:
        # Mask is good as is
        return mask
    
    # Also mask off all pixels that are adjacent to pixels above the given level
    mask_adj = np.zeros_like(image)
    height, width = image.shape
    for x in range(width):
        for y in range(height):
            if mask[y, x]:
                # Mask out the pixel at (x, y) along with all adjacent pixels
                for xdelta in (-1, 0, 1):
                    for ydelta in (-1, 0, 1):
                        i = y + ydelta
                        j = x + xdelta
                        if 0 <= i < height and 0 <= j < width:
                            mask_adj[i, j] = 1
    return mask_adj

def median_filter(image, window_size: int, mask_above, exclude_adjacent=True):
    """
    Performs the median filter on `image` using the given `window_size` to determine how large the
    sliding window for median calculation is, and subtracts it off the image. Pixels that are above
    the `mask_above` value will be excluded from the subtraction to avoid affecting low signal-to-noise
    pixels. If `exclude_adjacent` is True, adjacent pixels to high-value pixels will also be excluded
    from the subtraction.
    
    Process replicated from https://www.aanda.org/articles/aa/full_html/2016/06/aa27513-15/aa27513-15.html#S8
    """
    median_filtered = median_filter(image, size=window_size)
    mask = create_mask(image, mask_above, exclude_adjacent)
    return image - ma.filled(ma.masked_array(median_filtered, mask), 0)
