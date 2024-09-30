"""file_interaction.py: Functions for interacting with files."""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def save_text_to_file(text: str, file_path: Path) -> None:
    """
    Save text to a file.

    Parameters
    ----------
    text : str
        The text to save to the file.
    file_path : Path
        The path to the file to save the text to.
    """
    logger.debug(f"Saving text to file: {file_path}")
    with open(file_path, "w") as file:
        file.write(text)
    logger.info(f"Text saved to file: {file_path}")
