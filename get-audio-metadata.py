import argparse
import audio_metadata
import easygui
import librosa
import os
from csv import DictWriter
from pprint import pprint
from numpy import block
import soundfile as sf
import pyloudnorm as pyln

__author__ = "Nick Schipano"


def get_directory(msg, title, default=None) -> str:
    selected_dir = easygui.diropenbox(msg=msg, title=title)
    return selected_dir if selected_dir else default


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input-dir",
        nargs="?",
        required=False,
        help="Directory containing files to analyze",
    )
    parser.add_argument(
        "--output-dir",
        nargs="?",
        required=False,
        help="Directory into which to generate CSV report",
    )
    return parser.parse_args()


def get_loudness(filepath, duration) -> float:
    # print(f"{filepath}: {duration}")
    block_size = duration/2.0 if duration < 0.4 else 0.400
    data, rate = sf.read(filepath)
    meter = pyln.Meter(rate, block_size=block_size)  # create BS.1770 meter
    return meter.integrated_loudness(data)


if __name__ == "__main__":
    args = parse_args()

    input_dir = (
        args.input_dir
        if args.input_dir
        else get_directory(
            msg="Select folder full of audio files to analyze",
            title="Select Input Folder",
        )
    )
    if input_dir:
        output_dir = (
            args.output_dir
            if args.output_dir
            else get_directory(
                msg="Select output folder in which to wwrite CSV",
                title="Select Output Folder",
                default=".",
            )
        )

        print(f"Scanning {input_dir}")
        items = []
        for entry in os.scandir(path=input_dir):
            if not entry.is_dir() and entry.name.endswith(".wav"):
                x, sr = librosa.load(entry.path)
                onset_frames = librosa.onset.onset_detect(
                    y=x, sr=sr, wait=1, pre_avg=1, post_avg=1, pre_max=1, post_max=1
                )
                onset_times = librosa.frames_to_time(onset_frames)
                onset_times_str = ",".join(
                    ["%.4f" % onset_time for onset_time in onset_times]
                )
                metadata = audio_metadata.load(entry.path)
                # pprint(metadata)
                loudness = get_loudness(entry.path, metadata.streaminfo.duration)
                item = {
                    "file": os.path.basename(entry.path),
                    "format": str(metadata.streaminfo.audio_format),
                    "filesize": metadata.filesize,
                    "duration": metadata.streaminfo.duration,
                    "channels": metadata.streaminfo.channels,
                    "bit_depth": metadata.streaminfo.bit_depth,
                    "bitrate": metadata.streaminfo.bitrate,
                    "sample_rate": metadata.streaminfo.sample_rate,
                    "onsets": (onset_times_str),
                    "loudness": loudness,
                    "path": entry.path,
                }
                items.append(item)

        output_file = os.path.join(output_dir, "audio-metadata-output.csv")
        with open(output_file, "w", newline="") as f:
            print(f"Writing to {output_file}")
            if items:
                csv_headers = items[0].keys()
                writer = DictWriter(f, csv_headers)
                writer.writeheader()
                writer.writerows(items)
    else:
        print("No input folder provided!")
