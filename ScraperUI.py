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
import sys
import time
import random

Window.clearcolor = get_color_from_hex("#1c1c1c")

#root
class MainScreen(BoxLayout):

	def __init__(self,**kwargs):
		super (MainScreen, self).__init__(**kwargs)

	def changeScreen(self, next_screen):

		if next_screen == "yellowpagesaus":
			self.ids.kivy_screen_manager.current = "yellowpagesaus"

		if next_screen == "yellowpagesus":
			self.ids.kivy_screen_manager.current = "yellowpagesus"

		if next_screen == "yellowpagesuk":
			self.ids.kivy_screen_manager.current = "yellowpagesuk"

		if next_screen == "back to main screen":
			self.ids.kivy_screen_manager.current = "start_screen"

#app object
class ScraperUIApp(App):

    def __init__(self, **kwargs):
        super(ScraperUIApp, self).__init__(**kwargs)


    def build(self):
        self.title = 'Scraper App'
        return MainScreen()

if __name__== '__main__':
    ScraperUIApp().run()