from astropy.wcs import WCS

from ..logging.logger_config import setup_logger

# Assuming the logger has been set up globally or passed as an argument
logger = setup_logger()

def trim_image(hdu, ext_img, ext_header, x_range, y_range):
    try:
        # Log the start of the operation
        logger.verbose(f"Trimming image at extensions {ext_img} with header {ext_header}")
        
        fitting_header = hdu[ext_header].header
        img = hdu[ext_img].data
        # Check if x_range or y_range exceeds the image dimensions
        if x_range[1] > img.shape[1] or y_range[1] > img.shape[0]:
            logger.error("Trim range exceeds image dimensions")
            return None

        # trim the image and retain the WCS
        wcs = WCS(fitting_header)
        wcs = wcs[y_range[0] : y_range[1], x_range[0] : x_range[1]]

        # Update the header with the new WCS
        header = wcs.to_header()
        fitting_header.update(header)

        trimmed_img = img[y_range[0] : y_range[1], x_range[0] : x_range[1]]

        # add a comment to the header to indicate the image has been trimmed
        fitting_header.add_comment(f"Image has been trimmed with range: {x_range[0]}:{x_range[1]}, {y_range[0]}:{y_range[1]}")
        
        # Log successful trimming
        logger.info("Image successfully trimmed and WCS updated.")

        return trimmed_img, wcs, fitting_header

    except Exception as e:
        # Log any errors that occur
        logger.error(f"Failed to trim image: {e}", exc_info=True)
        return None
