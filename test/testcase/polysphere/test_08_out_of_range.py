# target: the table border
# method: try moving a random piece to a corner

from ..utils.glob import *

# configure
@pytest.fixture(scope="function")
def browser():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()

#test
def test_08_out_of_range(browser):
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

    # get the draggable pieces list
    draggable_pieces_list = browser.find_elements(By.XPATH, "//div[@class='piece']")

    # randomly choose one piece
    piece_choosen = random.choice(draggable_pieces_list)

    # find the target cells in the table
    try:
        target_cell_left_top = browser.find_element(By.XPATH, "//table/tbody/tr[1]/td[1]")
    except NoSuchElementException:
        pytest.fail("can not find element: target_cell_left_top")

    try:
        target_cell_left_bottom = browser.find_element(By.XPATH, "//table/tbody/tr[5]/td[1]")
    except NoSuchElementException:
        pytest.fail("can not find element: target_cell_left_bottom")

    try:
        target_cell_right_top = browser.find_element(By.XPATH, "//table/tbody/tr[1]/td[11]")
    except NoSuchElementException:
        pytest.fail("can not find element: target_cell_right_top")

    try:
        target_cell_right_bottom = browser.find_element(By.XPATH, "//table/tbody/tr[5]/td[11]")
    except NoSuchElementException:
        pytest.fail("can not find element: target_cell_right_bottom")

    # dragge the piece to the cell
    actions = ActionChains(browser)

    for target_cell in [target_cell_left_top, target_cell_left_bottom, target_cell_right_top, target_cell_right_bottom]:
        actions.drag_and_drop(piece_choosen, target_cell).perform()
        time.sleep(1)

        try:
            # get the javascript alert
            alert = browser.switch_to.alert
            alert.accept()
            continue
        except NoAlertPresentException:
            pytest.fail("can not find element: alert")

    assert True