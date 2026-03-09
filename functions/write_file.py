import os
from google.genai import types

def write_file(working_directory, file_path, content):
    """
    Write content to a file under the given working_directory.
    Always returns a string. On error, returns a string starting with 'Error:'.
    """
    try:
        # Absolute path of the working directory
        working_dir_abs = os.path.abspath(working_directory)

        # Full, normalized path to the target file
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Ensure target_file is inside working_dir_abs
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Ensure target_file is not an existing directory
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Create parent directories if needed
        parent_dir = os.path.dirname(target_file)
        os.makedirs(parent_dir, exist_ok=True)

        # Write the content to the file
        with open(target_file, "w") as f:
            f.write(content)

        # Success message with character count
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        # Catch-all: never raise, always return an error string
        return f"Error: {e}"
    
# Function schema for LLM tool calling
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites content to a file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)
