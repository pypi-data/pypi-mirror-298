import json
import numpy as np
import os
import struct
import msgpack

from colorama import just_fix_windows_console
from termcolor import colored

MSGPACK_ANALYSIS_EXTENSION = '.xaa'
JSON_ANALYSIS_EXTENSION = '.json'
JSON_TYPE_CHECK = 'sonosthesia-audio-pipeline'

AUDIO_EXTENSIONS = ['.wav', '.mp3']

ANALYSIS_VERSION = 2

CHANNEL_KEYS = {
    0: 'rms',
    1: 'lows',
    2: 'mids',
    3: 'highs'
}

just_fix_windows_console()


def audio_analysis_description(audio_analysis):
    continuous = audio_analysis['continuous']
    peaks = audio_analysis['peaks']
    return f'AudioAnalysis with {len(continuous)} continuous data points and {len(peaks)} peaks'


def signal_analysis_description(signal_analysis):
    rms_max = np.max(signal_analysis.rms)
    rms_min = np.min(signal_analysis.rms)
    num_peaks = len(signal_analysis.peaks)
    return f'SignalAnalysis with rms range ({rms_min} : {rms_max}) and {num_peaks} peaks'


def write_json_with_header(data, header, file_path):
    json_data = json.dumps({
        "type": JSON_TYPE_CHECK,
        "header": header,
        "content": data
    }, indent=2)
    print(colored(f'Serialized data to json string with length {len(json_data)}, written to {file_path} '
                  f'with header {header}',"green"))
    with open(file_path, 'w') as file:
        file.write(json_data)


def read_json_with_header(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    if json_data['type'] != JSON_TYPE_CHECK:
        raise ValueError(f"Expected type field with value {JSON_TYPE_CHECK}")
    header = json_data['header']
    print(colored(f'Loaded json data from {file_path} with header {header}',"green"))
    check_header(header)
    data = json_data['content']
    return header, data


def write_packed_with_header(data, header, file_path):
    if len(header) != 3:
        raise ValueError("Header must contain exactly three 32-bit integers")
    # Pack the header integers as 32-bit (4 bytes) integers
    header_packed = struct.pack('iii', *header)  # 'iii' means 3 int32 values
    packed_data = msgpack.packb(data, use_bin_type=True)
    combined_data = header_packed + packed_data
    print(colored(f'Packed data into {len(combined_data)} bytes, written to {file_path} with header {header}',"green"))
    with open(file_path, 'wb') as file:
        file.write(combined_data)


def read_packed_with_header(file_path):
    # Open the file in binary read mode
    with open(file_path, 'rb') as file:
        # Read the header: 3 x 32-bit integers (12 bytes total)
        header_packed = file.read(12)
        if len(header_packed) != 12:
            raise ValueError("File is too short to contain a valid header")
        # Unpack the header: 'iii' means 3 int32 values
        header = struct.unpack('iii', header_packed)
        check_header(header)
        # Read the remaining data (msgpack data)
        packed_data = file.read()
        if not packed_data:
            raise ValueError("No data found after header")
        # Unpack the msgpack data
        data = msgpack.unpackb(packed_data, raw=False)
        print(colored(f'Unpacked {len(packed_data)} data bytes from {file_path} with header {header}', "green"))
    return header, data


def check_header(header):
    if header[0] != ANALYSIS_VERSION:
        raise ValueError(f"Unexpected version {header[0]}, supported is {ANALYSIS_VERSION}")


def check_any_extension(name, extensions):
    return any(name.lower().endswith(ext.lower()) for ext in extensions)


def get_files_with_extensions(directory, extensions, recursive=True):
    matched_files = []
    if recursive:
        # Walk through the directory tree recursively
        for root, dirs, files in os.walk(directory):
            for file in files:
                if check_any_extension(file, extensions):
                    matched_files.append(os.path.abspath(os.path.join(root, file)))
    else:
        # Only search in the root directory (non-recursive)
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            # Ensure it's a file and check for extension
            if os.path.isfile(file_path) and check_any_extension(file, extensions):
                matched_files.append(os.path.abspath(file_path))
    return matched_files


def input_to_filepaths(input_path, extensions, recursive=False):
    # If the specified path is a directory, get absolute file paths of all files in the directory
    if os.path.isdir(input_path):
        return get_files_with_extensions(input_path, extensions, recursive)
    elif not check_any_extension(input_path, extensions):
        print(colored(f'{input_path} invalid file extension, expected {", ".join(extensions)}', "red"))
        return []
    return [os.path.abspath(input_path)]


def remap(array, in_min, in_max, out_min, out_max):
    # Clip the value to be within the input range
    array = np.clip(array, in_min, in_max)
    # Perform the linear transformation to the new range
    return (array - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def normalize_array(array):
    array_mean_centered = array - np.mean(array)
    max_abs_value = np.max(np.abs(array_mean_centered))
    normalized_array = array_mean_centered / max_abs_value
    return normalized_array


def normalize_array_01(array):
    min_val = np.min(array)
    max_val = np.max(array)
    normalized_array = (array - min_val) / (max_val - min_val)
    return normalized_array


def change_extension(file_path, new_extension):
    base = os.path.splitext(file_path)[0]
    return base + new_extension


def clip_bin_signal(signal):
    min_value = signal.min()
    max_value = signal.max()
    center = (max_value + min_value) / 2
    clipped = np.clip(signal, center, max_value)
    return clipped


