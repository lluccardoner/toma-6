from enum import StrEnum, auto
from logging import Formatter, getLogger, Logger, StreamHandler, INFO, FileHandler, ERROR, Handler
from logging.handlers import MemoryHandler
from typing import Optional

MEMORY_LOG_BUFFER_CAPACITY = 1_000_000

LOGGING_CONFIG_FILE = "src/logger/logging_config.json"

detailed_formatter = Formatter("%(asctime)s - %(name)s [%(levelname)s] %(message)s")
plain_formatter = Formatter("%(message)s")

memory_file_handlers = {}


class LoggingMode(StrEnum):
    TO_CONSOLE_SILENT = auto()  # Console ERROR log level
    TO_CONSOLE_VERBOSE = auto()  # Console INFO log level
    TO_FILE_SILENT = auto()  # File ERROR log level
    TO_FILE_VERBOSE = auto()  # File INFO log level


def get_controller_logger_by_mode(logging_mode: LoggingMode, logger_file: Optional[str] = None) -> Logger:
    return _get_logger_by_mode(logging_mode, logger_file, get_controller_logger)


def get_view_logger_by_mode(logging_mode: LoggingMode, logger_file: Optional[str] = None) -> Logger:
    return _get_logger_by_mode(logging_mode, logger_file, get_view_logger)


def _get_logger_by_mode(
        logging_mode: LoggingMode,
        logger_file: Optional[str],
        logger_getter_fn
) -> Logger:
    config_map = {
        LoggingMode.TO_CONSOLE_SILENT: (ERROR, None),
        LoggingMode.TO_CONSOLE_VERBOSE: (INFO, None),
        LoggingMode.TO_FILE_SILENT: (ERROR, logger_file),
        LoggingMode.TO_FILE_VERBOSE: (INFO, logger_file),
    }

    log_level, log_file = config_map[logging_mode]

    # Ensure that file logging modes have a valid logger_file
    if logging_mode in (LoggingMode.TO_FILE_SILENT, LoggingMode.TO_FILE_VERBOSE) and not logger_file:
        raise ValueError(f"Logger file path is required for {logging_mode} mode")

    return logger_getter_fn(log_level=log_level, log_file=log_file)


def get_simulation_logger() -> Logger:
    formatter = detailed_formatter
    handler = get_console_handler(formatter)
    logger = getLogger("Simulation")
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(handler)
    logger.setLevel(INFO)
    logger.propagate = False
    return logger


def get_controller_logger(log_level: int = INFO, log_file: Optional[str] = None) -> Logger:
    formatter = plain_formatter if log_file else detailed_formatter
    handler = get_memory_file_handler(formatter, log_file) if log_file else get_console_handler(formatter)
    logger = getLogger("Controller")
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(handler)
    logger.setLevel(log_level)
    logger.propagate = False
    return logger


def get_view_logger(log_level: int = INFO, log_file: Optional[str] = None) -> Logger:
    formatter = plain_formatter
    handler = get_memory_file_handler(formatter, log_file) if log_file else get_console_handler(formatter)
    logger = getLogger("View")
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(handler)
    logger.setLevel(log_level)
    logger.propagate = False
    return logger


def get_default_logger(logger_name: str) -> Logger:
    formatter = detailed_formatter
    handler = get_console_handler(formatter)
    logger = getLogger(logger_name)
    if logger.hasHandlers():
        return logger  # Already initialised
    logger.addHandler(handler)
    logger.setLevel(INFO)
    logger.propagate = False
    return logger


def get_console_handler(formatter: Formatter) -> StreamHandler:
    console_handler = StreamHandler()
    console_handler.setFormatter(formatter)
    return console_handler


def get_memory_file_handler(formatter: Formatter, file_name: str, ) -> MemoryHandler:
    if file_name in memory_file_handlers:
        # Reuse memory handler for the same file
        return memory_file_handlers[file_name]
    # Note that formatter will be the same for all loggers that use this handler
    file_handler = get_file_handler(formatter, file_name)
    memory_file_handler = get_memory_handler(target=file_handler)
    memory_file_handlers[file_name] = memory_file_handler
    return memory_file_handler


def get_file_handler(formatter: Formatter, file_name: str) -> FileHandler:
    file_handler = FileHandler(file_name)
    file_handler.setFormatter(formatter)
    return file_handler


def get_memory_handler(target: Handler) -> MemoryHandler:
    memory_handler = MemoryHandler(capacity=MEMORY_LOG_BUFFER_CAPACITY, target=target)
    return memory_handler
