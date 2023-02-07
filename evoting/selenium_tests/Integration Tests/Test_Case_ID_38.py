# Test_Case_ID_38.py 

"""
Title: Voter views vote event’s final result through an invalid link

Descriptions:
Test the system’s ability to identify validation of the voter authentication information before releasing out the final result information to the user. 

The system will check against the voter authentication information and the vote event status before providing the final result information to the user. 

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
driver.get("http://127.0.0.1:8000/harpocryption/voter/vote?auth=7PM4qrm0HhMPXWLAvky594b96zuLNtxZ5h5eOP1ciD4eOfTuH2rl9DFYxHhAaVuX")

error_message = driver.find_element(By.ID, "error_message").text

assert driver.title == "Error"
assert error_message == "Vote Event Has Not Started !"

print("Integration Test 38 Passed !")

driver.quit()