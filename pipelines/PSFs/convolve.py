from astropy.io import fits
from astropy.convolution import convolve_fft
from photutils.psf import create_matching_kernel, SplitCosineBellWindow
import pyfftw

def create_kernels(target_psf, source_psf, alpha=0.5, beta=0.0):
    """
    Create a kernel to match the PSFs of two images.

    Parameters
    ----------
    target_psf : np.ndarray
        The target PSF image.
    source_psf : np.ndarray
        The source PSF image.
    alpha : float
        The alpha parameter of the SplitCosineBellWindow.
    beta : float
        The beta parameter of the SplitCosineBellWindow.
    
    Returns
    -------
    kernel : np.ndarray
        The kernel that will match the PSFs of the two images.
    """
    window = SplitCosineBellWindow(alpha=alpha, beta=beta)
    kernel = create_matching_kernel(target_psf=target_psf, source_psf=source_psf, window=window)
    return kernel

def convolve_image(image, kernel, multithread=True):
    """
    Convolve an image with a kernel.

    Parameters
    ----------
    image : np.ndarray
        The image to convolve.
    kernel : np.ndarray
        The kernel to convolve with.
    
    Returns
    -------
    convolved : np.ndarray
        The convolved image.
    """

    if multithread:
        pyfftw.config.NUM_THREADS = 6
        pyfftw.config.PLANNER_EFFORT = 'FFTW_MEASURE'

        pyfftw.interfaces.cache.enable()
        pyfftw.interfaces.cache.set_keepalive_time(300)



        return convolve_fft(image, kernel, normalize_kernel=True, allow_huge=True,
                            fftn=pyfftw.interfaces.numpy_fft.fftn,
                            ifftn=pyfftw.interfaces.numpy_fft.ifftn,)

    return convolve_fft(image, kernel, normalize_kernel=True, allow_huge=True)