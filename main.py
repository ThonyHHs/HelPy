import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

def call_function(function_call_part, verbose=False):
    functions_dict = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    function_name = function_call_part.name
    function_args = function_call_part.args

    try:
        func = functions_dict[function_name]
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    function_result = func(working_directory="./calculator",**function_args)

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )

def main():
    try:
        user_prompt = sys.argv[1]
        user_args = ""
        if "--verbose" in sys.argv:
            user_args = sys.argv[2] == "--verbose"
        if user_prompt.strip() == "":
            raise Exception("Empty string")
    except Exception as e:
        print("ERROR:", e)
        print(f"No prompt has been provided. Please add an prompt to use the program.")
        exit(1)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            ),
        )

        if not response.function_calls and not "Warning: there are non-text parts in the response:" in response.text:
            print(response.text)
            break
        
        for candidate in response.candidates:
            messages.append(candidate.content)

        try:
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, user_args)

                if not function_call_result.parts[0].function_response.response:
                    raise Exception("ERROR: not have a response")

                if user_args:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                
                messages.append(types.Content(role="tool", parts=function_call_result.parts))
        except Exception as e:
            print(f"ERROR: {e}")

if __name__ == "__main__":
    main()