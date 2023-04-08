import os
import sys
import psutil
import time
from threading import Thread
from rich.console import Console
# > KivyMD
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.navigationdrawer import MDNavigationDrawerMenu, MDNavigationDrawer, MDNavigationDrawerItem
# > Kivy
from kivy.lang.builder import Builder
from kivy.clock import Clock
# > Typing
from typing import Tuple
# > Дополнительные библеотеки для создания плагинов
import keyboard, mouse
# > Locals Modules
try: from kivybsi.objects import *
except: from .kivybsi.objects import *

# ! App Info
__title__ = "BSI"
__version__ = "0.3.0"
__version_hash__ = hash(__version__)
__author__ = "Romanin"
__email__ = "semina054@gmail.com"

# ! Other
console = Console()
LOCAL_DIR_PATH = os.path.dirname(__file__) \
    if os.path.basename(sys.executable).startswith("python") \
    else os.path.dirname(sys.executable)

def get_asset_path(path: str) -> str:
    return os.path.join(LOCAL_DIR_PATH, path).replace('\\', os.sep).replace('/', os.sep)

# ! Path Constants
ICON_PATH = get_asset_path("bin/icon.png")
MAIN_UI_PATH = get_asset_path("bin/ui_main.kv")
PLUGINS_PATH = get_asset_path("plugins")

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
    
    def on_start(self) -> None:
        self.bsi_root.ids["LabelRAMTotal"].text = f"{get_ram_info()[0]} MB"
        self.bsi_root.ids["LabelSWAPTotal"].text = f"{get_swap_info()[0]} MB"
        self.clock.schedule_interval(self.update_bsi_ms, 0.5)

# ! Start
if __name__ == "__main__":
    bsi = BSI()
    bsi.run()