import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    workdir_abs = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(workdir_abs, file_path))

    valid_file_path = os.path.commonpath([workdir_abs, target_file_path]) == workdir_abs
    if not valid_file_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if os.path.isdir(target_file_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    os.makedirs(workdir_abs, exist_ok=True)

    try:
        with open(target_file_path, 'w') as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write the content of given text(content) to the given file on file_path and return the success with number of chars written or error mentioning what went wrong",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to write content to, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write into the file on given file_path"
                }
            },
        },
    },
}