from os import path
from google.genai import types

MAX_CHARS = 10000

def is_child(working_directory, full_path):
    common_path = path.commonpath([
        path.abspath(working_directory), 
        path.abspath(full_path)
    ])

    if common_path == path.abspath(working_directory):
        return True
    
    return False