# ====== Code Summary ======
# This module enhances Python's built-in logging by adding a distinct 'FATAL' log level,
# improving log formatting, and enabling color-coded log messages for better readability.
# It provides a custom Logger class that supports console and file logging with adjustable
# color settings, ensuring clear and structured log outputs.
#
# Additionally, the logger includes a monitoring system that automatically deletes
# excessive logs to prevent overflow, displays the remaining disk space, and offers
# various practical features for efficient log management.


# ====== Imports ======
# Standard library imports
import datetime
import logging
import sys

# Third-party library imports
from colorama import just_fix_windows_console

# Internal project imports
from logger.log_levels import LogLevels
from logger.monitoring import DiskMonitor
from logger.formatter import Formatter
from logger.colors import BaseColors
from logger.logger_configs import LoggerConfig
from logger.logger_manager import LoggerManager

# ====== Initialize Console for Colors ======
just_fix_windows_console()  # Enables colors in windows consoles (why not)

# ====== Modification of Native Logging Behavior ======
# Python's logging module treats 'CRITICAL' and 'FATAL' as synonyms.
# To distinguish 'FATAL' as a unique severity level, we manually add it.
logging.addLevelName(LogLevels.FATAL, "FATAL")


# Define a method for the Logger class to log messages at 'FATAL' level.
def class_fatal(self, msg, *args, **kwargs):
    """
    Log 'msg % args' with severity 'FATAL'.

    To pass exception information, use the keyword argument exc_info with
    a true value, e.g.

    This allows using `logger.fatal()` as a distinct logging level.

    logger.fatal("Houston, we have one %s", "major disaster", exc_info=True)

    Args:
        msg (str): The message to log.
    """
    if self.isEnabledFor(LogLevels.FATAL):
        self._log(LogLevels.FATAL, msg, args, **kwargs)


# Attach the new 'fatal' method to the logging.Logger class.
logging.Logger.fatal = class_fatal


# Define a global function to log fatal messages using the root logger.
def fatal(msg, *args, **kwargs):
    """
    Log a message with severity 'CRITICAL' on the root logger. If the logger
    has no handlers, call basicConfig() to add a console handler with a
    pre-defined format.
    """
    if len(logging.root.handlers) == 0:
        logging.basicConfig()
    logging.root.critical(msg, *args, **kwargs)


