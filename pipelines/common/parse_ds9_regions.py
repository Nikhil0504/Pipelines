import re


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
