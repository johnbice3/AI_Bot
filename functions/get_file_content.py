import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        working_dir_absolute_path = os.path.abspath(working_directory) #this sets the absolute path for the working directory
        abs_file_path = os.path.normpath(os.path.join(working_dir_absolute_path, file_path))
        valid_working_dir = os.path.commonpath([working_dir_absolute_path, abs_file_path]) == working_dir_absolute_path
        
        if valid_working_dir == False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if os.path.isfile(abs_file_path) == False:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string

    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns a string with up to the girst 10,000 characters in a file, assuming it falls within the working directory",
    parameters=types.Schema(
        required = ["file_path"],
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path for the file you wish to execute"
            ),
        },
    ),
)