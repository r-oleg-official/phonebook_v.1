from os.path import exists as file_exists
from datetime import datetime


def main(msg):
    file_log = "log/phonebook.log"
    if file_exists(file_log): mode = "a"
    else: mode = "a"

    with open(file_log, mode, encoding="UTF-8") as log:
        log.write(f'{str(datetime.now()).split(".")[0]}: {msg}\n')


message = "logger is run."

if __name__ == "__main__":
    main(message)
