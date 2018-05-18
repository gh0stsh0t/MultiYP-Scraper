#import os
#os.environ["KIVY_NO_CONSOLELOG"] = "1"
#os.environ["KIVY_NO_FILELOG"] = "1"
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.graphics import Rectangle, Color
from kivy.uix.widget import Widget
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import ListProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.audio import SoundLoader
from functools import partial
from kivy.properties import ObjectProperty
from kivy.core.window import Window



from kivy.utils import get_color_from_hex
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
import sys
import time
import random
import subprocess
import csv

#root
class MainScreen(BoxLayout):
    CheckBoxGrid = GridLayout(cols=8)

    def __init__(self,**kwargs):
        super (MainScreen, self).__init__(**kwargs)


        def start_wrapper(self, choice , category, filename, state=None):
            subprocess.call(['python', 'SpiderCrawl.py', choice, category, filename]) 
            
    def changeScreen(self, next_screen):
        if next_screen == "yellowpagesaus":
                self.ids.kivy_screen_manager.current = "yellowpagesaus"
        elif next_screen == "yellowpagesus":
                self.ids.kivy_screen_manager.current = "yellowpagesus"
                self.addCheckBox("us")
        elif next_screen == "yellowpagesuk":
                self.ids.kivy_screen_manager.current = "yellowpagesuk"
                self.addCheckBox("uk")
                self.nameRow = 1
        elif next_screen == "back to main screen":
                self.ids.kivy_screen_manager.current = "start_screen"

    def addCheckBox(self, countryname):
        if countryname == "uk":
            csvName = 'UKpostcodes.csv'
            checkBoxName = 'ukpostcode'
            nameRow = 1
        elif countryname == "us":
            csvName = 'UScities.csv'
            checkBoxName = 'usstate'
            nameRow = 0

        LocationDict = {}
        with open(csvName) as csvfile:  # Read in the csv file
            readCSV = csv.reader(csvfile, delimiter=',')
            states = []
            for row in readCSV:
                states.append(row[0])
                LocationDict[str(checkBoxName)+str(row)] = CheckBox(active=False)
                self.CheckBoxGrid.add_widget(LocationDict[str(checkBoxName)+str(row)])
                self.CheckBoxGrid.add_widget(Label(text=row[nameRow]))
        
        self.add_widget(self.CheckBoxGrid)
"""
class CkeckBoxGrid(GridLayout):
    self.cols = 8
    row_default_height: '30dp'

    def addCheckBox(countryname):

        if countryname == "uk"
            csvname = 'UKpostcodes.csv'
        elif countryname == "us"
            csvname = 'UScities.csv'

        LocationDict = {}
        with open(csvname) as csvfile:  # Read in the csv file
            readCSV = csv.reader(csvfile, delimiter=',')
            states = []
            for row in readCSV:
                states.append(row[0])
                self.LocationDict["location"+row] = CheckBox(active=False)
                self.add_widget(Label(text=row[1]))
"""
#app object
class ScraperUIApp(App):

    def __init__(self, **kwargs):
        super(ScraperUIApp, self).__init__(**kwargs)


    def build(self):
        self.title = 'Scraper App'
        return MainScreen()

if __name__== '__main__':
    ScraperUIApp().run()
