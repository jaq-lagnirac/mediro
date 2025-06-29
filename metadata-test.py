# Justin Caringal
# 
# testbed to extract EXIF tags

import os
import time
import exifread

file_path = os.path.join('MEDIRO_requires_sorting',
                         'WIN_20230426_14_15_23_Pro.jpg')

with open(file_path, 'rb') as handle:
    tags = exifread.process_file(handle)

    for key, value in tags.items():
        print(f'{key:<30}{value}')

    if 'EXIF DateTimeOriginal' in tags:
        date_taken_str = str(tags['EXIF DateTimeOriginal'])
        date_taken_obj = time.strptime(date_taken_str, '%Y:%m:%d %H:%M:%S')