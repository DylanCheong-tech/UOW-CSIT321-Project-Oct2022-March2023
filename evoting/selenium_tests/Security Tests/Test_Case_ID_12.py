# Test_Case_ID_12.py 

"""
Title: Access Control - Perform the view operation on the non-owned vote event object 

Descriptions:
Test the system to be able check the ownership of the vote event before allowing the user to perform the view on it. 
When the user tries to access the non-owned vote event, the system should be redirecting the user to the homepage. 

In this test case, terms “Event Owner A” and “Event Owner B” will be denoted as two different User Account entities. 

Before executing this security test, the vote event test data is loaded into the system database. 

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

driver.get("http://127.0.0.1:8000/evoting/eventowner/viewevent/78")

# assert the redirection 
assert driver.current_url == "http://127.0.0.1:8000/evoting/eventowner/homepage"

driver.quit()