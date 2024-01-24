import re

def try_parse_float(value_str: str):
    try:
        return (True, float(value_str))
    except:
        return (False, 'Input has to be numeric.')


variable_name_regex = None

def validate_variable_name(name: str):
    global variable_name_regex
    if variable_name_regex is None:
        variable_name_regex = re.compile("^[a-zA-Z_]\\w*$")
    if variable_name_regex.fullmatch(name):
        return (True, )
    return (False, 'Variable name has to start with a letter or underscore followed by zero or more letters, digits, and underscores')


