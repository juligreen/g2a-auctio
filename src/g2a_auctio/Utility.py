from contextlib import contextmanager
from selenium import webdriver
import time

@contextmanager
def managed_chromedriver(options):
    chrome_driver = webdriver.Chrome(options=options)
    try:
        yield chrome_driver
    finally:
        time.sleep(5)
        # chrome_driver.quit()

def get_chromedriver_options():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-notifications')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument('--disable-web-security')
    options.add_argument('user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"')
    # options.add_argument('--user-data-dir')
    options.add_argument('--allow-running-insecure-content')
    return options

