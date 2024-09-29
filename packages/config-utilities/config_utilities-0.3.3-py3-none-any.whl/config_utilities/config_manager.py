"""
config_manager.py

This module provides a centralized and consistent way to manage configuration files for your Python application.
It handles locating the project root, ensuring that a configuration file exists, and populating it with default
values if necessary. The module also validates the presence of required configuration sections, such as those
for logging.

Key functionalities include:
- Finding the project root directory by searching for specific marker files or directories.
- Ensuring the configuration file exists, creating it with default values if it does not.
- Setting default configuration values for logging settings.
- Loading and validating the configuration, ensuring it is ready for use in the application.

Example usage:
    from config_manager import load_and_validate_config

    config = load_and_validate_config()
    log_dir = config.get('Logging', 'log_dir')
    global_log_level = config.get('log_level', 'global_log_level')

This module is essential for maintaining consistent configuration management across different parts of your application.
"""

import os
import configparser
import logging
from typing import Optional, Tuple, List

# Global variables to track the first configuration path and control logging function calls
FIRST_CONFIG_PATH: Optional[str] = None

# Global variable to store the primary configuration loaded at the start
PRIMARY_CONFIG: Optional[configparser.ConfigParser] = None


def save_config(config: configparser.ConfigParser, config_path: str) -> None:
    """
    Save the configuration to the specified file path.

    Args:
        config (configparser.ConfigParser): The configuration object to save.
        config_path (str): The path to the configuration file.

    Raises:
        IOError: If the configuration file cannot be written to.
    """
    try:
        with open(config_path, 'w') as configfile:
            config.write(configfile)
        logging.info(f"Configuration saved to {config_path}")
    except IOError as e:
        raise IOError(f"Failed to write to the configuration file at {config_path}: {e}")


def find_project_root(start_path: str,
                      markers: Tuple[str, ...] = ('config.ini', '.git', 'setup.py', 'requirements.txt')) -> str:
    """
    Find the project root directory by searching for specific marker files or directories.

    Args:
        start_path (str): The directory path to start searching from.
        markers (Tuple[str, ...]): A tuple of marker file or directory names to identify the project root.

    Returns:
        str: The path to the project root directory if found, otherwise the original start path.
    """
    current_path: str = start_path
    while current_path != os.path.dirname(current_path):
        if any(os.path.exists(os.path.join(current_path, marker)) for marker in markers):
            return current_path
        current_path = os.path.dirname(current_path)
    return start_path


def ensure_config_exists(config_path: str) -> configparser.ConfigParser:
    """
    Ensure the configuration file exists at the specified path, creating a default one if necessary.

    Args:
        config_path (str): The path to the configuration file.

    Returns:
        configparser.ConfigParser: The configuration object populated with the content of the file.

    Raises:
        IOError: If the configuration file cannot be created or written to.
    """
    config: configparser.ConfigParser = configparser.ConfigParser()
    if os.path.exists(config_path):
        config.read(config_path)
    else:
        create_default_config(config_path, config)  # Create the config with default values

    # Check if the 'Logging' section exists; if not, populate defaults
    if not config.has_section("Logging"):
        set_default_logging_config(config)

    return config


def create_default_config(config_path: str, config: configparser.ConfigParser) -> None:
    """
    Create a default configuration file with initial sections and values.

    Args:
        config_path (str): The path where the configuration file should be created.
        config (configparser.ConfigParser): The ConfigParser object to be populated with default values.

    Raises:
        IOError: If the configuration file cannot be written to.
    """
    logging.info(f"Creating a default configuration file at {config_path}")
    set_default_logging_config(config)

    save_config(config, config_path)


def set_default_logging_config(config: configparser.ConfigParser) -> None:
    """
    Set default logging configuration values in the provided ConfigParser object.

    Args:
        config (configparser.ConfigParser): The configuration object to update.
    """
    if not config.has_section("Logging"):
        config.add_section("Logging")

    log_dir: str = config.get("Logging", "log_dir", fallback="logs")
    config.set("Logging", "log_dir", log_dir)
    config.set("Logging", "log_override", config.get("Logging", "log_override", fallback="true"))
    config.set("Logging", "log_function_calls", config.get("Logging", "log_function_calls", fallback="false"))

    if not config.has_section('log_level'):
        config.add_section('log_level')
        config.set('log_level', 'global_log_level', 'INFO')

    if not config.has_option('Logging', 'use_global_log_level'):
        config.set('Logging', 'use_global_log_level', 'true')


