# Test_Case_ID_21.py 

"""
Title: Event Owner Confirms Vote Event in Pending Confirmation (PC) Status

Descriptions:
Test the system to be able to change the status of the vote event into “Published” (PB) and generate all the relevant information for the vote event. 

When the vote event is confirmed, the system will generate the following items:
- Authentication String Token for each Voter 
- Cryptographic keys and salt value for the vote event 
- Encoding value for each of the vote options 

The system will send out the invitation email to each of the registered voters through their mailbox. 

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

updated_event_status = ""

# navigate to the update vote event page
rows = driver.find_elements(By.CSS_SELECTOR, "table tr:not(.header) td:nth-child(2)")
for index, row in zip(range(len(rows)), rows):
	if row.get_attribute("innerHTML") == "Vote Event Title 1":
		buttons = driver.find_elements(By.CSS_SELECTOR, "table tr:nth-child(" + str(index + 1 + 1) + ") td:nth-child(6) button")
		buttons[3].click()
		driver.implicitly_wait(5)
		driver.find_element(By.ID, "confirm_btn").click()
		driver.implicitly_wait(0)
		updated_event_status = driver.find_elements(By.CSS_SELECTOR, "table tr:nth-child(" + str(index + 1 + 1) + ") td:nth-child(5)")[0].text
		break

assert updated_event_status == "Published"

print("Integration Test 21 Passed !")

driver.quit()