import os
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def snap(driver, step_name):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs("screenshots", exist_ok=True)
    file_path = os.path.join("screenshots", f"{step_name}_{timestamp}.png")
    driver.save_screenshot(file_path)
    print(f"📸 Screenshot saved: {file_path}")


class SOPProposerApproval:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    def open_and_approve(self, title):
        """Goes to Under-Review Docs → jumps to last page → finds SOP by title → approves."""
        driver = self.driver

        # Step 1️⃣ Navigate to Under-Review Docs
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@class='switch-menu']"))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//i[@class='bi bi-file-earmark-text nav-icon']"))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Under-Review Docs']"))).click()
        snap(driver, "under_review_docs_opened")

        time.sleep(2)

        # Step 2️⃣ Click second-last pagination button (last numeric page)
        pagination = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.pagination")))
        driver.execute_script("arguments[0].scrollIntoView(true);", pagination)
        time.sleep(1)

        page_links = pagination.find_elements(By.XPATH, ".//li[not(contains(@class,'disabled'))]/a")

        if len(page_links) < 2:
            print("⚠️ Only one page found, staying on current page.")
        else:
            last_page_link = page_links[-2]
            driver.execute_script("arguments[0].scrollIntoView(true);", last_page_link)
            driver.execute_script("arguments[0].click();", last_page_link)
            print("➡️ Navigated to the last page of pagination.")
            time.sleep(3)

        snap(driver, "last_page_opened")

        # Step 3️⃣ Locate the document by title
        try:
            sop_doc = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//a[normalize-space(text())='{title}']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", sop_doc)
            driver.execute_script("arguments[0].click();", sop_doc)
            print(f"📄 Opened document titled: {title}")
            snap(driver, "sop_document_opened")
        except:
            print(f"❌ Document titled '{title}' not found on last page.")
            return

        # Step 4️⃣ Approve flow
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        self.wait.until(EC.element_to_be_clickable((By.ID, "page_no_confirmation"))).click()
        time.sleep(5)
        version_input = self.wait.until(EC.element_to_be_clickable((By.ID, "version_no")))
        version_input.clear()
        version_input.send_keys("2")
        effective_date = self.wait.until(EC.presence_of_element_located((By.ID, "effective_date")))
        driver.execute_script("arguments[0].value = arguments[1];", effective_date, "2025-11-06")

        approved_date = self.wait.until(EC.presence_of_element_located((By.ID, "approved_on")))
        driver.execute_script("arguments[0].value = arguments[1];", approved_date, "2025-11-06")

        summary = self.wait.until(EC.element_to_be_clickable((By.ID, "summary_changes")))
        summary.send_keys("all ok")
        time.sleep(5)

        to_publisher_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "toPublisher")))
        driver.execute_script("arguments[0].scrollIntoView(true);", to_publisher_btn)
        driver.execute_script("arguments[0].click();", to_publisher_btn)
        snap(driver, "proposer_final_approval_done")

        print(f"✅ Final Proposer approved SOP '{title}' successfully!")
