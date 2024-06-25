#!/bin/bash
# script used to automate reset between tests

mv ./20*/*/*/*.jpg requires_sorting/
rm -r 20*/

# python -m PyInstaller --onefile mediro.py --icon mediro.ico
