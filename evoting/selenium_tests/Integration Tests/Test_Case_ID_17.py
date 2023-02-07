# Test_Case_ID_17.py 

"""
Title: Event Owner Updates Vote Event in Pending Confirmation (PC) with less than two vote options 

Descriptions:
Test the system to be able raise an error when no sufficient vote options are provided. 
At least two vote options need to be provided. 

Test data “participant_csv_3.csv” will be located in the same directory with this test script
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
	if row.get_attribute("innerHTML") == "Vote Event Title 2":
		buttons = driver.find_elements(By.CSS_SELECTOR, "table tr:nth-child(" + str(index + 1 + 1) + ") td:nth-child(6) button")
		buttons[2].click()
		break
WebDriverWait(driver, timeout=100).until(lambda driver : driver.title == "Update Vote Event")

# fill in the form data
driver.find_element(By.NAME, "eventTitle").clear()
driver.find_element(By.NAME, "eventTitle").send_keys("New Vote Event Name 2")
driver.find_element(By.NAME, "startDate").send_keys("13032023")
driver.find_element(By.NAME, "startTime").send_keys("1200")
driver.find_element(By.NAME, "endDate").send_keys("15032023")
driver.find_element(By.NAME, "endTime").send_keys("1800")
driver.find_element(By.NAME, "eventQuestion").clear()
driver.find_element(By.NAME, "eventQuestion").send_keys("New Vote Question 2")

driver.find_element(By.CSS_SELECTOR, 'span.options_and_file span.fields:nth-child(2) input').clear()
driver.find_element(By.CSS_SELECTOR, 'span.options_and_file span.fields:nth-child(2) input').send_keys("Option 2C")
# remove the second input box
driver.execute_script("""
	let second_option_input = document.querySelector("span.options_and_file span.fields:nth-child(3) input");
	second_option_input.remove()
""")

driver.find_element(By.NAME, "voterEmail").send_keys(os.getcwd() + "/participant_csv_3.csv")

# submit the create form 
driver.find_element(By.ID, "submit_vote_event_btn").click()

error_msg_ele = driver.find_element(By.CSS_SELECTOR, "p.error_msg")

# Assert the Error Message
assert error_msg_ele.get_attribute("innerHTML") == "At Least Two Vote Options Are Needed !"

print("Integration Test 17 Passed !")

driver.quit()