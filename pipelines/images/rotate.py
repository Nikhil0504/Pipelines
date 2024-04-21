from scipy.ndimage import rotate


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
                  order=interp_order, reshape=False, prefilter=False)
