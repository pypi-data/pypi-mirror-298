"""image_processing.py: Contains functions for image processing."""

import logging
from pathlib import Path

import numpy as np
from PIL import Image

from ..config.constants import Constants

logger = logging.getLogger(__name__)


def png_to_brightness_matrix(png_path: Path) -> np.ndarray:
    """
    Convert a PNG image to a brightness matrix.

    Parameters
    ----------
    png_path : Path
        The path to the PNG image.

    Returns
    -------
    np.ndarray
        The brightness matrix with normalised values in the range [0, 1].

    Raises
    ------
    ValueError
        If the image is not a PNG image.

    Examples
    --------
    >>> png_to_brightness_matrix(Path("test.png"))
    """
    logger.info(f"Converting PNG image to brightness matrix: {png_path}")

    if png_path.suffix != ".png":
        raise ValueError("Image is not a PNG image.")

    with Image.open(png_path) as colour_image:
        grayscale_image = colour_image.convert("L")  # Convert to luminance
        brightness_matrix = np.array(grayscale_image) / 255  # Normalise to [0, 1]

    return brightness_matrix


def chunk_matrix_to_resolution(matrix: np.ndarray, resolution: tuple[int, int]) -> np.ndarray:
    """
    Chunk a matrix into a resolution.

    Parameters
    ----------
    matrix : np.ndarray
        The matrix to chunk.
    resolution : tuple[int, int]
        The resolution to chunk the matrix to.

    Returns
    -------
    np.ndarray
        The chunked matrix.

    Examples
    --------
    >>> chunk_matrix_to_resolution(np.array([[1, 2], [3, 4]]), (1, 1))
    """
    logger.info(f"Clipping matrix to resolution: {resolution}")

    # Get the dimensions of the matrix and the resolution
    rows, cols = matrix.shape
    resolution_rows, resolution_columns = resolution

    # Calculate the number of chunks to keep
    row_chunks = rows // resolution_rows
    column_chunks = cols // resolution_columns

    # Clip the matrix
    chunked_array = np.zeros((row_chunks, column_chunks), dtype=int)
    for row in range(row_chunks):
        for column in range(column_chunks):
            chunk = matrix[
                row * resolution_rows : (row + 1) * resolution_rows,  # noqa: E203
                column * resolution_columns : (column + 1) * resolution_columns,  # noqa: E203
            ]

            chunked_array[row, column] = np.mean(chunk)

    return chunked_array


def brightness_matrix_to_ascii(matrix: np.ndarray) -> str:
    """
    Convert a brightness matrix to ASCII.

    Parameters
    ----------
    matrix : np.ndarray
        The brightness matrix.

    Returns
    -------
    str
        The ASCII representation of the brightness matrix.

    Examples
    --------
    >>> brightness_matrix_to_ascii(np.array([[0.5, 0.5], [0.5, 0.5]]))
    """
    logger.info("Converting brightness matrix to ASCII")

    # Normalise to length of ASCII characters
    normalised_matrix = matrix * (len(Constants.ASCII_CHARACTERS) - 1)

    # Convert the brightness matrix to an ASCII matrix
    ascii_matrix = [
        [Constants.ASCII_CHARACTERS[int(element)] for element in row] for row in normalised_matrix
    ]

    return "\n".join("".join(row) for row in ascii_matrix)
