# Test_Case_ID_26.py 

"""
Title: Event Owner Views Vote Event in Result Published (RP) status

Descriptions:
Test the system’s ability to display all the completed vote event information to the event owner users. 
The system will categorize the vote event with status of Final Result Ready (FR) and Result Published (RP) as the completed vote events. 

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
driver.get("http://127.0.0.1:8000/evoting/eventowner/login")

# fill in the form data 
driver.find_element(By.NAME, "email").send_keys("jamessmith@mail.com")
driver.find_element(By.NAME, "password").send_keys("JamesSmith_1234")

# submit the login form
driver.find_element(By.ID, "form_submit_btn").click()
WebDriverWait(driver, timeout=100).until(lambda driver : driver.title == "Overview")

# navigate to the side menu bar and click the "Completed Vote Events"
menu_items = driver.find_elements(By.CSS_SELECTOR, "span#side_menu_bar>span.menu_item")
for menu_item in menu_items:
	if menu_item.text == "Completed Vote Events":
		menu_item.click()
		break

WebDriverWait(driver, timeout=100).until(lambda driver : driver.title == "Completed Vote Events")

# navigate to the view vote event page
rows = driver.find_elements(By.CSS_SELECTOR, "table tr:not(.header) td:nth-child(2)")
for index, row in zip(range(len(rows)), rows):
	if row.get_attribute("innerHTML") == "Vote Event Title 10":
		buttons = driver.find_elements(By.CSS_SELECTOR, "table tr:nth-child(" + str(index + 1 + 1) + ") td:nth-child(6) button")
		buttons[0].click()
		break
WebDriverWait(driver, timeout=100).until(lambda driver : driver.title == "View Vote Events")

assert "/evoting/eventowner/viewevent" in driver.current_url

print("Integration Test 26 Passed !")

driver.quit()