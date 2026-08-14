import argparse
import logging

from morajai_solver.domain.game_engine import GameEngine
from morajai_solver.infra.event_dispatcher import EventDispatcher
from morajai_solver.infra.logger import configure_logging
from morajai_solver.ui.gui import launch_gui


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

    ui_bus = EventDispatcher()

    GameEngine(ui_bus=ui_bus)
    app = launch_gui(ui_bus=ui_bus)
    ui_bus.configure_ctk_root(app)

    app.mainloop()


if __name__ == "__main__":
    main()
