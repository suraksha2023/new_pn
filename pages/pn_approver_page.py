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
    print(f"📸 Screenshot: {file_path}")


from selenium.common.exceptions import TimeoutException

class PNApproverPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    def open_and_approve_from_last_page(self, title):
        driver = self.driver

        # Step 1 – Navigate to Under-Review Docs
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@class='switch-menu']"))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//i[@class='bi bi-file-earmark-text nav-icon']"))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Under-Review Docs']"))).click()
        snap(driver, "under_review_docs_opened")
        time.sleep(2)

        # Step 2 – Try pagination (if present)
        try:
            pagination = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ul.pagination"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", pagination)
            time.sleep(1)

            page_links = pagination.find_elements(
                By.XPATH, ".//li[not(contains(@class,'disabled'))]/a"
            )

            if len(page_links) >= 2:
                last_page_link = page_links[-2]
                driver.execute_script("arguments[0].scrollIntoView(true);", last_page_link)
                driver.execute_script("arguments[0].click();", last_page_link)
                print("➡️ Navigated to the last page of pagination.")
                time.sleep(3)
            else:
                print("⚠️ Only one page or no numeric pagination; using current page.")
        except TimeoutException:
            print("ℹ️ No pagination found; using current page only.")

        snap(driver, "last_page_opened")

        # Step 3 – Locate the LAST document with given title on current page
        try:
            # Wait until at least one row/link is present in the list/table
            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//table//tr | //div[contains(@class,'table')]/descendant::a")
                )
            )

            # Use 'contains' to be more flexible with text
            all_docs = driver.find_elements(
                By.XPATH, f"//a[contains(normalize-space(.), '{title}')]"
            )
            print(f"DEBUG: found {len(all_docs)} links containing '{title}'")

            if not all_docs:
                print(f"❌ No document containing title '{title}' found on current page.")
                snap(driver, "no_doc_found_current_page")
                return

            pn_doc = all_docs[-1]
            driver.execute_script("arguments[0].scrollIntoView(true);", pn_doc)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", pn_doc)
            print(f"📄 Opened last document containing title: {title}")
            snap(driver, "sop_document_opened")

        except TimeoutException:
            print(f"❌ Timed out waiting for any document rows/links for '{title}'.")
            snap(driver, "timeout_waiting_for_docs")
            return

        # Step 4 – Approve flow (unchanged)
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        approve_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Approve')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", approve_btn)
        driver.execute_script("arguments[0].click();", approve_btn)
        snap(driver, "approve_button_clicked")

        tick = self.wait.until(EC.element_to_be_clickable((By.ID, "accept_doc")))
        tick.click()
        ok_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "acceptToProposer")))
        ok_btn.click()
        snap(driver, "approval_popup_closed")

        print(f"✅ PN '{title}' approved successfully!")
