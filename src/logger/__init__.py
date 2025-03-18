from logging import Formatter, getLogger, Logger, StreamHandler, INFO, FileHandler, Handler
from logging.handlers import MemoryHandler
from typing import Optional

MEMORY_LOG_BUFFER_CAPACITY = 1_000_000

LOGGING_CONFIG_FILE = "src/logger/logging_config.json"

detailed_formatter = Formatter("%(asctime)s - %(name)s [%(levelname)s] %(message)s")
plain_formatter = Formatter("%(message)s")


def get_simulation_logger() -> Logger:
    formatter = detailed_formatter
    handler = get_console_handler(formatter)
    logger = getLogger("Simulation")
    logger.addHandler(handler)
    logger.setLevel(INFO)
    logger.propagate = False
    return logger


def get_controller_logger(log_file: Optional[str] = None) -> Logger:
    formatter = detailed_formatter
    handler = get_memory_file_handler(formatter, log_file) if log_file else get_console_handler(formatter)
    logger = getLogger("Controller")
    logger.addHandler(handler)
    logger.setLevel(INFO)
    logger.propagate = False
    return logger


def get_view_logger(log_file: Optional[str] = None) -> Logger:
    formatter = plain_formatter
    handler = get_memory_file_handler(formatter, log_file) if log_file else get_console_handler(formatter)
    logger = getLogger("View")
    logger.addHandler(handler)
    logger.setLevel(INFO)
    logger.propagate = False
    return logger


def get_default_logger(logger_name: str) -> Logger:
    formatter = detailed_formatter
    handler = get_console_handler(formatter)
    logger = getLogger(logger_name)
    logger.addHandler(handler)
    logger.setLevel(INFO)
    logger.propagate = False
    return logger


def get_console_handler(formatter: Formatter) -> StreamHandler:
    console_handler = StreamHandler()
    console_handler.setFormatter(formatter)
    return console_handler


def get_memory_file_handler(formatter: Formatter, file_name: str, ) -> MemoryHandler:
    file_handler = get_file_handler(formatter, file_name)
    return get_memory_handler(target=file_handler, formatter=formatter)


def get_file_handler(formatter: Formatter, file_name: str) -> FileHandler:
    file_handler = FileHandler(file_name)
    file_handler.setFormatter(formatter)
    return file_handler


def get_memory_handler(target: Handler, formatter: Formatter) -> MemoryHandler:
    memory_handler = MemoryHandler(capacity=MEMORY_LOG_BUFFER_CAPACITY, target=target)
    memory_handler.setFormatter(formatter)
    return memory_handler
