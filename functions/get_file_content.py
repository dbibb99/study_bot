import os
from google.genai import types
from config import MAX_CHAR

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
     
    try:
        with open(abs_file_path, 'r') as f:
            content = f.read(MAX_CHAR)
            if os.path.getsize(abs_file_path) > MAX_CHAR:
                content += f'\n [...File "{file_path}" truncated at {MAX_CHAR} characters]'
            return content
    except Exception as e:
        return f"Error reading file: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Read and returns the contents of a specified file up to a {MAX_CHAR} character limit, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"]
    ),
)
