import argparse

import matplotlib.pyplot as plt
from astropy.io import fits

from pipelines.common import utils
from pipelines.PSFs import makewebbpsf

# test for now
# fp = '/Users/nikhilgaruda/Documents/Astronomy_Research/Data/plckg165/Images/anton/30mas/mosaic_plckg165_nircam_f200w_30mas_20230403_drz.fits'
# filter = 'F200W'

# hdu = fits.open(fp)

# psf = makewebbpsf.generate_webbpsf(filter=filter, img_hdu=hdu, ext=0,
#                                    pixscl=None, oversample=3, fov_pixels=None,
#                                    fov_arcsec=None)

# psf_rot = makewebbpsf.rotate_webbpsf(psf, img_hdu=hdu, ext=0, pa=None)

def main(args):
    fp = args.imgpath
    img_ext = args.img_ext
    
    pixscl = args.ps
    pa = args.pa

    filter = args.filter

    oversample = args.ovsam
    fov_pixels = args.fov_pix
    fov_arcsec = args.fov_as

    output_directory = args.output_directory
    output_filename = args.output_filename


    hdu = fits.open(fp)
    psf = makewebbpsf.generate_webbpsf(filter=filter, img_hdu=hdu, ext=img_ext,
                                        pixscl=pixscl, oversample=oversample, fov_pixels=fov_pixels,
                                        fov_arcsec=fov_arcsec)
    
    psf_rot = makewebbpsf.rotate_webbpsf(psf, img_hdu=hdu, ext=img_ext, pa=pa)  

    full_output_path = utils.generate_filename(output_filename, 'fits', output_directory)
    psf_rot.writeto(full_output_path, overwrite=True)
    print(f"File saved as {full_output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate and rotate WebbPSF for a given filter and FITS image.',
        epilog='Example: ./generate_webbpsf.py file.fits F200W output psf_out --img_ext 0 --ps 0.03 --ovsam 3 --fov_pix 256 --fov_as 0.1 --pa 0.0'
    )

    parser.add_argument('imgpath', help='Path to the image FITS file')
    parser.add_argument('filter', help='Filter to generate the WebbPSF for')
    parser.add_argument('output_directory', help='Directory to save the output FITS file')
    parser.add_argument('output_filename', help='Filename for the output FITS file')
    parser.add_argument('--img_ext', type=int, default=0, help='Image extension to use; default is 0 (primary HDU)')
    parser.add_argument('--ps', type=float, default=None, help='Pixel scale for the WebbPSF; default is None')
    parser.add_argument('--pa', type=float, default=None, help='Position angle for the WebbPSF; default is None')
    parser.add_argument('--ovsam', type=int, default=3, help='Oversampling factor for the WebbPSF; default is 3')
    parser.add_argument('--fov_pix', type=int, default=None, help='Field of view in pixels for the WebbPSF; default is None')
    parser.add_argument('--fov_as', type=float, default=None, help='Field of view in arcseconds for the WebbPSF; default is None')

    args = parser.parse_args()
    main(args)