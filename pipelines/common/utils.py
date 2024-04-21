import os
from datetime import datetime


def generate_filename(base_file, extension, output_dir):
    date_str = datetime.now().strftime('%Y%m%d')
    filename = f'{base_file}_{date_str}.{extension}'
    return os.path.join(output_dir, filename)