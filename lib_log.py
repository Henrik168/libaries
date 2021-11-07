# -*- coding: utf-8 -*-

# global libraries
import logging
import os
import datetime

# local libraries
from lib_path import get_dir_path, make_path


class ColoredFormatter(logging.Formatter):
    """ColoredFormatter to change colors depending on severity level"""

    CSI = '\x1b'
    GREEN = CSI + '[32m'
    GREY = CSI + '[97m'
    YELLOW = CSI + '[33m'
    RED = CSI + '[31m'
    MAGENTA = CSI + '[95m'
    RESET = CSI + '[0m'

    FORMAT = '%(asctime)s.%(msecs)03d - %(name)s - %(module)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s'

    FORMATS = {
        logging.DEBUG: GREEN + FORMAT + RESET,
        logging.INFO: GREY + FORMAT + RESET,
        logging.WARNING: YELLOW + FORMAT + RESET,
        logging.ERROR: RED + FORMAT + RESET,
        logging.CRITICAL: MAGENTA + FORMAT + RESET,
        logging.NOTSET: MAGENTA + FORMAT + RESET
    }

    def format(self, record):
        log_format = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_format, '%d.%m.%Y %H:%M:%S')
        return formatter.format(record)


class Log:
    def __init__(self,
                 name: str = 'custom_logger',
                 level: int = 20,
                 path: str = './log/'):
        # create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)  # Debug = 10 #INFO = 20 #WARNING = 30 # ERROR=40

        # create console handler
        self.ch = logging.StreamHandler()

        # add formatter to ch
        self.ch.setFormatter(ColoredFormatter())

        # add ch to logger
        self.logger.addHandler(self.ch)

        # create file handler and set level to debug
        self.path = make_path(path)
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d")
        self.fh = logging.FileHandler(os.path.join(self.path, str(self.timestamp) + '_python.log'))

        # create formatter
        self.formatter = logging.Formatter(
            '%(asctime)s.%(msecs)03d - %(name)s - %(module)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s',
            '%d.%m.%Y %H:%M:%S')

        # add formatter to fh
        self.fh.setFormatter(self.formatter)

        # add fh to logger
        self.logger.addHandler(self.fh)

        # setting logging level
        self.set_level(level)

        self.logger.info(f"Logger started. Write Logfile to: {self.path}")

    def set_level(self, level: int) -> None:
        """Setting Logging Level, Console Handler and Filehandler has same logging level
        Debug = 10 INFO = 20 WARNING = 30 ERROR=40
        """
        self.logger.setLevel(level)
        self.fh.setLevel(level)
        self.ch.setLevel(min(40, level + 10))

    def set_path(self, path: str) -> None:
        """
        Set a new path for storing Logfiles
        :param path: String representing path to the folder
        :return: None
        """
        self.path = make_path(path)
        self.fh = logging.FileHandler(os.path.join(self.path, str(self.timestamp) + '_python.log'))

    def get_logger(self) -> logging.Logger:
        """
        Returns the Loggerobject
        :return:
        """
        return self.logger

    def close(self) -> None:
        """
        Close and remove all handlers
        :return: None
        """
        self.fh.close()
        self.logger.removeHandler(self.fh)
        self.ch.close()
        self.logger.removeHandler(self.ch)
