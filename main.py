import os
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# import time
# from PIL import Image
# import io
# import requests

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