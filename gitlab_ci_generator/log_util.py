import logging

date_format = "%Y-%m-%dT%H:%M:%S"
log_format = "%(asctime)s.%(msecs)03d %(levelname)s %(message)s"


class LogFormatter(logging.Formatter):

    white = "\x1b[37;20m"
    blue = "\x1b[34;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    FORMATS = {
        logging.DEBUG: white + log_format + reset,
        logging.INFO: blue + log_format + reset,
        logging.WARNING: yellow + log_format + reset,
        logging.ERROR: red + log_format + reset,
        logging.CRITICAL: bold_red + log_format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, date_format)
        return formatter.format(record)


def setup_logger(verbose: bool, color: bool):
    log_level = logging.DEBUG if verbose else logging.INFO

    if color:
        ch = logging.StreamHandler()
        ch.setFormatter(LogFormatter())
        logging.basicConfig(level=log_level, handlers=[ch])
        return

    logging.basicConfig(level=log_level, format=log_format, datefmt=date_format)
