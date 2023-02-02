# Test_Case_ID_35.py 

"""
Title: Voter Casts a vote on the vote event successfully

Descriptions:
Test the system’s ability to accept the voter casted vote and record it into the system database correctly.

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
driver.get("http://127.0.0.1:8000/harpocryption/voter/vote?auth=HsCEGsZ9mT6tDJvgGxYloya59ycwwOQcIm2hPlfJPtxZvXiMOklXbYrAH52Y3beB")

WebDriverWait(driver, timeout=100).until(lambda driver : driver.title == "Voting Booth")

# select the Option 5-2
options = driver.find_elements(By.CSS_SELECTOR, "form label.options")
for option in options:
	if "Option 5-2" in option.get_attribute("innerHTML"):
		option.click()

driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()

driver.implicitly_wait(10)
ack_message = driver.find_element(By.CSS_SELECTOR, "div#vote_acknowledge_page p").text

assert ack_message == "We have received you casted vote option. Thank you !"

print("Integration Test 35 Passed !")

driver.quit()