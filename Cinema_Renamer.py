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


def main():
    c = Controller(argv[1:], ViewCLI())
    c.start()


if __name__ == "__main__":
    main()

os.system("pause")
