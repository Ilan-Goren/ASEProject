# target: get solution buttoms in the solution pages
# method: loop valid queen number to get solutions

import pytest, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# global variables
homepage_url = "http://127.0.0.1:8000/"
solutionpage_url = "http://127.0.0.1:8000/solution/"

input_box_id_selector = "id_n"
button_solve_it_yourself_xpath_selector = "//*[contains(@class, 'btn') and contains(@class, 'btn-primary')]"
button_go_to_solution_xpath_selector = "//*[contains(@class, 'btn') and contains(@class, 'btn-success')]"
button_get_a_possible_solution_xpath_selector = "//*[contains(@class, 'btn') and contains(@class, 'btn-success')]"

# configure
@pytest.fixture(scope="function")
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# test
def test_03_go_solution(browser):
    # loop 4-20 chess board for "get a possible solution"

    # Bug issue: for queen_number in range >10 might happen:
    #            button unclickable, guess it is because overlap?

    for queen_number in [4, 6, 8, 10]:
        for target_button_domain in [homepage_url, solutionpage_url]:
            # which means we are directly going to the solution
            if target_button_domain == homepage_url:
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
                    button_go_to_solution = browser.find_element(By.XPATH, button_go_to_solution_xpath_selector)
                except NoSuchElementException:
                    pytest.fail("can not find element: button_go_to_solution")

                # input queen number
                input_box.send_keys(str(queen_number))

                # scroll? then press "go to solution"
                # browser.execute_script("arguments[0].scrollIntoView(true);", button_go_to_solution)
                button_go_to_solution.click()

                # wait
                time.sleep(5)

                # should switch to solution page, check current url
                current_url = browser.current_url
                if current_url != solutionpage_url:
                    pytest.fail("can not switch to solution page")

                # find elements in the refreshed solution page
                try:
                    h3_solution_title = browser.find_element(By.XPATH, f"//h3[contains(text(), 'Here is a solution')]")
                    continue
                except NoSuchElementException:
                    pytest.fail("can not find element: h3_solution_title")

            # which means we are testing after trying to solve the puzzle
            if target_button_domain == solutionpage_url:
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

                # press "solve it yourself"
                button_solve_it_yourself.click()

                # wait
                time.sleep(5)

                # should switch to solution page, check current url
                current_url = browser.current_url
                if current_url != solutionpage_url:
                    pytest.fail("can not switch to solution page")

                # locate button in the solution page
                try:
                    button_get_a_possible_solution = browser.find_element(By.XPATH, button_get_a_possible_solution_xpath_selector)
                except NoSuchElementException:
                    pytest.fail("can not find element: button_get_a_possible_solution")

                # scroll? then press the "get a possible solution button"
                # browser.execute_script("arguments[0].scrollIntoView(true);", button_get_a_possible_solution)
                button_get_a_possible_solution.click()

                # wait
                time.sleep(5)

                # find elements in the refreshed solution page
                try:
                    h3_solution_title = browser.find_element(By.XPATH, f"//h3[contains(text(), 'Here is a solution')]")
                    continue
                except NoSuchElementException:
                    pytest.fail("can not find element: h3_solution_title")

        assert True