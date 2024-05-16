from pipelines.PSFs.convolve import create_kernels, convolve_image
from pipelines.plotting.psf_plots import display_kernel
from astropy.io import fits

p1 = fits.open('output/test_psf_f090_20240427.fits')
p2 = fits.open('output/test_psf_f444_20240427.fits')

k = create_kernels(p2[-1].data, p1[-1].data, alpha=0.35, beta=0.3)

ax = display_kernel(k, return_ax=True)
from matplotlib import pyplot as plt
plt.show()

fits.writeto('output/test_kernel_f444_f090_20240427.fits', k, overwrite=True)

img = fits.open('/Users/nikhilgaruda/Documents/Astronomy_Research/Data/plckg165/Images/anton/30mas/mosaic_plckg165_nircam_f090w_30mas_20230403_drz.fits')

c = convolve_image(img[0].data, k)

fits.writeto('output/test_convolved_f444_f090_20240427.fits', c, overwrite=True)