# ====== Logger Class ======
class Logger:
    """
        Custom Logger class that extends Python's built-in logging functionality.
        Supports console and file logging with customizable settings, including colored
        output for improved readability in terminals.
    """

    def __init__(self, **kwargs):
        """
        Initialize the logger with customizable parameters.

        Supports:
        - Full dictionary configuration
        - Partial updates of specific configurations
        - Directly passing configuration objects (LogLevelsConfig, PlacementConfig, etc.)
        """

        # Convert kwargs into LoggerConfig instance
        if isinstance(kwargs.get("config"), LoggerConfig):
            self.config: LoggerConfig = kwargs["config"]
        else:
            self.config: LoggerConfig = LoggerConfig.from_kwargs(**kwargs)

        # Register the logger with the LoggerManager
        LoggerManager.register_logger(self)

        # Initialize the logger
        self.__post_init__()

    def __post_init__(self):
        # If already exists we just have to get the logger instance
        # (the formatter and handlers are already set) so we will skip their steps
        already_exists = self.config.identifier in logging.root.manager.loggerDict

        self.logger: logging.Logger = logging.getLogger(self.config.identifier)
        self.logger.setLevel(LogLevels.DEBUG)  # Set the logger's level to the lowest level (DEBUG)

        if self.config.monitor_config.is_monitoring_enabled():
            self.disk_monitor = DiskMonitor(
                logger=self,
                directory=self.config.path,
                config=self.config.monitor_config
            )

        # Console logging setup / File logging setup
        if not already_exists:
            self.set_print_handler()
            self.set_file_handler()

        # Map log levels to logger methods
        self.log_level_to_logger_function = {
            LogLevels.FATAL: self.logger.fatal,
            LogLevels.CRITICAL: self.logger.critical,
            LogLevels.ERROR: self.logger.error,
            LogLevels.WARNING: self.logger.warning,
            LogLevels.INFO: self.logger.info,
            LogLevels.DEBUG: self.logger.debug,
        }

        # Display information about disk usage and log files
        if self.config.monitor_config.display_monitoring and not already_exists:
            self.disk_monitor.display_monitoring()
        if self.config.monitor_config.files_monitoring and not already_exists:
            self.disk_monitor.clean_logs()

    def set_print_handler(
            self,
            identifier: str = None,
            identifier_max_width: int = None,
            filename_lineno_max_width: int = None,
            level_max_width: int = None,
            colors: type[BaseColors] = None
    ):
        if self.config.log_levels_config.print_log:
            # Update config from parameters if provided
            self.config.identifier = self.config.identifier if identifier is None else identifier
            self.config.placement_config.placement_improvement = self.config.placement_config.placement_improvement if identifier_max_width is None else identifier_max_width
            self.config.placement_config.filename_lineno_max_width = self.config.placement_config.filename_lineno_max_width if filename_lineno_max_width is None else filename_lineno_max_width
            self.config.placement_config.level_max_width = self.config.placement_config.level_max_width if level_max_width is None else level_max_width
            self.config.colors = self.config.colors if colors is None else colors

            # If the logger is already set, we don't need to set the formatter and handler again
            if getattr(self, "logger", None) is None:
                return

            self.print_formatter: Formatter = Formatter(
                identifier=self.config.identifier,
                identifier_max_width=self.config.placement_config.placement_improvement,
                filename_lineno_max_width=self.config.placement_config.filename_lineno_max_width,
                level_max_width=self.config.placement_config.level_max_width,
                colors=self.config.colors,
            )

            # Vérifier si un FileHandler existe déjà
            print_handler = None
            for handler in self.logger.handlers:
                if isinstance(handler, logging.StreamHandler):
                    print_handler = handler
                    break

            if print_handler:
                # Mettre à jour uniquement le formatter
                print_handler.setFormatter(self.print_formatter)
            else:
                # Ajouter un nouveau handler
                print_handler = logging.StreamHandler(stream=sys.stdout)
                print_handler.setLevel(self.config.log_levels_config.print_log_level)
                print_handler.setFormatter(self.print_formatter)
                self.logger.addHandler(print_handler)

    def set_file_handler(
            self,
            identifier: str = None,
            identifier_max_width: int = None,
            filename_lineno_max_width: int = None,
            level_max_width: int = None
    ):
        if self.config.log_levels_config.write_to_file:
            # Update config from parameters if provided
            self.config.identifier = self.config.identifier if identifier is None else identifier
            self.config.placement_config.placement_improvement = self.config.placement_config.placement_improvement if identifier_max_width is None else identifier_max_width
            self.config.placement_config.filename_lineno_max_width = self.config.placement_config.filename_lineno_max_width if filename_lineno_max_width is None else filename_lineno_max_width
            self.config.placement_config.level_max_width = self.config.placement_config.level_max_width if level_max_width is None else level_max_width

            # If the logger is already set, we don't need to set the formatter and handler again
            if getattr(self, "logger", None) is None:
                return

            self.file_formatter: Formatter = Formatter(
                identifier=self.config.identifier,
                identifier_max_width=self.config.placement_config.placement_improvement,
                filename_lineno_max_width=self.config.placement_config.filename_lineno_max_width,
                level_max_width=self.config.placement_config.level_max_width,
                colors=None,
            )

            # Vérifier si un FileHandler existe déjà
            file_handler = None
            for handler in self.logger.handlers:
                if isinstance(handler, logging.FileHandler):
                    file_handler = handler
                    break

            if file_handler:
                # Mettre à jour uniquement le formatter
                file_handler.setFormatter(self.file_formatter)
            else:
                # Ajouter un nouveau handler
                file_handler = logging.FileHandler(filename=self.config.path)
                file_handler.setLevel(self.config.log_levels_config.file_log_level)
                file_handler.setFormatter(self.file_formatter)
                self.logger.addHandler(file_handler)

    # ====== Logging Methods ======
    def log(self, msg: str, level: LogLevels) -> None:
        """ Logs a message at the specified log level. """
        self.log_level_to_logger_function.get(
            level,
            lambda bind_msg, stack_level: self.logger.warning(
                msg=f"Invalid log level [log message: {bind_msg}]", stacklevel=stack_level
            ),
        )(msg, 2)

    def fatal(self, msg: str) -> None:
        """ Logs a fatal message. """
        # 3 because the logging library doesn't support the 'fatal' level natively so I have added it manually
        # (this added 1 to depth level)
        self.logger.fatal(msg, stacklevel=3)

    def critical(self, msg: str) -> None:
        """ Logs a critical message. """
        self.logger.critical(msg, stacklevel=2)

    def error(self, msg: str) -> None:
        """ Logs an error message. """
        self.logger.error(msg, stacklevel=2)

    def warning(self, msg: str) -> None:
        """ Logs a warning message. """
        self.logger.warning(msg, stacklevel=2)

    def info(self, msg: str) -> None:
        """ Logs an informational message. """
        self.logger.info(msg, stacklevel=2)

    def debug(self, msg: str) -> None:
        """ Logs a debug message. """
        self.logger.debug(msg, stacklevel=2)
