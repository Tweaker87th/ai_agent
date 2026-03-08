import os
from config import MAX_FILE_READ_CHARS


def get_file_content(working_directory, file_path):
    """
    Read up to MAX_FILE_READ_CHARS from a file under working_directory.
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
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Ensure target_file exists and is a regular file
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read up to MAX_FILE_READ_CHARS
        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read(MAX_FILE_READ_CHARS)
            
            # Check if truncated by trying to read one more char
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_FILE_READ_CHARS} characters]'

        return content

    except Exception as e:
        return f"Error: {e}"
