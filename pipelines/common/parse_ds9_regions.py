import re

from astropy.coordinates import SkyCoord
from astropy import units as u
from photutils.aperture import SkyRectangularAperture

def parse_ds9_reg_file(filename):
    # Regular expression to match region lines (simplified for circle, box, and ellipse)
    reg_exp = r"(circle|box|ellipse)\(([^,]+),([^,]+),([^)]+)\)"
    regions = []

    with open(filename, 'r') as file:
        for line in file:
            # Skip comments and empty lines
            if line.startswith('#') or not line.strip():
                continue
            
            match = re.search(reg_exp, line)
            if match:
                shape = match.group(1)
                ra = match.group(2)
                dec = match.group(3)
                sizes = match.group(4).split(',')
                
                region = {
                    'shape': shape,
                    'ra': ra,
                    'dec': dec,
                    'sizes': sizes
                }
                regions.append(region)
    
    return regions

def get_apertures(reg_file, frame='fk5') -> list[SkyRectangularAperture]:
    regions = parse_ds9_reg_file(reg_file)

    sky_coords = [SkyCoord(ra=float(region['ra'])*u.degree, dec=float(region['dec'])*u.degree, frame=frame) for region in regions]
    apertures = [SkyRectangularAperture(positions=sky_coord, 
                                        w=float(region['sizes'][0].split('\"')[0])*u.arcsec, 
                                        h=float(region['sizes'][1].split('\"')[0])*u.arcsec, 
                                        theta=(int(region['sizes'][2]) - 90) * u.deg )for sky_coord, region in zip(sky_coords, regions)]

    return apertures

