# Test_Case_ID_8.py 

"""
Title: Event Owner Logout with success

Descriptions:
Test the system to be able to logout the user from the logged in session. 

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

# login the user first 
driver.get("http://127.0.0.1:8000/harpocryption/eventowner/login")

# fill in the form data 
driver.find_element(By.NAME, "email").send_keys("jamessmith@mail.com")
driver.find_element(By.NAME, "password").send_keys("JamesSmith_1234")

# submit the webform 
driver.find_element(By.ID, "form_submit_btn").click()

# after login and get redirect to the homepage, perform the logout 
driver.find_element(By.ID, "logout_btn").click()

# Assert the application will redirect to the login page
WebDriverWait(driver, timeout=100).until(lambda driver : driver.title != "Home Page")
assert driver.current_url == "http://127.0.0.1:8000/harpocryption/eventowner/login"

print("Integration Test 8 Passed !")

driver.quit()