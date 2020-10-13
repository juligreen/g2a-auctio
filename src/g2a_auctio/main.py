"""Main Module to start managing G2A"""
import sys
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions, expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from g2a_auctio.Utility import managed_chromedriver, get_chromedriver_options
import typer
from selenium.common.exceptions import NoSuchElementException
import random

app = typer.Typer()

min_transactions = 1000


@app.command()
def execute_this_shit(google_mail: str, google_password: str, g2a_username: str, g2a_password: str):
    """Main function to manage G2A, initialize driver and start later functions"""
    with managed_chromedriver(get_chromedriver_options()) as driver:
        driver.implicitly_wait(30)
        driver.maximize_window()
        google_login(driver, google_mail, google_password)
        lookup_game_price(driver, "Monster Hunter World")
        offer_game(g2a_username, g2a_password)


def offer_game(g2a_username: str, g2a_password: str):
    with managed_chromedriver(get_chromedriver_options()) as driver:
        login(driver, g2a_username, g2a_password)


def google_login(driver: webdriver.Chrome, google_mail, google_password):
    """Login to google first to make Captchas easier"""
    # from https://stackoverflow.com/questions/60117232/selenium-google-login-block/60342877#60342877
    driver.get("https://stackoverflow.com/users/signup?ssrc=head&returnurl=%2fusers%2fstory%2fcurrent%27")
    wait_set_time_plus_random_time(3)
    driver.find_element_by_xpath('//*[@id="openid-buttons"]/button[1]').click()
    driver.find_element_by_xpath('//input[@type="email"]').send_keys(google_mail)
    driver.find_element_by_xpath('//*[@id="identifierNext"]').click()
    wait_set_time_plus_random_time(3)
    driver.find_element_by_xpath('//input[@type="password"]').send_keys(google_password)
    driver.find_element_by_xpath('//*[@id="passwordNext"]').click()
    wait_set_time_plus_random_time(2)


def wait_set_time_plus_random_time(wait_time: int):
    complete_sleep_time = wait_time + random.randint(0, 9) * 0.1 + random.randint(0, 9) * 0.01
    time.sleep(complete_sleep_time)


def lookup_game_price(driver: webdriver.Chrome, game_name: str):
    driver.get(f"https://www.g2a.com/")
    wait_set_time_plus_random_time(2)
    cookie_clicker(driver)
    driver.get(f"https://www.g2a.com/search?query={game_name.replace(' ', '%2B')}")

    WebDriverWait(driver, 800).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "offers-list")))
    print("found offer site")

    offer_list_elements = driver.find_elements_by_class_name("offers-list__element")
    for list_element in offer_list_elements:
        transactions = int(list_element.find_element_by_class_name("seller-info__transactions").text)
        print(transactions)
        if transactions > min_transactions:
            offer_price = list_element.find_element_by_class_name("offer__price").text
            print(offer_price)
            return offer_price
    wait_set_time_plus_random_time(10)


def login(driver, username, password):
    """Open G2A and login"""
    driver.get("https://id.g2a.com/login")
    wait_set_time_plus_random_time(1)

    cookie_clicker(driver)

    login_form = driver.find_element_by_class_name("form-box__form")
    email_field = login_form.find_element_by_css_selector("input[type='email']")
    password_field = login_form.find_element_by_css_selector("input[type='password']")

    email_field.send_keys(username)
    password_field.send_keys(password)

    driver.switch_to.default_content()
    login_button = driver.find_element_by_xpath("//button[text()='Sign in']")
    login_button.click()
    wait_set_time_plus_random_time(3)


def cookie_clicker(driver):
    """Remove cookie popup"""
    try:
        confirm_button = driver.find_element_by_xpath('//button[contains(text(), "Confirm")]')
        confirm_button.click()
    except NoSuchElementException:
        print("No cookie button, was it already clicked?")


if __name__ == "__main__":
    app()
