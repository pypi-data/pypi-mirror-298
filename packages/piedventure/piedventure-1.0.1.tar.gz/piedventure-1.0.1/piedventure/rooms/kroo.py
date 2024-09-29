"""Module to simulate a corridor scene in a game.

The player interacts with
a mysterious setting after hugging a statue that transports them to an unknown location.

The player can navigate between various rooms (east, west, and south) or perform
different actions, all while advancing the game's storyline in a surreal environment.
"""

import time
from pathlib import Path

from piedventure import lib

from . import bigroom, gameroom, grue


def main(data_path: Path) -> None:
    """Handle the player's interactions within the corridor scene.

    After hugging a kitten statue, the player finds themselves in a small corridor
    with glowing rooms to the east and west, and a large door to the south. This function
    allows the player to navigate by entering directional commands or attempting to
    interact with their surroundings. Depending on the input, the player may be
    transported to different rooms (bigroom, gameroom, or grue).

    Args:
        data_path (Path): Path to the game data, used to maintain or modify game state.

    Returns:
        None

    """
    # Clear the terminal (works for most terminals)
    print('\033c', end='')

    # Initialise the Title Art
    lib.display_art('titleart.ben')
    print('\n')

    # Room description
    time.sleep(1)
    print('What. The. Actual. Fuck.')
    print()
    time.sleep(3)
    print('You hugged a statue of a beautiful kitten. As you do.')
    print()
    print("But you weren't expecting it to come to life and transport")
    print('you to another mystery room. This is getting a bit weird.')
    print()
    print('You now seem to find yourself in a small-ish corridor. You can')
    print('see a glow coming from the rooms to your east and west, and')
    print("there's a big, old looking door south of you.")
    print()
    print('What would you like to do?')

    # Room logic
    while True:
        nsewuh = input('> ').strip().lower()  # Read user input and normalize
        if nsewuh == 'n':
            print('You faceplant the wall. Idiot.')
        elif nsewuh == 's':
            bigroom.main(data_path)
            break
        elif nsewuh == 'e':
            gameroom.main(data_path)
            break
        elif nsewuh == 'w':
            grue.main(data_path)
            break
        elif nsewuh == 'u':
            print("There's nothing you can use right here.")
        elif nsewuh == 'h':
            print("After hugging that cat you aren't sure"
                  ' you should try to hug yourself again.')
        else:
            print(
                "I'm sorry, I don't understand you. Commands are: n, e, s, w, u, and h.")

    # Exit script
