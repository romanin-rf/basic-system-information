import os
import sys
import psutil
from rich.console import Console
# > KivyMD
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.navigationdrawer import MDNavigationDrawerMenu
# > Kivy
from kivy.lang.builder import Builder
from kivy.clock import Clock, ClockBase
# > Typing
from typing import Tuple
# > Дополнительные библеотеки для создания плагинов
import keyboard, mouse
# > Locals Modules
try:    from .uix import *
except: from uix import *
try:    from .pluginloader import PluginLoader
except: from pluginloader import PluginLoader

# ! App Info
__title__ = "BSI"
__version__ = "0.3.1"
__version_hash__ = hash(__version__)
__author__ = "Romanin"
__email__ = "semina054@gmail.com"

# ! Environment
console: Console
LOCAL_DIR_PATH: str
ICON_PATH: str
MAIN_UI_PATH: str
PLUGINS_PATH: str
PLUGINS_CONFIG_PATH: str

bsi: BSI = ...
pl: PluginLoader = ...

# ! Functions
def get_asset_path(path: str) -> str: ...
def init(file: str) -> None: ...
def get_ram_info() -> Tuple[int, int, int, float]: ...
def get_swap_info() -> Tuple[int, int, int, float]: ...
def start_bsi() -> None: ...

# ! Main Class
class BSI(MDApp):
    clock: ClockBase
    bsi_version: str
    bsi_root: MDScreen
    bsi_msm: MDScreenManager
    bsi_ms: BSIScreen
    def update_bsi_ms(self, dt) -> None: ...