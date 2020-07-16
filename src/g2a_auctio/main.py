"""Main Module to start managing G2A"""
import sys
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from g2a_auctio.Utility import managed_chromedriver, get_chromedriver_options
import typer

app = typer.Typer()


@app.command()
def execute_this_shit(google_mail: str, google_password: str):
    """Main function to manage G2A, initialize driver and start later functions"""
    with managed_chromedriver(get_chromedriver_options()) as driver:
        driver.implicitly_wait(30)
        driver.maximize_window()
        # google_login(driver, google_mail, google_password)
        lookup_game_price(driver, "Monster Hunter World")
        login(driver, "test", "test")


def google_login(driver: webdriver.Chrome, google_mail, google_password):
    """Login to google first to make Captchas easier"""
    # from https://stackoverflow.com/questions/60117232/selenium-google-login-block/60342877#60342877
    driver.get("https://stackoverflow.com/users/signup?ssrc=head&returnurl=%2fusers%2fstory%2fcurrent%27")
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="openid-buttons"]/button[1]').click()
    driver.find_element_by_xpath('//input[@type="email"]').send_keys(google_mail)
    driver.find_element_by_xpath('//*[@id="identifierNext"]').click()
    time.sleep(3)
    driver.find_element_by_xpath('//input[@type="password"]').send_keys(google_password)
    driver.find_element_by_xpath('//*[@id="passwordNext"]').click()
    time.sleep(2)



def lookup_game_price(driver: webdriver.Chrome, game_name: str):
    driver.get(f"https://www.g2a.com/search?query={game_name.replace(' ', '+')}")
    cookie_clicker(driver)
    time.sleep(10)


def login(driver, username, password):
    """Open G2A and login"""
    driver.get("https://id.g2a.com/login")
    time.sleep(1)

    cookie_clicker(driver)

    login_form = driver.find_element_by_class_name("form-box__form")
    email_field = login_form.find_element_by_css_selector("input[type='email']")
    password_field = login_form.find_element_by_css_selector("input[type='password']")

    email_field.send_keys(username)
    password_field.send_keys(password)

    # from: http://isaacviel.name/make-web-driver-wait-element-become-visiable/
    if EC.presence_of_element_located((By.TAG_NAME, "iframe")):
        # from: https://stackoverflow.com/questions/7534622/selecting-an-iframe-using-python-selenium
        driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
        recaptcha_checkbox = driver.find_element_by_class_name("recaptcha-checkbox-checkmark")
        recaptcha_checkbox.click()
        try:
            WebDriverWait(driver, 120).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "recaptcha-checkbox-checked"))
            )
        except selenium.common.exceptions.TimeoutException:
            driver.close()
            print("Selenium.Timeoutexception")
            sys.exit(0)

    driver.switch_to.default_content()
    login_button = driver.find_element_by_xpath("//button[text()='Log in']")
    login_button.click()
    time.sleep(3)


def cookie_clicker(driver):
    """Remove cookie popup"""
    confirm_button = driver.find_element_by_xpath('//button[contains(text(), "Confirm")]')
    confirm_button.click()


if __name__ == "__main__":
    app()
