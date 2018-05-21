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
from kivy.uix.scrollview import ScrollView
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


Window.size = (1100, 600)
#root
class MainScreen(BoxLayout):
    CheckBoxGrid = GridLayout(cols=10, spacing=10, padding=(0, 30, 40, 30), size_hint_y=None)
    CheckBoxGrid.bind(minimum_height=CheckBoxGrid.setter('height'))

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
                self.nameRow = 0
                self.addButtons("us")
        elif next_screen == "yellowpagesuk":
                self.ids.kivy_screen_manager.current = "yellowpagesuk"
                #self.addCheckBox("uk")
                self.nameRow = 1

        elif next_screen == "back to main screen":
                self.ids.kivy_screen_manager.current = "start_screen"
                self.CheckBoxGrid.clear_widgets()
                self.GridScroll.clear_widgets()
                self.remove_widget(self.CheckBoxGrid)
                self.remove_widget(self.GridScroll)
"""
    def addButtons(self, countryname):
        buttonStart = Button(text = "Start", height = 40, width = 10, color = color("#ffffff"), background_color = color("#2ecc71"))
        buttonBack = Button(text = "Back to Main Screen", height = 40, width = 10)
        buttonBack.bind(on_press = app.root.changeScreen(self.text.lower()))
        if countryname == "uk":
            #buttonStart.bind(on_press = app.root.start_wrapper('ypUS', category.theTxt.text, filename.theTxt.text, usstate.theTxt.text))
            self.add_widget(buttonStart)
            self.add_widget(buttonBack)

        elif countryname == "us":
            self.add_widget(buttonStart)
            self.add_widget(buttonBack)
"""
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
                LocationDict[str(checkBoxName)+str(row)] = CheckBox(active=False, size_hint_y=None, height=30)
                self.CheckBoxGrid.add_widget(LocationDict[str(checkBoxName)+str(row)])
                LabelTxt = Label(text=row[nameRow], halign="left")
                self.CheckBoxGrid.add_widget(LabelTxt)

        self.GridScroll = ScrollView(size_hint=(1, None), size=(Window.width, Window.height/3))
        self.GridScroll.add_widget(self.CheckBoxGrid)
        self.add_widget(self.GridScroll)

#app object
class ScraperUIApp(App):

    def __init__(self, **kwargs):
        super(ScraperUIApp, self).__init__(**kwargs)


    def build(self):
        self.title = 'Scraper App'
        return MainScreen()

if __name__== '__main__':
    ScraperUIApp().run()
