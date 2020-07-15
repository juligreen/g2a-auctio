"""Main Module to start managing G2A"""
import sys
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import typer


def execute_this_shit():
    """Main function to manage G2A,
    initialize driver and start later functions"""
    driver = webdriver.Chrome()
    driver.implicitly_wait(30)
    driver.maximize_window()
    # google_login(driver, 'test', 'test')
    login(driver, 'test', 'test')


def google_login(driver: webdriver.Chrome, google_mail, google_password):
    """Login to google first to make Captchas easier"""
    driver.get("https://www.google.com/accounts/Login")
    email_field = driver.find_element_by_css_selector(
        "input[type='email']")
    email_field.send_keys(google_mail)
    next = driver.find_element_by_id('identifierNext')
    next.click()
    time.sleep(1)
    password_field = driver.find_element_by_css_selector(
        "input[type='password']")
    password_field.send_keys(google_password)
    next = driver.find_element_by_id('passwordNext')
    next.click()


def login(driver, username, password):
    """Open G2A and login"""
    driver.get("https://id.g2a.com/login")
    time.sleep(1)

    cookie_clicker(driver)

    login_form = driver.find_element_by_class_name("form-box__form")
    email_field = login_form.find_element_by_css_selector(
        "input[type='email']")
    password_field = login_form.find_element_by_css_selector(
        "input[type='password']")

    email_field.send_keys(username)
    password_field.send_keys(password)

    # from: http://isaacviel.name/make-web-driver-wait-element-become-visiable/
    if EC.presence_of_element_located((By.TAG_NAME, "iframe")):
        # from: https://stackoverflow.com/questions/7534622/selecting-an-iframe-using-python-selenium
        driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
        recaptcha_checkbox = driver.find_element_by_class_name(
            "recaptcha-checkbox-checkmark")
        recaptcha_checkbox.click()
        try:
            WebDriverWait(driver, 120).until(
                EC.visibility_of_element_located(
                    (By.CLASS_NAME, "recaptcha-checkbox-checked"))
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
    buttons_div = driver.find_element_by_class_name('modal-options__buttons')
    confirm_button = buttons_div.find_element_by_class_name("btn-primary")
    confirm_button.click()


if __name__ == '__main__':
    typer.run(execute_this_shit)
