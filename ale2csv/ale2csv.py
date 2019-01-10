from helpers import read_file_to_string
from parser import parse_ale
from render import render_csv

def ale2csv(file_path, destination, converters=None):
    file_string = read_file_to_string(file_path)
    
    ale_map = parse_ale(file_string, converters=converters)

    render_csv(ale_map['data'], destination, column_labels=ale_map['columns'])