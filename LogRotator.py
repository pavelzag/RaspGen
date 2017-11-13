import logging
import os.path

from logging.handlers import TimedRotatingFileHandler


def create_timed_rotating_log(path):
    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.INFO)

    handler = TimedRotatingFileHandler(path,
                                       when="midnight",
                                       interval=1)
    logger.addHandler(handler)


if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_logging_path = os.path.join(dir_path, 'generator.log')
    create_timed_rotating_log(file_logging_path)
