# Justin Caringal
# 
# testbed to extract EXIF tags

import os
import sys
import time
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
    tags = exifread.process_file(handle)

    for key, value in tags.items():
        print(f'{key:<30}{value}')

    # search_value = 'Image DateTime'
    search_value = 'EXIF DateTimeOriginal'
    if search_value in tags:
        date_taken_str = str(tags[search_value])
        date_taken_obj = time.strptime(date_taken_str, '%Y:%m:%d %H:%M:%S')
        print(f'\n\n{date_taken_str}\n{date_taken_obj}')
        
        year = str(date_taken_obj.tm_year)
        month = str(date_taken_obj.tm_mon).zfill(2)
        day = str(date_taken_obj.tm_mday)
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
creation_obj = time.strptime(creation_time, '%Y-%m-%dT%H:%M:%S.%fZ')
print(creation_obj)

year = str(creation_obj.tm_year)
month = str(creation_obj.tm_mon).zfill(2)
day = str(creation_obj.tm_mday)
print(f'{year}_{month}_{day}\n\n')
from time import sleep
print('this is a test.')
sleep(1000)