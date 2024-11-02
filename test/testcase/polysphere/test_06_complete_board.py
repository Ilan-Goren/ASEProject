# target: test if init state is capable of getting completed
# method: route to the puzzle page and press "Complete my board"

from ..utils.glob import *

# configure
@pytest.fixture(scope="function")
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# test
def test_06_complete_board(browser):
    # open target page
    browser.get(polysphere_page_url)
    time.sleep(1)
    
    # find "Go to puzzle" button
    try:
        button_polysphere_go_to_puzzle = browser.find_element(By.XPATH, button_polysphere_go_to_puzzle_xpath_selector)
    except NoSuchElementException:
        pytest.fail("can not find element: button_polysphere_go_to_puzzle")

    # press the button and "Go to puzzle" page
    button_polysphere_go_to_puzzle.click()
    time.sleep(1)

    # find "Reset" button
    try:
        button_polysphere_reset_puzzle = browser.find_element(By.XPATH, button_polysphere_reset_puzzle_xpath_selector)
    except NoSuchElementException:
        pytest.fail("can not find element: button_polysphere_reset_puzzle")

    # press "Reset" to get init state
    button_polysphere_reset_puzzle.click()
    time.sleep(1)

    # find "Complete my board" button
    try:
        button_polysphere_complete_my_board = browser.find_element(By.XPATH, button_polysphere_complete_my_board_xpath_selector)
    except NoSuchElementException:
        pytest.fail("can not find element: button_polysphere_complete_my_board")

    # press "complete my board" to get solution
    button_polysphere_complete_my_board.click()
    time.sleep(1)

    # should detect "No piece left" on this page
    # find elements in the refreshed solution page
    try:
        h3_feedback = browser.find_element(By.XPATH, f"//h3[contains(text(), 'No pieces left.')]")
    except NoSuchElementException:
        pytest.fail("can not find element: h3_solution_title")

    assert True