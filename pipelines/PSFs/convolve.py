from astropy.io import fits
from astropy.convolution import convolve_fft
from photutils.psf import create_matching_kernel, SplitCosineBellWindow

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

def convolve_image(image, kernel):
    # TODO: Convolve the image with the kernel.
    ...