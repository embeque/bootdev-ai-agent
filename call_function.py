import json
from collections.abc import Callable

from functions.get_files_info import *
from functions.get_file_content import *
from functions.write_file import *
from functions.run_python_file import *

available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python_file
]

def call_function(tool_call, verbose: bool = False) -> dict:
    func_name = tool_call.function.name
    func_args = json.loads(tool_call.function.arguments or {})

    if verbose:
        print(f" - Calling function: {func_name}({func_args})")
    else:
        print(f" - Calling function: {func_name}")

    function_map: dict[str, Callable[..., str]] = {
        "get_file_content": get_file_content,
        'get_files_info': get_files_info,
        'write_file': write_file,
        'run_python_file': run_python_file
    }

    tool = {
        'role': "tool",
        'tool_call_id': tool_call.id,
        'content': f"Error: Unknown function: {func_name}"
    }
    if func_name not in function_map:
        return tool
    func_args['working_directory'] = './calculator'

    result = function_map[func_name](**func_args)
    tool['content'] = result

    return tool

