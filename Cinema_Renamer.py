import os
from sys import argv
from controller import Controller
from viewCLI import ViewCLI


API_KEY = "8eac7bdc5eac6879ab8c8a97848f0e74"

# print(sys.path)
queue = argv[1:]
# validateInput(queue)


def main():
    c = Controller(queue, ViewCLI())
    c.start()


if __name__ == "__main__":
    main()

os.system("pause")
