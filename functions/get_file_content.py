import os
from config import MAX_CHARS

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