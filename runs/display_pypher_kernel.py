import argparse
from dataclasses import dataclass

from astropy.io import fits

from pipelines.plotting.psf_plots import display_kernel
from pipelines.common.utils import generate_filename

@dataclass
class Args:
    filename: str
    save_path: str = None

def parse_arguments() -> Args:
    parser = argparse.ArgumentParser(description="Display Pypher kernel")
    parser.add_argument("filename", type=str, help="FITS file containing the Pypher kernel")
    parser.add_argument("--save_path", type=str, help="Path to save the plot")

    parsed_arhs = parser.parse_args()
    args_dict = vars(parsed_arhs)

    return Args(**args_dict)

def main(args: Args) -> None:
    with fits.open(args.filename) as hdul:
        kernel = hdul[0].data

    display_kernel(kernel, save_path=args.save_path, save=True if args.save_path else False)

if __name__ == "__main__":
    args = parse_arguments()

    main(args)