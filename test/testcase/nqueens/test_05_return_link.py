# target: href link at the buttom
# method: click the link then check current url

from ..utils.glob import *

# configure
@pytest.fixture(scope="function")
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_05_return_link(browser):
    # open target page
    browser.get(nqueens_page_url)
    time.sleep(1)
    
    # find link
    try:
        link = browser.find_element(By.XPATH, "//footer//a[1]")
    except NoSuchElementException:
        pytest.fail("can not find element: link")

    # click link
    link.click()

    # wait
    time.sleep(1)

    # check current url should be home page
    currnet_url = browser.current_url
    assert currnet_url == home_page_url