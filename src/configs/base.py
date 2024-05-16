from os import path as os_path
from sys import stdout as sys_std_out

# Current and main working directory
CURRENT_PATH = os_path.dirname(__file__)
MAIN_PATH = "\\".join(CURRENT_PATH.split("\\")[:-2])
# The directory with the database
DB_PATH = f"{MAIN_PATH}/db/users.db"

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
