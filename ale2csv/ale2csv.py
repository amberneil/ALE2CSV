from .helpers import read_target
from .parser import parse_ale
from .render import render_csv

def ale2csv(target, destination, converters=None):
    
    file_string = read_target(target)
    
    ale_map = parse_ale(file_string, converters=converters)

    render_csv(ale_map['data'], destination, column_labels=ale_map['columns'])