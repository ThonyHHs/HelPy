from functions.config import *

def get_file_content(working_directory, file_path):
    if not path.exists(path.abspath(working_directory)):
        return f'Error: working directory "{working_directory}" does not exists'

    full_path = path.join(working_directory, file_path)
    file_contents = ""

    if not is_child(working_directory, full_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(full_path, 'r') as file:
            file_contents = file.read(MAX_CHARS)
    except Exception as e:
        return f'Error: {e}'

    if path.getsize(full_path) > MAX_CHARS:
        file_contents += f'[...File "{file_path}" truncated at 10000 characters]'

    return file_contents