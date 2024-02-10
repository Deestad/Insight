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

    def google_search(self, query):
        with requests.session() as session:
            # Insight gets a Google result
            url = f"""https://www.google.com/search?q="{query}"
            """
            headers = {
                "referer": "referer: https://www.google.com/",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/89.0.4389.114 Safari/537.36"
            }
            session.post(url, headers=headers)
            response = session.get(url, headers=headers)

            soup = BeautifulSoup(response.text, 'html.parser')
            company_url = soup.find('cite').text
            return company_url

    def verify_competitor(self, target):
        with requests.session() as session:
            url = f"{target}"
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/89.0.4389.114 Safari/537.36"
            }
            session.post(url, headers=headers)
            response = session.get(url, headers=headers)

            soup = BeautifulSoup(response.text, 'html.parser')
            page_text = soup.get_text()
            context = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                max_tokens=256,
                messages=[

                    {"role": "system",
                     "content": ""},
                    {"role": "user",
                     "content": f"Look at this page and tell me what this company is about in one SMALL paragraph. Make it short."
                                f"PAGE: {page_text}"}
                ]

            )
            self.description = context.choices[0].message.content

    def search_routine(self, query, top):
        # Make a Google search from Query and use Query as target
        # ++ Verification of competitor's website
        with requests.session() as session:
            self.verify_competitor(self.google_search(query))
            # titles = soup.findAll('h3')
            # titles_url = [element for element in soup.findAll('a', href=True)]
            # titles = [element.get_text() for element in titles]
            # for i in range(0, len(titles) - 2):
            #     print(titles[i], titles_url[i]['href'])

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
    initialization_routine = threading.Thread(target=Initialize().run())
    initialization_routine.start()
    initialization_routine.join()
    InsightApp().run()
