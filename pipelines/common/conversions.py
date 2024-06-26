import astropy.units as u
import numpy as np


def flux_to_abmag(flux_densities, wavelengths):
    from astropy.constants import c
    """
    Convert flux densities from ergs/cm^2/s/A to AB magnitudes.
    
    Parameters:
    - flux_densities: list of flux densities in ergs/cm^2/s/A.
    - wavelengths: list of wavelengths in Angstroms corresponding to the flux densities.
    
    Returns:
    - List of AB magnitudes.
    """
    # Speed of light in Angstroms per second
    c = c.to(u.AA / u.s).value
    
    # Convert flux densities to ergs/cm^2/s/Hz
    flux_densities_hz = [(f_lambda * ((lambda_value**2) / c)) for f_lambda, lambda_value in zip(flux_densities, wavelengths)]
    
    # Calculate AB magnitudes
    ab_magnitudes = [-2.5 * np.log10(f_nu) - 48.60 for f_nu in flux_densities_hz]
    
    return np.array(ab_magnitudes)


def abmag_to_jansky(m_ab, m_ab_err=None):
    """
    Convert AB magnitudes to Janskys.
    
    Parameters:
    - m_ab: list of AB magnitudes.
    - m_ab_err: list of errors in AB magnitudes.
    
    Returns:
    - List of Janskys.
    """
    # Convert AB magnitudes to Janskys
    janskys = 10 ** (-(m_ab - 8.90) / 2.5)

    if m_ab_err:
        # Calculate errors in Janskys
        janskys_err = janskys * (10 ** (m_ab_err / 2.5) - 1)
        return janskys, janskys_err

    return janskys

def mjy_sr_to_ab_mag(flux_mjy_sr, pixar_sr):
    """
    Convert flux density from MJy/sr to AB Magnitude.

    Parameters:
    flux_mjy_sr (float): Flux density in MJy/sr
    pixar_sr (float): Pixel area in steradians

    Returns:
    float: AB Magnitude
    """
    # Convert MJy/sr to Jy for the given pixel area
    flux_jy_pixel = flux_mjy_sr * pixar_sr * 1e6

    # Calculate AB magnitude
    ab_mag = -2.5 * np.log10(flux_jy_pixel) + 8.9

    return ab_mag