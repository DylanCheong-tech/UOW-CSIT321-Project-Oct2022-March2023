# Test_Case_ID_44.py 

"""
Title: Voter Accesses Final Result booth when private key file is missing

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

# direct access the voting booth 
driver.get("http://127.0.0.1:8000/harpocryption/voter/finalresult?auth=tpOF3CwS0oZJXN2GabLDjXnoun7c0Nw6m9gaqbIUzLtzzHfIRnKcALBTjGZnpq4k")

WebDriverWait(driver, timeout=100).until(lambda driver : driver.title == "Error")

error_message = driver.find_element(By.ID, "error_message").text

assert error_message == "Private Key Information Lost !"

print("Integration Test 44 Passed !")

driver.quit()