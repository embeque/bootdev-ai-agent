import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    workdir_abs = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(workdir_abs, file_path))

    valid_file_path = os.path.commonpath([workdir_abs, target_file_path]) == workdir_abs
    if not valid_file_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if file_path[-3:] != '.py':
        return f'Error: "{file_path}" is not a Python file'

    command = ['python', target_file_path]
    if args != None:
        command.extend(args)

    try:
        output = ''

        response: subprocess.CompletedProcess = subprocess.run(command, cwd=workdir_abs, capture_output=True, text=True, timeout=30)
        if response.returncode != 0:
            output += f"Process exited with code {response.returncode}"
        if response.stdout and response.stderr:
            output += "No output produced"
        else:
            output += f"STDOUT: {response.stdout}\nSTDERR: {response.stderr}"

        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "given any python file path in file_path and args list, runs that python file with argument list and return the stdout and stderr on success and if fails return the returncode and in case of no output produced, simply return no output produced text",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to python file to run, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "string",
                    "description": "Arguments to pass on to python command to run with",
                },
            },
        },
    },
}