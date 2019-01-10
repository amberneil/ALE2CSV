import os
import traceback

def read_file_to_string(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError('File does not exist.')
    with open(file_path, 'r') as f:
        return f.read()