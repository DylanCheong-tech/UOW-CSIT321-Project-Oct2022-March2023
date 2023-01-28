# Test_Case_ID_3.py 

"""
Title: Session Management - Login Session max age and idle time

Descriptions:
Test the system to be able to logout the user when the idle time is larger than the predefined login session max age.  
When the idle time is longer than the predefined login session max age, the user will be logged out and need to log in again to be able access the system resource again. 

"""
import os 
from threading import Timer 
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

# wait for 10 minutes 
timeout_task = Timer(10 * 60, lambda : driver.refresh())
timeout_task.start()

WebDriverWait(driver, timeout=11 * 60).until(lambda driver : driver.title == "Event Owner Login")

# assert the redirection 
assert driver.current_url == "http://127.0.0.1:8000/evoting/eventowner/login"

print("Security Test 3 Passed !")

driver.quit()