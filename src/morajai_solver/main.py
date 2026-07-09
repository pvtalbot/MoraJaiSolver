import argparse
import logging

from morajai_solver.logger import configure_logging
from morajai_solver.core.game_engine import GameEngine
from morajai_solver.gui import launch_gui

import sys
import os

if sys.stdout is None:
    sys.stdout = open(os.devnull, 'w')
if sys.stderr is None:
    sys.stderr = open(os.devnull, 'w')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        default=False,
        help="Réduit le niveau de logs",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Augmente le niveau de logs",
    )

    args = parser.parse_args()
    if args.quiet:
        configure_logging(logger_level=logging.WARNING)
    elif args.verbose:
        configure_logging(logger_level=logging.DEBUG)
    else:
        configure_logging(logger_level=logging.INFO)

    GameEngine()
    launch_gui()


if __name__ == "__main__":
    main()
