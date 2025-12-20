import os
import subprocess

from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    absolute_working_dir = os.path.abspath(working_directory)
    absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not absolute_file_path.startswith(absolute_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(absolute_file_path):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        completed_process = subprocess.run(
            ["python", absolute_file_path] + args,
            stdout=None,
            stderr=None,
            capture_output=True,
            timeout=3000,
        )

        if completed_process.returncode != 0:
            formatted_string = f"STDOUT: {completed_process.stdout.decode('utf-8')}\nSTDERR:Process exited with code {completed_process.returncode}"
        elif completed_process.stdout == f'b""':
            formatted_string = "No output produced"
        else:
            formatted_string = f"STDOUT: {completed_process.stdout.decode('utf-8')}\nSTDERR: {completed_process.stderr.decode('utf-8')}"
    except Exception as e:
        return f"Error: executing file: {e}"

    return formatted_string


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in the specified working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="An optional list of arguments to pass to the Python file during execution.",
            ),
        },
        required=["file_path"],
    ),
)
