# ====== Imports ======
# Standard library imports
from colorama import Fore, Back, Style

# Internal project imports
from logger.log_levels import LogLevels
from logger.colors.base import BaseColors


class ClassicColors(BaseColors):
    """
    Classic color theme for logs.
    """
    LogLevelsColorsDict = {
        LogLevels.DEBUG: Style.RESET_ALL + Fore.BLUE,
        LogLevels.INFO: Style.RESET_ALL + Back.BLUE,
        LogLevels.WARNING: Style.RESET_ALL + Back.YELLOW,
        LogLevels.ERROR: Style.RESET_ALL + Back.RED,
        LogLevels.CRITICAL: Style.RESET_ALL + Back.RED + Fore.YELLOW,
        LogLevels.FATAL: Style.BRIGHT + Back.RED + Fore.WHITE + BaseColors.BRIGHT,
    }

    DATE = Style.RESET_ALL + Fore.YELLOW
    IDENTIFIER = Style.RESET_ALL + Style.BRIGHT + Fore.LIGHTGREEN_EX
    FILENAME = Style.RESET_ALL + Fore.LIGHTCYAN_EX
    LINENO = Style.RESET_ALL + Fore.LIGHTMAGENTA_EX
    MESSAGE = ""
