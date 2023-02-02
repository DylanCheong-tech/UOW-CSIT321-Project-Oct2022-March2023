# Test_Case_ID_12.py 

"""
Title: Event Owner Creates Vote Event with less than two vote options 

Descriptions:
Test the system to be able raise an error when no sufficient vote options are provided. 
At least two vote options need to be provided. 

Test data “participant_csv_1.csv” will be located in the same directory with this test script
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

# navigate to the create vote event page
driver.find_element(By.ID, "create_vote_event_btn").click()
WebDriverWait(driver, timeout=100).until(lambda driver : driver.title == "Create New Vote Event" )


# fill in the form data
driver.find_element(By.NAME, "eventTitle").send_keys("Vote Event Name 4")
driver.find_element(By.NAME, "startDate").send_keys("15032023")
driver.find_element(By.NAME, "startTime").send_keys("1300")
driver.find_element(By.NAME, "endDate").send_keys("17032023")
driver.find_element(By.NAME, "endTime").send_keys("1800")
driver.find_element(By.NAME, "eventQuestion").send_keys("Vote Question 4")

driver.find_element(By.CSS_SELECTOR, 'span.options_and_file span.fields:nth-child(2) input').send_keys("Option 4A")
# remove the second input box
driver.execute_script("""
	let second_option_input = document.querySelector("span.options_and_file span.fields:nth-child(3) input");
	second_option_input.remove()
""")

driver.find_element(By.NAME, "voterEmail").send_keys(os.getcwd() + "/participant_csv_1.csv")

# submit the create form 
driver.find_element(By.ID, "submit_vote_event_btn").click()

error_msg_ele = driver.find_element(By.CSS_SELECTOR, "p.error_msg")

# Assert the Error Message
assert error_msg_ele.get_attribute("innerHTML") == "At Least Two Vote Options Are Needed !"

print("Integration Test 12 Passed !")

driver.quit()