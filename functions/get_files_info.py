import os
from google import genai
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        working_dir_absolute_path = os.path.abspath(working_directory) #this sets the absolute path for the working directory
        target_directory = os.path.normpath(os.path.join(working_dir_absolute_path, directory)) #this sets the path for the target directory
        valid_target_dir = os.path.commonpath([working_dir_absolute_path, target_directory]) == working_dir_absolute_path #this compares the paths and the target to make sure its valid

        if valid_target_dir == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if os.path.isdir(target_directory) == False:
            return f'Error: "{directory}" is not a directory'
        list_of_files = []
        for files in os.listdir(target_directory): #this iterats through the loop of files in the target directory to assess properties
            list_of_files.append(f"- {files}: file_size={os.path.getsize(os.path.join(target_directory,files))} bytes, is_dir={os.path.isdir(os.path.join(target_directory, files))}")
        joined_files = "\n  ".join(list_of_files)
        return joined_files
    except Exception as e:
        return f"Error: {e}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)