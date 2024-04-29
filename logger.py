import logging

class Logger:
    """
    Class: Logger

    This class provides a logging utility for setting up logging configuration and logging preprocessing steps.

    Methods:
        __init__: Initializes the Logger object with a log file.
        setup_logger: Sets up logger configuration.
        log: Logs a message.

    Example usage:
        logger = Logger(log_file="custom.log")
        logger.log("Preprocessing data for DataFrame 1")
    """

    def __init__(self, log_file="preprocessing.log"):
        """
        Initialize Logger object with a log file.

        Args:
        log_file (str): Name of the log file to write logs to. Default is "preprocessing.log".
        """
        self.log_file = log_file
        self.logger = self.setup_logger()

    def setup_logger(self):
        """
        Set up logger configuration.
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    def log(self, message):
        """
        Log a message.

        Args:
        message (str): Message to be logged.
        """
        self.logger.info(message)
