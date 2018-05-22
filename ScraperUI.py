#!python2.7.14
#os.environ["KIVY_NO_CONSOLELOG"] = "1"
#os.environ["KIVY_NO_FILELOG"] = "1"
import os
import sys
sys.path.append(os.path.dirname(__file__))
os.chdir(os.path.dirname(__file__))
sys.path.append('pkgs')
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
from kivy.animation import Animation, AnimationTransition
import time
import random
import subprocess
import csv
import threading
print sys.path
Window.size = (1100, 600)
#root
class MainScreen(BoxLayout):
    CheckBoxGrid = GridLayout(cols=10, spacing=10, padding=(0, 30, 40, 30), size_hint_y=None, background_color= Color("#282828"))
    CheckBoxGrid.bind(minimum_height=CheckBoxGrid.setter('height'))
    LocationDict = {}

    def __init__(self,**kwargs):
	super (MainScreen, self).__init__(**kwargs)

    def start_wrapper(self, choice , category, filename, state=False):

        if state:
            state = []
            for key in self.LocationDict:
                if self.LocationDict[key].active:
                    state.append(key)
            state = ",".join(state)
            crawler = subprocess.Popen(['python', 'SpiderCrawl.pyc', choice, category, filename, state], cwd=sys.path[0]) 
        else:
            crawler = subprocess.Popen(['python', 'SpiderCrawl.pyc', choice, category, filename], cwd=sys.path[0]) 
        threa = threading.Thread(target=self.runInThread, args=(crawler,))
        threa.start()
        self.conpop2(crawler)

    def runInThread(self, proc):
        proc.wait()
        self.popup.dismiss()

    def conpop2(self, scraper):
        content = BoxLayout(orientation="horizontal")
        self.popup = Popup(title="Scraper is Running", size_hint=(None, None), size=(500, 200), auto_dismiss=False, content=content)
        kill = lambda x:scraper.terminate()
        cancel = Button(text="Stop Scraper", on_press=kill)
        content.add_widget(cancel)
        self.popup.open()

    def changeScreen(self, next_screen):
        self.LocationDict.clear()
        if next_screen == "yellowpagesaus":
                self.ids.kivy_screen_manager.current = "yellowpagesaus"
        elif next_screen == "yellowpagesus":
                self.ids.kivy_screen_manager.current = "yellowpagesus"
                self.addCheckBox()
        elif next_screen == "yellowpagesuk":
                self.ids.kivy_screen_manager.current = "yellowpagesuk"
                self.addCheckBox(True)

        elif next_screen == "back to main screen":
                if self.ids.kivy_screen_manager.current == "yellowpagesuk" or self.ids.kivy_screen_manager.current == "yellowpagesus":
                    self.CheckBoxGrid.clear_widgets()
                    self.remove_widget(self.CheckBoxGrid)
                    x = self.ids['yellowPagesUK' if self.ids.kivy_screen_manager.current == "yellowpagesuk" else 'yellowPagesUS']
                    x.ids['blankScrollView'].clear_widgets()
                self.ids.kivy_screen_manager.current = "start_screen"

    def addCheckBox(self, countryname=False):
        if countryname:
            csvName = 'UKpostcodes.csv'
            checkBoxName = 'ukpostcode'
            nameRow = 1
        else:
            csvName = 'UScities.csv'
            checkBoxName = 'usstate'
            nameRow = 0

        with open(csvName) as csvfile:  # Read in the csv file
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                key = row[0 if countryname else 1]
                self.LocationDict[key] = CheckBox(active=False, size_hint_y=None, height=30)
                self.CheckBoxGrid.add_widget(self.LocationDict[key])
                LabelTxt = Label(text=row[nameRow], halign="left")
                self.CheckBoxGrid.add_widget(LabelTxt)
        x = self.ids['yellowPagesUK' if self.ids.kivy_screen_manager.current == "yellowpagesuk" else 'yellowPagesUS']
        x.ids['blankScrollView'].add_widget(self.CheckBoxGrid)


#app object
class ScraperUIApp(App):

    def __init__(self, **kwargs):
        super(ScraperUIApp, self).__init__(**kwargs)

    def build(self):
        self.title = 'Scraper App'
        return MainScreen()

if __name__== '__main__':
    ScraperUIApp().run()
