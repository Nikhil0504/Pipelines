from astropy.modeling.models import Sersic2D
import numpy as np
import matplotlib.pyplot as plt

from ..logging.logger_config import setup_logger

_log = setup_logger()

try:
    import petrofit as pf
    from petrofit.segmentation import get_amplitude_at_r
except ImportError:
    _log.error("petrofit is not installed. Please install it to use this module.")
    raise ImportError("petrofit is not installed. Please install it to use this module.")


def make_sersic_model(
    petrosian_prop: dict,
    id: int,
    n_sersic: int = 1,
    theta: float = 1e-99,
    center_slack=4,
    override_bounds: dict = {},
    verbose: bool = False,
    plot: bool = True,
    vmax=None,
    vmin=None,
    fitting_image=None,
) -> Sersic2D:
    # get object
    object = petrosian_prop[id]
    source = object["source"]
    p_prop = object["p"]

    # Estimate center
    position = pf.get_source_position(source)
    x_0, y_0 = position

    # Estimate shape
    ellip = pf.get_source_ellip(source)
    elong = pf.get_source_elong(source)
    if theta == 1e-99:
        theta = pf.get_source_theta(source)
    else:
        theta = theta

    # Estimate Sersic index
    n = n_sersic

    # Estimate r_half_light
    r_eff = p_prop.r_half_light

    amplitude = get_amplitude_at_r(r_eff, fitting_image, x_0, y_0, ellip, theta)

    # Allow for 4 pixel center slack
    center_slack = center_slack

    override = {
        "x_0": (x_0 - center_slack / 2, x_0 + center_slack / 2),
        "y_0": (y_0 - center_slack / 2, y_0 + center_slack / 2),
    }
    if override_bounds == {}:
        bounds = pf.get_default_sersic_bounds(override=override)
    else:
        override.update(override_bounds)
        bounds = pf.get_default_sersic_bounds(override=override)

    # Make astropy model
    sersic_model = Sersic2D(
        amplitude=amplitude,
        r_eff=r_eff,
        n=n,
        x_0=x_0,
        y_0=y_0,
        ellip=ellip,
        theta=theta,
        bounds=bounds,
    )

    if verbose:
        print(ellip, elong, theta)
        print(f"Modeling sersic at ({x_0}, {y_0}) with r_eff = {r_eff}")

    if plot:
        p_prop.imshow(position=position, elong=elong, theta=theta, lw=1.25)
        # Plot image of sources
        plt.imshow(fitting_image.data, vmax=vmax, vmin=vmin)
        pf.mpl_tick_frame()
        plt.xlabel("Pixels")
        plt.ylabel("Pixels")

        plt.show()

    return sersic_model

def shift_model(compound_model, psf, X_RANGE=None, Y_RANGE=None, OVERSAMPLE=1):
    """
    Makes a copy of the model, shifting it to the correct (x, y) location since the original
    fit has (x, y) locations relative to the cutout's location.
    compound_model: PSF convolved compound model
    psf: PSF the model was convolved with
    """
    model_copy = np.sum([model.copy() for model in compound_model.model])
    if X_RANGE != None and Y_RANGE != None:
        for model in model_copy:
            model.x_0 += X_RANGE[0]
            model.y_0 += Y_RANGE[0]
    return pf.PSFConvolvedModel2D(model_copy, psf=psf, oversample=OVERSAMPLE)
