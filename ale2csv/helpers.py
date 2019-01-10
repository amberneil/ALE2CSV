import os
import traceback

def read_file_to_string(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError('File does not exist.')
    with open(file_path, 'r') as f:
        return f.read()

def read_target(target):
    if not isinstance(target, str):
        raise ValueError('ale2csv needs a string, either raw ALE or a file path.')
    if os.path.exists(target):
        return read_file_to_string(target)
    else:
        return target    
