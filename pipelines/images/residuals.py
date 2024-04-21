import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from ..logging.logger_config import setup_logger

# Configure logger for this module
logger = setup_logger()

def get_residuals(actual_img, residual_img, wcs, apertures, filename):
    """
    Saves plots for each aperture to a single PDF file, including residual histograms.

    Parameters:
    - actual_img (numpy.ndarray): The original image array.
    - residual_img (numpy.ndarray): The residual image array.
    - wcs (WCS object): WCS object for the images.
    - apertures (list): List of aperture objects.
    - filename (str): Path to the output PDF file.
    """
    logger.verbose(f"Creating residual plots PDF: {filename} with {len(apertures)} apertures from the images.")
    try:
        with PdfPages(filename) as pdf:
            for aperture in apertures:
                ap_pix = aperture.to_pixel(wcs)
                mask = ap_pix.to_mask(method='exact')

                mask_data = mask.get_values(actual_img)
                mask_res = mask.get_values(residual_img)

                noise_std = np.std(mask_res)

                cutout_data = mask.cutout(actual_img)
                cutout_res = mask.cutout(residual_img)

                fig, ax = plt.subplots(1, 3, figsize=(10, 5), dpi=300)
                ax[0].imshow(cutout_data, origin='lower')
                ax[0].set_title('Original')
                ax[1].imshow(cutout_res, origin='lower')
                ax[1].set_title('Residual')

                ax[2].hist(mask_res.flatten(), bins=100, range=(-8*noise_std, 8*noise_std),
                           align='left', color='k', label='Residual Image Values')
                ax[2].axvline(np.median(mask_data), color='r', label='Original Median')
                ax[2].axvline(np.median(mask_res), color='b', label='Residual Median')
                ax[2].legend(loc='upper left', fontsize=6)

                plt.tight_layout(rect=[0, 0, 0.75, 1])
                pdf.savefig(fig, bbox_inches='tight')
                plt.close(fig)

            logger.info("Successfully created the PDF with residual plots.")
    except Exception as e:
        logger.error(f"Failed to create residual plots PDF: {str(e)}")
        raise
