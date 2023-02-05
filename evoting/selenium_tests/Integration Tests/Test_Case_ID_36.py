# Test_Case_ID_36.py 

"""
Title: Voter views the published vote event’s final result through a valid link

Descriptions:
Test the system’s ability to release the computed vote event’s final result to the participated voter. 

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
driver.get("http://127.0.0.1:8000/harpocryption/voter/finalresult?auth=tpOF3CwS0oZJXN2GabLDjXnoun7c0Nw6m9gaqbIUzLtzzHfIRnKcALBTjGZnpq4k")

assert driver.title == "Vote Results"

vote_event_title = driver.find_element(By.CSS_SELECTOR, "div#result_booth h1").text

assert vote_event_title == "Vote Event Title 9"

print("Integration Test 36 Passed !")

driver.quit()