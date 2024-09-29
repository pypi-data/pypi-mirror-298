"""Game module for managing player instances and game state.

This module handles the setup and execution of the game by creating
temporary directories for new player instances, copying necessary game
files, and starting the game. It provides functions to load the game
environment and manage the lifecycle of player instances, ensuring
proper cleanup of temporary files after the game ends.

Key functionalities include:

- Copying game logic files to a new player directory.
- Removing player directories upon game completion.
- Simulating a loading screen during game startup.
- Initiating the game with the new player instance.

Usage:
    This module is intended to be run as a script. The main function
    is executed when the module is run directly, initiating the game.
"""

from __future__ import annotations

import shutil
import tempfile
import time
import uuid
from pathlib import Path

from .rooms import start


def copy_game_files(data_path: Path) -> None:
    """Copy the necessary directories for a new player instance.

    This function copies the contents of the 'logic' directory to a new
    directory specific to the player, creating a fresh instance of the
    game environment for the player.

    Args:
        data_path (Path): The path to the new player directory where
                          game files will be copied.

    Returns:
        None

    """
    logic_dir = Path(__file__).parent / 'logic'
    shutil.copytree(logic_dir, data_path / 'logic')


def remove_game_files(data_path: Path) -> None:
    """Remove the temporary game instance after the game ends.

    This function deletes the directory created for the player's game
    instance to clean up temporary files.

    Args:
        data_path (Path): The path to the player directory that needs
                          to be removed.

    Returns:
        None

    """
    shutil.rmtree(data_path)


def load_game() -> None:
    """Simulate a loading screen.

    This function displays a loading message and pauses the program
    for a few seconds to create a loading effect.

    Returns:
        None

    """
    print('Loading...')
    time.sleep(4)


def start_game(data_path: Path) -> None:
    """Start the game with the new player instance.

    This function initializes the game by calling the main function
    of the start module, passing the player's directory.

    Args:
        data_path (Path): The path to the player's game instance.

    Returns:
        None

    """
    start.main(data_path)


def main() -> None:
    """Serve as main entry point for the game.

    This function orchestrates the game setup by creating a new player
    instance, copying necessary game files, simulating a loading
    screen, and starting the game. It also handles clean-up by removing
    the player directory upon exiting the game.

    Returns:
        None

    """
    try:
        data_path = Path(tempfile.gettempdir(), str(uuid.uuid4())).resolve()
        data_path.mkdir()
        copy_game_files(data_path)
        load_game()
        start_game(data_path)
    except KeyboardInterrupt:
        print('Ctrl-C pressed by user')
    finally:
        remove_game_files(data_path)


if __name__ == '__main__':
    main()
