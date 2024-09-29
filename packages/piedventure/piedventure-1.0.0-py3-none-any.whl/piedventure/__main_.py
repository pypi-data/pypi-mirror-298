"""Entry point for the adventure module.

This script serves as the main entry point when the package is executed as
a standalone program. It imports the main function from the adventure
module and invokes it, initiating the game's execution.
"""

if __name__ == '__main__':
    from .adventure import main

    main()
