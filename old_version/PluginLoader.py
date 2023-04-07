import os
import imp
import json
# > KivyMD
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
# > Kivy
from kivy.uix.switch import Switch
from kivy.uix.widget import Widget
# > Custom Modules
from kivymore.table import Table
# > Typing
from typing import Optional, List, Dict, Any, Tuple
# > Local Imports
try: from .PluginCreator import Plugin, PluginInfo, PluginUI, HiddenInt, Environ
except: from PluginCreator import Plugin, PluginInfo, PluginUI, HiddenInt, Environ

# ! Info
__title__ = "PluginLoader"
__version__ = "0.2.5"
__version_hash__ = hash(__version__)
__author__ = "Romanin"
__email__ = "semina054@gmail.com"

# ! Constants
LOCAL_PATH = os.path.dirname(__file__)
IGNORE_FILES = [os.path.basename(__file__), "__pycache__"]

# ! Functions
def ender(string: str, wigth: int=7) -> str:
    return string+(" "*(wigth-len(string)))

def log(tp: str="INFO", source: str="PLUGINS", text: str="") -> str:
    return "[{type_name}] [{source_name}] {text}".format(
        type_name=ender(tp, 7),
        source_name=ender(source, 12),
        text=text
    )

# ! Class Plugin Loader UI
plugin_loader_info = PluginInfo("PluginLoaderUI", __version__, __author__, "pl.ui")

class PluginLoaderUI(Plugin):
    def build_ui(self):
        scroll_view = MDScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=10,
            size_hint=(1.0, 1.0)
        )
        self.table = Table(["Priority", "ID", "Name", "Version", "Author", "UI", "On"])
        scroll_view.add_widget(self.table)
        return PluginUI("Plugin\nLoader UI", scroll_view, True)

    def build_priority(self) -> int:
        return HiddenInt(-4096)
    
    def change_button_text(self, instance: Switch, value: bool, plugin_id: str) -> None:
        self.environ.environ["plugin_loader"].update_plugin_config(plugin_id, value)
    
    def add_button_func(self, plugin_id: str):
        return lambda instance, value: self.change_button_text(instance, value, f"{plugin_id}")
    
    def init(self) -> None:
        for i in self.environ.environ["plugin_loader"].plugins:
            if i.info.id != self.info.id:
                switch_i = Switch(active=True)
                switch_i.bind(active=self.add_button_func(i.info.id))
            else:
                switch_i = MDLabel(text="...")
            with_ui = (i.ui.initialising) and (i.ui.ui is not None)
            with_ui_color = "00ff00" if with_ui else "ff0000"
            self.table.add_row(
                (
                    MDLabel(text=str(i.priority)),
                    MDLabel(text=str(i.info.id)),
                    MDLabel(text=i.info.name),
                    MDLabel(text=i.info.version),
                    MDLabel(text=i.info.author),
                    MDLabel(text=f"[color={with_ui_color}]{with_ui}[/color]", markup=True),
                    switch_i
                )
            )
        for i in self.environ.environ["plugin_loader"].off_plugins:
            switch_i = Switch(
                active=False,
                on_press=self.add_button_func(i.id)
            )
            switch_i.bind(active=self.add_button_func(i.id))
            self.table.add_row_alternative(
                (
                    "...",
                    MDLabel(text=str(i.id)),
                    MDLabel(text=i.name),
                    MDLabel(text=i.version),
                    MDLabel(text=i.author),
                    "...",
                    switch_i
                )
            )

