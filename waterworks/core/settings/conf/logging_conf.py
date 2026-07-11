from os import makedirs
import logging

from core.settings.base import BASE_DIR
from colorama import Fore, Style, init


# Ensure the 'logs' directory exists
makedirs(f'{BASE_DIR}/logs', exist_ok=True)
# Initialize colorama for colored output in the console
init(autoreset=True)


class ColorFormatter(logging.Formatter):
    """
    Custom logging formatter that adds color to log messages based on their severity level.
    """

    # Define color mappings for different log levels
    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record with color based on its severity level.

        Arguments:
            record (logging.LogRecord): The log record to format.
        """

        color = self.COLORS.get(record.levelno, "")

        record.levelname = (
            f"{color}{record.levelname}{Style.RESET_ALL}"
        )

        record.name = (
            f"{Fore.BLUE}{record.name}{Style.RESET_ALL}"
        )

        record.asctime = (
            f"{Fore.MAGENTA}{self.formatTime(record)}{Style.RESET_ALL}"
        )

        return super().format(record)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'standard': {
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
        },
        'color': {
            '()': ColorFormatter,
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
        }
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'color',
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': f'{BASE_DIR}/logs/waterworks.log',
            'formatter': 'standard',
        }
    },

    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': False
        },

        # Local apps
        'apps.accounts.views': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'apps.common.views': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'apps.devices.views': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
