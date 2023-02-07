# Test_Case_ID_16.py 

"""
Title: Access Control - Perform the Confirm Vote Event operation without any login session information provided

Descriptions:
Test the system to be able check the authenticate before allowing the user to access the resources. 
The confirm vote event is a POST action, where the attacker tries to script the POST request without any successful login attempts, the system should be able identify the unauthorized request.   

Before executing this security test, the vote event test data is loaded into the system database. 

"""
import os 
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# wait strategy 
from selenium.webdriver.support.wait import WebDriverWait

# Locator 
from selenium.webdriver.common.by import By

# UI Select Interaction
from selenium.webdriver.support.ui import Select

# MySQL connecter
import mysql.connector

# load the environment variables
load_dotenv()

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# login to the system
driver.get("http://127.0.0.1:8000/harpocryption/eventowner/login")

driver.execute_script(
	"""
	let genuine_form_csrf_token = document.querySelector("div#left_pane form>input[name=csrfmiddlewaretoken]");

	let form = document.createElement("form");

	form.action = "/harpocryption/eventowner/confirmevent/1";
	form.method = "POST";
	form.appendChild(genuine_form_csrf_token);

	document.body.appendChild(form);
	form.submit();

	""")

# assert the redirection 
assert driver.current_url == "http://127.0.0.1:8000/harpocryption/eventowner/login"

# inspect the database see if the vote event is modified 
mydb = mysql.connector.connect(
	host=os.getenv("MYSQL_HOST"),
	user=os.getenv("MYSQL_USER"),
	password=os.getenv("MYSQL_PASSWORD"),
	database=os.getenv("MYSQL_DATABASE_NAME")
)

mycursor = mydb.cursor()

query = """SELECT COUNT(*) FROM evoting_voteevent WHERE eventNo = %s and status = 'PB'"""

mycursor.execute(query, (1, ))

result = mycursor.fetchone()

assert int(result[0]) == 0

print("Security Test 16 Passed !")

driver.quit()