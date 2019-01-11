_BLANK_LINE = ""
_HEADING_LABEL = 'Heading'
_COLUMN_LABEL = 'Column'
_DATA_LABEL = 'Data'
_DELIMITER = "\t"
_LINE_BREAK = "\n"

def _get_slice(name, text_lines, start_condition, end_condition):
    section_start = None
    section_end = None
    for count, text in enumerate(text_lines):
        if start_condition(text, count, text_lines):
            section_start = count
        if end_condition(text, count, text_lines):
            section_end = count
            break
            
    if (section_start is None) or (section_end is None):
        errors = []
        if section_start is None:
            errors.append(f'{name.upper()} START')
        if section_end is None:
            errors.append(f'{name.upper()} END')
        raise ValueError('Could not find ' + ' or '.join(errors) + '.')
    
    return slice(section_start, section_end)


def _heading_start(text, count, text_lines):
    # Start should be first line, but no check for that.
    if text == _HEADING_LABEL:
        return True

def _heading_end(text, count, text_lines):
    # End should be followed by a blank line, then column_label.
    # Checking for blank line first to omit it from result.
    if text_lines[count + 1] == _BLANK_LINE:
        if text_lines[count + 2] == _COLUMN_LABEL:
            return True

def _column_start(text, count, text_lines):
    # End should be preceeded by a blank line, then followed by data_label.
    if text == _COLUMN_LABEL:
        if text_lines[count - 1] == _BLANK_LINE:
            if text_lines[count + 2] == _DATA_LABEL:
                return True

def _column_end(text, count, text_lines):
    # Column section should only be two lines long.
    # End should be two lines preceeded by column label.
    # Checking for data_label first to omit it from result.
    if text == _DATA_LABEL:
        if text_lines[count - 2] == _COLUMN_LABEL:
            return True
    
def _data_start(text, count, text_lines):
    # Start should be two lines preceeded by column label.
    if text == _DATA_LABEL:
        if text_lines[count - 2] == _COLUMN_LABEL:
            return True

def _data_end(text, count, text_lines):
    # Checking for blank line first to omit it from result if present.
    # As a default, returning true if we're at the last line.
    # Remember the -1. len() is not zero-based, but count is.
    if text == _BLANK_LINE:
        if count == len(text_lines) - 1:
            return True
    if count == len(text_lines) - 1:
        return True
        
def _format_heading(header_list):
    assert header_list[0] == _HEADING_LABEL, 'Heading label not found.'
    header = {}

    for pair in header_list[1:]:
        elements = pair.split(_DELIMITER)
        assert len(elements) == 2, 'Too many elements in heading pair.'
        key, value = elements
        header[key] = value

    return header      

def _format_column(column_list):
    assert column_list[0] == _COLUMN_LABEL, 'Column label not found.'
    return column_list[1].split(_DELIMITER)

def _format_data(data_list):
    assert data_list[0] == _DATA_LABEL, 'Data label not found.'
    data = []
    for i in data_list[1:]:
        data.append(i.split(_DELIMITER))
    return data

def _string_labels_to_integers(converter_dict, column_label_list):
    data_indices = {}
    for string_key, converter_func in converter_dict.items():
        try:
            label_index = column_label_list.index(string_key)
        except ValueError:
            raise ValueError('Converter column label not found in ALE file.')
        data_indices[label_index] = converter_func
    
    return data_indices

def validate_converters(converters, column_label_list):
    if not isinstance(converters, dict):
        raise TypeError('Converters must be in a dictionary.')

    if not all(hasattr(value, '__call__') for value in converters.values()):
        raise TypeError('Converters values must be callables.')

    is_all_strings = all(isinstance(key, str) for key in converters.keys())
    is_all_integers = all(isinstance(key, int) for key in converters.keys())
    
    if not is_all_strings and not is_all_integers:
        raise TypeError('Converters keys must be either all strings or all integers') 

    if is_all_strings:
        converters = _string_labels_to_integers(converters, column_label_list)
    
    return converters


def parse_ale(file_string, converters=None):
    text_lines = file_string.split(_LINE_BREAK)
    heading_lines = text_lines[_get_slice('heading', text_lines, _heading_start, _heading_end)]
    column_lines = text_lines[_get_slice('column', text_lines, _column_start, _column_end)]
    data_lines = text_lines[_get_slice('data', text_lines, _data_start, _data_end)]

    formatted_heading =_format_heading(heading_lines)
    formatted_column = _format_column(column_lines)
    formatted_data = _format_data(data_lines)
    
    if converters:
        converters = validate_converters(converters, formatted_column)      
        for row in formatted_data:
            for label_index, converter_func in converters.items():                        
                row[label_index] = converter_func(row[label_index])         

    return {
        'heading': formatted_heading,
        'columns': tuple(formatted_column),
        'data': [tuple(row) for row in formatted_data]
    }