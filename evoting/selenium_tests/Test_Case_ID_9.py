# Test_Case_ID_9.py 

"""
Title: Event Owner Creates Vote Event with all correct values

Descriptions:
Test the system to be able to create a new vote event record into the system database by providing the correct field values. 
After the vote event is created successfully, users will be redirected to the homepage with reflected changes. 

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
driver.find_element(By.NAME, "eventTitle").send_keys("Vote Event Name 1")
driver.find_element(By.NAME, "startDate").send_keys("13032023")
driver.find_element(By.NAME, "startTime").send_keys("1200")
driver.find_element(By.NAME, "endDate").send_keys("17032023")
driver.find_element(By.NAME, "endTime").send_keys("1500")
driver.find_element(By.NAME, "eventQuestion").send_keys("Vote Question 1")

driver.find_element(By.CSS_SELECTOR, 'span.options_and_file span.fields:nth-child(2) input').send_keys("Option 1A")
driver.find_element(By.CSS_SELECTOR, 'span.options_and_file span.fields:nth-child(3) input').send_keys("Option 1B")

driver.find_element(By.NAME, "voterEmail").send_keys(os.getcwd() + "/participant_csv_1.csv")

# submit the create form 
driver.find_element(By.ID, "submit_vote_event_btn").click()
WebDriverWait(driver, timeout=100).until(lambda driver : driver.title == "Overview")

assert driver.current_url == "http://127.0.0.1:8000/evoting/eventowner/homepage"

driver.quit()