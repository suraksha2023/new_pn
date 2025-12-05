import os
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def snap(driver, step_name):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs("screenshots", exist_ok=True)
    file_path = os.path.join("screenshots", f"{step_name}_{timestamp}.png")
    driver.save_screenshot(file_path)

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
        self.url = "https://uc3.netiapps.net/login"

    def login(self, username, password):
        self.driver.get(self.url)
        self.wait.until(EC.presence_of_element_located((By.ID, "email"))).clear()
        self.driver.find_element(By.ID, "email").send_keys(username)
        self.driver.find_element(By.ID, "password").clear()
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "loginBtn").click()
        snap(self.driver, f"login_{username}")

    def logout(self):
        self.driver.get("https://uc3.netiapps.net/home")
        wait = WebDriverWait(self.driver, 10)

        # Wait for and click the user drop-down button (adjust letter 'M' if different)
        user_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                               "//a[contains(@class, 'dropdown-toggle')]//div[contains(@class, 'rounded-circle')]")))
        user_dropdown.click()

        # Wait for and click the logout button
        logout_button = wait.until(EC.element_to_be_clickable((By.ID, "logoutBtn")))
        logout_button.click()

        snap(self.driver, "logout")

