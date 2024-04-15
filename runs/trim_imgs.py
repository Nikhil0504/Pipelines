import argparse
from astropy.io import fits
from pipelines.images import trim_images
from pipelines.common import utils

def main(args):
    path = args.path
    x_range = (args.x_start, args.x_end)
    y_range = (args.y_start, args.y_end)
    output_directory = args.output_directory
    output_filename = args.output_filename

    img_ext = args.img_ext
    hdr_ext = args.hdr_ext

    hdu = fits.open(path)
    img, _, head = trim_images.trim_image(hdu, img_ext, hdr_ext, x_range, y_range)
    full_output_path = utils.generate_filename(output_filename, 'fits', output_directory)

    fits.writeto(full_output_path, img, head, overwrite=True, output_verify='fix')
    print(f"File saved as {full_output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Process and trim FITS images based on specified coordinates and extensions.',
        epilog='Example: ./process_fits.py file.fits 100 200 100 200 output trimmed_image --img_ext 0 --hdr_ext 0'
    )
    parser.add_argument('path', help='Path to the input FITS file')
    parser.add_argument('x_start', type=int, help='Start x-coordinate of the range to trim')
    parser.add_argument('x_end', type=int, help='End x-coordinate of the range to trim')
    parser.add_argument('y_start', type=int, help='Start y-coordinate of the range to trim')
    parser.add_argument('y_end', type=int, help='End y-coordinate of the range to trim')
    parser.add_argument('output_directory', help='Directory to save the output FITS file')
    parser.add_argument('output_filename', help='Filename for the output FITS file')
    parser.add_argument('--img_ext', type=int, default=0, help='Image extension to use; default is 0 (primary HDU)')
    parser.add_argument('--hdr_ext', type=int, default=0, help='Header extension to use if different from image extension; default is 0')

    args = parser.parse_args()
    main(args)
