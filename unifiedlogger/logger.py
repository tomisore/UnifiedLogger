import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
import json


class CustomFormatter(logging.Formatter):
	"""
    Custom formatter for logs with color support and structured output
    """
	grey = "\x1b[38;21m"
	blue = "\x1b[38;5;39m"
	yellow = "\x1b[38;5;226m"
	red = "\x1b[38;5;196m"
	bold_red = "\x1b[31;1m"
	reset = "\x1b[0m"

	def __init__(self, use_colors: bool = True):
		super().__init__()
		self.use_colors = use_colors
		self.fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

		self.FORMATS = {
			logging.DEBUG: self.grey + self.fmt + self.reset,
			logging.INFO: self.blue + self.fmt + self.reset,
			logging.WARNING: self.yellow + self.fmt + self.reset,
			logging.ERROR: self.red + self.fmt + self.reset,
			logging.CRITICAL: self.bold_red + self.fmt + self.reset
		}

	def format(self, record):
		if not self.use_colors:
			return super().format(record)

		log_fmt = self.FORMATS.get(record.levelno)
		formatter = logging.Formatter(log_fmt)
		return formatter.format(record)


class JsonFormatter(logging.Formatter):
	"""
    JSON formatter for structured logging
    """

	def format(self, record):
		log_data = {
			'timestamp': datetime.utcnow().isoformat(),
			'level': record.levelname,
			'logger': record.name,
			'message': record.getMessage(),
			'module': record.module,
			'function': record.funcName,
			'line': record.lineno
		}

		if hasattr(record, 'extra'):
			log_data.update(record.extra)

		if record.exc_info:
			log_data['exception'] = self.formatException(record.exc_info)

		return json.dumps(log_data)


class Logger:
	"""
    Enhanced logger with multiple handlers and formatting options
    """

	def __init__(
			self,
			name: str,
			log_level: int = logging.INFO,
			log_file: Optional[str] = None,
			use_colors: bool = True,
			use_json: bool = False
	):
		self.logger = logging.getLogger(name)
		self.logger.setLevel(log_level)

		# Remove existing handlers
		self.logger.handlers = []

		# Console handler
		console_handler = logging.StreamHandler(sys.stdout)
		if use_json:
			console_handler.setFormatter(JsonFormatter())
		else:
			console_handler.setFormatter(CustomFormatter(use_colors))
		self.logger.addHandler(console_handler)

		# File handler
		if log_file:
			log_path = Path(log_file)
			log_path.parent.mkdir(parents=True, exist_ok=True)

			file_handler = logging.FileHandler(log_file)
			if use_json:
				file_handler.setFormatter(JsonFormatter())
			else:
				file_handler.setFormatter(logging.Formatter(
					'%(asctime)s - %(name)s - %(levelname)s - %(message)s'
				))
			self.logger.addHandler(file_handler)

	def debug(self, msg: str, **kwargs):
		"""Log debug message"""
		self.logger.debug(msg, extra=kwargs)

	def info(self, msg: str, **kwargs):
		"""Log info message"""
		self.logger.info(msg, extra=kwargs)

	def warning(self, msg: str, **kwargs):
		"""Log warning message"""
		self.logger.warning(msg, extra=kwargs)

	def error(self, msg: str, **kwargs):
		"""Log error message"""
		self.logger.error(msg, extra=kwargs)

	def critical(self, msg: str, **kwargs):
		"""Log critical message"""
		self.logger.critical(msg, extra=kwargs)

	def exception(self, msg: str, **kwargs):
		"""Log exception with traceback"""
		self.logger.exception(msg, extra=kwargs)


# Create default logger instance
# default_logger = Logger(
# 	name="OptionTrader",
# 	log_file="logs/option_trader.log",
# 	use_colors=True
# )
