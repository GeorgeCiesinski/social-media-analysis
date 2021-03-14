"""
INSTRUCTIONS

1) To add logging to any module, add the following:

    from logging.Logger import base_logger

    logger = base_logger.getChild(__name__)

2) Use logging with the below. Levels (info, debug, warning, error, critical):

    logger.level("Message.")

Optional: To set up default console & file levels, modify the logger.ini file.
"""

import logging
import os

from logging import handlers
from configparser import RawConfigParser

"""
Setup paths
"""

# Set config and log directories
_config_dir = 'config'
_log_dir = 'logs'

# Create Logs directory if it doesn't exist
if not os.path.exists(_log_dir):
    print("Creating log directory.")
    os.mkdir(_log_dir)

# Set filename for config and log files
_config_filename = os.path.join(_config_dir, 'logger.ini')
_log_filename = os.path.join(_log_dir, 'social-media-analysis.log')

"""
Acquire settings from Config File
"""

# Read the config file
_config = RawConfigParser()
_config.read(_config_filename)

# Get settings

_valid_levels = [
    'DEBUG',
    'INFO',
    'WARNING',
    'ERROR',
    'CRITICAL'
]

_logger_level = _config['Settings']['setLevel']
if _logger_level not in _valid_levels:
    _logger_level = 'DEBUG'
    print("Settings/setLevel is not a valid level. Using default value.")

try:
    _rotating_max_bytes = int(_config['Rotating File Handler']['maxBytes'])
except ValueError:
    print("Rotating File Handler/maxBytes must be an integer. Using default value.")
    _rotating_max_bytes = 20000000

try:
    _rotating_backup_count = int(_config['Rotating File Handler']['backupCount'])
except ValueError:
    print("Rotating File Handler/backupCount must be an integer. Using default value.")
    _rotating_backup_count = 5

_rotating_level = _config['Rotating File Handler']['setLevel']
if _rotating_level not in _valid_levels:
    _rotating_level = 'DEBUG'
    print("Rotating File Handler/setLevel is not a valid level. Using default value.")

_console_level = _config['Console Handler']['setLevel']
if _console_level not in _valid_levels:
    _console_level = 'DEBUG'
    print("Settings/setLevel is not a valid level. Using default value.")

_log_format = _config['Formatter']['logFormat']

"""
Create Base Logger
"""

# Create Logger
base_logger = logging.getLogger(name='logger')
base_logger.setLevel(getattr(logging, _logger_level))

# Create Rotating File Handler
_rotating_file_handler = handlers.RotatingFileHandler(
    filename=_log_filename,
    mode='a',
    maxBytes=_rotating_max_bytes,
    backupCount=_rotating_backup_count
)
_rotating_file_handler.setLevel(getattr(logging, _rotating_level))

# Create Console Handler - Streams to Console
_console_handler = logging.StreamHandler()
_console_handler.setLevel(getattr(logging, _console_level))

# Create a Formatter and add it to the handlers
_formatter = logging.Formatter(_log_format)
_rotating_file_handler.setFormatter(_formatter)
_console_handler.setFormatter(_formatter)

# Add the handlers to logger
base_logger.addHandler(_rotating_file_handler)
base_logger.addHandler(_console_handler)
