from logger import Logger, ClassicColors, LogLevels, DarkModeColors, NeonColors, PastelColors, CyberpunkColors, LoggerManager

LoggerManager.enable_files_logs_monitoring_only_for_one_logger = True
LoggerManager.enable_dynamic_config_update = True
LoggerManager.enable_unique_logger_identifier = True

loggers = [
    Logger(
        identifier="Main",
        decorator_log_level=LogLevels.DEBUG,
        print_log_level=LogLevels.DEBUG,
        file_log_level=LogLevels.DEBUG,
        print_log=True,
        write_to_file=True,
        colors=PastelColors,
        files_monitoring=True,
        display_monitoring=True,
    ),
    Logger(
        identifier="Main",
        decorator_log_level=LogLevels.DEBUG,
        print_log_level=LogLevels.DEBUG,
        file_log_level=LogLevels.DEBUG,
        print_log=True,
        write_to_file=True,
        colors=PastelColors,
        files_monitoring=True,
        display_monitoring=True,
    )
]

print("################")
for logger in loggers:
    print("-----------------------")
    logger.debug("Hello World")
    logger.info("Hello World")
    logger.warning("Hello World")
    logger.critical("Hello World")
    logger.fatal("Hello World")
