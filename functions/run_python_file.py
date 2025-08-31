from functions.config import *
import subprocess

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a specified Python file with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to run, relative to the working directory. Must be provided.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="An array of string arguments to pass to the Python file. If not provided, the file runs without arguments.",
                items=types.Schema(type=types.Type.STRING)
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    if not path.exists(path.abspath(working_directory)):
        return f'Error: working directory "{working_directory}" does not exists'
    
    full_path = path.join(working_directory, file_path)

    if not is_child(working_directory, full_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    
    if not full_path.split('/')[-1].endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        command = ["python3", path.abspath(full_path)] + args
        result = subprocess.run(args=command, timeout=30, capture_output=True)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    if not result.stdout and not result.stderr:
        return "No output produced"

    result_str = f"STDOUT: \n{result.stdout.decode()} \nSTDERR: \n{result.stderr.decode()}"

    if result.returncode != 0:
        result_str += f"Process exited with code {result.returncode}"

    return result_str