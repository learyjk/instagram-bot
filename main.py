from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
from datetime import datetime
import os

CHROME_DRIVER_PATH_LOCAL = "/Users/keeganleary/Development/chromedriver"
CHROME_DRIVER_PATH_VPS = "/home/keegadmin/chrome-driver"
NUM_DAILY_ACCOUNTS_TO_FOLLOW = 100
NUM_DAILY_ACCOUNTS_TO_UNFOLLOW = 15
STARTING_HOUR = 8


def get_accounts_to_follow(target_account):
    pass


def write_log(filename, data):
    if os.path.isfile(filename):
        with open(filename, "a") as f:
            f.write('\n' + data)
    else:
        with open(filename, "w") as f:
            f.write(data)


def print_time():
    now = datetime.now()
    data = "Current Time: " + now.strftime("%m/%d/%Y %H:%M:%S")
    return data


options = Options()
options.headless = True
driver = webdriver.Chrome(CHROME_DRIVER_PATH_VPS, options=options)

driver.get("https://google.com/")
print(driver.title)

driver.quit()





write_log('test.txt', print_time())


