"""Module to represent a central room in a game.

The player can navigate
to various colored rooms (brown, green, red, and white) after waking up in a
mysterious large space. The player can interact with the environment by
inputting directional commands to explore different areas.

The player can also attempt to perform actions such as using items or hugging themselves.
"""

import time
from pathlib import Path

from piedventure import lib

from . import brown, green, red, white


def main(data_path: Path) -> None:
    """Handle the player's interactions within the central room.

    After waking up in a large room, the player is presented with options to
    navigate to adjacent colored rooms (north, east, south, and west). This function
    listens for directional commands, allowing the player to explore the environment
    and advance the game's storyline by moving to different rooms.

    Args:
        data_path (Path): Path to the game data, used for maintaining or modifying game state.

    Returns:
        None

    """
    # Clear the terminal (works for most terminals)
    print('\033c', end='')

    # Initialise the Title Art
    lib.display_art('titleart.ben')
    print()

    # Shakespeare wrote this, honest.
    time.sleep(1)
    print('You are back in the room you first woke up in.')
    print("It's huge. You can't really fathom how large, but it took")
    print('long enough to get from that last room back to the middle of')
    print('this one. You wonder how you got here, and who is responsible.')
    print()
    print('You can just about see doors to the north, east, south, and west.')
    print()
    print('What would you like to do?')

    # Room logic loop
    while True:
        nsewuh = input('> ').strip().lower()
        if nsewuh == 'n':
            # Call the white.py script (adjust as necessary)
            print('Going to the white room...')
            white.main(data_path)
            break
        if nsewuh == 's':
            print('Going to the brown room...')
            brown.main(data_path)
            break
        if nsewuh == 'e':
            print('Going to the red room...')
            red.main(data_path)
            break
        if nsewuh == 'w':
            print('Going to the green room...')
            green.main(data_path)
            break
        if nsewuh == 'u':
            print("There's nothing you can use right here.")
        elif nsewuh == 'h':
            print("You give yourself a quick hug. It's not very satisfying.")
        else:
            print(
                "I'm sorry, I don't understand you. Commands are: n, e, s, w, u, and h.")

    print('Exiting the room...')
