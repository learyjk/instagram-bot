from selenium import webdriver
from datetime import datetime
import os


def write_file(filename, data):
    if os.path.isfile(filename):
        with open(filename, "a") as f:
            f.write('\n', + data)
    else:
        with open(filename, "w") as f:
            f.write(data)


def print_time():
    now = datetime.now()
    data = "Current Time: " + now
    return data


write_file('test.txt', print_time())


