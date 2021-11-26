import os
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# import time
# from PIL import Image
# import io
# import requests

# Taking a list of tax form names (ex: "Form W-2", "Form 1095-C"), 
# search the website and return some informational results. 
# Specifically, you must return the "Product Number", the "Title", and the maximum and minimum years the form is available for download. 
# The forms returned should be an exact match for the input (ex: "Form W-2" should not return "Form W-2 P", etc.)

# Upon start of the script, prompt the user for the desired actions to take
# Error handle incorrect entries, there will be 2 options to take.
# Upon selection of the action, prompt for arguements to use for the function.
# Error handle 404 responses when nothing is returned

# Declare a function that takes the Form Name and search through the website to find
# the Product Name, the Title, and max - min years of the form availability.
# return all instances as a list of dicts containing the key value pairs of the aforementioned info


driver = webdriver.Firefox()
driver.get("https://apps.irs.gov/app/picklist/list/priorFormPublication.html")
print(f"Driver {driver}")
# assert "IRS" in driver.title
# elem = driver.find_element()
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
driver.close()