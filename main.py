# Basic imports

import webbrowser
import sys
import os
import logging
import requests
import winsound
import time
import threading
from multiprocessing import Process
import json

# Third-party imports
import PySimpleGUI as SG
import openai
from bs4 import BeautifulSoup
# -- Kivy
import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.properties import NumericProperty

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
from kivy.animation import Animation

# Logging
LOG_FILE = 'Insight.log'
if os.path.isfile(LOG_FILE) and os.access(LOG_FILE, os.R_OK):
    os.remove('Insight.log')
logging.basicConfig(filename='Insight.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# METHODS
from methods.initialization import Initialize

# Screens
class StartWindow(Screen):
    pass


class ResultsWindow(Screen):
    pass


class LoadingScreen(Screen):
    pass


class WindowManager(ScreenManager):
    pass


# KV Files
kv = Builder.load_file('Insight.kv')


class SearchRoutine:

    def __init__(self):
        self.description = None

    def run(self, query, top):
        self.move_screens("loading", top)

        def construct(inner):
            self.build(query, top)

        def init(inner):
            routine_thread = Process(target=self.search_routine(query=query, top=top))
            routine_thread.start()
            routine_thread.join()
            Clock.schedule_once(construct, 5)

        Clock.schedule_once(init, 5)

    def build(self, query, top):
        logging.info(f"[Interface          ] Building...")
        top.root.ids.summary.text = self.description

    def move_screens(self, target, top):
        top.root.current = f"{target}"

    def search_routine(self, query, top):
        with requests.session() as s:
            url = f"""https://www.google.com/search?q="{query}"
"""
            headers = {
                "referer": "referer: https://www.google.com/",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/89.0.4389.114 Safari/537.36"
            }
            s.post(url, headers=headers)
            response = s.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            self.description = soup.find(class_='VwiC3b yXK7lf lVm3ye r025kc hJNv6b Hdw6tb').get_text()
            titles = soup.findAll('h3')
            titles_url = [element for element in soup.findAll('a', href=True)]
            titles = [element.get_text() for element in titles]
            for i in range(0, len(titles) - 2):
                print(titles[i], titles_url[i]['href'])
            time.sleep(3)
            self.move_screens("results", top)


class InsightApp(App):
    def build(self):
        self.title = 'Insight: Competitor Analysis'
        return kv

    def search_callback(self):
        logging.info(f"[Search Callback Function          ] Running...")
        query = self.root.ids.searchbar.text
        query = query.replace(' ', '+')
        logging.info(f"[Search Callback Function          ] Query set as {query}...")
        SearchRoutine().run(query, self)


if __name__ == '__main__':
    initialization_routine = threading.Thread(target=Initialize.run(logging=logging))
    initialization_routine.start()
    initialization_routine.join()
    InsightApp().run()
