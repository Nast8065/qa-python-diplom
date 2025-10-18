import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


# Глобальная переменная для отслеживания добавленных опций
_OPTIONS_ADDED = False


def pytest_addoption(parser):
    """Добавляем кастомные опции только один раз"""
    global _OPTIONS_ADDED

    if _OPTIONS_ADDED:
        return

    parser.addoption("--browser", action="store", default="chrome",
                    help="browser to run tests: chrome or firefox")
    parser.addoption("--headless", action="store_true",
                    help="run tests in headless mode")

    _OPTIONS_ADDED = True


@pytest.fixture
def browser():
    """Простая фикстура с автоматическим управлением драйверами"""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    # Selenium 4 автоматически управляет драйверами
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)

    yield driver
    driver.quit()

@pytest.fixture
def browser(request):
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    driver = None

    try:
        if browser_name == "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-gpu")
            options.add_experimental_option('excludeSwitches', ['enable-logging'])

            # Используем webdriver-manager с последней версией
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=options
            )

        elif browser_name == "firefox":
            # Временно отключаем Firefox из-за проблем с совместимостью
            pytest.skip("Firefox временно отключен из-за проблем с драйверами")
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

        driver.implicitly_wait(10)
        driver.maximize_window()

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
    """Фикстура для главной страницы"""
    from pages.main_page import MainPage
    page = MainPage(browser)
    page.open()
    page.wait_for_main_page_loaded()
    return page


@pytest.fixture
def login_page(browser):
    """Фикстура для страницы логина"""
    from pages.login_page import LoginPage
    return LoginPage(browser)


@pytest.fixture
def order_feed_page(browser):
    """Фикстура для страницы ленты заказов"""
    from pages.order_feed_page import OrderFeedPage
    page = OrderFeedPage(browser)
    page.open()
    page.wait_for_page_loaded()
    return page


@pytest.fixture
def order_modal(browser):
    """Фикстура для модального окна заказа"""
    from pages.order_modal import OrderModal
    return OrderModal(browser)


@pytest.fixture
def authenticated_user(main_page, login_page):
    """Фикстура для авторизованного пользователя"""
    # Используем тестовые данные
    test_email = "test@example.com"
    test_password = "password123"

    # Переходим на страницу логина
    main_page.click_personal_account()

    # Выполняем логин
    login_page.enter_email(test_email)
    login_page.enter_password(test_password)
    login_page.click_login_button()

    # Ждем загрузки главной страницы после логина
    main_page.wait_for_main_page_loaded()

    return main_page


# Вспомогательные классы для тестовых данных
class DataGenerator:
    def __init__(self):
        import random
        import string
        self.random = random
        self.string = string

    def generate_email(self):
        username = ''.join(self.random.choices(self.string.ascii_lowercase, k=8))
        domain = ''.join(self.random.choices(self.string.ascii_lowercase, k=6))
        return f"test_{username}@{domain}.com"

    def generate_password(self):
        return ''.join(self.random.choices(self.string.ascii_letters + self.string.digits, k=10))

    def generate_name(self):
        return ''.join(self.random.choices(self.string.ascii_letters, k=10))


@pytest.fixture
def data_generator():
    return DataGenerator()


@pytest.fixture
def user_data(data_generator):
    return {
        "email": data_generator.generate_email(),
        "password": data_generator.generate_password(),
        "name": data_generator.generate_name()
    }


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для создания скриншотов при падении тестов"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        try:
            browser = item.funcargs.get('browser')
            if browser:
                allure.attach(
                    browser.get_screenshot_as_png(),
                    name="screenshot_on_failure",
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception:
            pass

@pytest.fixture
def mock_main_page():
    """Mock фикстура для главной страницы"""
    mock_page = Mock()
    mock_page.open.return_value = mock_page
    mock_page.wait_for_main_page_loaded.return_value = True
    mock_page.click_constructor.return_value = mock_page
    mock_page.click_order_feed.return_value = mock_page
    mock_page.click_personal_account.return_value = mock_page
    mock_page.click_ingredient.return_value = mock_page
    mock_page.is_ingredient_modal_visible.return_value = True
    mock_page.add_ingredient_to_constructor.return_value = mock_page
    mock_page.get_ingredient_counter.return_value = "1"
    mock_page.click_make_order.return_value = mock_page
    mock_page.create_test_order.return_value = mock_page
    mock_page.is_constructor_active.return_value = True
    mock_page.is_order_feed_active.return_value = False
    mock_page.click_buns_section.return_value = mock_page
    mock_page.click_sauces_section.return_value = mock_page
    mock_page.click_fillings_section.return_value = mock_page
    mock_page.is_buns_section_active.return_value = True
    mock_page.is_sauces_section_active.return_value = False
    mock_page.is_fillings_section_active.return_value = False
    return mock_page


@pytest.fixture
def mock_order_feed_page():
    """Mock фикстура для ленты заказов"""
    mock_page = Mock()
    mock_page.open.return_value = mock_page
    mock_page.wait_for_page_loaded.return_value = True
    mock_page.get_total_orders_count.return_value = 150
    mock_page.get_today_orders_count.return_value = 25
    mock_page.get_orders_in_progress.return_value = ["12345", "12346"]
    mock_page.get_all_visible_orders.return_value = ["12345", "12346", "12347", "12348"]
    mock_page.is_order_in_feed.return_value = True
    mock_page.refresh_order_counters.return_value = mock_page
    return mock_page


@pytest.fixture
def mock_order_modal():
    """Mock фикстура для модального окна"""
    mock_modal = Mock()
    mock_modal.is_modal_visible.return_value = True
    mock_modal.close_modal.return_value = True
    mock_modal.get_order_number.return_value = "12345"
    mock_modal.get_ingredient_name.return_value = "Test Ingredient"
    return mock_modal


@pytest.fixture
def mock_login_page():
    """Mock фикстура для страницы логина"""
    mock_page = Mock()
    mock_page.enter_email.return_value = mock_page
    mock_page.enter_password.return_value = mock_page
    mock_page.click_login_button.return_value = mock_page
    mock_page.complete_login.return_value = mock_page
    mock_page.is_login_form_present.return_value = True
    return mock_page
