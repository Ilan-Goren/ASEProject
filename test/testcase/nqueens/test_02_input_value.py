# target: input box in the middle
# method: enter out of range numbers, then press the 2 buttons, check if url changes

import pytest, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# global variables
homepage_url = "http://127.0.0.1:8000/"
input_box_id_selector = "id_n"
button_solve_xpath_selector = "//*[contains(@class, 'btn') and contains(@class, 'btn-primary')]"
button_go_xpath_selector = "//*[contains(@class, 'btn') and contains(@class, 'btn-success')]"

# configure
@pytest.fixture(scope="function")
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# test
def test_02_input_value(browser):
    # url change counter
    url_change_time = 0

    # open target homepage
    browser.get(homepage_url)

    # wait
    time.sleep(1)

    # locate input box and buttons
    try:
        input_box = browser.find_element(By.ID, input_box_id_selector)
    except NoSuchElementException:
        pytest.fail("can not find element: input_box")

    try:
        button_solve = browser.find_element(By.XPATH, button_solve_xpath_selector)
    except NoSuchElementException:
        pytest.fail("can not find element: button_solve")

    try:
         button_go = browser.find_element(By.XPATH, button_go_xpath_selector)
    except NoSuchElementException:
        pytest.fail("can not find element: button_go")

    # define test numbers list
    test_value_list = ["test_string", -1, 0, 1, 2, 3, 4.5, 8.99, 21, 9999999]

    # try input values
    for value in test_value_list:
        # clear input box and type in value
        input_box.clear()
        input_box.send_keys(str(value))

        # first click "solve it your self"
        button_solve.click()

        # wait to see if url changing
        time.sleep(5)

        # check if url changed after pressing "solve it your self"
        current_url = browser.current_url
        if current_url != homepage_url:
            url_change_time += 1
        
        # then click "go to solution"
        button_go.click()

        # wait to see if url changing
        time.sleep(5)

        # check if url changed after pressing "go to solution"
        current_url = browser.current_url
        if current_url != homepage_url:
            url_change_time += 1

    # if url changing happened, case fail
    assert url_change_time == 0