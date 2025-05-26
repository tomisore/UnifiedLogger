import unittest
import logging
import os
from pathlib import Path
import json
from unifiedlogger.logger import Logger, CustomFormatter, JsonFormatter

class TestLogger(unittest.TestCase):
    """Test cases for the Logger class and its formatters"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_log_file = "test_logs/test.log"
        self.test_json_log_file = "test_logs/test_json.log"
        self.loggers = []  # Keep track of created loggers
        
        # Create test logs directory
        Path("test_logs").mkdir(exist_ok=True)
        
        # Remove any existing test log files
        if os.path.exists(self.test_log_file):
            os.remove(self.test_log_file)
        if os.path.exists(self.test_json_log_file):
            os.remove(self.test_json_log_file)
    
    def tearDown(self):
        """Clean up test environment"""
        # Close all logger handlers
        for logger in self.loggers:
            for handler in logger.logger.handlers[:]:
                handler.close()
                logger.logger.removeHandler(handler)
        
        # Remove test log files
        if os.path.exists(self.test_log_file):
            os.remove(self.test_log_file)
        if os.path.exists(self.test_json_log_file):
            os.remove(self.test_json_log_file)
        
        # Remove test logs directory
        if os.path.exists("test_logs"):
            os.rmdir("test_logs")
    
    def test_custom_formatter(self):
        """Test CustomFormatter class"""
        formatter = CustomFormatter(use_colors=True)
        
        # Create a test log record
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Test message",
            args=(),
            exc_info=None
        )
        
        # Format the record
        formatted = formatter.format(record)
        
        # Check if the formatted string contains the expected components
        self.assertIn("test", formatted)
        self.assertIn("INFO", formatted)
        self.assertIn("Test message", formatted)
        
        # Test without colors
        formatter_no_colors = CustomFormatter(use_colors=False)
        formatted_no_colors = formatter_no_colors.format(record)
        self.assertNotIn("\x1b[", formatted_no_colors)
    
    def test_json_formatter(self):
        """Test JsonFormatter class"""
        formatter = JsonFormatter()
        
        # Create a test log record
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Test message",
            args=(),
            exc_info=None
        )
        
        # Format the record
        formatted = formatter.format(record)
        
        # Parse the JSON string
        log_data = json.loads(formatted)
        
        # Check if the JSON contains the expected fields
        self.assertEqual(log_data["level"], "INFO")
        self.assertEqual(log_data["logger"], "test")
        self.assertEqual(log_data["message"], "Test message")
        self.assertIn("timestamp", log_data)
        self.assertIn("module", log_data)
        self.assertIn("function", log_data)
        self.assertIn("line", log_data)
    
    def test_logger_initialization(self):
        """Test Logger initialization"""
        # Test with default settings
        logger = Logger("test_logger")
        self.loggers.append(logger)
        self.assertEqual(logger.logger.name, "test_logger")
        self.assertEqual(logger.logger.level, logging.INFO)
        self.assertEqual(len(logger.logger.handlers), 1)  # Only console handler
        
        # Test with file handler
        logger_with_file = Logger(
            "test_logger_file",
            log_file=self.test_log_file
        )
        self.loggers.append(logger_with_file)
        self.assertEqual(len(logger_with_file.logger.handlers), 2)  # Console and file handlers
        
        # Test with JSON formatting
        logger_json = Logger(
            "test_logger_json",
            log_file=self.test_json_log_file,
            use_json=True
        )
        self.loggers.append(logger_json)
        self.assertEqual(len(logger_json.logger.handlers), 2)
    
    def test_logger_output(self):
        """Test logger output methods"""
        logger = Logger(
            "test_logger_output",
            log_file=self.test_log_file
        )
        self.loggers.append(logger)
        
        # Set logging level to DEBUG to capture all messages
        logger.logger.setLevel(logging.DEBUG)
        
        # Test different log levels
        test_message = "Test message"
        logger.debug(test_message)
        logger.info(test_message)
        logger.warning(test_message)
        logger.error(test_message)
        logger.critical(test_message)
        
        # Read the log file
        with open(self.test_log_file, 'r') as f:
            log_content = f.read()
        
        # Check if all log levels are present
        self.assertIn("DEBUG", log_content)
        self.assertIn("INFO", log_content)
        self.assertIn("WARNING", log_content)
        self.assertIn("ERROR", log_content)
        self.assertIn("CRITICAL", log_content)
        self.assertIn(test_message, log_content)
    
    def test_logger_json_output(self):
        """Test logger JSON output"""
        logger = Logger(
            "test_logger_json_output",
            log_file=self.test_json_log_file,
            use_json=True
        )
        self.loggers.append(logger)
        
        # Log a test message
        test_message = "Test JSON message"
        logger.info(test_message)
        
        # Read the log file
        with open(self.test_json_log_file, 'r') as f:
            log_line = f.readline().strip()
        
        # Parse the JSON log entry
        log_data = json.loads(log_line)
        
        # Check the log entry contents
        self.assertEqual(log_data["level"], "INFO")
        self.assertEqual(log_data["logger"], "test_logger_json_output")
        self.assertEqual(log_data["message"], test_message)
    
    def test_logger_extra_fields(self):
        """Test logger with extra fields"""
        logger = Logger("test_logger_extra")
        self.loggers.append(logger)
        
        # Log with extra fields
        extra_data = {"user_id": 123, "action": "test"}
        logger.info("Test message with extra data", **extra_data)
        
        # Create a test record with extra data
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Test message",
            args=(),
            exc_info=None
        )
        record.extra = extra_data
        
        # Test JSON formatter with extra data
        formatter = JsonFormatter()
        formatted = formatter.format(record)
        log_data = json.loads(formatted)
        
        # Check if extra fields are included
        self.assertEqual(log_data["user_id"], 123)
        self.assertEqual(log_data["action"], "test")

if __name__ == '__main__':
    unittest.main() 