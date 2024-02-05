# Basic imports

import webbrowser
import sys
import os
import winsound
# Third-party imports

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

options = webdriver.FirefoxOptions()
options.add_argument("-headless")

class MainScreen(TabbedPanel):
    pass

class InsightApp(App):
    def build(self):
        self.title = 'Insight: Internet Browsing Optimizer'
        return MainScreen()


if __name__ == '__main__':
    InsightApp().run()

