from enum import Enum

from morajai_solver.domain.colors import MoraColor

COLOR_HEX_MAP = {
    MoraColor.GREY: "#2B2B2B",
    MoraColor.WHITE: "#FFFFFF",
    MoraColor.BLACK: "#111111",
    MoraColor.RED: "#E53935",
    MoraColor.YELLOW: "#FFD700",
    MoraColor.PURPLE: "#8A2BE2",
    MoraColor.GREEN: "#2E7D32",
    MoraColor.PINK: "#FF69B4",
    MoraColor.ORANGE: "#FF8C00",
    MoraColor.BLUE: "#1E88E5",
}

HIGHLIGHT_MAP = {
    MoraColor.ORANGE: "#00FFFF",
    MoraColor.RED: "#00FFFF",
    MoraColor.GREEN: "#00FFFF",
    MoraColor.WHITE: "#FF007F",
    MoraColor.PINK: "#39FF14",
}


class UITheme(Enum):
    # Structures et Arrières-plans principaux
    BG_PANEL = "#1E1E1E"  # Fond des grands panneaux (Board, Controls, Solution)
    BG_CONSOLE = "#101010"  # Fond noir profond (Console de logs, Zones défilantes)
    BG_TILE_CONTAINER = "#1A1A1A"  # Fond pour la palette ou les lignes d'étapes

    # Bordures
    BORDER_DEFAULT = "#1E1E1E"  # Bordure par défaut des boutons de la grille
    BORDER_DARK = "#333333"  # Bordure de la palette
    BORDER_HIGHLIGHT = "#FFFFFF"  # Bordure blanche de sélection active

    # Boutons génériques et Configuration
    BTN_CONFIG_BG = "#3A3A3A"
    BTN_CONFIG_HOVER = "#4A4A4A"
    BTN_SELECT_SELECTED = "#1E88E5"
    BTN_SELECT_HOVER = "#1565C0"
    BTN_SOLVE_BG = "#2E7D32"
    BTN_SOLVE_HOVER = "#1B5E20"

    # États du pas-à-pas et Éléments de jeu
    STEP_SUCCESS_BG = "#1B5E20"  # Vert de validation
    STEP_ERROR_BG = "#421515"  # Fond rouge sombre d'erreur
    STEP_ERROR_BORDER = "#E53935"  # Bordure rouge d'erreur
    STEP_ACTIVE_BG = "#152535"  # Fond bleu nuit de l'étape active
    STEP_ACTIVE_BORDER = "#1E88E5"  # Bordure bleue de l'étape active
    STEP_NUMBER_BG = "#1E88E5"  # Fond du badge numérique des étapes

    # Bouton d'arrêt (Quit)
    BTN_QUIT_BG = "#D32F2F"
    BTN_QUIT_HOVER = "#B71C1C"

    # Textes spéciaux
    TEXT_CONSOLE = "#00FF00"  # Vert console rétro
    TEXT_MUTED = "#666666"  # Gris discret pour le placeholder
    TEXT_WHITE = "#FFFFFF"

    # Tile highlight
    DEFAULT_HIGHLIGHT = "#FF9800"


def get_highlight_color(color: MoraColor):
    return HIGHLIGHT_MAP.get(color, UITheme.DEFAULT_HIGHLIGHT.value)
