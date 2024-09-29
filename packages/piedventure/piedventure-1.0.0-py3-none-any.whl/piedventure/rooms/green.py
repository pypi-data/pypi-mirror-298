"""Module to simulate a room within a game where the player is overwhelmed by a green environment.

The player is presented with various choices to interact with the room and can eventually
leave the room by moving east, triggering the transition to another scene (mainroom).
The green room provides a humorous, surreal atmosphere as part of the game's narrative.
"""

import time
from pathlib import Path

from piedventure import lib

from . import mainroom


def main(data_path: Path) -> None:
    """Run the interaction in the green room of the game.

    The player enters a green room that is humorously described as overwhelmingly
    green. The player can explore the room by entering different commands
    (north, south, east, west, up, hug), each of which triggers a unique description
    or action. If the player chooses to move east, the function transitions to
    the 'mainroom'.

    Args:
        data_path (Path): Path to the game data, which is used to pass to other
        functions or modules that manage game states.

    Returns:
        None

    """
    # Clear the terminal (works for most terminals)
    print('\033c', end='')

    # Initialise the Title Art
    lib.display_art('titleart.ben')

    # Room description
    print('\n')
    time.sleep(1)
    print("You're off to see the wizard. Well, maybe not - but this")
    print('room is so green you might as well be in Emerald City.')
    print("Seriously. Think of the greenest thing you've ever seen,")
    print("then add another suitcase full of green. It's that bad.")
    print("\nIt's getting to you. Such pain. Is there a door? Who knows.")
    print('\nWhat would you like to do?')

    # Actions loop
    while True:
        nsewuh = input('> ').strip().lower()
        if nsewuh == 'n':
            print('The green is a bit more intense over here. Oops.')
        elif nsewuh == 's':
            print('Such green. Much bad. Go back. SCHTAP.')
        elif nsewuh == 'e':
            # Call mainroom.py
            mainroom.main(data_path)
            break  # Exit the loop after the call
        elif nsewuh == 'w':
            print('You attempt to go west, but ALL YOU SEE IS GREEN.')
        elif nsewuh == 'u':
            print("You think about 'using' green, "
                  "but realise it's not legal in this country.")
        elif nsewuh == 'h':
            print('You curl yourself up into a ball and rock back and forth.')
        else:
            print(
                "I'm sorry, I don't understand you. Commands are: n, e, s, w, u, and h.")
