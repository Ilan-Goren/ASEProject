# Assert: Only by vaild queen number input, url changes

import pytest, time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Configure WebDriver for this test module
@pytest.fixture(scope="session")
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

    button_go = browser.find_element(By.XPATH, "//*[contains(@class, 'btn') and contains(@class, 'btn-success')]")


def test_input_then_solve(browser):
    # Open target homepage
    browser.get("http://127.0.0.1:8000/")
    time.sleep(1)
    
    # Locate input box and buttons
    input_box = browser.find_element(By.ID, "id_n")
    button_solve = browser.find_element(By.XPATH, "//*[contains(@class, 'btn') and contains(@class, 'btn-primary')]")

    # Define test input set
    test_values = [-1, 0, 1, 2, 3, 21]

    # Try input values
    for value in test_values:
        # Clear input box and type in value
        input_box.clear()
        input_box.send_keys(str(value))

        # Click button
        button_solve.click()

        # Wait to see if URL changing
        try:
            browser.implicitly_wait(5)
            assert browser.current_url == "http://127.0.0.1:8000/"
        except TimeoutError:
            pytest.fail(f"System crashed down.")
    
def test_input_then_go(browser):
    # Open target homepage
    browser.get("http://127.0.0.1:8000/")
    time.sleep(1)
    
    # Locate input box and buttons
    input_box = browser.find_element(By.ID, "id_n")
    button_go = browser.find_element(By.XPATH, "//*[contains(@class, 'btn') and contains(@class, 'btn-success')]")

    # Define test input set
    test_values = [-1, 0, 1, 2, 3, 21]

    # Try input values
    for value in test_values:
        # Clear input box and type in value
        input_box.clear()
        input_box.send_keys(str(value))

        # Click button
        button_go.click()

        # Wait to see if URL changing
        try:
            browser.implicitly_wait(5)
            assert browser.current_url == "http://127.0.0.1:8000/"
        except TimeoutError:
            pytest.fail(f"System crashed down.")