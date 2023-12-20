import os
from sys import argv
from controller import Controller
from viewCLI import ViewCLI
import traceback


API_KEY = "8eac7bdc5eac6879ab8c8a97848f0e74"  # TMDB

def main():
    c = Controller(argv[1:], ViewCLI())
    # TODO load settings
    # TODO validate settings; error flag will either be set or not
    # TODO pass settings to controller and continue; error handling/reporting should be done by View

    try:
        c.start()
    except Exception:  # Attempt to prevent the terminal from starting then stopping too fast to figure out what went wrong
        traceback.print_exc()
        os.system("pause")
        exit(1)


if __name__ == "__main__":
    main()

os.system("pause")
