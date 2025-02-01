# ====== Imports ======
# Standard library imports
from colorama import Fore, Back, Style

# Internal project imports
from logger.log_levels import LogLevels
from logger.colors.base import BaseColors


class DarkModeColors(BaseColors):
    """
    Dark mode theme with high contrast for readability.
    """
    LogLevelsColorsDict = {
        LogLevels.DEBUG: Style.DIM + Fore.LIGHTBLACK_EX,
        LogLevels.INFO: Style.RESET_ALL + Fore.CYAN,
        LogLevels.WARNING: Style.BRIGHT + Fore.LIGHTYELLOW_EX,
        LogLevels.ERROR: Style.BRIGHT + Fore.LIGHTRED_EX,
        LogLevels.CRITICAL: Style.BRIGHT + Fore.RED + Back.BLACK,
        LogLevels.FATAL: Style.BRIGHT + Back.RED + Fore.WHITE + BaseColors.BRIGHT,
    }

    DATE = Style.DIM + Fore.LIGHTWHITE_EX
    IDENTIFIER = Style.BRIGHT + Fore.LIGHTBLUE_EX
    FILENAME = Style.BRIGHT + Fore.LIGHTCYAN_EX
    LINENO = Style.BRIGHT + Fore.LIGHTMAGENTA_EX
    MESSAGE = Style.BRIGHT + Fore.WHITE
