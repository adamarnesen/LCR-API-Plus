from pathlib import Path


def create_and_get_output_path(filename: str, parent_directory: str = None):
    """Get the output path.

    Constructs the correct output path for this project and ensures that the output directory
    exists.
    """
    DEFAULT_OUTPUT_DIRECTORY = "analytics/data"
    if not parent_directory:
        parent_directory = DEFAULT_OUTPUT_DIRECTORY
    output_directory = Path(parent_directory)
    output_directory.mkdir(parents=True, exist_ok=True)
    output_file = output_directory / str(filename)
    return output_file
