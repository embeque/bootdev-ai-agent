import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    workdir_abs = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(workdir_abs, file_path))

    valid_file_path = os.path.commonpath([workdir_abs, target_file_path]) == workdir_abs
    
    if not valid_file_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(target_file_path, 'r') as f:
            content = f.read(MAX_CHARS)
            
            # After reading the first MAX_CHARS...
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content
    except Exception as e:
        return f'Error: {e}'

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Read the content of some given file of about maxchars=10000 and provide the content itself and additional text if the content of file is trucated at 10000 chars",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to read content from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}