import copy
import logging
import sys


class ColoredFormatter(logging.Formatter):
    RESET = "\033[0m"  # RESET COLOR
    TITLE = "\033[0;94m"  # BRIGHT BLUE

    COLORS = {
        "DEBUG": "\033[0;37m",  # WHITE
        "INFO": "\033[0;36m",  # CYAN
        "SUCCESS": "\033[0;32m",  # GREEN
        "WARNING": "\033[0;33m",  # YELLOW
        "ERROR": "\033[0;31m",  # RED
    }

    def format(self, record):
        colored_record = copy.copy(record)

        name = colored_record.name
        colored_record.name = f"{self.TITLE}{name}{self.RESET}"

        if colored_record.msg.startswith("$S"):
            colored_record.msg = colored_record.msg[2:]
            levelname = "SUCCESS"
        else:
            levelname = colored_record.levelname

        seq = self.COLORS.get(levelname, self.RESET)
        colored_record.levelname = f"{seq}{levelname}{self.RESET}"

        return super().format(colored_record)


logger = logging.getLogger("Hoshimi")
logger.propagate = False

if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(ColoredFormatter("[%(name)s] - %(levelname)s :\t%(message)s"))
    logger.addHandler(handler)

logger.setLevel(logging.INFO)
