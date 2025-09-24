# Justin Caringal
#
# The main handler of the Mediro program,
# contains the functions which create directories
# and sort through the media.

import os
import sys
from datetime import datetime, timezone
import exifread # for parsing images
import ffmpeg # for parsing videos
from paths import create_path

def _read_photo_metadata(filename : str) -> datetime:
    """Handles attempts to read photo metadata using ExifRead.

    Args:
        filename (str): The file path of the media in question.
    
    Returns:
        datetime: Returns a datetime object if successfully read metadata,
            None otherwise.
    """
    EXIFREAD_STOP_TAG = 'DateTimeOriginal'
    EXIFREAD_SEARCH_VAL = f'EXIF {EXIFREAD_STOP_TAG}'

    # opens media as binary read file
    tags = None # scope resolution
    with open(filename, 'rb') as handle:
        tags = exifread.process_file(handle,
                                    stop_tag=EXIFREAD_STOP_TAG,
                                    builtin_types=True,
                                    details=False,
                                    extract_thumbnail=False,
                                    strict=True)
    
    # if datetime found, return datetime object localized to system time
    localized_date = None # default return, scope resolution
    if EXIFREAD_SEARCH_VAL in tags:
        date_str = tags[EXIFREAD_SEARCH_VAL]
        localized_date = datetime.fromisoformat(date_str).astimezone()
    return localized_date

def _read_video_metadata(filename : str) -> datetime:
    """Handles attempts to read video metadata using FFmpeg.

    Args:
        filename (str): The file path of the media in question.
    
    Returns:
        datetime: Returns a datetime object if successfully read metadata,
            None otherwise.
    """

    creation_time = None # scope resolution
    try:
        # attempts to extract creation time from file metadata
        file_probe = ffmpeg.probe(filename)
        creation_time = file_probe \
            .get('format', {}) \
            .get('tags') \
            .get('creation_time')
    except Exception as e:
        return
    
    # T stands for Time (Hours, Minutes, Seconds)
    # Z stands for Zulu time format (UTC)
    DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

    # converts creation time to localized datetime object based on system time
    naive_datetime = datetime.strptime(creation_time, DATETIME_FORMAT)
    zulu_time_date = naive_datetime.replace(tzinfo=timezone.utc)
    localized_date = zulu_time_date.astimezone()
    return localized_date

def _extract_datetime_metadata(filename : str):
    """Handles reading metadata for a given file.
    """

    # attempts to read photo metadata using exifread
    datetime_obj = _read_photo_metadata(filename)
    if not datetime_obj: # if photo metadata unsuccessful
        # attempts to read video metadata using ffmpeg
        datetime_obj = _read_video_metadata(filename)
    
    # TODO: 2025-09-17 - can possibly implement Mediro v1.0
    # filename parsing here as a last resort. This may be
    # accomplished in a future release in order to maintain
    # backwards compatibility and preserve original
    # functionality.

    return datetime_obj

def _datetime_to_relpath(datetime_obj : datetime) -> str:
    """Generates a directory path string from a datetime object.

    Args:
        datetime_obj (str): A datetime object containing at least
            year, month, and day information.
    
    Returns:
        str: Returns a filepath of nested directories.
    """

    DIR_FORMAT = {
        'year' : '%Y',
        'month' : '%Y_%m',
        'day' : '%Y_%m_%d'
    }
    year_dir = datetime_obj.strftime(DIR_FORMAT['year'])
    month_dir = datetime_obj.strftime(DIR_FORMAT['month'])
    day_dir = datetime_obj.strftime(DIR_FORMAT['day'])
    
    directory_path = os.path.join(year_dir, month_dir, day_dir)
    return directory_path

def mediro_sort(input_dir : str,
                output_dir : str,
                unsorted_dir : str) -> None:
    """Performs main MEDIRO tasks.

    A function which takes an input directory path, reads
    the metadata for all of the media, and sorts them into
    a file tree based on the date created.

    Args:
        input_dir (str): The relative path to the input
            directory of media to be sorted.
        output_dir (str): The relative path to the output
            directory, where the generated folders will go.
        unsorted_dir (str): The relative path to the unosrted
            directory, where media that cannot be sorted by
            Mediro will go.
    
    Returns:
        None
    """

    for filename in os.listdir(input_dir):
        
        full_input_path = os.path.join(input_dir, filename)
        if os.path.isdir(full_input_path):
            continue # skips past directories in input_dir

        # attempts to extract datetime object from metadata
        datetime_metadata = _extract_datetime_metadata(full_input_path)

        # if metadata found, generates output pathway
        # otherwise defaults path to unsorted directory
        target_dir_path = unsorted_dir # default, scope resolution
        if datetime_metadata:
            target_date_dir = _datetime_to_relpath(datetime_metadata)
            target_dir_path = os.path.join(output_dir, target_date_dir)
        create_path(target_dir_path)

        full_target_path = os.path.join(target_dir_path, filename)
        print(full_input_path, full_target_path)
        if not os.path.exists(full_target_path):
            # does not touch file if duplicate found in target location
            # 
            # TODO: 2025-09-24 - Possible future direction:
            # implement different handling for duplicate files, allow
            # user to determine changes
            os.replace(full_input_path, full_target_path)

__all__ = ['mediro_sort']

# test code, remove before production
if __name__ == "__main__":
    test_dir = os.path.join('..', 'test')
    output_dir = os.path.join(test_dir, 'output')
    unsorted_dir = os.path.join(test_dir, 'unsorted')
    mediro_sort(test_dir, output_dir, unsorted_dir)