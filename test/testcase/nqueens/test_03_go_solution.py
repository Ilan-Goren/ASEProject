# target: get solution buttoms in the solution pages
# method: loop valid queen number to get solutions

from ..utils.glob import *

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
        for target_button_domain in [nqueens_page_url, nqueens_solution_page_url]:
            # which means we are directly going to the solution without solving it ourselves
            if target_button_domain == nqueens_page_url:
                # open nqueens page
                # Note: it seems this project does not require some login or prerequist stuff
                #       so, jut directly visit the nqueens page it seems to be fine...
                browser.get(nqueens_page_url)

                # wait
                time.sleep(1)
    
                # locate input box in homepage
                try:
                    input_box = browser.find_element(By.ID, input_box_id_selector)
                except NoSuchElementException:
                    pytest.fail("can not find element: input_box")

                # locate button in homepage
                try:
                    button_go_to_solution = browser.find_element(By.XPATH, button_nqueens_go_to_solution_xpath_selector)
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
                if current_url != nqueens_solution_page_url:
                    pytest.fail("can not switch to solution page")

                # find elements in the refreshed solution page
                try:
                    h3_solution_title = browser.find_element(By.XPATH, f"//h3[contains(text(), 'Here is a solution')]")
                    continue
                except NoSuchElementException:
                    pytest.fail("can not find element: h3_solution_title")

            # which means we are testing after trying to solve the puzzle
            if target_button_domain == nqueens_solution_page_url:
                # open target homepage
                browser.get(nqueens_page_url)

                # wait
                time.sleep(1)
    
                # locate input box in homepage
                try:
                    input_box = browser.find_element(By.ID, input_box_id_selector)
                except NoSuchElementException:
                    pytest.fail("can not find element: input_box")

                # locate button in homepage
                try:
                    button_solve_it_yourself = browser.find_element(By.XPATH, button_nqueens_solve_it_yourself_xpath_selector)
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
                if current_url != nqueens_solution_page_url:
                    pytest.fail("can not switch to solution page")

                # locate button in the solution page
                try:
                    button_get_a_possible_solution = browser.find_element(By.XPATH, button_nqueens_get_a_possible_solution_xpath_selector)
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