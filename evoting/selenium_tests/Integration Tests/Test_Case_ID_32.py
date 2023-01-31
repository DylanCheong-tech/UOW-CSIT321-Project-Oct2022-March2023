# Test_Case_ID_32.py 

"""
Title: Voter Access Vote Event Platform through an Invalid Invitation Link without any vote casting attempted before. 

Descriptions:
Test the system’s ability to verify the voter information correctly and the access constraints before providing the access of the voting platform to the voter. 

The system will be checking the following constraints:
	1. Vote Event is in status of Published (PB)
	2. Voter has not been voted before, no double voting allowed 

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
driver.get("http://127.0.0.1:8000/evoting/voter/vote?auth=HsCEGsZ9mT6tDJvgGxYloya59ycwwOQcIm2hPlfJPtxZvXiMOklopsXbH52Y3beB")

error_message = driver.find_element(By.ID, "error_message").text

assert driver.title == "Error"
assert error_message == "Voter Information Not Founded !"

print("Integration Test 32 Passed !")

driver.quit()