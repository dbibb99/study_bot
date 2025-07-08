from google.genai import types

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python import schema_run_python, run_python

from config import WORKING_DIR

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python
    ]
)

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f'Calling function: {function_call_part.name}({function_call_part.args})')
    else:
        print(f' - Calling function: {function_call_part.name}')

    function_map = {
        "get_files_info" : get_files_info,
        "get_file_content" : get_file_content,
        "write_file" : write_file,
        "run_python" : run_python,
    }

    working_dir = WORKING_DIR

    function_name = function_call_part.name
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    args_dic = dict(function_call_part.args)
    args_dic["working_directory"] = working_dir

    function_output = function_map[function_name](**args_dic)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result" : function_output}
            )
        ]
    )

