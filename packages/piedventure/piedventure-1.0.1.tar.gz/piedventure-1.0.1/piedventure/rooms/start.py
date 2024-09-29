"""Module to start the adventure game.

This module contains the game introduction and navigation logic for
the initial room and other areas.
"""

import time
from pathlib import Path

from piedventure import lib

from . import brown, green, red, white


def game_intro() -> None:
    """Display the game introduction with title art and an opening script."""
    print('Loading introduction...')
    lib.display_art('titleart.ben')
    time.sleep(5)
    lib.display_script('opening.ben')
    input('Press [ENTER] to start...')
    print('\033[H\033[J')  # Clear screen


def start_room() -> None:
    """Display the initial room's description."""
    lib.display_art('titleart.ben')
    time.sleep(1)
    print()
    print('You awake to find yourself on the floor of a large room.')
    print('You still have your pillow, but your bed and duvet are gone.')
    print('You stand up, dazed and confused. '
          "It's a Thursday, or - at least - you think it is.")
    print('You never could quite get the hang of Thursdays.')
    print()
    print('You can just about see doors to the north, east, south, and west.')
    print("It's kinda cold, and you're hungry.")
    print()


def navigate_rooms(data_path: Path) -> None:
    """Handle player navigation between rooms based on player input.

    Args:
        data_path (Path): Path to the data file for game state.

    """
    while True:
        choice = input('> ').strip().lower()

        if choice == 'n':
            white.main(data_path)
            break
        elif choice == 's':
            brown.main(data_path)
            break
        elif choice == 'e':
            red.main(data_path)
            break
        elif choice == 'w':
            green.main(data_path)
            break
        elif choice == 'u':
            print("There's nothing you can use right here.")
        elif choice == 'h':
            print("You give yourself a quick hug. It's not very satisfying.")
        else:
            print("I'm sorry, I don't understand you. "
                  "Commands are: n, e, s, w, u, and h.")


def main(data_path: Path) -> None:
    """Start the game and manage navigation.

    Resets game state, shows the introduction, and initiates the room navigation.

    Args:
        data_path (Path): Path to the data file for game state.

    """
    lib.reset_logic(data_path)
    game_intro()
    start_room()
    navigate_rooms(data_path)
