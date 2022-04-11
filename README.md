# What is it?

`get-audio-metadata.py` is a python script to analyze a folder full of wav files and generate a CSV report containing various metadata including:

- filename
- file length (in bytes)
- format
- bit depth
- bitrate
- number of channels
- sample rate (in Hz)
- duration (in seconds)
- file path
- onsets (i.e. offset from beginning of file)
- loudness

It will generate a file called `audio-metadata-output.csv` in the specified output folder. It should run on Windows, Mac or Linux (or theoretically any platform that can run python 3).

# Install

- install latest python 3 (https://python.org)
- unzip contents into a folder
- navigate to that folder and install requirements (see below)

Windows:

```
py -3 -m pip install -r requirements.txt
```

or run `install.bat`

Mac:

```
pip3 install -r requirements.txt
```

or run `install.sh`

# Usage

```
usage: get-audio-metadata.py [-h] --input-dir [INPUT_DIR] [--output-dir [OUTPUT_DIR]]

options:
  -h, --help            show this help message and exit
  --input-dir [INPUT_DIR]
                        Directory containing files to analyze
  --output-dir [OUTPUT_DIR]
                        Directory into which to generate CSV report
```

If you don't supply an input folder or output folder at the command line, you'll be prompted with a dialog box to select the folders.

# Examples

Directly via python:

```
py get-audio-metadata.py --input-dir C:\path\to\audio\files --output-dir D:\output
```

With helper batch file:

```
.\get-audio-metadata.bat  C:\path\to\audio\files D:\
```
