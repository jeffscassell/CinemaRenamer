import os
from sys import argv
from controller import Controller
from viewCLI import ViewCLI
from configparser import ConfigParser


# # Writing to a config file
# config = ConfigParser()
# config.add_section("locations")
# config.set("locations", "shows", "shows folder location")
# config.set("locations", "movies", "movies folder location")
# with open("cr_config.ini", "w") as outp:
#     config.write(outp)

# Reading from a config file
# config = ConfigParser()
# config.read("cr_config.ini")
# moviesDir: str = config.get("locations", "movies")
# moviesDir = moviesDir.replace("\"", "")
# showsDir: str = config.get("locations", "shows")
# showsDir = showsDir.replace("\"", "")
# print(f"{moviesDir}")
# print(f"{showsDir}")


API_KEY = "8eac7bdc5eac6879ab8c8a97848f0e74"  # TMDB

def main():
    c = Controller(argv[1:], ViewCLI())
    # TODO load settings
    # TODO validate settings; error flag will either be set or not
    # TODO pass settings to controller and continue; error handling/reporting should be done by View
    c.start()


if __name__ == "__main__":
    main()

os.system("pause")
