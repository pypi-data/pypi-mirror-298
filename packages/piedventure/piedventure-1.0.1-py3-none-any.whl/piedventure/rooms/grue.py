"""Module representing the Grue encounter in the adventure game.

This module contains the logic for encountering a Grue, where the player
listens to Grue poetry and faces a gruesome death.
"""

import time
from pathlib import Path

from piedventure import lib

from . import mainroom


def main(data_path: Path) -> None:
    """Handle the Grue encounter.

    Clears the terminal, displays the Grue encounter, and processes the player's
    ultimate demise after being forced to listen to Grue poetry.

    Args:
        data_path (Path): Path to the data file for game state.

    """
    # Clear the terminal (works for most terminals)
    print('\033c', end='')

    # Initialise the Title Art
    lib.display_art('titleart.ben')
    print('\n')

    # Room description and encounter
    time.sleep(1)
    print('This is a long room, and as you walk down it, you see a person.')
    print('Finally! Another person! You start to run toward the shadowy figure')
    print("but then stop dead. This isn't... no... it can't be. It's... it's...")
    print("IT'S A GRUE.")
    time.sleep(3)
    print('\nNo. NO! You cry, as he sits you down and, rather than beating you to')
    print("death, starts to read you some of his Grue Poetry. It's awful. Your")
    print('brain starts to melt and, as a result, your nose starts bleeding.')
    print('\n')
    time.sleep(5)
    print("You start to feel dizzy. You can't think straight. As you fall to the")
    print('floor, your own blood and brains all around you, you begin')
    print("to wonder why the grue didn't just kill you quickly like")
    print('most do. Bloody liberal arts students.')
    print('\nYou slip into unconsciousness.')
    time.sleep(4)
    print('YOU ARE DEAD.')
    print('\n')
    input('Press [ENTER] to try again...')

    # Call mainroom.py
    mainroom.main(data_path)
