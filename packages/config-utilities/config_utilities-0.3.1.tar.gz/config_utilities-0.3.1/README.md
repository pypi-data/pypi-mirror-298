# Config Utilities

## Overview

The `config_utilities` project provides utilities for managing configurations and logging in Python applications. It simplifies setting up a `config.ini` file, configuring logging, and optionally logging function calls with detailed information about arguments and return values.

This manual guides you through installation, setting up configurations, enabling logging, and customizing function call logging.

## Quick Start Guide

### Installation

To install the project directly from the GitHub repository, run:

```bash
pip install git+https://github.com/audkus/config_utilities.git
```

### Example Application

Here’s a simple example of how to use the `config_utilities` in a Python application. This example demonstrates basic setup, configuring logging, and logging function calls.

1. **Create your application module** (`app.py`):

```python
# app.py

from logging_util import setup_logging, log_function_call

# Initialize logging for the application
setup_logging('app')

@log_function_call
def add(a, b):
    return a + b

@log_function_call
def subtract(a, b):
    return a - b

def main():
    result_add = add(5, 3)
    result_subtract = subtract(10, 7)
    print(f"Addition Result: {result_add}")
    print(f"Subtraction Result: {result_subtract}")

if __name__ == "__main__":
    main()
```

2. **Run the application**:
   This will generate logs in the directory specified by the `config.ini` file (explained below). If the configuration file does not exist, it will be created automatically with default settings.

### Application Imports

Whether you install the module from GitHub or PyPI, the import statements will be the same:

```python
from logging_util import setup_logging, log_function_call
```

These imports will work regardless of where the package is installed (GitHub, PyPI, or locally).

---

## Detailed Setup and Usage

### Config Manager

The `config_manager` module provides centralized management of your application's configuration files, ensuring consistent behavior across different parts of the project.

Key features include:
- **Locating the project root**: The module searches for specific marker files (e.g., `config.ini`, `.git`, `setup.py`) to determine the root directory of your project.
- **Ensuring the existence of the configuration file**: If no configuration file is found, the module creates a default `config.ini` file.
- **Setting default values**: Default settings for logging are added to the configuration file if they are missing.
- **Loading and validating the configuration**: The module validates the configuration file and makes sure it is ready for use in the application.

### Example usage:

```python
from config_manager import load_and_validate_config

config = load_and_validate_config()
log_dir = config.get('Logging', 'log_dir')
global_log_level = config.get('log_level', 'global_log_level')
```

This ensures that your application is always running with the correct configuration settings, even if the configuration file needs to be created from scratch.

To demonstrate the functionality, you can use the `main` function in `config_manager.py`:

```python
if __name__ == "__main__":
    config, config_path = load_and_validate_config()
    log_dir = config.get('Logging', 'log_dir', fallback='logs')
    global_log_level = config.get('log_level', 'global_log_level', fallback='INFO')
    print(f"Log directory: {log_dir}")
    print(f"Effective log level: {global_log_level}")
```

---

### Saving Configuration

The `save_config` function allows you to save any changes made to the configuration back to the configuration file. This is useful if you modify any values during runtime and want to persist them to the `config.ini`.

#### Example Usage

Here’s an example of how to use the `save_config` function:

```python
from config_manager import load_and_validate_config, save_config

# Load the existing configuration
config, config_path = load_and_validate_config()

# Modify the configuration as needed
config.set('Logging', 'log_dir', '/new/log/directory')

# Save the updated configuration
save_config(config, config_path)

print(f"Configuration saved to {config_path}")
```

In this example, the `log_dir` setting in the `Logging` section is updated and then saved back to the configuration file.

#### Function Signature

```python
def save_config(config: configparser.ConfigParser, config_path: str) -> None:
    """
    Save the configuration to the specified file path.

    Args:
        config (configparser.ConfigParser): The configuration object to save.
        config_path (str): The path to the configuration file.

    Raises:
        IOError: If the configuration file cannot be written to.
    """
```

