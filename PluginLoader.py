import os
import imp
import json
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang.builder import Builder
from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Tuple

# ! Info
__title__ = "PluginLoader"
__version__ = "0.1.5"
__version_hash__ = hash(__version__)
__author__ = "Romanin"
__email__ = "semina054@gmail.com"

# ! Constants
LOCAL_PATH = os.path.dirname(__file__)
IGNORE_FILES = [os.path.basename(__file__), "__pycache__"]

# ! Dataclasses
@dataclass
class PluginInfo:
    name: str
    version: str
    author: str
    id: str

@dataclass
class PluginUI:
    title: str
    ui: Optional[Widget]
    initialising: bool

# ! Classes
class Plugin:
    def build_info(self) -> PluginInfo:
        return PluginInfo(__title__, __version__, __author__, "bsi.plugins.loader")
    
    def build_environ(self) -> Dict[str, Any]:
        return {}
    
    def build_ui(self) -> PluginUI:
        return PluginUI("Plugin\nLoader", None, False)
    
    def build_priority(self) -> int:
        return 0
    
    def __init__(self) -> None:
        self.priority = self.build_priority()
        self.info: PluginInfo = self.build_info()
        self.environ: Dict[str, Any] = self.build_environ()
        self.ui: PluginUI = self.build_ui()
    
    def init(self, self_pl: Any) -> None:
        pass
    
    def on_start(self) -> None:
        pass
    
    def on_stop(self) -> None:
        pass

# ! Class Plugin Loader UI
plugin_loader_ui = Builder.load_string(
"""\
BoxLayout:
    GridLayout:
        id: COLID
        cols: 1
        row_force_default: True
        row_default_height: 30
        Button:
            text: 'ID'
    GridLayout:
        id: COLPriority
        cols: 1
        row_force_default: True
        row_default_height: 30
        Button:
            text: 'Priority'
    GridLayout:
        id: COLName
        cols: 1
        row_force_default: True
        row_default_height: 30
        Button:
            text: 'Name'
    GridLayout:
        id: COLVersion
        cols: 1
        row_force_default: True
        row_default_height: 30
        Button:
            text: 'Version'
    GridLayout:
        id: COLAuthor
        cols: 1
        row_force_default: True
        row_default_height: 30
        Button:
            text: 'Author'
    GridLayout:
        id: COLWithUI
        cols: 1
        row_force_default: True
        row_default_height: 30
        Button:
            text: 'UI'
    GridLayout:
        id: COLOn
        cols: 1
        row_force_default: True
        row_default_height: 30
        Button:
            text: 'On'
"""
)

class HiddenInt(int):
    def __str__(self) -> None:
        return "..."

class PluginLoaderUIPlugin(Plugin):    
    def build_info(self) -> PluginInfo:
        return PluginInfo("PluginLoaderUI", __version__, __author__, "pl.ui")
    
    def build_ui(self):
        return PluginUI("Plugin\nLoader UI", plugin_loader_ui, True)

    def build_priority(self) -> int:
        return HiddenInt(-1024)
    
    def add_row_in_ui(self, data: Tuple[Widget, Widget, Widget, Widget, Widget, Widget, Widget]) -> int:
        self.ui.ui.ids["COLPriority"].add_widget(data[0])
        self.ui.ui.ids["COLID"].add_widget(data[1])
        self.ui.ui.ids["COLName"].add_widget(data[2])
        self.ui.ui.ids["COLVersion"].add_widget(data[3])
        self.ui.ui.ids["COLAuthor"].add_widget(data[4])
        self.ui.ui.ids["COLWithUI"].add_widget(data[5])
        self.ui.ui.ids["COLOn"].add_widget(data[6])
    
    def change_button_text(self, instance: Button, plugin_id: str) -> None:
        is_on = False if (instance.text == "Yes") else True
        instance.text = "Yes" if is_on else "No"
        self.environ["plugin_loader"].update_plugin_config(plugin_id, is_on)
    
    def add_button_func(self, plugin_id: str, none: bool=False):
        if not none:
            return lambda instance: self.change_button_text(instance, f"{plugin_id}")
        else:
            return lambda instance: None
    
    def init(self, self_pl: Any) -> None:
        for i in self_pl.plugins:
            button_i = Button(
                text="Yes" if (i.info.id != self.info.id) else "...",
                on_press=self.add_button_func(i.info.id, i.info.id==self.info.id)
            )
            self.add_row_in_ui(
                (
                    Label(text=str(i.priority)),
                    Label(text=str(i.info.id)),
                    Label(text=i.info.name),
                    Label(text=i.info.version),
                    Label(text=i.info.author),
                    Label(text=str( (i.ui.initialising) and (i.ui.ui is not None) )),
                    button_i
                )
            )
        i: Plugin
        for i in self_pl.off_plugins:
            button_i = Button(
                text="No",
                on_press=self.add_button_func(i.info.id, False)
            )
            self.add_row_in_ui(
                (
                    Label(text=str(i.priority)),
                    Label(text=str(i.info.id)),
                    Label(text=i.info.name),
                    Label(text=i.info.version),
                    Label(text=i.info.author),
                    Label(text=str( (i.ui.initialising) and (i.ui.ui is not None) )),
                    button_i
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
        ignore_files: Optional[List[str]]=None
    ) -> None:
        self.plugins_dirpath: str = plugins_dirpath or LOCAL_PATH
        self.ignore_files: List[str] = IGNORE_FILES if ignore_files is None else IGNORE_FILES+ignore_files
        self.environ: Dict[str, Any] = {"plugin_loader": self}
        self.plugins: List[Plugin] = [PluginLoaderUIPlugin()]
        self.plugins[0].environ.update(self.environ)
        self.config_name: str = "plugins_config.json"
        self.config: List[Dict[str, Any]] = self.load_plugins_config(self.config_name)
        self.off_plugins: List[Plugin] = []
    
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
            plugin: Plugin = imp.load_module(plugin_name, *plugin_data).Main
            if (cpli:=self.exist_in_config(plugin.info.id)) is not None:
                plugin_on = cpli["on"]
            else:
                self.add_plugin_in_config(plugin.info)
                plugin_on = True
            if plugin_on:
                plugin.environ.update(self.environ)
                self.plugins.append(plugin)
            else:
                self.off_plugins.append(plugin)
        self.plugins.sort(key=lambda plugin: plugin.priority)
    
    def init_plugins(self) -> None:
        for plugin in self.plugins:
            plugin.init(self)
    
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
