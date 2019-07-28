from selenium import webdriver


def execute_this_shit():
    """Start main function to manage G2A"""
    driver = webdriver.Chrome()
    driver.set_window_size(1800, 1070)
    driver.get("www.G2A.com")


if __name__ == '__main__':
    execute_this_shit()
