from sys import stdout as sys_std_out

# Date and Time formatting
DATETIME_FORMAT = "%d-%m-%Y %I:%M:%S"
# Logging formatting for console
# LOGGING_FORMAT = "[%(asctime)s.%(msecs)03d] [module=%(module)s.py] [level=%(levelname)s]: %(message)s"
LOGGING_FORMAT = "[{time}] [module={module}.py] [level={level}]: {message}"

# Settings for logger
config_map = {
    "handlers": [
        {
            "sink": sys_std_out,
            "level": "DEBUG",
            "colorize": True,
            "backtrace": True,
            "diagnose": True,
        },
    ]
}
