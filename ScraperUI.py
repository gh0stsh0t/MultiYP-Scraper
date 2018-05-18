#import os
#!python2.7.14
#os.environ["KIVY_NO_CONSOLELOG"] = "1"
#os.environ["KIVY_NO_FILELOG"] = "1"
import sys
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
from kivy.core.audio import SoundLoader
from functools import partial
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
import time
import random
import subprocess

#root
class MainScreen(BoxLayout):

	def __init__(self,**kwargs):
	    super (MainScreen, self).__init__(**kwargs)

        def start_wrapper(self, choice , category, filename, state=None):
            if state:
                crawler = subprocess.Popen(['python', 'SpiderCrawl.py', choice, category, filename, state], cwd=sys.path[0]) 
            else:
                crawler = subprocess.Popen(['python', 'SpiderCrawl.py', choice, category, filename], cwd=sys.path[0]) 
            
            while isinstance(App.get_running_app().root_window.children[0], Popup):
                if crawler.poll():
                    self.popup.dismiss()


	def changeScreen(self, next_screen):
	    if next_screen == "yellowpagesaus":
                self.ids.kivy_screen_manager.current = "yellowpagesaus"
	    elif next_screen == "yellowpagesus":
                self.ids.kivy_screen_manager.current = "yellowpagesus"
	    elif next_screen == "yellowpagesuk":
                self.ids.kivy_screen_manager.current = "yellowpagesuk"
	    elif next_screen == "back to main screen":
                self.ids.kivy_screen_manager.current = "start_screen"

    def addCheckBoxUS():
        

#app object
class ScraperUIApp(App):

    def __init__(self, **kwargs):
        super(ScraperUIApp, self).__init__(**kwargs)


    def build(self):
        self.title = 'Scraper App'
        return MainScreen()

if __name__== '__main__':
    ScraperUIApp().run()
