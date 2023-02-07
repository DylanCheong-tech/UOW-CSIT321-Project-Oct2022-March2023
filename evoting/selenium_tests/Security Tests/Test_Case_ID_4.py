# Test_Case_ID_4.py 

"""
Title: Password Management - Register an account with compliance to the Password Policy

Descriptions:
Test the system to be able check the password rules when registering a new user. 
The system should validate the password via the backend (views file)

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
driver.get("http://127.0.0.1:8000/harpocryption/eventowner/createaccount")

# fill in the form data 
driver.find_element(By.NAME, "firstname").send_keys("James")
driver.find_element(By.NAME, "lastname").send_keys("Smith")
driver.find_element(By.NAME, "email").send_keys("james-smith@gmail.com")
driver.find_element(By.ID,"otp_request_btn").click()

gender = Select(driver.find_element(By.NAME, "gender"))
gender.select_by_value("M")

driver.find_element(By.NAME, "password").send_keys("JamesSmith_123456")
driver.find_element(By.NAME, "repeat_password").send_keys("JamesSmith_123456")

# fill in the otp manually
# implement the explicitly wait to listen the otp inputs
WebDriverWait(driver, timeout=100).until(lambda driver : len(driver.find_element(By.NAME, "otp").get_attribute("value")) == 6 )

# submit the webform 
driver.find_element(By.ID, "form_submit_btn").click()

# assert the redirection 
assert driver.current_url == "http://127.0.0.1:8000/harpocryption/eventowner/login"

print("Security Test 4 Passed !")

driver.quit()