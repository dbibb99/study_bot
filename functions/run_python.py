import os
import subprocess
from google.genai import types

def run_python(working_directory, file_path, args=None):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not abs_file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        commands = ["python", abs_file_path]
        if args:
            commands.extend(args)

        result = subprocess.run(
            commands, capture_output=True, text=True, timeout=30, check=True, cwd=abs_working_dir
        )

        output = []

        if result == None:
            return f'No output produced when executing "{file_path}"'

        std_out = f"STDOUT:\n{result.stdout}"
        std_err = f"STDERR:\n{result.stderr}"
        output.append(std_out)
        output.append(std_err)

        if result.returncode != 0:
            std_code = f"Process exited with code {result.returncode}"
            output.append(std_code)
        
        return "\n".join(output) if output else "No results produced."
    except subprocess.CalledProcessError as e:
        return f'Error: executing Python file "{file_path}": {e}'


schema_run_python = types.FunctionDeclaration(
    name='run_python',
    description="Exceute a python file with optional arguments from the specified directory, returning the output. Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            'file_path' : types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory."
            ),
            'args' : types.Schema(
                type=types.Type.STRING,
                description="Optional arguments to pass to the Python file."
            )
        },
        required=['file_path']
    )
)