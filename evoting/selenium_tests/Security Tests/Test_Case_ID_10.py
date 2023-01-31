# Test_Case_ID_10.py 

"""
Title: Access Control - Perform the Delete Vote Event operation without any login session information provided

Descriptions:
Test the system to be able check the authenticate before allowing the user to access the resources. 
The delete vote event is a POST action, where the attacker tries to script the POST request without any successful login attempts, the system should be able identify the unauthorized request.   

Before executing this security test, the vote event test data is loaded into the system database. 

"""
import os 
from dotenv import load_dotenv
import mysql.connector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# wait strategy 
from selenium.webdriver.support.wait import WebDriverWait

# Locator 
from selenium.webdriver.common.by import By

# UI Select Interaction
from selenium.webdriver.support.ui import Select

# load the environment variables
load_dotenv()

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# access the login page
driver.get("http://127.0.0.1:8000/evoting/eventowner/login")

driver.execute_script(
	"""
	let form = document.createElement("form");

	let genuine_form_csrf_token = document.querySelector("div#left_pane form>input[name=csrfmiddlewaretoken]")

	form.action = "/evoting/eventowner/deleteevent/12";
	form.method = "POST"
	form.appendChild(genuine_form_csrf_token)

	document.body.appendChild(form)
	form.submit()

	""")

# assert the redirection 
assert driver.current_url == "http://127.0.0.1:8000/evoting/eventowner/login"

# inspect the database see if the vote event is deleted
mydb = mysql.connector.connect(
  host=os.getenv("MYSQL_HOST"),
  user=os.getenv("MYSQL_USER"),
  password=os.getenv("MYSQL_PASSWORD"),
  database=os.getenv("MYSQL_DATABASE_NAME")
)

cursor = mydb.cursor()

cursor.execute("SELECT COUNT(*) FROM evoting_voteevent WHERE eventNo = 12")

result = cursor.fetchone()

assert result[0] == 1

print("Security Test 10 Passed !")

driver.quit()