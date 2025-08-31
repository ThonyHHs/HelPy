from functions.config import *
from os import listdir

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    if not path.exists(path.abspath(working_directory)):
        return f'Error: working directory "{working_directory}" does not exists'

    full_path = path.join(working_directory, directory)

    if not is_child(working_directory, full_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    
    files_list = list(map(lambda item: 
        f"- {item}: file_size={path.getsize(path.join(full_path, item))} bytes, is_dir={path.isdir(path.join(full_path, item))}", 
        listdir(full_path)
    ))

    return '\n'.join(files_list)