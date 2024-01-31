import pickle
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge

edge_options = EdgeOptions()



browser = Edge(executable_path=r"C:\Users\ADM\MSEDGEWEBDRIVER\MicrosoftWebDriver.exe", options=edge_options)

browser.get("https://manage.wix.com/dashboard/0c9f100b-eb1d-4a24-bd7f-1f5fbed92b78")
pickle.dump(browser.get_cookies(), open("cookies.pkl", "wb"))
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
        browser.add_cookie(cookie)

browser.find_element_by_name("Email").click
browser.find_element_by_name("Email").send_keys("marketing@mactab.com.br")