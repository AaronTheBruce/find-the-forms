import os
import selenium
from services.promptAction import promptAction
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# import time
# from PIL import Image
import io
import json
# import requests

# global variables
url = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html"

# input state
prompt = True
action = None

def setUp():
    driver = webdriver.Firefox()
    driver.get(url)
    return driver

def tearDown(driver):
    driver.close()

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


# function that will populate the input with the user provided form names
# select the Title option for the criteria selector and hit the submitSearch button
# wait for the results to return
# obtain the available form elements
    

def searchByFormName(forms):
    driver = setUp()
    searchBox = driver.find_element(By.ID, 'searchFor')
    selector = driver.find_element(By.NAME, 'criteria')
    searchBtn = driver.find_element(By.NAME, 'submitSearch')
    # Form Title located in class = MiddleCellSpacer
    # Year Located in class = EndCellSpacer
    # Download asset located in class = LeftCellSpacer
    try:
        results_list = []
        print(f"searchBox {searchBox}")
        print(f"selector {selector}")
        print(f"searchBtn {searchBtn}")
        for form in forms:    
            form = json(form)
            searchBox.clear()
            searchBox.send_keys(form.getText())
            searchBox.send_keys(Keys.RETURN)
            dom_form_elements = driver.find_elements(By.CLASS_NAME, 'MiddleCellSpacer')
            for item in dom_form_elements:
                print(f"item {item}")
                results_list.append(item)
        return results_list
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        tearDown(driver)

def getFormNames():
    more = True
    form_names = []
    while more:
        form_name = input('Enter Form Name: ')
        again = input('Done? (y/n): ')
        form_names.append(form_name)
        if again == 'y' or again == 'Y': break
        elif again == 'n' or again == 'N': continue
        else:
            print("I'm gonna assume that's a No?")
            continue
    return form_names

# Prompt the user for an action, f/F denotes to searchByFormName
action = promptAction(prompt)
if action == 'F':
    form_names = getFormNames()
    searchByFormName(form_names)
    

# assert "IRS" in driver.title
# elem = driver.find_element()
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()