import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        working_dir_absolute_path = os.path.abspath(working_directory) 
        abs_file_path = os.path.normpath(os.path.join(working_dir_absolute_path, file_path))
        valid_working_dir = os.path.commonpath([working_dir_absolute_path, abs_file_path]) == working_dir_absolute_path
        
        if valid_working_dir == False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.exists(abs_file_path):    
            if os.path.isdir(abs_file_path):
                return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(abs_file_path),exist_ok=True)

        with open(abs_file_path,"w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: writing to file: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a python file with user submitted content, assuming it falls within the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content that should be added to the target file"
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path for the file you wish to execute"
            ),
        },
        required = ["file_path", "content"],
    ),
)