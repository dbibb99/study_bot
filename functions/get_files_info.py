import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    abs_working_dir = os.path.abspath(working_directory)

    if directory:
        abs_dir_path = os.path.abspath(os.path.join(working_directory, directory))

    if not abs_dir_path.startswith(abs_working_dir):
        return f'Error: Cannot locate "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(abs_dir_path):
        return f'Error: "{abs_dir_path} if not a directory"'
    
    try:
        files_info = []
        for filename in os.listdir(abs_dir_path):
            file_path = os.path.join(abs_dir_path, filename)
            file_size = 0
            is_dir = os.path.isdir(file_path)
            file_size = os.path.getsize(file_path)
            files_info.append(f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(files_info)
    except Exception as e:
        return f'Error listing files in {abs_dir_path}: {e}'
    
    
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
    