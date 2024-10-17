# Assert:  return_to_homepage href on-click return to homepage

import pytest, time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Configure WebDriver for this test module
@pytest.fixture(scope="module")
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_href_return_home(browser):
    # Open target homepage
    browser.get("http://127.0.0.1:8000/")
    time.sleep(1)
    
    # Click icon
    link = browser.find_element(By.XPATH, "//footer//a[1]")
    link.click()
    time.sleep(1)

    # Check current url
    url = browser.current_url
    assert url == "http://127.0.0.1:8000/", f"Expected URL: http://127.0.0.1:8000/."