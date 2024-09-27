import logging
from typing import Self


class Formatter:
    def __init__(
        self,
        msg_fmt="[%(levelname)s] - %(message)s (%(name)s)",
        info_fmt="%(message)s",
    ) -> None:
        self.msg_fmt = msg_fmt
        self.info_fmt = info_fmt

        grey = "\x1b[38;20m"
        yellow = "\x1b[33;20m"
        red = "\x1b[31;20m"
        bold_red = "\x1b[31;1m"
        reset = "\x1b[0m"
        green = "\033[0;32m"

        self.formats = {
            logging.DEBUG: grey + self.msg_fmt + reset,  # 10
            logging.INFO: grey + self.info_fmt + reset,  # 20
            25: green + self.info_fmt + reset,  # 'logging.SUCCESS'
            logging.WARNING: yellow + self.msg_fmt + reset,  # 30
            logging.ERROR: red + self.msg_fmt + reset,  # 40
            logging.CRITICAL: bold_red + self.msg_fmt + reset,  # 50
        }

    def format(self, record: logging.LogRecord) -> Self:
        log_fmt = self.formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class Logger(Formatter):
    def __init__(
        self,
        name: str,
        msg_fmt: str = "[%(levelname)s] - %(message)s (%(name)s)",
        info_fmt: str = "%(message)s",
    ) -> None:
        """Logger class with color-coded log messages.

        Args:
            name (str): String expression representing the name of the logger class.
            msg_fmt (str, optional): String expression representing how the debug, warning, error, and critical log messages are formatted. Defaults to "[%(levelname)s] - %(message)s (%(name)s)".
            info_fmt (str, optional): String expression representing how the info and success messages are formatted. Defaults to "%(message)s".
        """

        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        self.formatter = Formatter(msg_fmt, info_fmt)

        self._add_success_level()
        self._get_handler()

    def _get_handler(self) -> None:
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(self.formatter)

        self.logger.addHandler(handler)

    def _log_for_level(self, msg, *args, **kwargs):
        if self.logger.isEnabledFor(25):
            self.logger._log(25, msg, args, **kwargs)

    def _add_success_level(self) -> None:
        level_name = "SUCCESS"
        method_name = "success"
        level_num = 25

        def log_to_root(msg, *args, **kwargs):
            logging.log(level_num, msg, **args, **kwargs)

        logging.addLevelName(level_num, level_name)

        setattr(logging, level_name, level_num)
        setattr(logging.getLoggerClass(), method_name, self._log_for_level)
        setattr(logging, method_name, log_to_root)

    def debug(self, msg: str) -> None:
        self.logger.debug(msg)

    def info(self, msg: str) -> None:
        self.logger.info(msg)

    def error(self, msg: str) -> None:
        self.logger.error(msg)

    def warn(self, msg: str) -> None:
        self.logger.warning(msg)

    def success(self, msg: str) -> None:
        self.logger.success(msg)

    def critical(self, msg) -> None:
        self.logger.critical(msg)
