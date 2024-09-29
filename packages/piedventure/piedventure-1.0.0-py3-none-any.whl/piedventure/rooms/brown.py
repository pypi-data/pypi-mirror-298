"""Module to simulate a player's interaction within a dimly lit, eerie room.

The player enters a room with a lever on the wall and an exit leading back north.
The function narrates the scene and allows the player to perform actions such as
moving, interacting with the lever, and giving humorous commands. Depending on the
state of the lever, the player can turn it on or be notified if it's already on.
"""

import time
from pathlib import Path

from piedventure import lib

from . import mainroom


def main(data_path: Path) -> None:
    """Introduce the player to a dim room with a lever and prompts for actions.

    The player steps into a room with a retro-style carpet and a lever on the wall.
    The function describes the room and checks the state of the lever (on or off).
    The player can interact with the environment by issuing commands to move or manipulate
    the lever. Depending on the player's input, they can either return to the main room,
    toggle the lever, or perform humorous non-actions.

    Args:
        data_path (Path): Path to the game data, which is used to check or change the
        lever state and passed to the mainroom function when returning.

    Returns:
        None

    """
    # Clear the terminal (works for most terminals)
    print('\033c', end='')

    # Initialise the Title Art
    lib.display_art('titleart.ben')
    print()

    time.sleep(1)

    # Room description
    print('You run south and through an open archway into a dark, dingy place.')
    print('The carpet looks like the 70s threw up on it, and the place smells faintly')
    print('of cabbage. This could well be every retirement home ever made, combined')
    print("into one place. It's tragic.")
    print()
    print("Oddly, though, there's a lever set into the right hand wall.")

    # Check the lever state
    leverstate = lib.get_leverstate(data_path)
    if leverstate == 'on':
        print(
            "The last time you were in this room, you turned the lever on. It's still on.",
        )
    else:
        print(f"It looks like it's in the {leverstate} position.")

    print()
    print('The only exit is north, back the way you came.')
    print()
    print('What would you like to do?')

    # Actions loop
    while True:
        nsewuh = input('> ').strip().lower()
        if nsewuh == 'n':
            # Call the mainroom.py script
            print('Going back to the main room...')
            mainroom.main(data_path)
            break
        if nsewuh == 's':
            print('You attempt to walk through the wall. You fail.')
        elif nsewuh == 'e':
            print("Right, let me explain this whole 'wall' thing to you...")
        elif nsewuh == 'w':
            print("Seriously? Through the wall? Sorry, I can't do that.")
        elif nsewuh == 'u':
            # Check the lever state again
            leverstate = lib.get_leverstate(data_path)
            if leverstate == 'on':
                print('Having already turned it on, you try to turn it off. And fail.')
            else:
                # Change the lever state from off to on
                lib.set_leverstate(data_path, 'on')
                print("You push the lever to 'on',"
                      ' and hear a humming start elsewhere in the building.')
        elif nsewuh == 'h':
            print('You hug yourself, and hope nobody is watching.')
        else:
            print(
                "I'm sorry, I don't understand you. Commands are: n, e, s, w, u, and h.")

    print('Exiting the room...')
