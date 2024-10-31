# target: chess icon on the top
# method: click the icon then check current url

from ..utils.glob import *

# configure
@pytest.fixture(scope="function")
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# test
def test_01_nav_icon(browser):
    # open home page
    browser.get(home_page_url)
    time.sleep(1)
    
    # find chess icon
    try:
        icon = browser.find_element(By.CSS_SELECTOR, chess_icon_css_selector)
    except NoSuchElementException:
        pytest.fail("can not find element: icon")

    # click chess icon
    icon.click()

    # wait
    time.sleep(1)

    # check current url
    current_url = browser.current_url

    assert current_url == home_page_url