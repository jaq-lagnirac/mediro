<div align="center">
    <img src="images/logo-color.svg" width="500px" alt="Mediro Logo">
</div>

# mediro
The MEdia DIRectory Organizer, a tool to partition a directory into subdirectories and sort files (originally for visual multimedia) based on time-of-creation. For use on Windows.

## User Manual

1. Download the latest release from the [Github page](https://github.com/jaq-lagnirac/mediro/releases).
2. Move the `.exe` file to the root of your `Pictures` directory or other location that you want to sort.
3. Click the `.exe` and follow the prompts to create the input subdirectory.
4. Move your media files (labeled following the [ISO 8601 Basic format](https://en.wikipedia.org/wiki/ISO_8601)) into the input subdirectory. Your camera of choice should have an ISO 8601 naming option or is defaulted to the standard.
    
    Below are a few examples of acceptable file naming conventions (you can also mix and match these when inputting them):
    ```
    20240625.png
    20220330_190103.jpg
    WIN_20230417_13_57_52_Pro.jpg
    ```
    As long as the file has a string of digits in the format `YYYYMMDD`, it will be sorted.
5. Click the `.exe` once again and follow the prompts to begin sorting the files. You will notice that the any files unsuccessfully sorted will be located in a separate output directory.