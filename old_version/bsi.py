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
# > Kivy
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.config import Config
from kivy.lang.builder import Builder
# > Typing
from typing import Tuple
# > Дополнительные библеотеки для создания плагинов
import keyboard, mouse

# ! Other
NO_PLUGIN_ARGUMENT = "/noplugins"
if NO_PLUGIN_ARGUMENT not in sys.argv:
    try: import PluginLoader as PluginLoader
    except: from . import PluginLoader as PluginLoader

# ! Constants Info
__title__ = "BSI"
__version__ = "0.2.12"
__version_hash__ = hash(__version__)
__author__ = "Romanin"
__email__ = "semina054@gmail.com"

# ! Constants Path
LOCAL_DIR_PATH = os.path.dirname(__file__) \
    if os.path.basename(sys.executable).startswith("python") \
    else os.path.dirname(sys.executable)
ICON_PATH = os.path.join(LOCAL_DIR_PATH, "bin", "icon.png")
CONFIG_PATH = os.path.join(LOCAL_DIR_PATH, "bin", "config.ini")
KIVY_UI_PATH = os.path.join(LOCAL_DIR_PATH, "bin", "ui.kv")
PLUGINS_PATH = os.path.join(LOCAL_DIR_PATH, "plugins")

# ! Plugin Loader Initialization
if NO_PLUGIN_ARGUMENT not in sys.argv:
    bsi_environ = PluginLoader.Environ()
    plugin_loader = PluginLoader.PluginLoader(PLUGINS_PATH, ["_ExamplePlugin"], bsi_environ)

# ! Config Initialization
Config.read(CONFIG_PATH)
if NO_PLUGIN_ARGUMENT not in sys.argv:
    bsi_environ.environ["config"] = Config

# ! Functions
def get_ram_info() -> Tuple[int, int, int, float]:
    vm = psutil.virtual_memory()
    return \
        round((vm.total/1024)/1024), \
        round(((vm.total-vm.free)/1024)/1024), \
        round((vm.free/1024)/1024), \
        round(((vm.total-vm.free)/vm.total)*100,1)

def get_swap_info():
    sm = psutil.swap_memory()
    return \
        round((sm.total/1024)/1024), \
        round(((sm.total-sm.free)/1024)/1024), \
        round((sm.free/1024)/1024), \
        round(((sm.total-sm.free)/sm.total)*100,1)

# ! Loading Plugins
if NO_PLUGIN_ARGUMENT not in sys.argv:
    plugin_loader.load_plugins()

# ! Main Class
class BSI(MDApp):
    def build(self):
        self.icon = ICON_PATH
        self.w_root: TabbedPanel = Builder.load_file(KIVY_UI_PATH)
        if NO_PLUGIN_ARGUMENT not in sys.argv:
            for i in plugin_loader.get_uis():
                tpi = TabbedPanelItem(text=i[0])
                tpi.add_widget(i[1])
                self.w_root.add_widget(tpi)
        return self.w_root
    
    def ubsi(
        self,
        obj_cpu_load_value: MDLabel,
        obj_cpu_load_prbar: MDProgressBar,
        obj_ram_busy_value: MDLabel,
        obj_ram_busy_prbar: MDProgressBar,
        obj_swap_busy_value: MDLabel,
        obj_swap_busy_prbar: MDProgressBar
    ):
        while self.ubsi_running:
            try:
                cpu_load = psutil.cpu_percent()
                ram_busy = get_ram_info()
                swap_busy = get_swap_info()
                # // print(self.root_window.width, self.root_window.height, sep="x")
                obj_cpu_load_value.text = f"{round(cpu_load,1)} %"
                obj_cpu_load_prbar.value = cpu_load
                obj_ram_busy_value.text = f"{ram_busy[1]} MB ({ram_busy[3]} %)"
                obj_ram_busy_prbar.value = ram_busy[3]
                obj_swap_busy_value.text = f"{swap_busy[1]} MB ({swap_busy[3]} %)"
                obj_swap_busy_prbar.value = swap_busy[3]
                
                time.sleep(self.update_timeout)
            except:
                pass
    
    def on_start(self):
        self.ubsi_running = True
        self.w_root.ids["LabelRAMTotal"].text = f"{get_ram_info()[0]} MB"
        self.w_root.ids["LabelSWAPTotal"].text = f"{get_swap_info()[0]} MB"
        Thread(
            target=self.ubsi,
            args=(
                self.w_root.ids["LabelCPULoad"],
                self.w_root.ids["ProgressBarCPULoad"],
                self.w_root.ids["LabelRAMBusy"],
                self.w_root.ids["ProgressBarRAMBusy"],
                self.w_root.ids["LabelSWAPBusy"],
                self.w_root.ids["ProgressBarSWAPBusy"]
            )
        ).start()
        if NO_PLUGIN_ARGUMENT not in sys.argv:
            plugin_loader.start()
    
    def on_stop(self):
        self.ubsi_running = False
        if NO_PLUGIN_ARGUMENT not in sys.argv:
            plugin_loader.stop()
    
    ubsi_running: bool = False
    update_timeout = float(Config.get("bsi", "update_timeout"))

# ! Starting
if __name__ == '__main__':
    bsi = BSI()
    if NO_PLUGIN_ARGUMENT not in sys.argv:
        bsi_environ.environ["bsi"] = bsi
        plugin_loader.init_plugins()
    bsi.title = f"{__title__} v{__version__}"
    bsi.run()
