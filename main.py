from logger import Logger, ClassicColors, LogLevels, DarkModeColors, NeonColors, PastelColors, CyberpunkColors, \
    LoggerManager
from logger import time_tracker

LoggerManager.enable_files_logs_monitoring_only_for_one_logger = True
LoggerManager.enable_dynamic_config_update = False
LoggerManager.enable_unique_logger_identifier = False

loggers_list = [
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


@time_tracker(param_logger="Tracker")
def run_logger(loggers, interations=1000):
    for i in range(interations):
        for logger in loggers:
            print("-----------------------")
            logger.debug(f"Hello World {i}")
            logger.info(f"Hello World {i}")
            logger.warning(f"Hello World {i}")
            logger.critical(f"Hello World {i}")
            logger.fatal(f"Hello World {i}")
@time_tracker(param_logger="Tracker")
def test():
    pass




run_logger(loggers_list)
test()

from logger.analyser import LogAnalyser

analyser = LogAnalyser("logs/2025-02-01.log")
analyser.analyse_time_tracker()
