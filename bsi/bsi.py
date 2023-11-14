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
from kivy.clock import Clock
# > Typing
from typing import Tuple, Dict, Any
# > Locals Modules
try:    from .uix import *
except: from bsi.uix import *
try:    from .plugin.loader import PluginLoader
except: from bsi.plugin.loader import PluginLoader

# ! App Info
__title__ = "BSI"
__version__ = "0.4.0"
__version_hash__ = hash(__version__)
__author__ = "Romanin"
__email__ = "semina054@gmail.com"

# ! Other
console = Console()

def lsattr(obj: object) -> Dict[str, Any]:
    attrs = {}
    for i in dir(obj): attrs[i] = eval(f"obj.{i}")
    return attrs

LOCAL_DIR_PATH = ...
ICON_PATH = ...
MAIN_UI_PATH = ...
PLUGINS_PATH = ...
PLUGINS_CONFIG_PATH = ...
def get_asset_path(path: str) -> str: ...

def init(file: str) -> None:
    global LOCAL_DIR_PATH, ICON_PATH, MAIN_UI_PATH, PLUGINS_PATH, PLUGINS_CONFIG_PATH, get_asset_path
    
    LOCAL_DIR_PATH = os.path.dirname(file) \
        if os.path.basename(sys.executable).startswith("python") \
        else os.path.dirname(sys.executable)
    
    def get_asset_path(path: str) -> str:
        return os.path.join(LOCAL_DIR_PATH, path).replace('\\', os.sep).replace('/', os.sep)

    # ! Path Constants
    ICON_PATH = get_asset_path("bin/icon_100x100.png")
    MAIN_UI_PATH = get_asset_path("bin/ui_main.kv")
    PLUGINS_PATH = get_asset_path("plugins")
    PLUGINS_CONFIG_PATH = get_asset_path("plugins_config.json")

# ! Functions
def get_ram_info() -> Tuple[int, int, int, float]:
    vm = psutil.virtual_memory()
    return \
        round((vm.total/1024)/1024), \
        round(((vm.total-vm.free)/1024)/1024), \
        round((vm.free/1024)/1024), \
        round(((vm.total-vm.free)/vm.total)*100,1)

def get_swap_info() -> Tuple[int, int, int, float]:
    sm = psutil.swap_memory()
    return \
        round((sm.total/1024)/1024), \
        round(((sm.total-sm.free)/1024)/1024), \
        round((sm.free/1024)/1024), \
        round(((sm.total-sm.free)/sm.total)*100,1)

# ! Main Class
class BSI(MDApp):
    def build(self):
        self.icon = ICON_PATH
        self.title = f"{__title__}"
        self.bsi_version = f"v{__version__}"
        
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"
        self.clock = Clock
        
        self.bsi_root: MDScreen = Builder.load_file(MAIN_UI_PATH)
        self.bsi_msm: MDScreenManager = self.bsi_root.ids["main_screen_manager"]
        self.bsi_ms: BSIScreen = self.bsi_msm.get_screen("bsi")
        self.bsi_nmfi: MDNavigationDrawerMenu = self.bsi_root.ids["main_navigate_menu_driwer"]
        
        pl.init_plugins()
        
        return self.bsi_root
    
    def update_bsi_ms(self, dt) -> None:
        cpu_load = round(psutil.cpu_percent())
        ram_busy = get_ram_info()
        swap_busy = get_swap_info()
        
        self.bsi_root.ids["ProgressBarCPULoad"].value = cpu_load
        self.bsi_root.ids["LabelCPULoad"].text = f"{cpu_load} %"
        
        self.bsi_root.ids["ProgressBarRAMBusy"].value = ram_busy[3]
        self.bsi_root.ids["LabelRAMBusy"].text = f"{ram_busy[1]} MB ({ram_busy[3]} %)"
        
        self.bsi_root.ids["ProgressBarSWAPBusy"].value = swap_busy[3]
        self.bsi_root.ids["LabelSWAPBusy"].text = f"{swap_busy[1]} MB ({swap_busy[3]} %)"
    
    def on_start(self):
        pl.start_plugins()
        self.bsi_root.ids["LabelRAMTotal"].text = f"{get_ram_info()[0]} MB"
        self.bsi_root.ids["LabelSWAPTotal"].text = f"{get_swap_info()[0]} MB"
        self.clock.schedule_interval(self.update_bsi_ms, 0.5)
    
    def on_stop(self):
        pl.stop_plugins()

pl: PluginLoader = ...

# ! Start
def start_bsi() -> None:
    global pl

    pl = PluginLoader(PLUGINS_PATH, PLUGINS_CONFIG_PATH, BSI)
    pl.run()