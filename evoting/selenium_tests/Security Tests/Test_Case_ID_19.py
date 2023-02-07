# Test_Case_ID_19.py 

"""
Title: Constraints Violation - Perform the vote submission by ignoring the defined constraints 

Descriptions:
Test the system to be able check the defined constraints before processing the vote casting form submission. 

The malicious attacker can pass by the provided web form interface, which the GET request of the web form will check the constraints before allowing the user to cast and submit the vote, to submit the vote form when he/she manages to obtain the encrypted encoded vote option strings. 

When the attacker tries to submit a vote cast form on the non-requirement fulfilled vote event, the system should be able to identify the violation and show an error message. 

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

driver.execute_script(
	"""
	let genuine_form_csrf_token = document.querySelector("div#left_pane form>input[name=csrfmiddlewaretoken]");

	let form = document.createElement("form");

	form.action = "/harpocryption/voter/vote";
	form.method = "POST";
	form.appendChild(genuine_form_csrf_token);

	let option = document.createElement("input");
	option.type = "text";
	option.name = "voteOption";
	option.value = "93576922464651637612415809299369294219621467169969212704228907691411083443010718274378547905703384280252024152140307939495018520182396399773172397762681921770471148176589133544984543810311768990730493713632588321068980155391776861223898058399975051160024491154014347659920875053311094503751127117479045276447";

	let auth_token = document.createElement("input");
	auth_token.text = "voterAuth";
	auth_token.name = "voterAuth";
	auth_token.value = "Do4hbN0qZFw4cYA6AgzTBe9qDqklzj103XjOap7IIxITa9tfCSczBGNydrG0QrWI";

	form.append(option);
	form.append(auth_token);

	document.body.appendChild(form);
	form.submit();

	""")

# assert the redirection 
assert driver.current_url == "http://127.0.0.1:8000/harpocryption/voter/vote"
# assert the page title 
assert driver.title == "Error"

error_message = driver.find_element(By.ID, "error_message").text
assert error_message == "Invitation Link Invalid !"

print("Security Test 19 Passed !")

driver.quit()