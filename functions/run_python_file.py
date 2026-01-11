import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_absolute_path = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(working_dir_absolute_path, file_path))
        valid_working_dir = os.path.commonpath([working_dir_absolute_path, abs_file_path]) == working_dir_absolute_path

        if valid_working_dir == False:
           return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if file_path.endswith(".py") == False:
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", abs_file_path]

        if args != None:
            command.extend(args)

        result_subprocess = subprocess.run(
            command,
            cwd = working_dir_absolute_path,
            capture_output = True,
            text = True,
            timeout = 30
        )

        results_output = []

        if result_subprocess.returncode != 0:
            results_output.append(f"Process exicted with code {result_subprocess.returncode}")
        
        if len(result_subprocess.stdout) == 0 and len(result_subprocess.stderr) == 0:
            results_output.append("No output produced")
        
        if len(result_subprocess.stdout) > 0:
            results_output.append(f"STDOUT: {result_subprocess.stdout}")
        
        if len(result_subprocess.stderr) > 0:
            results_output.append(f"STDERR: {result_subprocess.stderr}")
        
        joined_output = "\n".join(results_output)

        return joined_output

    except Exception as e:
        return (f"Error: executing Python file: {e}")

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a .py file based on the file name provided, assuming it falls within the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Items are the strings in the args array",
                ),
                description="Additional arguments for the file you wish to run"
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path for the file you wish to execute"
            ),
        },
        required = ["file_path"],
    ),
)