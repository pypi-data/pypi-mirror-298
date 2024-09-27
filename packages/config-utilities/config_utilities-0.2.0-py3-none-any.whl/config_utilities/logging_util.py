"""
logging_util.py

This module provides utilities for setting up and managing logging within a Python project.
It automatically locates the project's root directory, configures logging settings from a
`config.ini` file, and enables detailed function call logging if desired.

Key functionalities include:
- Locating the project root directory.
- Ensuring the existence of a configuration file and setting default logging configurations.
- Setting up logging based on the configuration settings.
- Decorating functions to automatically log their calls and results.

Usage:
    1. Place a `config.ini` file in your project's root directory. If the file doesn't exist,
       it will be created with default settings.
    2. Use `setup_logging` in your modules to initialize logging based on the configuration.
    3. Decorate functions with `@log_function_call` to automatically log their calls and outputs.

Example:
    from logging_util import setup_logging, log_function_call

    setup_logging('my_module')

    @log_function_call
    def my_function():
        pass
"""

# Standard Library Imports
import configparser
import os
import logging
import functools
from datetime import datetime
from typing import Optional, Tuple

# Global variable to control logging function calls
LOG_FUNCTION_CALLS: bool = True


def find_project_root(start_path: str,
                      markers: Tuple[str, ...] = ('config.ini', '.git', 'setup.py', 'requirements.txt')) -> str:
    """
    Find the project root by looking for specific marker files or directories.

    Args:
        start_path (str): The starting directory to begin searching from.
        markers (Tuple[str, ...]): A tuple of marker files or directories that signify the project root.

    Returns:
        str: The path to the project root directory.
    """
    current_path: str = start_path
    while current_path != os.path.dirname(current_path):  # Stop when reaching the filesystem root
        if any(os.path.exists(os.path.join(current_path, marker)) for marker in markers):
            return current_path
        current_path = os.path.dirname(current_path)
    return start_path  # Fallback to the start path if no marker was found


def setup_logging(module_name: str, config_path: Optional[str] = None) -> None:
    """
    Sets up logging configuration based on the provided config file.

    Args:
        module_name (str): Name of the module for logging purposes.
        config_path (Optional[str]): Path to the configuration file. If None, it tries to locate it automatically.

    Raises:
        ValueError: If the module name is not provided.
        FileNotFoundError: If the configuration file cannot be found.
        IOError: If there are issues with reading or writing the configuration file.
    """
    if not module_name:
        raise ValueError("module_name must be provided")

    # Ensure the config_path is resolved to an absolute path consistently
    if config_path is not None:
        config_path = os.path.abspath(config_path)

    # Load and validate configuration using config_manager
    from config_utilities.config_manager import load_and_validate_config  # Import within function to avoid circular dependencies
    config = load_and_validate_config(config_path)

    # Configure logging using the loaded configuration
    configure_logging(module_name, config)


def configure_logging(module_name: str, config: configparser.ConfigParser) -> None:
    """
    Configures the logging settings based on the configuration object.

    Args:
        module_name (str): Name of the module for logging purposes.
        config (configparser.ConfigParser): The configuration object containing logging settings.

    Raises:
        OSError: If there are issues with creating the log directory.
    """
    log_dir: str = config.get("Logging", "log_dir")
    log_override: bool = config.getboolean("Logging", "log_override")
    global LOG_FUNCTION_CALLS
    LOG_FUNCTION_CALLS = config.getboolean("Logging", "log_function_calls")
    use_global_log_level: bool = config.getboolean("Logging", "use_global_log_level", fallback=True)

    # Determine log level based on global settings
    log_level: str = config.get("log_level", "global_log_level", fallback="INFO").upper() if use_global_log_level else "INFO"

    log_format: str = config.get("Logging", "log_format", fallback="%(asctime)s - %(threadName)-10s - %(levelname)-8s - Line: %(lineno)4d - %(module)s - %(funcName)s - %(message)s")

    if log_level == 'NONE':
        logging.disable(logging.CRITICAL + 1)
        return

    try:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
    except OSError as e:
        raise OSError(f"Failed to create log directory {log_dir}: {e}")

    log_file, file_mode = determine_log_file(log_dir, module_name, log_override)

    file_handler = logging.FileHandler(log_file, mode=file_mode, encoding='utf-8')
    console_handler = logging.StreamHandler()

    reset_root_logger()

    logging_level = getattr(logging, log_level, logging.INFO)  # Default to INFO if not found

    logging.basicConfig(
        level=logging_level,
        format=log_format,  # Use the format from the config file
        handlers=[file_handler, console_handler]
    )

    logging.info("Logging setup complete.")
    logging.debug(f"Log file is set to: {log_file}")
    logging.debug(f"Final log level: {logging.getLevelName(logging.getLogger().level)}")
    logging.debug(f"Log function calls: {LOG_FUNCTION_CALLS}")


def determine_log_file(log_dir: str, module_name: str, log_override: bool) -> Tuple[str, str]:
    """
    Determines the log file path and mode based on configuration settings.

    Args:
        log_dir (str): Directory where logs should be stored.
        module_name (str): Name of the module for logging purposes.
        log_override (bool): Should the logging output overwrite the previous log file (i.e., start fresh)
                             or append to the existing log file.

    Returns:
        Tuple[str, str]: The log file path and file mode ('w' for write, 'a' for append).
    """
    if log_override:
        log_file = os.path.join(log_dir, f"{module_name}.log")
        file_mode = 'w'  # Overwrite mode
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"{module_name}_{timestamp}.log")
        file_mode = 'a'  # Append mode

    return log_file, file_mode


def reset_root_logger() -> None:
    """
    Clears all existing handlers from the root logger in Python's logging module.

    This function ensures that when logging is configured, it starts from a clean slate,
    preventing issues that can arise from duplicate or unwanted logging handlers, such
    as multiple log entries, inconsistent formatting, and performance degradation.
    """
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)


def log_function_call(func):
    """
    Decorator to log function call details - parameters and return values.
    It preserves the original function's name, docstring, and other attributes.

    Args:
        func: The function to be decorated.

    Returns:
        The wrapped function with logging.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if LOG_FUNCTION_CALLS:
            logging.debug(f"Entering {func.__name__}() with arguments: {args} and keyword arguments: {kwargs}")
        result = func(*args, **kwargs)
        if LOG_FUNCTION_CALLS:
            logging.debug(f"Exiting {func.__name__}() with result: {result}")
        return result

    return wrapper


@log_function_call
def main() -> None:
    """
    Main function demonstrating how to use the logging_util module.
    """
    setup_logging('logging_util')
    logger = logging.getLogger('logging_util')
    logger.info("This is a test log entry from the main function.")


if __name__ == "__main__":
    main()
