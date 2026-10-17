import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    # print(f'Result for {f"'{directory}'" if directory != "." else "current"} directory:')

    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    elif os.path.isdir(target_dir):
        # return f'Success: "{directory}" is within the working directory'
        pass


    record = ''
    try: 
        for item in os.listdir(target_dir):
            # os.chdir(target_dir)
            item_dir = os.path.join(target_dir, item)
            record += f'- {item}: file_size={os.path.getsize(item_dir)}bytes, is_dir={os.path.isdir(item_dir)}\n'
    except Exception as e:
        return f'Error: {e}'

    return record
    
schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}