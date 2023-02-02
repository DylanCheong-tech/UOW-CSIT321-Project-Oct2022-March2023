# Test_Case_ID_30.py 

"""
Title: Event Owner Publishes Vote Result on Vote Event not in Final Result Ready (FR) status

Descriptions:
Test the system’s ability to check the vote event status before the user makes the final result publication. 

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

# navigate to the view vote event page
rows = driver.find_elements(By.CSS_SELECTOR, "table tr:not(.header) td:nth-child(2)")
for index, row in zip(range(len(rows)), rows):
	if row.get_attribute("innerHTML") == "Vote Event Title 7":
		buttons = driver.find_elements(By.CSS_SELECTOR, "table tr:nth-child(" + str(index + 1 + 1) + ") td:nth-child(6) button")
		buttons[0].click()
		break
WebDriverWait(driver, timeout=100).until(lambda driver : driver.title == "View Vote Events")

driver.execute_script(
	"""
	let form = document.createElement("form");

	let genuine_form_csrf_token = document.querySelector("span.logout_section form input[name=csrfmiddlewaretoken]");

	form.action = "/harpocryption/eventowner/event/finalresult/publish/7";
	form.method = "POST";
	form.appendChild(genuine_form_csrf_token);

	document.body.appendChild(form);
	form.submit();

	""")

driver.implicitly_wait(5)
error_message = driver.find_element(By.ID, "message_content").text

assert error_message == "Final Result Published Failed !"

print("Integration Test 30 Passed !")

driver.quit()