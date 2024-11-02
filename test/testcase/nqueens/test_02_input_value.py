# target: input box in the middle
# method: enter out of range numbers, then press the 2 buttons, check if url changes

from ..utils.glob import *

# configure
@pytest.fixture(scope="function")
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# test
def test_02_input_value(browser):
    # url change times counter
    url_change_time = 0

    # open home page
    browser.get(home_page_url)

    # wait
    time.sleep(1)

    # find N Queens puzzle-title
    try:
        nqueens_title = browser.find_element(By.XPATH, nqueens_title_xpath_selector)
    except NoSuchElementException:
        pytest.fail("can not find element: nqueens_title")

    # set a hover waiting for the real nav button
    nav_nqueens_hover = ActionChains(browser).move_to_element(nqueens_title)
    nav_nqueens_hover.perform()

    # waiting for nav_nqueens_button show up
    nav_nqueens_button = WebDriverWait(browser, 3).until(
        EC.presence_of_element_located((By.XPATH, nqueens_navbar_xpath_selector))
    )

    # click navigate to nqueens page 
    nav_nqueens_button.click()

    # wait for browser response
    time.sleep(5)

    # locate input box and buttons
    try:
        input_box = browser.find_element(By.ID, input_box_id_selector)
    except NoSuchElementException:
        pytest.fail("can not find element: input_box")

    try:
        button_solve_it_yourself = browser.find_element(By.XPATH, button_nqueens_solve_it_yourself_xpath_selector)
    except NoSuchElementException:
        pytest.fail("can not find element: button_solve_it_yourself")

    try:
         button_go_to_solution = browser.find_element(By.XPATH, button_nqueens_go_to_solution_xpath_selector)
    except NoSuchElementException:
        pytest.fail("can not find element: button_go_to_solution")

    # define test numbers list
    test_value_list = ["test_string", -1, 0, 1, 2, 3, 4.5, 8.99, 21, 9999999]

    # try input values
    for value in test_value_list:
        # clear input box and type in value
        input_box.clear()
        input_box.send_keys(str(value))

        # first click "solve it your self"
        button_solve_it_yourself.click()

        # wait to see if url changing
        time.sleep(5)

        # check if url changed after pressing "solve it your self"
        current_url = browser.current_url
        if current_url != nqueens_page_url:
            url_change_time += 1
        
        # then click "go to solution"
        button_go_to_solution.click()

        # wait to see if url changing
        time.sleep(5)

        # check if url changed after pressing "go to solution"
        current_url = browser.current_url
        if current_url != nqueens_page_url:
            url_change_time += 1

    # if url changing happened, case fail
    assert url_change_time == 0