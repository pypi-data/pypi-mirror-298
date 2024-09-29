"""Module to handle the player interaction in a room scene within the game.

The player is introduced to a dining room where they encounter mysterious diners
and are presented with a series of choices. The player can explore the room or
interact with the environment using simple commands. The outcome of the game can
change based on these interactions, and the player can eventually progress to the
endroom by selecting the correct command.
"""

import time
from pathlib import Path

from piedventure import lib

from . import endroom


def main(data_path: Path) -> None:
    """Introduce the player to a room scene and prompts for actions.

    The player steps into a dining room scene and interacts with other diners.
    The function provides a description of the room, and repeatedly prompts the player
    for commands to explore or perform actions in the room. Depending on the player's
    input, they can explore, interact with the environment, or proceed to the next
    section of the game by calling `endroom.main()`.

    Args:
        data_path (Path): Path to the game data, which will be passed to the
        endroom function if the player chooses to proceed.

    Returns:
        None

    """
    # Clear the terminal (works for most terminals)
    print('\033c', end='')

    # Initialise the Title Art
    lib.display_art('titleart.ben')

    # Introduction to the scene
    print('\n')
    time.sleep(1)
    print('You step through the door and into what looks like a scene from a movie.')
    time.sleep(3)
    print()
    print("There's a long table in front of you. Sat around it are several well-dressed")
    print('people, both men and women, eating a very elaborate looking dinner.')
    time.sleep(2)
    print('Weird.')
    time.sleep(3)
    print('\nThere appears to have been a place laid at the table for you.')
    time.sleep(5)
    print('\nSuddenly nervous, you take a seat and look around at the other diners.')
    print('Are these the people who summoned you here? You try to ask them, but')
    print('seem to be rendered more speechless than a test subject in a portal game.')
    time.sleep(5)
    print('\nA waiter brings out a tray and places it in front of you. Lifting the lid,')
    print(
        "you find a weird rainbow coloured pill in front of you. Very 'Matrix', you think",
    )
    print('to yourself. What does this mean? Are you supposed to take the pill?')
    print('Is this some kind of test? And who ARE these people?!')
    time.sleep(5)
    print()
    print('What would you like to do?')

    # Actions loop
    while True:
        nsewuh = input('> ').strip().lower()
        if nsewuh == 'n':
            print('You get up and look around. Not much over here.')
        elif nsewuh == 's':
            print("You take a look at the decor of the room. It's pretty nice.")
        elif nsewuh == 'e':
            print("There's a curtain - but no window behind it. How odd.")
        elif nsewuh == 'w':
            print('WHO ARE THESE PEOPLE?!')
        elif nsewuh == 'u':
            # Call the end.py script
            print('Going to the end...')
            endroom.main(data_path)
            break
        elif nsewuh == 'h':
            print("You hug the person next to you. He feels cold, and doesn't move.")
        else:
            print(
                "I'm sorry, I don't understand you. Commands are: n, e, s, w, u, and h.")

    print('Exiting the big room...')
