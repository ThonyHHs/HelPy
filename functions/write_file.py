from functions.config import *
from os import makedirs

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Create or overwrite a specified file with the provided content, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write, relative to the working directory. Must be provided.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that will be written to the file. Must be provided.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    if not path.exists(path.abspath(working_directory)):
        return f'Error: working directory "{working_directory}" does not exists'
    
    full_path = path.join(working_directory, file_path)

    if not is_child(working_directory, full_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    p = '/'.join(full_path.split('/')[:1])
    print(p)
    if not path.exists(p):
        try:
            makedirs(p)
        except Exception as e:
            return f'Error: {e}'

    try:
        with open(full_path, 'w') as file:
            file.write(content)
    except Exception as e:
        return f'Error: {e}'
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'