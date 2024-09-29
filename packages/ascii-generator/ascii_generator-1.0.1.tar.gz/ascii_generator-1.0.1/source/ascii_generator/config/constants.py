"""constants.py: Constants for the application."""

from pathlib import Path
from typing import Literal


class Constants:
    """
    Constants for the application.

    Notes
    -----
    This class contains constants used throughout the application.
    By storing constants in a single location, it is easier to
    manage and update them. Constants should be defined as class
    attributes and should be named in uppercase with underscores
    separating words. Constants should use type hints to indicate
    to the user what type of data they should store.
    """

    # Logging constants
    POSSIBLE_LOGGING_LEVELS = Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]
    LOGGING_LEVEL_LOGFILE_DEFAULT: POSSIBLE_LOGGING_LEVELS = "DEBUG"
    LOGGING_LEVEL_CONSOLE_DEFAULT: POSSIBLE_LOGGING_LEVELS = "INFO"
    LOGGING_LOGFILE_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOGGING_CONSOLE_FORMAT: str = "%(message)s"
    LOGGING_TIMESTAMP_FORMAT: str = "%Y-%m-%d_%H-%M-%S"
    LOGGING_DATE_FORMAT: str = "[%X]"
    LOGGING_TRACEBACKS: bool = True

    # API response constants
    SUCCESS_CODE: int = 200
    SUCCESS_TEXT: str = "OK"
    FORBIDDEN_CODE: int = 403

    # Default values
    DEFAULT_LOG_SAVE_PATH: Path = Path("ascii-generator_log.txt")

    # ASCII constants
    DEFAULT_RESOLUTION: tuple[int, int] = (36, 36)
    ASCII_CHARACTERS: list[str] = [
        " ",
        ".",
        ",",
        ":",
        ";",
        "i",
        "1",
        "t",
        "f",
        "L",
        "C",
        "G",
        "0",
        "8",
        "#",
    ]
