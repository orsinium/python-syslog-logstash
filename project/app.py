
# CONFIGURE LOGGING

import logging
from logging.config import dictConfig

import logging.handlers


CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '{levelname:8} {asctime} {module}:{lineno} {message}',
            'style': '{',  # only for python>=3.3
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'syslog': {
            # additional data for log:
            'format': '%(name)s %(module)s %(lineno)s %(message)s',
            # format to json (https://github.com/madzak/python-json-logger)
            # Use '()' instead of 'class' for python2
            'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
        },
    },
    'handlers': {
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'syslog': {
            'level': 'INFO',
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'syslog',
            'facility': 'user',
            # for UNIX socket connection:
            # 'address': '/dev/log',
            # For TCP/IP connection:
            'address': ('psl-rsyslog', 514),
            # for TCP connection (UDP by default):
            # 'socktype': socket.SOCK_STREAM,
        },
    },
    'loggers': {
        '': {
            'handlers': ['syslog', 'console'],
            'level': 'INFO',
            'disabled': False,
            'propagate': False,
        },
    }
}

dictConfig(CONFIG)


# USE LOGGING


from random import choice, randint  # noQA
from string import ascii_lowercase  # noQA
from time import sleep              # noQA


LEVELS = 'debug', 'info', 'warning', 'error', 'critical'


logger = logging.getLogger('app_name')

while 1:
    # make payload
    data = {
        'random_string': ''.join(choice(ascii_lowercase) for _ in range(10)),
        'random_integer': randint(1, 1000),
    }

    # write payload to syslog
    level = choice(LEVELS)
    getattr(logger, level)(data)

    sleep(1)
