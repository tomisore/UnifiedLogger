# UnifiedLogger

A Python logging package that provides enhanced logging capabilities with support for colored output and JSON formatting.

## Features

- Colored console output for different log levels
- JSON formatted logging for structured log data
- File and console logging support
- Customizable log formats
- Support for extra fields in log messages

## Installation

```bash
pip install unifiedlogger
```

## Usage

```python
from unifiedlogger.logger import Logger

# Create a logger instance
logger = Logger(
    name="MyApp",
    log_file="logs/app.log",  # Optional
    use_colors=True,          # Optional, defaults to True
    use_json=False           # Optional, defaults to False
)

# Log messages
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")

# Log with extra fields
logger.info("User action", user_id=123, action="login")
```

## Development

To run tests:

```bash
python -m unittest test_logger.py
```

## License

MIT License
