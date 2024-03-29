# Test_Case_ID_23.py 

"""
Title: Event Owner Updates Vote Event in Published (PB) status with invalid end datetime settings 

Descriptions:
Test the system to be able to identify the invalid end datetime when a user is trying to update a vote event with an ending datetime earlier than the starting datetime. 
When the user is trying to submit the vote event update form, the system will raise an error regarding the datetime invalid settings. 

Test data “participant_csv_5.csv” will be located in the same directory with this test script
"""
import os 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# wait strategy 
from selenium.webdriver.support.wait import WebDriverWait

# Locator 
from selenium.webdriver.common.by import By

# UI Select Interaction
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# login to the system
driver.get("http://127.0.0.1:8000/harpocryption/eventowner/login")

# fill in the form data 
driver.find_element(By.NAME, "email").send_keys("jamessmith@mail.com")
driver.find_element(By.NAME, "password").send_keys("JamesSmith_1234")

# submit the login form
driver.find_element(By.ID, "form_submit_btn").click()
WebDriverWait(driver, timeout=100).until(lambda driver : driver.title == "Overview")

# navigate to the update vote event page
rows = driver.find_elements(By.CSS_SELECTOR, "table tr:not(.header) td:nth-child(2)")
for index, row in zip(range(len(rows)), rows):
	if row.get_attribute("innerHTML") == "Vote Event Title 4":
		buttons = driver.find_elements(By.CSS_SELECTOR, "table tr:nth-child(" + str(index + 1 + 1) + ") td:nth-child(6) button")
		buttons[2].click()
		break
WebDriverWait(driver, timeout=100).until(lambda driver : driver.title == "Update Vote Event")

# fill in the form data
driver.find_element(By.NAME, "endDate").send_keys("01022024")
driver.find_element(By.NAME, "endTime").send_keys("1200")

driver.find_element(By.NAME, "voterEmail").send_keys(os.getcwd() + "/participant_csv_5.csv")

# submit the create form 
driver.find_element(By.ID, "submit_vote_event_btn").click()

error_msg_ele = driver.find_element(By.CSS_SELECTOR, "p.error_msg")

# Assert the Error Message
assert error_msg_ele.get_attribute("innerHTML") == "Date Time Settings Invalid !"

print("Integration Test 23 Passed !")

driver.quit()