Use `save_config` whenever you need to persist changes made to the configuration object during runtime. Ensure that the `config_path` is correct to avoid overwriting the wrong configuration file.

---

### Configuration File (`config.ini`)

By default, the application looks for a `config.ini` file in the project’s root directory. If it does not exist, the module will create one with the following default contents:

```ini
[Logging]
log_dir = logs
log_override = true
log_function_calls = false
use_global_log_level = true

[log_level]
global_log_level = INFO
```

### Customize the Configuration

You can modify `config.ini` to suit your project’s needs:

1. **log_dir**: The directory where log files are saved.
2. **log_override**: When `True`, logs are overwritten with each new application run. If `False`, logs are appended to the existing file.
3. **log_function_calls**: When `True`, logs function calls (if decorated with `@log_function_call`).
4. **use_global_log_level**: Controls whether the global log level applies to all modules.
5. **global_log_level**: Sets the default log level for all modules.

For more granular control, specify log levels for individual modules in the `[log_level]` section:

```ini
[log_level]
global_log_level = INFO
myapp.module1 = DEBUG
myapp.module2 = ERROR
```

### Setting Up Logging in Your Code

In each module of your project, initialize logging with `setup_logging`:

```python
from logging_util import setup_logging

setup_logging('my_module')
```

This configures logging based on the settings in the `config.ini` file. Logs will be saved in the directory specified by `log_dir`.

---

## Function Call Logging

### Why You Need to Use `@log_function_call`

In Python, it is not possible to automatically log all function calls without explicitly decorating them. The `@log_function_call` decorator allows detailed logging for specific functions, including:
- Function name
- Arguments passed
- Return value

Testing showed that it was not feasible to apply this feature globally across all functions. Therefore, functions must be decorated individually to enable logging.

### Example:

```python
from logging_util import log_function_call

@log_function_call
def multiply(x, y):
    return x * y
```

With `log_function_calls` enabled (`log_function_calls = true` in `config.ini`), the following logs will be produced when `multiply()` is called:

```plaintext
DEBUG - Entering multiply() with arguments: (3, 5)
DEBUG - Exiting multiply() with result: 15
```

---

## Advanced Topics

### `log_override`
The `log_override` setting controls whether log files are overwritten or appended with each new application run:
- **When `True`**: The log file is overwritten.
- **When `False`**: Logs are appended to the existing log file.

Use `log_override` to control how long you want to retain log data. For example, in development, you may want to overwrite logs on each run, but in production, appending logs may be preferable.

### `log_function_calls`
This setting controls whether function calls and their parameters/return values are logged. To enable function logging:
1. Set `log_function_calls = true` in the `config.ini`.
2. Decorate the functions you want to log with `@log_function_call`.

### Global Log Level
The **global log level** is a single log level that applies across all modules in your application. This simplifies logging configuration by providing a consistent log level for the entire application.

- **When `use_global_log_level` is `True`**: The global log level applies to all modules.
- **When `use_global_log_level` is `False`**: Each module can have its own log level, specified under the `[log_level]` section.

---

## Best Practices

1. **Use Global Log Level for Simplicity**: Set `use_global_log_level = true` to simplify logging across the project. Use individual module levels only when necessary.
2. **Function Call Logging**: Enable function call logging selectively for functions where argument tracking and debugging are critical. Avoid enabling it globally to prevent performance overhead.
3. **Log Rotation**: If `log_override = false`, ensure you manage log file sizes appropriately by implementing log rotation to avoid excessive log growth.

---

## Contributing

We welcome contributions to the project. Please submit issues or pull requests on [GitHub](https://github.com/audkus/config_utilities).

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Conclusion

The `config_utilities` project provides an efficient and flexible way to manage configurations and logging in Python applications. By using decorators like `@log_function_call`, you can easily track function execution while keeping your logs organized and manageable through the `config.ini` file.