def load_and_validate_config(config_path: Optional[str] = None) -> Tuple[configparser.ConfigParser, str]:
    """
    Load the configuration file, validate its sections, and populate with default values if needed.
    Warns if the configuration file is loaded from a different path than the first load.

    Args:
        config_path (Optional[str]): The path to the configuration file. If None, it tries to locate it automatically.

    Returns:
        Tuple[configparser.ConfigParser, str]: The validated configuration object and the path to the
        configuration file.
    """
    global FIRST_CONFIG_PATH, PRIMARY_CONFIG

    if config_path is None:
        project_root: str = find_project_root(os.getcwd())
        config_path = os.path.join(project_root, 'config.ini')  # Ensure config.ini is in the project root

    config_path = os.path.abspath(config_path)
    logging.debug(f"Resolved config_path: {config_path}")

    if FIRST_CONFIG_PATH is not None and FIRST_CONFIG_PATH != config_path:
        logging.warning(f"Configuration file loaded from a different location: {config_path} "
                        f"(first loaded from {FIRST_CONFIG_PATH})")
        return PRIMARY_CONFIG, FIRST_CONFIG_PATH

    if FIRST_CONFIG_PATH is None:
        FIRST_CONFIG_PATH = config_path
        config: configparser.ConfigParser = ensure_config_exists(config_path)
        PRIMARY_CONFIG = config
    else:
        config = PRIMARY_CONFIG

    save_config(config, config_path)

    return config, config_path


def get_all_module_names(config: configparser.ConfigParser, config_path: str) -> List[str]:
    """
    Combines a static list of modules from config.ini with dynamically discovered modules in the project.

    Excludes modules found in the `tests` directory and avoids third-party or standard library modules unless
    explicitly listed in the config.ini.

    Any dynamically discovered modules not already listed in config.ini are added with a default log level.

    Args:
        config (configparser.ConfigParser): The configuration object containing the log level settings.
        config_path (str): The path to the configuration file for updating with new modules.

    Returns:
        List[str]: A combined list of module names as strings.
    """
    static_modules: List[str] = list(config['log_level'].keys())
    project_root: str = find_project_root(os.getcwd())
    dynamic_modules: List[str] = discover_project_modules(project_root)

    new_modules_added: bool = False
    for module in dynamic_modules:
        if module not in static_modules:
            config.set('log_level', module, 'INFO')
            static_modules.append(module)
            new_modules_added = True

    if new_modules_added:
        save_config(config, config_path)

    return static_modules


def discover_project_modules(root_path: str) -> List[str]:
    """
    Recursively discovers all Python modules in the project directory, excluding specific folders like 'tests'
    and '.venv'.

    Args:
        root_path (str): The root directory of the project.

    Returns:
        List[str]: A list of module names relative to the project root.
    """
    module_names: List[str] = []
    exclude_dirs: set[str] = {'tests', '__pycache__', '.venv'}

    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                relative_path: str = os.path.relpath(os.path.join(root, file), root_path)
                module_name: str = relative_path.replace(os.path.sep, '.')[:-3]
                module_names.append(module_name)

    return module_names


def main() -> None:
    """
    Main function demonstrating how to use the config_manager module.
    """
    config, config_path = load_and_validate_config()

    log_dir = config.get('Logging', 'log_dir', fallback='logs')
    global_log_level = config.get('log_level', 'global_log_level', fallback='INFO')
    use_global_log_level = config.getboolean('Logging', 'use_global_log_level', fallback=True)

    effective_log_level = global_log_level if use_global_log_level else "INFO"

    print(f"Log directory: {log_dir}")
    print(f"Effective log level: {effective_log_level}")

    # Example of logging a message with the retrieved configuration
    logging.basicConfig(level=effective_log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized in directory: {log_dir}")


if __name__ == "__main__":
    main()
