# Test_Case_ID_40.py 

"""
Title: Event Owner Updates Vote Event when private key file is missing 

Descriptions:
Test the system to be able to provide and display the vote event information correctly. Test the system’s ability to handle the error when the required private keys information is not found. 

The system should be able to catch the error and display the “Server Internal Error” to the end user instead of system halts. 

Make sure the private keys file (.private) is removed when executing this test cases. 

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

# direct access the update page
driver.get("http://127.0.0.1:8000/harpocryption/eventowner/updateevent/3")

WebDriverWait(driver, timeout=100).until(lambda driver : driver.title == "Error")

error_message = driver.find_element(By.ID, "error_message").text

assert error_message == "Private Key Information Lost !"

print("Integration Test 40 Passed !")

driver.quit()