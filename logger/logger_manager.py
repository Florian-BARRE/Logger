from logger.logger_configs import PlacementConfig, LogLevelsConfig, MonitorConfig, LoggerConfig
from logger.colors import BaseColors, ClassicColors

from collections import defaultdict


class LoggerManager:
    enable_files_logs_monitoring_only_for_one_logger: bool = False
    enable_dynamic_config_update: bool = False
    enable_unique_logger_identifier: bool = False

    global_config: LoggerConfig = LoggerConfig()

    loggers = []

    __monitoring_logger_is_initialized: bool = False

    @classmethod
    def register_logger(cls, logger_instance):
        cls.loggers.append(logger_instance)

        if cls.enable_dynamic_config_update:
            cls._dynamic_update_global_config(logger_instance)

        if logger_instance.config.follow_logger_manager_rules:
            # on recurpere tous attributs si y'en a un qui est différent de celui de base on le garde sinon on met celui configuré par le logger manager
            default_logger_config_dict = LoggerConfig().get_attributes()
            new_logger_config_dict = logger_instance.config.get_attributes()

            for key, value in new_logger_config_dict.items():
                # Current logger have same value than the default one, LOGGER MANAGER CONFIG IS APPLIED
                if value != default_logger_config_dict.get(key, value):
                    setattr(logger_instance.config, key, getattr(cls.global_config, key))

        if cls.enable_unique_logger_identifier:
            cls._make_logger_identifier_unique()

        if cls.enable_files_logs_monitoring_only_for_one_logger:
            cls._unique_monitoring_logger(logger_instance)

    @classmethod
    def _dynamic_update_global_config(cls, new_logger_registered):
        # Ici on essaye de récupère une config global à partir de tous les loggers enregistréq

        # PlacementConfig -> on garde les plus grandes valeurs
        cls.global_config.placement_config.identifier_max_width = max(
            cls.global_config.placement_config.identifier_max_width,
            new_logger_registered.config.placement_config.identifier_max_width
        )
        cls.global_config.placement_config.level_max_width = max(
            cls.global_config.placement_config.level_max_width,
            new_logger_registered.config.placement_config.level_max_width
        )
        cls.global_config.placement_config.filename_lineno_max_width = max(
            cls.global_config.placement_config.filename_lineno_max_width,
            new_logger_registered.config.placement_config.filename_lineno_max_width
        )

    @classmethod
    def _make_logger_identifier_unique(cls):
        count_dict = defaultdict(int)
        occurrences = {
            logger.config.identifier: sum(
                1 for l in cls.loggers if l.config.identifier == logger.config.identifier
            )
            for logger in cls.loggers
        }
        renamed_loggers = []

        for logger in cls.loggers:
            identifier = logger.config.identifier
            count_dict[identifier] += 1

            if occurrences[identifier] > 1:
                new_identifier = f"{count_dict[identifier]}_{identifier}"
                logger.config.identifier = new_identifier  # Mise à jour de l'identifiant
                # Reset des formatters et handlers pour que les modifications soient prises en compte

                logger.set_print_handler(identifier=new_identifier)
                logger.set_file_handler(identifier=new_identifier)

            renamed_loggers.append(logger)

        cls.loggers = renamed_loggers

    @classmethod
    def _unique_monitoring_logger(cls, new_logger_registered):
        if new_logger_registered.config.monitor_config.is_monitoring_enabled():
            # desactive le monitoring pour tous les autres loggers
            if cls.__monitoring_logger_is_initialized:
                new_logger_registered.config.monitor_config.display_monitoring = False
                new_logger_registered.config.monitor_config.files_monitoring = False
            else:
                cls.__monitoring_logger_is_initialized = True
