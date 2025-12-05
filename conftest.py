import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import os


@pytest.fixture
def driver(request):
    """Start and yield a Chrome WebDriver, then quit afterward."""
    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # Uncomment to run without opening browser window

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)

    request.node.driver = driver
    yield driver
    driver.quit()


# ⛔ Automatic screenshot capture + embed in HTML report
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook called after each test phase to attach screenshot on failure."""
    outcome = yield
    rep = outcome.get_result()

    # Only act if the test failed
    if rep.when == "call" and rep.failed:
        driver = getattr(item, "driver", None)
        if driver:
            # Create screenshots folder
            os.makedirs("screenshots", exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            test_name = item.name.replace("/", "_").replace("\\", "_")
            screenshot_path = os.path.join("screenshots", f"{test_name}_{timestamp}.png")

            # Save screenshot
            driver.save_screenshot(screenshot_path)
            print(f"\n📸 Screenshot saved: {screenshot_path}")

            # Attach screenshot to pytest-html report
            if hasattr(rep, "extra"):
                from pytest_html import extras
                rep.extra.append(extras.image(screenshot_path))
