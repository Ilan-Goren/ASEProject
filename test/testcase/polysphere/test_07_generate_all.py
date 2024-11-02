# target: any button related to generate all possible solutions
# method: go to all pages that has a generate all solutions then press to check

from ..utils.glob import *

# configure
@pytest.fixture(scope="function")
def browser():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()

# running this test might crash your computer, so marked dangerous
# this test will not be runned unless modifying the start_test.sh
@pytest.mark.dangerous
def test_07_generate_all(browser):
    for target_button_domain in [polysphere_page_url, polysphere_solution_page_url]:
        # which means we are directly going to the solution without solving it ourselves
        if target_button_domain == polysphere_page_url:
            # open polysphere page
            browser.get(polysphere_page_url)
            time.sleep(1)
    
            # find "Generate all possible solutions"
            try:
                button_polysphere_generate_all_possible = browser.find_element(By.XPATH, button_polysphere_generate_all_possible_xpath_selector)
            except NoSuchElementException:
                pytest.fail("can not find element: button_polysphere_generate_all_possible")

            # click "Generate all possible solutions" button
            button_polysphere_generate_all_possible.click()
            time.sleep(1)

            # should be capable of seeing "Solutions found" on the page
            # find elements in the refreshed solution page
            try:
                h3_feedback = browser.find_element(By.XPATH, f"//h3[contains(text(), 'Solutions found')]")
                continue
            except NoSuchElementException:
                pytest.fail("can not find element: h3_feedback")

            # which means we are testing after trying to solve the puzzle
            if target_button_domain == polysphere_solution_page_url:
                # open polysphere solution page
                browser.get(polysphere_solution_page_url)
                time.sleep(1)
    
                # find the "Show all possible solutions for my board" button
                try:
                    button_polysphere_show_all_solutions = browser.find_element(By.XPATH, button_polysphere_show_all_solutions_xpath_selector)
                except NoSuchElementException:
                    pytest.fail("can not find element: button_polysphere_show_all_solutions")

                # click "Show all possible solutions for my board" button
                button_polysphere_show_all_solutions.click()
                time.sleep(1)
                
                # since we have not placed any pieces yet, we should get a warning
                # find the warning "You have to place at least one piece!"
                try:
                    alert_place_piece = browser.find_element(By.XPATH, "//div[@role='alert']")
                except NoSuchElementException:
                    pytest.fail("can not find element: alert_place_piece")

                # find "Reset" button
                try:
                    button_polyshpere_reset_puzzle = browser.find_element(By.XPATH, button_polyshpere_reset_puzzle_xpath_selector)
                except NoSuchElementException:
                    pytest.fail("can not find element: button_polyshpere_reset_puzzle")

                # press "Reset" to get init state
                button_polyshpere_reset_puzzle.click()
                time.sleep(1)

                # get the draggable pieces list
                draggable_pieces_list = browser.find_elements(By.XPATH, "//div[@class='piece']")

                # randomly choose one piece
                piece_choosen = random.choice(draggable_pieces_list)

                # find the target cell in the table
                target_cell = browser.find_element(By.XPATH, "//table/tbody/tr[3]/td[6]")

                # drag the piece into target cell
                actions = ActionChains(browser)
                actions.drag_and_drop(piece_choosen, target_cell).perform()
                # this time sleep might not be enough
                time.sleep(5)

                # find the solution number in h5 label
                h5_solution_element = driver.find_element(By.XPATH, "//form[@class='mb']//h5")

                # record the h5 content before calculations
                before_action_content = h5_solution_element.text

                # click "Show all possible solutions for my board" button
                button_polysphere_show_all_solutions.click()
                
                # WARNING: this is a extremely time consuming task
                # And it might crash your server...
                # avoid doing such test using docker, that is extremely unworthwhile
                time.sleep(900)

                # record the h5 content after calculations
                after_action_content = h5_solution_element.text

                assert before_action_content == after_action_content   