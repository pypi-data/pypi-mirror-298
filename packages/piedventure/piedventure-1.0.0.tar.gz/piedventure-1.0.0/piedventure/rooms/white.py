"""Module to represent the White Room within the game.

In this room, the player
can interact with a statue of a kitten and navigate back to the main room.
The player is also able to check the state of a lever that influences the
environment and their interactions.

The player can issue commands to navigate or interact with the statue.
"""

import time
from pathlib import Path

from piedventure import lib

from . import kroo, mainroom


def main(data_path: Path) -> None:
    """Handle player interactions within the White Room.

    The player enters the White Room and is greeted by its brightness. They can
    interact with a statue of a kitten, check the state of a lever, and navigate
    back to the main room. The function processes user input for navigation and
    actions within this room.

    Args:
        data_path (Path): Path to the game data, which is used for maintaining
                          or modifying game state.

    Returns:
        None

    """
    # Clear the terminal (works for most terminals)
    print('\033c', end='')

    # Initialise the Title Art
    lib.display_art('titleart.ben')
    print()

    # Setting up the room...
    time.sleep(1)
    print('You run north, pushing through the half-open doorway ahead.')
    print('The room you find yourself in is bright. A sign on the wall tells')
    print("you that you are in the White Room. I guess that explains why it's")
    print('so bright and all that...')
    print()

    # Check the lever state
    leverstate = lib.get_leverstate(data_path)
    if leverstate == 'on':
        print("There's a delicately carved statue at the end of the room.")
        print("It's a kitten, hewn from beautiful white marble.")
        print('It is also emitting a strange humming noise.')
    else:
        print("There's a delicately carved statue at the end of the room.")
        print("It's a kitten, hewn from beautiful white marble.")

    print()
    print('The only exit is south, back the way you came.')
    print()
    print('What would you like to do?')

    # Capture this room's actions
    while True:
        nsewuh = input('> ').strip().lower()
        if nsewuh == 'n':
            print("Somehow you think walls don't apply to you. They do.")
        elif nsewuh == 's':
            # Call the mainroom.py script
            print('Going back to the main room...')
            mainroom.main(data_path)
            break
        elif nsewuh == 'e':
            print("No can do. There's a wall there.")
        elif nsewuh == 'w':
            print("Seriously? Through the wall? Sorry, I can't do that.")
        elif nsewuh == 'u':
            print('You try to use the statue. It feels weird, so you stop.')
        elif nsewuh == 'h':
            if leverstate == 'on':
                kroo.main(data_path)
                break
            print('You hug the statue. It seems to vibrate a little. Weird.')
        else:
            print(
                "I'm sorry, I don't understand you. Commands are: n, e, s, w, u, and h.")

    print('Exiting...')
