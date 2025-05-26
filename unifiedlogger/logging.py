import logging
from logging.handlers import RotatingFileHandler


class Logger:
	def __init__(self, name, log_file=None, level=logging.DEBUG):
		self.logger = logging.getLogger(name)
		self.logger.setLevel(level)

		# Formatter to include timestamp
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

		# StreamHandler for stdout
		stream_handler = logging.StreamHandler()
		stream_handler.setFormatter(formatter)
		self.logger.addHandler(stream_handler)

		# Optional file handler
		if log_file:
			file_handler = RotatingFileHandler(log_file, maxBytes=10 ** 6, backupCount=3)
			file_handler.setFormatter(formatter)
			self.logger.addHandler(file_handler)

	def debug(self, message):
		self.logger.debug(message)

	def info(self, message):
		self.logger.info(message)

	def warn(self, message):
		self.logger.warning(message)

	def warning(self, message):
		self.logger.warning(message)

	def error(self, message):
		self.logger.error(message)

	def critical(self, message):
		self.logger.critical(message)

