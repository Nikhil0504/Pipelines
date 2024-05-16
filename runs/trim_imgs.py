import argparse
from dataclasses import dataclass
from typing import Union
from astropy.io import fits
from pipelines.common import utils
from pipelines.images import trim_images

@dataclass
class Args:
    path: str
    x_start: int
    x_end: int
    y_start: int
    y_end: int
    output_directory: str
    output_filename: str
    img_ext: Union[int, str] = '0'
    hdr_ext: Union[int, str] = '0'

def validate_extension_arg(ext: str) -> Union[int, str]:
    if ext.isdigit():
        return int(ext)
    return ext

def parse_arguments() -> Args:
    parser = argparse.ArgumentParser(
        description='Process and trim FITS images based on specified coordinates and extensions.',
        epilog='Example: ./process_fits.py file.fits 100 200 100 200 output trimmed_image --img_ext 0 --hdr_ext 0'
    )
    parser.add_argument('path', type=str, help='Path to the input FITS file')
    parser.add_argument('x_start', type=int, help='Start x-coordinate of the range to trim')
    parser.add_argument('x_end', type=int, help='End x-coordinate of the range to trim')
    parser.add_argument('y_start', type=int, help='Start y-coordinate of the range to trim')
    parser.add_argument('y_end', type=int, help='End y-coordinate of the range to trim')
    parser.add_argument('output_directory', type=str, help='Directory to save the output FITS file')
    parser.add_argument('output_filename', type=str, help='Filename for the output FITS file')
    parser.add_argument('--img_ext', type=str, default='0', help='Image extension to use; default is 0 (primary HDU)')
    parser.add_argument('--hdr_ext', type=str, default='0', help='Header extension to use if different from image extension; default is 0')

    parsed_args = parser.parse_args()
    args_dict = vars(parsed_args)
    
    # Convert dictionary to Args dataclass
    args = Args(**args_dict)
    return args

def main(args: Args) -> None:
    x_range = (args.x_start, args.x_end)
    y_range = (args.y_start, args.y_end)
    img_ext = validate_extension_arg(args.img_ext)
    hdr_ext = validate_extension_arg(args.hdr_ext)

    hdu = fits.open(args.path)
    img, _, head = trim_images.trim_image(hdu, img_ext, hdr_ext, x_range, y_range)
    full_output_path = utils.generate_filename(args.output_filename, 'fits', args.output_directory)

    # Preserve the extension name if img_ext is a string (name of the extension)
    if isinstance(img_ext, str):
        ext_name = img_ext
    else:
        ext_name = head.get('EXTNAME', 'UNKNOWN')

    # Create a new HDU with the trimmed image and original header
    new_hdu = fits.PrimaryHDU(data=img, header=head)
    new_hdu.header['EXTNAME'] = ext_name

    # Write the new HDU to the output file
    new_hdul = fits.HDUList([new_hdu])
    new_hdul.writeto(full_output_path, overwrite=True, output_verify='fix')

    print(f"File saved as {full_output_path}")

if __name__ == "__main__":
    args = parse_arguments()
    main(args)
