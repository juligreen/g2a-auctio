from selenium import webdriver


def execute_this_shit():
    """Start main function to manage G2A"""
    driver = webdriver.Chrome()
    # create a new Firefox session
    driver.implicitly_wait(30)
    driver.maximize_window()

    # Navigate to the application home page
    driver.get("http://www.G2A.com")


if __name__ == '__main__':
    execute_this_shit()
