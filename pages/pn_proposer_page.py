import os
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def snap(driver, step_name):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs("screenshots", exist_ok=True)
    file_path = os.path.join("screenshots", f"{step_name}_{timestamp}.png")
    driver.save_screenshot(file_path)
    print(f"📸 Screenshot saved: {file_path}")


class SOPProposerPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    def create_new_document(self, title, file_path):
        """Creates and submits a new SOP document."""
        try:
            # Step 1: Navigate
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//label[text()='Back to Dashboard']"))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//i[@class='bi bi-file-earmark-text nav-icon']"))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Under-Review Docs']"))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='btn btn-primary']"))).click()
            snap(self.driver, "new_doc_opened")

            # Step 2: Fill form
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@id='action'])[1]"))).click()
            Select(self.wait.until(EC.element_to_be_clickable((By.ID, "document_type")))).select_by_value("2")
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@name='sub_product_type'])[2]"))).click()
            Select(self.wait.until(EC.element_to_be_clickable((By.ID, "department")))).select_by_value("19")
            Select(self.wait.until(EC.element_to_be_clickable((By.ID, "sub_department")))).select_by_value("48")
            snap(self.driver, "dropdowns_selected")

            # Step 3: Fill title and upload file
            title_element = self.wait.until(EC.visibility_of_element_located((By.ID, "title")))
            title_element.clear()
            title_element.send_keys(title)
            snap(self.driver, "title_entered")

            file_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='document']")))
            file_input.send_keys(file_path)
            snap(self.driver, "file_uploaded")

            Select(self.wait.until(EC.element_to_be_clickable((By.ID, "assign_approver")))).select_by_value("DUM00519")

            # Step 4: Scroll to and submit document
            submit_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='toReview']")))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
            time.sleep(1)  # allow scroll to settle
            self.driver.execute_script("arguments[0].click();", submit_btn)
            snap(self.driver, "submitted")

            # Step 5: Handle popup safely
            time.sleep(3)
            print("⏳ Waiting for confirmation popup...")

            try:
                swal_locator = (By.XPATH, "//button[contains(@class, 'swal2-confirm') and contains(@class, 'swal2-styled')]")
                popup = self.wait.until(EC.visibility_of_element_located(swal_locator))
                snap(self.driver, "popup_visible")

                ok_button_locator = (By.XPATH, "//button[contains(@class, 'swal2-confirm')]")
                self.wait.until(EC.element_to_be_clickable(ok_button_locator)).click()
                self.wait.until(EC.invisibility_of_element(ok_button_locator))
                snap(self.driver, "popup_closed")

                print("✅ Popup handled successfully!")

            except Exception:
                print("⚠️ No popup appeared or popup locator mismatch — continuing test.")

            print("✅ Document submitted successfully!")

        except Exception as e:
            print(f"❌ Error occurred: {e}")
            snap(self.driver, "failure_step")
            raise
