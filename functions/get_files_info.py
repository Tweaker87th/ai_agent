import os

def get_files_info(working_directory, directory="."):
    """
    List files in a directory under the given working_directory, with size and is_dir info.
    Always returns a string. On error, returns a string starting with 'Error:'.
    """
    try:
        # Absolute path of the working directory
        working_dir_abs = os.path.abspath(working_directory)

        # Full, normalized path to the target directory
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # Ensure target_dir is inside working_dir_abs
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Ensure target_dir is actually a directory
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # Iterate over items and build result lines
        entries = []
        with os.scandir(target_dir) as it:
            for entry in it:
                name = entry.name
                if name.startswith("__"):
                    continue
                is_dir = entry.is_dir()
                try:
                    size = entry.stat().st_size
                except OSError as e:
                    # If stat fails, report the error for this entry
                    entries.append(f"- {name}: Error: {e}")
                    continue

                entries.append(
                    f"- {name}: file_size={size} bytes, is_dir={bool(is_dir)}"
                )

        # Join all lines into a single string
        return "\n".join(entries)

    except Exception as e:
        # Catch-all: never raise, always return an error string
        return f"Error: {e}"