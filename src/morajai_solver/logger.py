"""
Configuration du système de log du script.
"""
import logging, sys

class ColorFormatter(logging.Formatter):
    """
    Formateur de logs appliquant des couleurs selon le niveau de sévérité.
    """
    # ANSI Codes
    GRAY = "\033[90m"
    CYAN = "\033[36m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    BOLD_RED = "\033[1;31m"
    RESET = "\033[0m"

    def __init__(self):
        """Constructeur du formateur"""
        super().__init__(datefmt="%H:%M:%S")
        # formatters pre-instancing
        self.formatters = {
            level: logging.Formatter(
                f"%(asctime)s | {color}%(levelname)-8s{self.RESET} | %(name)-30s | %(message)s",
                datefmt="%H:%M:%S"
            )
            for level, color in {
                logging.DEBUG: self.GRAY,
                logging.INFO: self.CYAN,
                logging.WARNING: self.YELLOW,
                logging.ERROR: self.RED,
                logging.CRITICAL: self.BOLD_RED
            }.items()
        }
        # default formatter
        self.default_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s", 
            datefmt="%H:%M:%S"
        )

    def format(self, record):
        """Sélectionne le formateur en fonction du niveau du message"""
        return self.formatters.get(record.levelno, self.default_formatter).format(record)

def get_logger(logger_level=logging.INFO, name=None):
    """
    Configure le logger racine de l'application.

    Args:
        logger_level (int): Niveau de log minimum souhaité (INFO par défaut)

    Returns:
        logging.Logger: l'instance du logger configurée

    Note:
        Désactive automatiquement les couleurs si la sortie standard
        n'est pas un terminal.
    """
    if name is None:
        logger = logging.getLogger()
    else:
        logger = logging.getLogger(name)
    # basic config does nothing if the logger already has handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)

    if sys.stdout.isatty():
        handler.setFormatter(ColorFormatter())
    else:
        # Format simple sans codes ANSI pour les fichiers .log
        plain_fmt = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
        handler.setFormatter(plain_fmt)

    logging.basicConfig(
        level=logger_level,
        handlers=[handler],
    )

    return logger