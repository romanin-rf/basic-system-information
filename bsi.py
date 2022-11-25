import os
import sys
import psutil
import time
from threading import Thread
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.config import Config
from kivy.lang.builder import Builder
from typing import Tuple
try:
    from plugins import PluginLoader as PluginLoader
except:
    import plugins.PluginLoader as PluginLoader

# ! Constants Info
__title__ = "BSI"
__version__ = "0.2.0"
__version_hash__ = hash(__version__)
__author__ = "Romanin"
__email__ = "semina054@gmail.com"

# ! Constants Path
LOCAL_DIR_PATH = os.path.dirname(__file__) \
    if os.path.basename(sys.executable).startswith("python") \
    else os.path.dirname(sys.executable)
CONFIG_PATH = os.path.join(LOCAL_DIR_PATH, "bin", "config.ini")
KIVY_UI_PATH = os.path.join(LOCAL_DIR_PATH, "bin", "ui.kv")

# ! Plugin Loader Initialization
plugin_loader = PluginLoader.PluginLoader(ignore_files=["_ExamplePlugin"])

# ! Config Initialization
Config.read(CONFIG_PATH)

plugin_loader.environ["config"] = Config

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
plugin_loader.load_plugins()

# ! Main Class
class BSI(App):
    def build(self):
        for i in plugin_loader.get_uis():
            tpi = TabbedPanelItem(text=i[0])
            tpi.add_widget(i[1])
            self.w_root.add_widget(tpi)
        return self.w_root
    
    def ubsi(
        self,
        obj_cpu_load_value: Label,
        obj_cpu_load_prbar: ProgressBar,
        obj_ram_busy_value: Label,
        obj_ram_busy_prbar: ProgressBar,
        obj_swap_busy_value: Label,
        obj_swap_busy_prbar: ProgressBar
    ):
        while self.ubsi_running:
            try:
                cpu_load = psutil.cpu_percent()
                ram_busy = get_ram_info()
                swap_busy = get_swap_info()
                #print(self.root_window.width, self.root_window.height, sep="x")
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
        plugin_loader.start()
    
    def on_stop(self):
        self.ubsi_running = False
        plugin_loader.stop()
    
    w_root: TabbedPanel = Builder.load_file(KIVY_UI_PATH)
    ubsi_running: bool = False
    update_timeout = float(Config.get("bsi", "update_timeout"))

# ! Starting
if __name__ == '__main__':
    plugin_loader.init_plugins()
    bsi = BSI()
    bsi.title = f"{__title__} v{__version__}"
    bsi.config = plugin_loader.environ["config"]
    bsi.run()
