# Test_Case_ID_9.py 

"""
Title: Access Control - Access the view vote event page without any login attempts by its URL

Descriptions:
Test the system to be able check the authenticate before allowing the user to access the resources. 
When there is no user logged into the system, the system should be redirecting the user to the login page instead of rendering the authentication needed pages. 

Before executing this security test, the vote event test data is loaded into the system database. 

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

# direct access the View Vote Event Page
driver.get("http://127.0.0.1:8000/evoting/eventowner/viewevent/2")

# assert the redirection 
assert driver.current_url == "http://127.0.0.1:8000/evoting/eventowner/login"

driver.quit()