import os
from pprint import pp
import selenium
from services.promptAction import promptAction
from services.getRangeOfYears import getRangeOfYears
from services.downloadFile import downloadFile
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException  
from pathlib import Path
from prettyprinter import pprint
import time

# global variables
url = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html"

# input state
prompt = True
action = None

def setUp(download=False):
    if download == False:
        driver = webdriver.Chrome()
        driver.get(url)
        return driver
    else:
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('prefs', {
            # "download.default_directory": "C:/Users/XXXX/Desktop", #Change default directory for downloads
            # "download.prompt_for_download": False, #To auto download the file
            # "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
        })
        driver = webdriver.Chrome(options=chromeOptions)
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

def checkForSurvey(driver):
    try:
        time.sleep(.5)
        no_thanky=driver.find_element(By.XPATH, "//a[contains(text(),'No Thanks')]")
        print("survey found!")
        no_thanky.click()
        time.sleep(.5)
        return
    except NoSuchElementException:
        return
    
def checkForNoResults(driver):
    try:
        time.sleep(.5)
        driver.find_element(By.ID, 'errorText')
        return True
    except NoSuchElementException:
        return False
    
def getDownloadsByFileNameAndYear(name, years):
    
    driver = setUp(True)
    
    try:        
        searchBox = driver.find_element(By.ID, 'searchFor')
        # preemptively clear the searchBox to remove any possible values
        searchBox.clear()
        # populate the searchBox with one of the form values the user provided
        searchBox.send_keys(name)
        # Submit the document
        searchBox.send_keys(Keys.RETURN)
        # Wait for the form to update
        time.sleep(.5)
        if checkForNoResults(driver):
            return
        checkForSurvey(driver)
        
        # Show as many records as possible
        show_200 = driver.find_element(By.XPATH, "//a[contains(text(),'200')]")
        show_200.click()

        checkForSurvey(driver)
        # Refactor into function, driver as an argument
        # obtain the elements and total from the page
        total = int(driver.find_element(By.CLASS_NAME, 'ShowByColumn').text.split(' of ')[1].split(' ')[0].replace(",", ""))
        count = 0
        while count < total:
            dom_prod_number = driver.find_elements(By.CLASS_NAME, 'LeftCellSpacer')
            dom_year_elements = driver.find_elements(By.CLASS_NAME, 'EndCellSpacer')
            # Check if there is a nextPage, if so, obtain it. Otherwise, ensure the script doesn't crash
            nextPage = None
            try:
                nextPage = driver.find_element(By.XPATH, "//a[contains(text(),'Next')]")
            except NoSuchElementException:
                nextPage = None
            # initialize an indexer to track parallel lists
            index = 0
            # check each record to see if it matches the given form name
            for ele in dom_year_elements:
                # If it the names match, compare the years and track max and mins
                if dom_prod_number[index].text.strip() == name.strip() and int(ele.text) in years:
                    print(f"prod_num {dom_prod_number[index].text.strip()} name {name} year {ele.text}")
                    time.sleep(.5)
                    dom_prod_number[index].find_element(By.CSS_SELECTOR, 'a').click()
                    time.sleep(.5)
                # increment the count
                count += 1
                index += 1
            # Upon exhausting the page, Check that the nextPage is capable of being clicked
            if nextPage:
                nextPage.click()
                time.sleep(.5)
                checkForSurvey(driver)
            # Otherwise, commit what we have, because we're done
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        tearDown(driver)
        print("Ta Da!!")

def searchByFormName(forms):
    driver = setUp()
    # Form Title located in class = MiddleCellSpacer
    # Year Located in class = EndCellSpacer
    # Download asset located in class = LeftCellSpacer
    try:
        results_list = []
        for form in forms:    
            searchBox = driver.find_element(By.ID, 'searchFor')
            # preemptively clear the searchBox to remove any possible values
            searchBox.clear()
            # populate the searchBox with one of the form values the user provided
            searchBox.send_keys(form)
            # Submit the document
            searchBox.send_keys(Keys.RETURN)
            # Wait for the form to update
            time.sleep(.5)
            if checkForNoResults(driver):
                continue
            checkForSurvey(driver)
            
            # Show as many records as possible
            show_200 = driver.find_element(By.XPATH, "//a[contains(text(),'200')]")
            show_200.click()
            time.sleep(.5)
            checkForSurvey(driver)
            # Refactor into function, driver as an argument
            # obtain the elements and total from the page
            total = int(driver.find_element(By.CLASS_NAME, 'ShowByColumn').text.split(' of ')[1].split(' ')[0].replace(",", ""))
            count = 0
            min_year = 3000
            max_year = 0
            form_title = None
            form_prod_number = None
            while count < total:
                dom_prod_number = driver.find_elements(By.CLASS_NAME, 'LeftCellSpacer')
                dom_title_elements = driver.find_elements(By.CLASS_NAME, 'MiddleCellSpacer')
                dom_year_elements = driver.find_elements(By.CLASS_NAME, 'EndCellSpacer')
                # Check if there is a nextPage, if so, obtain it. Otherwise, ensure the script doesn't crash
                nextPage = None
                try:
                    nextPage = driver.find_element(By.XPATH, "//a[contains(text(),'Next')]")
                except NoSuchElementException:
                    nextPage = None
                # initialize an indexer to track parallel lists
                index = 0
                # check each record to see if it matches the given form name
                for ele in dom_year_elements:
                    # If it the names match, compare the years and track max and mins
                    if dom_prod_number[index].text.strip() == form.strip():
                        form_title = dom_title_elements[index].text.strip()
                        form_prod_number = dom_prod_number[index].text.strip()
                        if int(ele.text) > max_year:
                            max_year = int(ele.text)
                        if int(ele.text) < min_year:
                            min_year = int(ele.text)
                    # increment the count
                    count += 1
                    index += 1
                # Upon exhausting the page, Check that the nextPage is capable of being clicked
                if nextPage:
                    nextPage.click()
                    time.sleep(.5)
                    checkForSurvey(driver)
                # Otherwise, commit what we have, because we're done
                else:
                    # if for some reason the entered values are invalid, don't append anything and just continue on.
                    if form_prod_number == None or form_title == None or min_year == 0 or max_year == 3000:
                        continue
                    else:
                        results_list.append({
                            "form_number": form_prod_number, 
                            "form_title": form_title, 
                            "min_year": min_year, 
                            "max_year": max_year
                        })
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
    results = searchByFormName(form_names)
    print("Results:")
    pprint(results)
elif action == 'D':
    form_name = input("What is the name of your form?: ")
    first_year = int(input("Enter starting year: "))
    last_year = int(input("Enter ending year: "))
    years = getRangeOfYears(first_year, last_year)
    
    getDownloadsByFileNameAndYear(form_name, years)
    
