import pytest
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="browser to run tests: chrome or firefox")
    parser.addoption("--headless", action="store_true", help="run tests in headless mode")

@pytest.fixture
def browser(request):
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    driver = None
    try:
        if browser_name == "chrome":
            options = Options()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-gpu")
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=options
            )
        elif browser_name == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=options
            )
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

        driver.implicitly_wait(10)
        driver.set_page_load_timeout(30)
        driver.set_script_timeout(30)

        yield driver

    except Exception as e:
        pytest.fail(f"Browser setup failed: {str(e)}")
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass

@pytest.fixture
def main_page(browser):
    from pages.main_page import MainPage
    page = MainPage(browser)
    page.open()
    return page

@pytest.fixture
def order_feed_page(browser):
    from pages.order_feed_page import OrderFeedPage
    page = OrderFeedPage(browser)
    page.open()
    return page

@pytest.fixture
def order_modal(browser):
    from pages.order_modal import OrderModal
    return OrderModal(browser)

@pytest.fixture
def constructor_page(browser):
    from pages.constructor_page import ConstructorPage
    page = ConstructorPage(browser)
    page.open()
    return page

@pytest.fixture
def login_page(browser):
    from pages.login_page import LoginPage
    page = LoginPage(browser)
    page.open()
    return page

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        try:
            browser = item.funcargs.get('browser')
            if browser:
                screenshot_dir = "screenshots"
                os.makedirs(screenshot_dir, exist_ok=True)
                screenshot_path = os.path.join(screenshot_dir, f"{item.name}.png")
                browser.save_screenshot(screenshot_path)
        except Exception:
            pass
