"""Utility module for managing game logic and displaying art and scripts.

This module contains functions to reset game logic, get and set the state
of levers, and display ASCII art and scripts from specified directories.
"""

from pathlib import Path

# Define paths for art and script directories
art_dir = Path(__file__).parent / 'art'
script_dir = Path(__file__).parent / 'script'


def reset_logic(data_path: Path) -> None:
    """Reset the game logic for the lever.

    This function writes 'off' to the lever logic file, effectively resetting
    its state.

    Args:
        data_path (Path): The path to the directory containing the lever logic file.

    """
    path = data_path / 'logic' / 'leverlogic.ben'
    path.write_text('off')


def get_leverstate(data_path: Path) -> str:
    """Retrieve the current state of the lever.

    This function reads the lever logic file and returns its content as a string.

    Args:
        data_path (Path): The path to the directory containing the lever logic file.

    Returns:
        str: The current state of the lever ('on' or 'off').

    """
    path = data_path / 'logic' / 'leverlogic.ben'
    return path.read_text().strip()


def set_leverstate(data_path: Path, state: str) -> None:
    """Set the state of the lever.

    This function writes the specified state ('on' or 'off') to the lever
    logic file.

    Args:
        data_path (Path): The path to the directory containing the lever logic file.
        state (str): The desired state of the lever ('on' or 'off').

    """
    path = data_path / 'logic' / 'leverlogic.ben'
    path.write_text(state)


def display_art(filename: str) -> None:
    """Display ASCII art from the specified file.

    This function reads the content of the specified art file and prints it
    to the console.

    Args:
        filename (str): The name of the ASCII art file to display (located in the art directory).

    """
    path = art_dir / filename
    print(path.read_text())


def display_script(filename: str) -> None:
    """Display the script from the specified file.

    This function reads the content of the specified script file and prints it
    to the console.

    Args:
        filename (str): The name of the script file to display (located in the script directory).

    """
    path = script_dir / filename
    print(path.read_text())
