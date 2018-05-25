import logging as _logging
from colorlog import ColoredFormatter
import sys
import os

STREAM_LOG_FORMAT = "%(asctime)s %(log_color)s%(levelname)-6s%(reset)s | %(log_color)s%(message)s%(reset)s"
FILE_LOG_FORMAT = "%(asctime)s %(levelname)-6s | %(message)s"

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class LogWriter(object):

    def __init__(self, logger, log_level=_logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def read(self):
        pass

    def flush(self):
        pass


def get_logger():
    return _logging.getLogger(__package__)


def handle_exception(exc_type, exc_value, exc_traceback):
    # if issubclass(exc_type, KeyboardInterrupt):
    #     get_logger().warning("Keyboard Interrupt")
    #     sys.__excepthook__(exc_type, exc_value, exc_traceback)
    #     return

    get_logger().error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


def init_logging(logfile=None, redirect_stdout=True, redirect_stderr=True):
    logger = get_logger()
    logger.setLevel(_logging.DEBUG)
    formatter = ColoredFormatter(STREAM_LOG_FORMAT, DATE_FORMAT)
    stream_handler = _logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    sys.excepthook = handle_exception

    if logfile:
        log_to_file(logfile)
    if redirect_stdout:
        sys.stdout = LogWriter(logger, log_level=_logging.DEBUG)
    if redirect_stderr:
        sys.stderr = LogWriter(logger, log_level=_logging.ERROR)


def log_to_file(filename):
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname, exist_ok=True)
    logger = get_logger()
    file_handler = _logging.FileHandler(filename)
    formatter = _logging.Formatter(FILE_LOG_FORMAT, DATE_FORMAT)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
