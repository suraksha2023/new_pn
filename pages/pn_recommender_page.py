import os
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def snap(driver, step_name):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs("screenshots", exist_ok=True)
    file_path = os.path.join("screenshots", f"{step_name}_{timestamp}.png")
    driver.save_screenshot(file_path)
    print(f"📸 Screenshot saved: {file_path}")

class SOPRecommenderPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    def find_document_across_pages(self, title):
        driver = self.driver

        # Step 1️⃣ - Navigate to Under Review Docs
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@class='switch-menu']"))).click()
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//i[@class='bi bi-file-earmark-text nav-icon']"))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Under-Review Docs']"))).click()
        snap(self.driver, "under_review_docs_opened")

        time.sleep(2)

        # Step 2️⃣ - Locate pagination and click second-last page
        pagination = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.pagination")))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", pagination)
        time.sleep(1)

        # Find all clickable numbered page links
        page_links = pagination.find_elements(By.XPATH, ".//li[not(contains(@class,'disabled'))]/a")

        if len(page_links) < 2:
            print("⚠️ Only one page found, staying on current page.")
        else:
            # Click second-last link (the last numeric page)
            last_page_link = page_links[-2]
            self.driver.execute_script("arguments[0].scrollIntoView(true);", last_page_link)
            self.driver.execute_script("arguments[0].click();", last_page_link)
            print("➡️ Navigated to the last page of pagination.")
            time.sleep(3)

        snap(self.driver, "last_page_opened")

        # Step 3️⃣ - Try to locate document with given title
        try:
            sop_doc = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//a[normalize-space(text())='{title}']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", sop_doc)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", sop_doc)
            print(f"📄 Opened document titled: {title}")
            snap(self.driver, "sop_document_opened")
        except:
            print(f"❌ Document titled '{title}' not found on the last page.")
            return

        # Step 4️⃣ - Approve flow
        time.sleep(2)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        approve_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Approve')]"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", approve_btn)
        self.driver.execute_script("arguments[0].click();", approve_btn)
        snap(self.driver, "approve_button_clicked")

        # Tick confirmation and OK button
        tick = self.wait.until(EC.element_to_be_clickable((By.ID, "accept_doc")))
        tick.click()
        ok_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "acceptToApprover")))
        ok_btn.click()
        snap(self.driver, "approval_popup_closed")

        print(f"✅ SOP '{title}' approved successfully!")
