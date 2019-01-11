from .helpers import read_target
from .parser import parse_ale
from .render import render_csv

def ale2csv(target, destination=None, converters=None, to_stringIO=False):

    if destination and to_stringIO:
        raise ValueError('Cannot set both destination and to_stringIO parameters.')
    
    file_string = read_target(target)
    if len(file_string) == 0:
        raise ValueError('ale2csv received an empty string.')
    
    ale_map = parse_ale(file_string, converters=converters)

    rendered_buffer = render_csv(
        ale_map['data'],
        destination,
        column_labels=ale_map['columns'],
    )

    if to_stringIO:
        return rendered_buffer
    else:
        return rendered_buffer.getvalue()