# ! Class Plugin Loader
class PluginLoader:
    @staticmethod
    def load_plugins_config(filename: str) -> List[Dict[str, Any]]:
        if not os.path.exists(filename):
            with open(filename, "w") as file:
                json.dump([], file)
        return json.load(open(filename))
    
    @staticmethod
    def dump_plugins_config(filename: str, data: Any) -> None:
        with open(filename, "w") as file:
            json.dump(data, file)
    
    def __init__(
        self,
        plugins_dirpath: Optional[str]=None,
        ignore_files: Optional[List[str]]=None,
        environ: Optional[Environ]=None
    ) -> None:
        self.plugins_dirpath: str = plugins_dirpath or LOCAL_PATH
        self.ignore_files: List[str] = IGNORE_FILES if ignore_files is None else IGNORE_FILES+ignore_files
        self.config_name: str = "plugins_config.json"
        self.config: List[Dict[str, Any]] = self.load_plugins_config(self.config_name)
        
        # * Initialization Environs
        self.environ: Environ = environ or Environ()
        self.environ.environ.update({"plugin_loader": self})
        self.fake_environ: Environ = Environ()
        
        # * Initialization Plugins Lists
        self.plugins: List[Plugin] = [PluginLoaderUI(self.environ, plugin_loader_info)]
        self.off_plugins: List[PluginInfo] = []
    
    def get_plugin_from_id(self, plugin_id: str, version: Optional[str]=None) -> Optional[Plugin]:
        for i in self.plugins:
            if (i.info.id == plugin_id) and ((version == i.info.version) if version != None else True):
                return i
    
    def exist_in_config(self, plugin_id: str) -> Optional[Dict[str, Any]]:
        for i in self.config:
            if i["id"] == plugin_id:
                return i
        return None
    
    def add_plugin_in_config(self, plugin_info: PluginInfo) -> None:
        self.config.append({"name": plugin_info.name, "version": plugin_info.version, "id": plugin_info.id, "on": True})
        self.dump_plugins_config(self.config_name, self.config)
    
    def update_plugin_config(self, plugin_id: str, on: bool=None) -> None:
        for idx, item in enumerate(self.config):
            if item["id"] == plugin_id:
                plugin_cfg_idx, plugin_cfg = idx, item
                break
        plugin_cfg["on"] = on if (on is not None) else plugin_cfg["on"]

        self.config[plugin_cfg_idx] = plugin_cfg
        self.dump_plugins_config(self.config_name, self.config)
    
    def get_plugins_paths(self) -> List[Tuple[str, str]]:
        ls = []
        for i in os.listdir(self.plugins_dirpath):
            if i not in self.ignore_files:
                if os.path.exists(m_path:=os.path.join(self.plugins_dirpath, i, "__init__.py")):
                    ls.append((i, m_path))
        return ls
    
    def load_plugins(self) -> None:
        for plugin_name, plugin_path in self.get_plugins_paths():
            try:
                plugin_data = imp.find_module(plugin_name, [plugin_path, self.plugins_dirpath])
                plugin_module = imp.load_module(plugin_name, *plugin_data)
                print(log("INFO", "PLUGINS", f"The plugin `{plugin_name}` has been loaded"))
                plugin_info: PluginInfo = plugin_module.plugin_info
                print(log("INFO", "PLUGINS", f"Info about the `{plugin_name}` ({plugin_info.name}) plugin:"))
                print(log("INFO", "PLUGINS", f"\tID: {plugin_info.id}"))
                print(log("INFO", "PLUGINS", f"\tAUTHOR: {plugin_info.author}"))
                print(log("INFO", "PLUGINS", f"\tVERSION: {plugin_info.version}"))
                plugin: type[Plugin] = plugin_module.plugin_main

                if (cpli:=self.exist_in_config(plugin_info.id)) is not None:
                    plugin_on = cpli["on"]
                else:
                    self.add_plugin_in_config(plugin_info)
                    plugin_on = True
                if plugin_on:
                    self.plugins.append(plugin(self.environ, plugin_info))
                else:
                    self.off_plugins.append(plugin_info)
            except Exception as e:
                print(log("ERROR", "PLUGINS", f"Failed to load plugin `{plugin_name}` ({plugin_path})"))
                print(log("ERROR", "PLUGINS", f"{e.__class__.__name__}: {e.__str__()}"))
        self.plugins.sort(key=lambda plugin: plugin.priority)
    
    def init_plugins(self) -> None:
        for plugin in self.plugins:
            plugin.init()
    
    def get_uis(self) -> List[Tuple[str, Widget]]:
        ui_ls = []
        for plugin in self.plugins:
            if (plugin.ui.initialising) and (plugin.ui.ui is not None):
                ui_ls.append((plugin.ui.title, plugin.ui.ui))
        return ui_ls
    
    def start(self) -> None:
        for plugin in self.plugins:
            plugin.on_start()
    
    def stop(self) -> None:
        for plugin in self.plugins:
            plugin.on_stop()
