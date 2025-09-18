# Justin Caringal
# 
# testbed to extract EXIF tags

import os
import sys
import time
from datetime import datetime, timezone
import exifread # only works with images


# try:
#     base_path = sys._MEIPASS # only found in PyInstaller
# except AttributeError:
#     base_path = os.curdir
file_path = '20250214_183649.jpg'
# file_path = os.path.join(base_path, file_path)
# file_path = os.path.join('MEDIRO_requires_sorting',
#                          'WIN_20230426_14_15_23_Pro.jpg')

with open(file_path, 'rb') as handle:
    stop_tag = 'DateTimeOriginal'
    tags = exifread.process_file(handle,
                                 stop_tag=stop_tag,
                                 builtin_types=True,
                                 details=False,
                                 extract_thumbnail=False,
                                 strict=True)

    # for key, value in tags.items():
    #     print(f'{key:<40}{str(value):<30}{type(value)}')
    print('\n\n')

    # search_value = 'Image DateTime'
    # leaves it in local time
    search_value = f'EXIF {stop_tag}'
    if search_value in tags:
        date_taken_str = str(tags[search_value])
        date_taken_obj = datetime.fromisoformat(date_taken_str).astimezone()
        print(f'\n\n{date_taken_str}\n{date_taken_obj}')
        
        year = str(date_taken_obj.year).zfill(2)
        month = str(date_taken_obj.month).zfill(2)
        day = str(date_taken_obj.day).zfill(2)
        print(f'{year}_{month}_{day}\n\n')

import ffmpeg # videos, for windows --> https://www.gyan.dev/ffmpeg/builds/
from pprint import pp
video_path = '20250829_155438.mp4'
video_probe = ffmpeg.probe(video_path)
# pp(video_probe)
creation_time = video_probe \
    .get('format', {}) \
    .get('tags') \
    .get('creation_time')
print(creation_time)
creation_obj = datetime.strptime(creation_time, '%Y-%m-%dT%H:%M:%S.%fZ') # Z for Zulu time (UTC)
creation_obj = creation_obj.replace(tzinfo=timezone.utc) # assigns UTC to input
print(creation_obj)
creation_obj = creation_obj.astimezone() # localizes timezone to system time
print(creation_obj)

year = str(creation_obj.year).zfill(2)
month = str(creation_obj.month).zfill(2)
day = str(creation_obj.day).zfill(2)
print(f'{year}_{month}_{day}\n\n')
from time import sleep
print('this is a test.')
sleep(1000)