import time
import pytest
from utilities.data_access import read_pn_data
from pages.login_page import LoginPage
from pages.pn_proposer_page import SOPProposerPage
from pages.pn_recommender_page import SOPRecommenderPage
from pages.pn_approver_page import PNApproverPage
from pages.pn_proposer_verapproval import SOPProposerApproval
from pages.pn_published import SOPPublishPage

# Load Excel data once
raw_pn_data = read_pn_data("data/pn_data.xlsx")

# Keep only valid rows
pn_data = [
    row for row in raw_pn_data
    if row
    and row.get("role")
    and row.get("username")
    and row.get("password")
    and row.get("sop_title")
]

# Approver roles exactly as in Excel (Approver1..Approver6)
approver_roles = [f"Approver{i}" for i in range(1, 7)]

@pytest.mark.parametrize("data", pn_data)
def test_sop_full_flow_ddt(driver, data):
    login = LoginPage(driver)
    proposer = SOPProposerPage(driver)
    recommender = SOPRecommenderPage(driver)
    approver = PNApproverPage(driver)
    proposer_approval = SOPProposerApproval(driver)
    publisher = SOPPublishPage(driver)

    # Extract fields from the current row
    role = data["role"]
    username = data["username"]
    password = data["password"]
    sop_title = data["sop_title"]
    sop_file = data.get("file_path")  # only Proposer row will have this

    print(f"\n🔹 Running step for {role} ({username})")

    login.login(username, password)

    if role == "Proposer":
        proposer.create_new_document(sop_title, sop_file)
    elif role == "Recommender":
        recommender.find_document_across_pages(sop_title)
    elif role in approver_roles:
        approver.open_and_approve_from_last_page(sop_title)
    elif role == "Proposer_Verification":
        proposer_approval.open_and_approve(sop_title)
    elif role == "Publisher":
        publisher.open_and_approve(sop_title)
    else:
        pytest.skip(f"⚠️ Unknown role type: {role}")

    login.logout()
    time.sleep(3)
