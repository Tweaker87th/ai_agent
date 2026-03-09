import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    """
    Run a Python file under working_directory using subprocess.
    Always returns a string. On error, returns a string starting with 'Error:'.
    """
    try:
        # Absolute path of the working directory
        working_dir_abs = os.path.abspath(working_directory)

        # Full, normalized path to the target file
        absolute_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Ensure absolute_file_path is inside working_dir_abs
        valid_file_path = os.path.commonpath([working_dir_abs, absolute_file_path]) == working_dir_abs
        if not valid_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Ensure file exists and is a regular file
        if not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # Ensure it's a .py file
        if not absolute_file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        # Build command: ["python", absolute_file_path, ...args]
        command = ["python", absolute_file_path]
        if args is not None:
            command.extend(args)

        # Run with subprocess: capture output, set cwd, timeout, text mode
        result = subprocess.run(
            command,
            cwd=working_dir_abs,  # Working directory
            capture_output=True,  # Capture stdout+stderr
            text=True,            # Decode to strings (not bytes)
            timeout=30,           # 30 second timeout
        )

        # Build output string
        output_lines = []
        if result.returncode != 0:
            output_lines.append(f"Process exited with code {result.returncode}")

        if not result.stdout and not result.stderr:
            output_lines.append("No output produced")
        else:
            if result.stdout:
                output_lines.append("STDOUT:")
                output_lines.extend(result.stdout.strip().splitlines())
            if result.stderr:
                output_lines.append("STDERR:")
                output_lines.extend(result.stderr.strip().splitlines())

        return "\n".join(output_lines) if output_lines else "Process completed with no output"

    except subprocess.TimeoutExpired:
        return "Error: Process timed out after 30 seconds"
    except Exception as e:
        return f"Error: executing Python file: {e}"

# Function schema for LLM tool calling
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional arguments relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of string arguments to pass to the Python script",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    ),
)
    