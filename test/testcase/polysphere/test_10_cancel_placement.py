# target: the cell, before and after a piece is placed
# method: try moving a random piece to a cell then click the cell again

from ..utils.glob import *

# configure
@pytest.fixture(scope="function")
def browser():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()

#test
def test_10_cancel_placement(browser):
    # open polysphere page
    browser.get(polysphere_page_url)
    time.sleep(1)

    # find "Go to puzzle" button
    try:
        button_polysphere_go_to_puzzle = browser.find_element(By.XPATH, button_polysphere_go_to_puzzle_xpath_selector)
        print("1")
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

    # find the target cells in the table
    try:
        target_cell = browser.find_element(By.XPATH, "//table/tbody/tr[3]/td[6]")
    except NoSuchElementException:
        pytest.fail("can not find element: target_cell")

    # get the draggable pieces list
    draggable_pieces_list_init = browser.find_elements(By.XPATH, "//div[@class='piece']")

    # get a draggable piece
    piece = random.choice(draggable_pieces_list_init)

    # dragge the piece to the cell
    ActionChains(browser).drag_and_drop(piece, target_cell).perform()
    time.sleep(1)

    # record the state of the cell
    cell_state_after_placement = target_cell.text
 
    # click the cell again
    target_cell.click()
    time.sleep(1)
    cell_state_after_cancel = target_cell.text

    assert cell_state_after_placement != cell_state_after_cancel