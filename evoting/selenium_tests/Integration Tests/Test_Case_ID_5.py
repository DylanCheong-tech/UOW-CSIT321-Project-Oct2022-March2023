# Test_Case_ID_5.py 

"""
Title: Event Owner Login with correct email and password value

Descriptions:
Test the system to be able identify the registered user with the correct credentials provided. 

"""

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

driver.get("http://127.0.0.1:8000/harpocryption/eventowner/login")

# fill in the form data 
driver.find_element(By.NAME, "email").send_keys("jamessmith@mail.com")
driver.find_element(By.NAME, "password").send_keys("JamesSmith_1234")

# submit the webform 
driver.find_element(By.ID, "form_submit_btn").click()

# If success the application will redirect to the homepgae page
WebDriverWait(driver, timeout=100).until(lambda driver : driver.title != "Event Owner Login")
assert driver.current_url == "http://127.0.0.1:8000/harpocryption/eventowner/homepage"

print("Integration Test 5 Passed !")

driver.quit()