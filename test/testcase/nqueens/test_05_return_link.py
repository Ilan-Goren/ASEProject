# target: href link at the buttom
# method: click the link then check current url

import pytest, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# global variables
homepage_url = "http://127.0.0.1:8000/"
link_xpath_selector = "//footer//a[1]"

# configure
@pytest.fixture(scope="function")
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_05_return_link(browser):
    # open target homepage
    browser.get(homepage_url)
    time.sleep(1)
    
    # find link
    try:
        link = browser.find_element(By.XPATH, "//footer//a[1]")
    except NoSuchElementException:
        pytest.fail("can not find element: input_box")

    # click link
    link.click()

    # wait
    time.sleep(1)

    # check current url
    currnet_url = browser.current_url
    assert currnet_url == homepage_url