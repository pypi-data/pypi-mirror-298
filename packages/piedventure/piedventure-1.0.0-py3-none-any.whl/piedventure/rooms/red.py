"""Module representing the red room in the adventure game.

This module contains the logic for the red room, where the player can sit in a chair
or navigate back to the main room.
"""

import time
from pathlib import Path

from piedventure import lib

from . import mainroom


def main(data_path: Path) -> None:
    """Handle the red room interactions.

    Clears the terminal, displays the room's description, and processes the player's
    input for sitting, interacting with the environment, or exiting the room.

    Args:
        data_path (Path): Path to the data file for game state.

    """
    # Clear the terminal (works for most terminals)
    print('\033c', end='')

    # Initialise the Title Art
    lib.display_art('titleart.ben')
    print()

    # Set up the script for this room. It's a simple one!
    time.sleep(1)
    print("You're in a room that has an odd red glow to it.")
    print('Bookcases line the walls - dusty volumes with titles you')
    print("can't quite make out. Somehow they seem ancient.")
    print()
    print("There's a very comfortable looking chair in the corner.")
    print('The only exit is to the west, back in the direction you came.')
    print()
    print('What would you like to do?')

    # Choices loop
    while True:
        nsewuh = input('> ').strip().lower()
        if nsewuh == 'n':
            print('Face, meet wall. Wall, meet Face.')
        elif nsewuh == 's':
            print("You can't walk through walls.")
        elif nsewuh == 'e':
            print('Nothing but wall here.')
        elif nsewuh == 'w':
            # Call the mainroom.py script
            print('Going back to the main room...')
            mainroom.main(data_path)
            break
        elif nsewuh == 'u':
            print("You sit in the comfortable chair. It's like sitting on a cloud.")
        elif nsewuh == 'h':
            print("You give yourself a hug, hoping that the books won't judge you.")
        else:
            print(
                "I'm sorry, I don't understand you. Commands are: n, e, s, w, u, and h.")

    print('Exiting the room...')
