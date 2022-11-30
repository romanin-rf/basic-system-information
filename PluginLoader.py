import os
import imp
import json
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.uix.scrollview import ScrollView
from kivymore.table import Table
from typing import Optional, List, Dict, Any, Tuple
# * Local Imports
try:
    from .PluginCreator import Plugin, PluginInfo, PluginUI, HiddenInt, Environ
except:
    from PluginCreator import Plugin, PluginInfo, PluginUI, HiddenInt, Environ

# ! Info
__title__ = "PluginLoader"
__version__ = "0.2.2"
__version_hash__ = hash(__version__)
__author__ = "Romanin"
__email__ = "semina054@gmail.com"

# ! Constants
LOCAL_PATH = os.path.dirname(__file__)
IGNORE_FILES = [os.path.basename(__file__), "__pycache__"]

# ! Class Plugin Loader UI
plugin_loader_info = PluginInfo("PluginLoaderUI", __version__, __author__, "pl.ui")

class PluginLoaderUI(Plugin):
    def build_ui(self):
        scroll_view = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=10,
            size_hint=(1.0, 1.0)
        )
        self.table = Table(["ID", "Priority", "Name", "Version", "Author", "UI", "On"])
        scroll_view.add_widget(self.table)
        return PluginUI("Plugin\nLoader UI", scroll_view, True)

    def build_priority(self) -> int:
        return HiddenInt(-4096)
    
    def add_row_in_ui(self, data: Tuple[Widget, Widget, Widget, Widget, Widget, Widget, Widget]) -> int:
        self.table.add_row(data)
    
    def change_button_text(self, instance: Switch, value: bool, plugin_id: str) -> None:
        self.environ.environ["plugin_loader"].update_plugin_config(plugin_id, value)
    
    def add_button_func(self, plugin_id: str, none: bool=False):
        if not none:
            return lambda instance, value: self.change_button_text(instance, value, f"{plugin_id}")
        else:
            return lambda instance: None
    
    def init(self) -> None:
        for i in self.environ.environ["plugin_loader"].plugins:
            if i.info.id != self.info.id:
                switch_i = Switch(active=True)
                switch_i.bind(active=self.add_button_func(i.info.id))
            else:
                switch_i = Label(text="...")
            self.add_row_in_ui(
                (
                    Label(text=str(i.priority)),
                    Label(text=str(i.info.id)),
                    Label(text=i.info.name),
                    Label(text=i.info.version),
                    Label(text=i.info.author),
                    Label(text=str( (i.ui.initialising) and (i.ui.ui is not None) )),
                    switch_i
                )
            )
        i: PluginInfo
        for i in self.environ.environ["plugin_loader"].off_plugins:
            switch_i = Switch(
                active=False,
                on_press=self.add_button_func(i.id)
            )
            switch_i.bind(active=self.add_button_func(i.id))
            self.add_row_in_ui(
                (
                    Label(text="..."),
                    Label(text=str(i.id)),
                    Label(text=i.name),
                    Label(text=i.version),
                    Label(text=i.author),
                    Label(text="..."),
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
            plugin_data = imp.find_module(plugin_name, [plugin_path, self.plugins_dirpath])
            plugin_module = imp.load_module(plugin_name, *plugin_data)
            plugin_info: PluginInfo = plugin_module.plugin_info
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
