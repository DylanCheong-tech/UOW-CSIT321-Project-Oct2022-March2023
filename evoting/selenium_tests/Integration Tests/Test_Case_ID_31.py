# Test_Case_ID_31.py 

"""
Title: Voter Access Vote Event Platform through a Valid Invitation Link without any vote casting attempted before

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
driver.get("http://127.0.0.1:8000/harpocryption/voter/vote?auth=qokRHOjNLpuq6OzvIYZ1vrZgBURrey7c6LnmJc3xub6nZhDK3E1X2CQAsdSExVps")

assert driver.title == "Voting Booth"

print("Integration Test 31 Passed !")

driver.quit()