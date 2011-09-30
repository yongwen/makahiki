from selenium import selenium
import unittest, time, re

class test_event(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", "http://localhost:8000/")
        self.selenium.start()
    
    def test_test_event(self):
        sel = self.selenium
	sel.open("/account/login/")
        sel.type("id=id_username", "testbot")
        sel.type("id=id_password", "testbot")
        sel.click("css=input[type=\"submit\"]")
        sel.wait_for_page_to_load("10001")
        sel.open("/admin/")
        sel.click("//div[@id='content-main']/div[2]/table/tbody/tr/th/a")
        sel.wait_for_page_to_load("30000")
        sel.click("link=Attend Blue Planet Foundation Meeting")
        sel.wait_for_page_to_load("30000")
        sel.type("id=id_event_date_0", "2013-08-27")
        sel.click("name=_save")
        sel.wait_for_page_to_load("30000")
        sel.open("/activities/?ref=nav-button")
        sel.click("css=a[title=\"Blue Planet\"] > h3")
        sel.wait_for_page_to_load("30000")
        sel.click("//div[@id='activity-task-details-content']/center[2]/center/a/button")
        sel.wait_for_page_to_load("30000")
        sel.click("css=h3")
        self.assertEqual("34", sel.get_text("css=#header-user-overall-rank2 > #header-user-points > h3"))
        sel.click("id=task-reminder-button")
        sel.click("id=id_send_text")
        sel.click("id=id_text_number")
        sel.type("id=id_text_number", "111")
        sel.click("id=task-reminder-form-submit")
        time.sleep(3)
        try: self.failUnless(sel.is_text_present("A valid phone number is required"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id=id_text_number", "")
        sel.click("//div[@id='activity-task-stats-content']/p[5]")
        sel.click("id=id_text_number")
        sel.type("id=id_text_number", "111-111-1111")
        sel.click("id=task-reminder-form-submit")
        sel.wait_for_page_to_load("30000")
        sel.click("id=task-reminder-button")
        try: self.assertEqual("111-111-1111", sel.get_value("id=id_text_number"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("id=task-reminder-form-cancel")
        sel.open("/admin/")
        sel.click("//div[@id='content-main']/div[2]/table/tbody/tr/th/a")
        sel.wait_for_page_to_load("30000")
        sel.click("link=Attend Blue Planet Foundation Meeting")
        sel.wait_for_page_to_load("30000")
        sel.click("css=p.datetime > span.datetimeshortcuts > a")
        sel.type("id=id_event_date_1", "0:00:01")
        sel.click("name=_save")
        sel.wait_for_page_to_load("30000")
        sel.open("/activities/")
        sel.click("id=activity-categories-title")
        sel.click("link=Blue Planet")
        sel.wait_for_page_to_load("30000")
        sel.click("css=p > a > button")
        sel.click("id=id_response")
        sel.type("id=id_response", "atte-expn2")
        sel.click("css=#activity-task-form-content-button > button")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("54", sel.get_text("css=#header-user-floor-rank3 > #header-user-points > h3"))
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
