# Test_Case_ID_2.py 

"""
Title: Session Management - Login Session Termination After Logout 

Descriptions:
Test the system to be able to terminate the logged in session after the user performs the logout. 
After the login session is terminated, there is no way to access the authentication needed resources from the system. 

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

# logout the system
driver.find_element(By.ID, "logout_btn").click()

# direct access the homepage
driver.get("http://127.0.0.1:8000/harpocryption/eventowner/homepage")

# assert the redirection 
assert driver.current_url == "http://127.0.0.1:8000/harpocryption/eventowner/login"

print("Security Test 2 Passed !")

driver.quit()