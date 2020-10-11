import undetected_chromedriver as uc
from contextlib import contextmanager
import time

@contextmanager
def managed_chromedriver(options):
    chrome_driver = uc.Chrome(options=options)
    try:
        yield chrome_driver
    finally:
        time.sleep(5)
        # chrome_driver.quit()

def get_chromedriver_options():
    options = uc.ChromeOptions()
    # options.headless=True
    # options.add_argument('--headless')
    options.add_argument("window-size=1280,800")
    # options.add_argument('--user-data-dir=/home/julius/.user_data')
    # options.add_argument('--disable-notifications')
    # options.add_argument('--allow-running-insecure-content')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-setuid-sandbox')
    # options.add_argument('--disable-web-security')
    return options
