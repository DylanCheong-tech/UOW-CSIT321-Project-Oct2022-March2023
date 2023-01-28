# Test_Case_ID_24.py 

"""
Title: Event Owner Updates Vote Event in Published (PB) with uploading some invalid email address in csv file

Descriptions:
Test the system to be able to identify the invalid email address in the csv file. 
The system will append the new valid email addresses and ignore the non-valid email addresses. 

Test data “participant_csv_6.csv” will be located in the same directory with this test script
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
driver.get("http://127.0.0.1:8000/evoting/eventowner/login")

# fill in the form data 
driver.find_element(By.NAME, "email").send_keys("jamessmith@mail.com")
driver.find_element(By.NAME, "password").send_keys("JamesSmith_1234")

# submit the login form
driver.find_element(By.ID, "form_submit_btn").click()
WebDriverWait(driver, timeout=100).until(lambda driver : driver.title == "Overview")

# navigate to the update vote event page
rows = driver.find_elements(By.CSS_SELECTOR, "table tr:not(.header) td:nth-child(2)")
for index, row in zip(range(len(rows)), rows):
	if row.get_attribute("innerHTML") == "Vote Event Title 2":
		buttons = driver.find_elements(By.CSS_SELECTOR, "table tr:nth-child(" + str(index + 1 + 1) + ") td:nth-child(6) button")
		buttons[2].click()
		break
WebDriverWait(driver, timeout=100).until(lambda driver : driver.title == "Update Vote Event")

# fill in the form data
driver.find_element(By.NAME, "endDate").send_keys("18112024")
driver.find_element(By.NAME, "endTime").send_keys("1800")

driver.find_element(By.NAME, "voterEmail").send_keys(os.getcwd() + "/participant_csv_6.csv")

# submit the create form 
driver.find_element(By.ID, "submit_vote_event_btn").click()

WebDriverWait(driver, timeout=100).until(lambda driver : driver.title == "Overview")

# navigate to the update vote event page
rows = driver.find_elements(By.CSS_SELECTOR, "table tr:not(.header) td:nth-child(2)")
for index, row in zip(range(len(rows)), rows):
	if row.get_attribute("innerHTML") == "Vote Event Title 5":
		buttons = driver.find_elements(By.CSS_SELECTOR, "table tr:nth-child(" + str(index + 1 + 1) + ") td:nth-child(6) button")
		buttons[0].click()
		break

WebDriverWait(driver, timeout=100).until(lambda driver : driver.title == "View Vote Events")

enrolled_namelist = [
	"John Smith","john-smith@mail.com",
	"David Brown","david-brown@mail.com",
	"Susan Jones","susan-jones@mail.com",
	"Michael Scott","michael-scoot@mail.com",
	"Ivan Leu","ivan-leu@mail.com",
	"Isabel Martin","isabel-martin@mail.com",
	"Sophie Paul", "loara-paul@mail.com",
	"Jonathan Brown","jonathan-brown@mail.com"
]

table_contents = driver.find_elements(By.CSS_SELECTOR, "table tr td")
for column in table_contents:
	assert column.get_attribute("innerHTML") in enrolled_namelist

print("Integration Test 24 Passed !")

driver.quit()