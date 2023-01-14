# Test_Case_ID_1.py 

"""
Title: Event Owner Create Account with correct field and OTP values

Descriptions:
Test the system to be able successfully create an account when the correct data is provided. 
The data provided will be matching the respective field data type and requirement, (such as email) and numeric value for OTP

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

driver.get("http://127.0.0.1:8000/evoting/eventowner/createaccount")

# fill in the form data 
driver.find_element(By.NAME, "firstname").send_keys("James")
driver.find_element(By.NAME, "lastname").send_keys("Smith")
driver.find_element(By.NAME, "email").send_keys("cheongwaihong44@gmail.com")
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

# If success the application will redirect to the login page
WebDriverWait(driver, timeout=100).until(lambda driver : driver.title != "Sign Up")
assert driver.current_url == "http://127.0.0.1:8000/evoting/eventowner/login"

driver.quit()