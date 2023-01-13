# Test_Case_ID_13.py 

"""
Title: Event Owner Creates Vote Event with uploading some invalid email address in csv file

Descriptions:
Test the system to be able to identify the invalid email address in the csv file. 
The system will enroll all the valid emails and ignore the invalid emails. 

Test data “participant_csv_2.csv” will be located in the same directory with this test script
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

# navigate to the create vote event page
driver.find_element(By.ID, "create_vote_event_btn").click()
WebDriverWait(driver, timeout=100).until(lambda driver : driver.title == "Create New Vote Event" )


# fill in the form data
driver.find_element(By.NAME, "eventTitle").send_keys("Vote Event Name 5")
driver.find_element(By.NAME, "startDate").send_keys("10032023")
driver.find_element(By.NAME, "startTime").send_keys("1300")
driver.find_element(By.NAME, "endDate").send_keys("12032023")
driver.find_element(By.NAME, "endTime").send_keys("1500")
driver.find_element(By.NAME, "eventQuestion").send_keys("Vote Question 5")

driver.find_element(By.CSS_SELECTOR, 'span.options_and_file span.fields:nth-child(2) input').send_keys("Option 5A")
driver.find_element(By.CSS_SELECTOR, 'span.options_and_file span.fields:nth-child(3) input').send_keys("Option 5B")

driver.find_element(By.NAME, "voterEmail").send_keys(os.getcwd() + "/participant_csv_2.csv")

# submit the create form 
driver.find_element(By.ID, "submit_vote_event_btn").click()
WebDriverWait(driver, timeout=100).until(lambda driver : driver.title == "Overview")

driver.find_element(By.CSS_SELECTOR, 'div#vote_events table tr:last-child td.buttons_col button:nth-child(1)').click()
WebDriverWait(driver, timeout=100).until(lambda driver : driver.title == "View Vote Events")

enrolled_namelist = [
	"Ivan Leu","ivan-leu@mail-csit.com",
	"Darren","darren@gmaol.com",
	"David Brown","david-brown@mail.com"
]

table_contents = driver.find_elements(By.CSS_SELECTOR, "table tr td")
for column in table_contents:
	assert column.get_attribute("innerHTML") in enrolled_namelist

driver.quit()