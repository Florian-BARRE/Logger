from logger import LoggerConfig, LogLevels

from logger.logger_configs import LogLevelsConfig, PlacementConfig, MonitorConfig

log_level_config = LogLevelsConfig.info()
placement_config = PlacementConfig.from_kwargs(
    identifier_max_width=10000,decorator_log_level=LogLevels.FATAL,
)

print(log_level_config)
print(placement_config)

config = LoggerConfig.from_kwargs(
    identifier_max_width=999,
    decorator_log_level=LogLevels.FATAL,

)

print(config.get_attributes())


print()