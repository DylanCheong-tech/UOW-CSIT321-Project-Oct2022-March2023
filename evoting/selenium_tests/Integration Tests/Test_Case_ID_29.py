# Test_Case_ID_29.py 

"""
Title: Event Owner Publishes Vote Result on Vote Event in Final Result Ready (FR) status

Descriptions:
Test the system's ability to create the final result view link and deliver it to the voter who participated through email.
For this operation, the system will not be using the same authentication token as generated in the vote event confirming stage, 
a new token string will be generated and sent out accordingly. 

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
driver.get("http://127.0.0.1:8000/harpocryption/eventowner/login")

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
	if row.get_attribute("innerHTML") == "Vote Event Title 8":
		buttons = driver.find_elements(By.CSS_SELECTOR, "table tr:nth-child(" + str(index + 1 + 1) + ") td:nth-child(6) button")
		buttons[0].click()
		break
WebDriverWait(driver, timeout=100).until(lambda driver : driver.title == "View Vote Events")

# click the "View Final Result" button
driver.find_element(By.CSS_SELECTOR, "div#action_buttons button:nth-child(2)").click()

WebDriverWait(driver, timeout=100).until(lambda driver : driver.title == "Vote Event Final Result")

buttons = driver.find_elements(By.CSS_SELECTOR, "button[type=submit]")
for button in buttons:
	if button.text == "Publish Final Result":
		button.click()
		break

driver.find_element(By.ID, "confirm_btn").click()

ack_message = driver.find_element(By.ID, "message_content").text

assert ack_message == "Final Result Published Successfully !"

print("Integration Test 29 Passed !")

driver.quit()