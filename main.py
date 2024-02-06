# Basic imports

import webbrowser
import sys
import os
import logging
import requests
import winsound

# Third-party imports
from bs4 import BeautifulSoup
# -- Kivy
import kivy
from kivy.app import App
from kivy.config import Config

Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '400')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
kivy.require('2.1.0')
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen

# -- Others
import pickle
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

# Logging
LOG_FILE = 'Insight.log'
if os.path.isfile(LOG_FILE) and os.access(LOG_FILE, os.R_OK):
    os.remove('Insight.log')
logging.basicConfig(filename='Insight.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

options = webdriver.FirefoxOptions()
options.add_argument("-headless")


# Screens
class StartWindow(Screen):
    pass


class ResultsWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


# KV Files
kv = Builder.load_file('Insight.kv')


class InsightApp(App):
    def build(self):
        self.title = 'Insight: Internet Browsing Optimizer'
        return kv

    def search_callback(self):
        logging.info(f"[Search Callback Function          ] Running...")
        query = self.root.ids.searchbar.text
        query = query.replace(' ', '+')
        logging.info(f"[Search Callback Function          ] Query set as {query}...")
        if query:
            self.root.current = "results"
            with requests.session() as s:
                url = f"https://www.google.com/search?q=`{query}`"
                headers = {
                    "referer": "referer: https://www.google.com/",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/89.0.4389.114 Safari/537.36"
                }
                s.post(url, headers=headers)
                response = s.get(url, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                titles = soup.findAll('h3')
                titles_url = [element for element in soup.findAll('a', href=True)]
                titles = [element.get_text() for element in titles]
                for i in range(0, len(titles) - 2):
                    print(titles[i], titles_url[i]['href'])


if __name__ == '__main__':
    InsightApp().run()
