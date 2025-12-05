import time

from pages.login_page import LoginPage
from pages.pn_proposer_page import SOPProposerPage
from pages.pn_recommender_page import SOPRecommenderPage
from pages.pn_approver_page import SOPApproverPage
from pages.pn_proposer_verapproval import SOPProposerApproval
from pages.pn_published import SOPPublishPage


def test_sop_full_flow(driver):
    """End-to-End SOP Approval Flow: loops through all approvers and proposer verification."""

    login = LoginPage(driver)
    proposer = SOPProposerPage(driver)
    reviewer = SOPRecommenderPage(driver)
    approver = SOPApproverPage(driver)
    proposerapproval = SOPProposerApproval(driver)  # ✅ instantiated correctly
    publisher = SOPPublishPage(driver)
    #
    sop_title = "SOP_AutoTest_04"
    sop_file = "/home/suraksha/Downloads/Correct_Doc.pdf.docx"
    #
    # # Uncomment if proposer & reviewer steps are needed
    login.login("DUM39995", "123456789")
    proposer.create_new_document(sop_title, sop_file)
    time.sleep(5)
    login.logout()

    login.login("DUM42711", "123456789")
    reviewer.review_document(sop_title)
    login.logout()

    # 🧑‍⚖️ Approvers Loop
    approvers = [
        ("DUM20670", "123456789"),
        ("DUM48265", "123456789"),
        ("DUM17968", "123456789"),
        ("DUM23160", "123456789"),
        ("DUM50338", "123456789"),
        ("DUM18466", "123456789"),
        ("DUM21980", "123456789"),
    ]

    for username, password in approvers:
        print(f"👤 Approver login: {username}")
        login.login(username, password)
        approver.open_and_approve_from_last_page(sop_title)
        login.logout()

    print("✅ All approvers completed successfully")

    # 🧾 Proposer Final Approval
    login.login("DUM39995", "123456789")
    proposerapproval.open_and_approve(sop_title)
    login.logout()



    publisher.publisherlogin("DUMSA002", "123456789")
    publisher.open_and_approve(sop_title)
    login.logout()

    print(
        "🎉 End-to-End SOP Flow completed successfully (Proposer → Reviewer → Approvers → Final Proposer Verification → Published)")
