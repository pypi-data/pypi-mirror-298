"""main.py: Called when the package is ran as a script."""

from logging import shutdown as shutdown_logging
from pathlib import Path

from .computation.image_processing import (
    brightness_matrix_to_ascii,
    chunk_matrix_to_resolution,
    png_to_brightness_matrix,
)
from .config.constants import Constants
from .interface.command_line import command_line_interface
from .logs.setup_logging import setup_logging
from .utilities.file_interaction import save_text_to_file


def main() -> None:
    """
    Overall control flow of the application.

    Notes
    -----
    This function is the entry point for the application, so only really
    contains overall control flow logic. The actual work is done in the
    other modules.
    """
    # Get the arguments from the command line
    user_arguments = command_line_interface()

    # Setup logging
    setup_logging(
        user_arguments["log_output_location"],
        console_logging_level=(
            "DEBUG" if user_arguments["verbose"] else Constants.LOGGING_LEVEL_CONSOLE_DEFAULT
        ),
    )

    # Main application logic
    brightness_matrix = png_to_brightness_matrix(Path(user_arguments["input_file"]))
    chunked_matrix = chunk_matrix_to_resolution(brightness_matrix, user_arguments["resolution"])
    ascii_art = brightness_matrix_to_ascii(chunked_matrix)  # TODO: Add edge detection
    save_text_to_file(ascii_art, Path("ascii_art.txt"))

    # Shutdown logging
    shutdown_logging()


if __name__ == "__main__":
    main()
