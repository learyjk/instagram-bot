from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from datetime import datetime
from time import sleep
import os
import logging
from config import IG_USER, IG_PASS, TARGET_ACCOUNT

CHROME_DRIVER_PATH_LOCAL = "/Users/keeganleary/Development/chromedriver"
CHROME_DRIVER_PATH_VPS = "/usr/bin/chromedriver"
NUM_DAILY_ACCOUNTS_TO_FOLLOW = 100
NUM_DAILY_ACCOUNTS_TO_UNFOLLOW = 15
NUM_TO_FOLLOW_EACH_RUN = 7
STARTING_HOUR = 9


def login():
    logging.info("Headed to instagram.com...")
    driver.get("https://www.instagram.com/accounts/login/")
    sleep(2)
    logging.info("Logging in...")
    username_field = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
    username_field.send_keys(IG_USER)
    password_field = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
    password_field.send_keys(IG_PASS)
    password_field.send_keys(Keys.ENTER)

    sleep(2)
    try:
        not_now_save_button = driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/div/div/div/button')
        not_now_save_button.click()
    except NoSuchElementException:
        pass

    sleep(2)
    try:
        not_now_notify_button = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]')
        not_now_notify_button.click()
    except NoSuchElementException:
        pass
    logging.info("Login successful!")


def build_to_follow_file():
    logging.info(f"Headed to https://www.instagram.com/{TARGET_ACCOUNT}/")
    driver.get(f"https://www.instagram.com/{TARGET_ACCOUNT}/")
    sleep(2)
    followers_button = driver.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')
    followers_button.click()
    sleep(2)
    modal = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]')
    for _ in range(5):
        # scroll modal
        logging.info("scrolling the modal a bit...")
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
        sleep(1)

    all_account_names = driver.find_elements_by_css_selector("li a")[2:]
    sleep(1)

    with open("to_follow.txt", "w") as f:
        for account in all_account_names:
            account_name = account.text
            if account_name != '':
                logging.info(f"{account_name} added to to_follow.txt")
                f.write(account_name + '\n')


def follow_accounts(num):
    accounts_to_follow = []
    if os.path.isfile("to_follow.txt"):
        # reads the whole file
        with open('to_follow.txt', 'r') as fin:
            data = fin.read().splitlines(True)

        # get num accounts or however many remain
        if len(data) >= num:
            accounts_to_follow = data[0:num]
            data = data[num:]
        else:
            accounts_to_follow = data
            data = []

        # write unused accounts back to to_follow.txt
        with open('to_follow.txt', 'w') as fout:
            fout.writelines(data)
    else:
        logging.error("No file named to_follow.txt!")

    if not accounts_to_follow:
        logging.info("accounts_to_follow is empty")
    else:
        for account in accounts_to_follow:
            logging.info(f"Headed to https://www.instagram.com/{account}/")
            driver.get(f"https://www.instagram.com/{account}/")
            sleep(2)
            try:
                follow_button = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button')
                sleep(1)
                follow_button.click()
            except ElementClickInterceptedException:
                logging.info(f"Already following {account}!")
                cancel_button = driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[2]')
                sleep(1)
                cancel_button.click()


def write_log(filename, data):
    if os.path.isfile(filename):
        with open(filename, "a") as f:
            f.write('\n' + data)
    else:
        with open(filename, "w") as f:
            f.write(data)


def print_time():
    data = "Current Time: " + now.strftime("%m/%d/%Y %H:%M:%S")
    return data


# initial setup
logging.basicConfig(
    level=logging.DEBUG,
    filename="logfile",
    filemode="a+",
    format="%(asctime)-15s %(levelname)-8s %(message)s")
options = Options()
options.headless = True
driver = webdriver.Chrome(CHROME_DRIVER_PATH_VPS, options=options)
now = datetime.now()

login()

# build a list of ~72 accounts to follow for the day
if now.hour == STARTING_HOUR:
    build_to_follow_file()

follow_accounts(NUM_TO_FOLLOW_EACH_RUN)

driver.quit()

write_log('run_history.txt', print_time())
