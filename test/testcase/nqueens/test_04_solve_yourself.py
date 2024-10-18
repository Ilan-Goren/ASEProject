# target: chess board in the solution pages
# method: loop valid queen number to try incorrect solutions

import pytest, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# global variables
homepage_url = "http://127.0.0.1:8000/"
solutionpage_url = "http://127.0.0.1:8000/solution/"

input_box_id_selector = "id_n"
button_solve_it_yourself_xpath_selector = "//*[contains(@class, 'btn') and contains(@class, 'btn-primary')]"
button_check_your_solution_xpath_selector = "//*[contains(@class, 'btn') and contains(@class, 'btn-primary') and contains(@class, 'mt-3')]"
table_chess_board_xpath_selector = "//table[@id='nqueens-board']"

# configure
@pytest.fixture(scope="function")
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# test
def test_04_solve_yourself(browser):
    # loop 4-20 chess board, give incorrect layouts

    # Bug issue: for queen_number in range >10 might happen:
    #            button unclickable, guess it is because overlap?

    for queen_number in [4, 6, 8, 10]:
        # open target homepage
        browser.get(homepage_url)

        # wait
        time.sleep(1)

        # locate input box in homepage
        try:
            input_box = browser.find_element(By.ID, input_box_id_selector)
        except NoSuchElementException:
            pytest.fail("can not find element: input_box")

        # locate button in homepage
        try:
            button_solve_it_yourself = browser.find_element(By.XPATH, button_solve_it_yourself_xpath_selector)
        except NoSuchElementException:
            pytest.fail("can not find element: button_solve_it_yourself")

        # input queen number
        input_box.send_keys(str(queen_number))

        # press "go to solution"
        button_solve_it_yourself.click()

        # wait
        time.sleep(5)

        # should switch to solution page, check current url
        current_url = browser.current_url
        if current_url != solutionpage_url:
            pytest.fail("can not switch to solution page")

        # find chess table in the refreshed solution page
        try:
            table_chess_board = browser.find_element(By.XPATH, table_chess_board_xpath_selector)
        except NoSuchElementException:
            pytest.fail("can not find element: table_chess_board")

        # find button "check your solution" in the refreshed solution page
        try:
            button_check_your_solution = browser.find_element(By.XPATH, button_check_your_solution_xpath_selector)
        except NoSuchElementException:
            pytest.fail("can not find element: button_check_your_solution")

        # fullfill the chess board
        queen_location_list = table_chess_board.find_elements(By.TAG_NAME, "td")

        for possible_queen_location in queen_location_list:
            possible_queen_location.click()
            time.sleep(0.5)

        # click "check your solution"
        button_check_your_solution.click()

        # wait
        time.sleep(5)

        # should switch to home page, check current url
        current_url = browser.current_url
        if current_url != homepage_url:
            pytest.fail("can not switch to home page")

        # suppose to find the feedback div
        try:
            div_feedback = browser.find_element(By.XPATH, "//div[contains(@class, 'alert') and @role='alert']")
        except NoSuchElementException:
            pytest.fail("browser feedback not found")

    assert True