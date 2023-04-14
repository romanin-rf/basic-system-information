from rich.console import Console
# > KivyMD
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
# > Kivy
from kivy.clock import ClockBase
# > Typing
from typing import Tuple
# > Locals Modules
try:    from .uix import *
except: from uix import *
try:    from .pluginloader import PluginLoader
except: from pluginloader import PluginLoader

# ! App Info
__title__: str
__version__: str
__version_hash__: int
__author__: str
__email__: str

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