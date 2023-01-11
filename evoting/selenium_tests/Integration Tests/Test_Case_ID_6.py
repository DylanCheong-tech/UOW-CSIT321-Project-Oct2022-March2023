# Test_Case_ID_6.py 

"""
Title: Event Owner Login with incorrect email value

Descriptions:
Test the system to be able identify the not registered user when providing the incorrect email value. 

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

driver.get("http://127.0.0.1:8000/evoting/eventowner/login")

# fill in the form data 
driver.find_element(By.NAME, "email").send_keys("noaccount@mail.com")
driver.find_element(By.NAME, "password").send_keys("JamesSmith_123456")

# submit the webform 
driver.find_element(By.ID, "form_submit_btn").click()

error_msg_ele = driver.find_element(By.CSS_SELECTOR, "p.error_msg")

# Assert the Error Message
assert error_msg_ele.get_attribute("innerHTML") == "Incorrect Credentials"

driver.quit()