import os
import sys
import psutil
import time
from threading import Thread
# > KivyMD
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.navigationdrawer import MDNavigationDrawerMenu, MDNavigationDrawer, MDNavigationDrawerItem
# > Kivy
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.lang.builder import Builder
from kivy.properties import ColorProperty, StringProperty, NumericProperty
# > Typing
from typing import Tuple
# > Дополнительные библеотеки для создания плагинов
import keyboard, mouse
# > Locals Modules
try: from bsi_obj import *
except: from .bsi_obj import *

# ! App Info
__title__ = "BSI"
__version__ = "0.3.0"
__version_hash__ = hash(__version__)
__author__ = "Romanin"
__email__ = "semina054@gmail.com"

# ! Other
LOCAL_DIR_PATH = os.path.dirname(__file__) \
    if os.path.basename(sys.executable).startswith("python") \
    else os.path.dirname(sys.executable)

def get_asset_path(path: str) -> str:
    return os.path.join(LOCAL_DIR_PATH, path).replace('\\', os.sep).replace('/', os.sep)

# ! Path Constants
ICON_PATH = get_asset_path("bin/icon.png")
MAIN_UI_PATH = get_asset_path("bin/ui_main.kv")
PLUGINS_PATH = get_asset_path("plugins")

# ! Main Class
class BSI(MDApp):
    def build(self):
        self.icon = ICON_PATH
        self.title = f"{__title__}"
        self.bsi_version = f"v{__version__}"
        
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"
        
        root: MDScreen = Builder.load_file(MAIN_UI_PATH)

        return root

# ! Start
if __name__ == "__main__":
    bsi = BSI()
    bsi.run()