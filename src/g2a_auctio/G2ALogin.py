import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import selenium
from selenium import webdriver


class G2ALogin:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome("chromedriver.exe")

    def login(self):
        driver = self.driver
        driver.set_window_size(1800, 1200)
        driver.get(
            "https://id.g2a.com/auth/auth/?client_id=g2a&redirect_uri=https%3A%2F%2Fwww.g2a.com%2Foauth2%2Ftoken&response_type=code")

        username_field = driver.find_element_by_name("username")
        password_field = driver.find_element_by_name("password")

        username_field.send_keys(self.username)
        password_field.send_keys(self.password)

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
        loginButton = driver.find_element_by_xpath("//button[text()='Log in']")
        loginButton.click()
        time.sleep(3)

    def goToSellingPage(self):
        driver = self.driver
        driver.get("https://www.g2a.com/marketplace/customer/addproduct/")


# g2ALogin = G2ALogin(sys.argv[1],sys.argv[2])
# g2ALogin.login()

