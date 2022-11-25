import os
import importlib
from kivy.uix.widget import Widget
from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Tuple

# ! Constants
LOCAL_PATH = os.path.dirname(__file__)
IGNORE_FILES = [os.path.basename(__file__), "__pycache__"]

# ! Dataclasses
@dataclass
class PluginInfo:
    name: str
    version: str

@dataclass
class PluginUI:
    title: str
    ui: Optional[Widget]
    initialising: bool

# ! Classes
class Plugin:
    def build_info(self) -> PluginInfo:
        return PluginInfo("PluginLoader", "0.1.0")
    
    def build_environ(self) -> Dict[str, Any]:
        return {}
    
    def build_ui(self) -> PluginUI:
        return PluginUI("PluginLoader", None, False)
    
    def build_priority(self) -> int:
        return 0
    
    def __init__(self) -> None:
        self.priority = self.build_priority()
        self.info: PluginInfo = self.build_info()
        self.environ: Dict[str, Any] = self.build_environ()
        self.ui: PluginUI = self.build_ui()
    
    def init(self) -> None:
        pass
    
    def on_start(self) -> None:
        pass
    
    def on_stop(self) -> None:
        pass

class PluginLoader:
    def __init__(
        self,
        plugins_dirpath: Optional[str]=None,
        ignore_files: Optional[List[str]]=None
    ) -> None:
        self.plugins_dirpath: str = plugins_dirpath or LOCAL_PATH
        self.ignore_files: List[str] = IGNORE_FILES if ignore_files is None else IGNORE_FILES+ignore_files
        self.environ: Dict[str, Any] = {}
        self.plugins: List[Plugin] = []
        self.dir_name = os.path.basename(self.plugins_dirpath)
    
    def get_plugins_paths(self) -> List[str]:
        ls = []
        for i in os.listdir(self.plugins_dirpath):
            if i not in self.ignore_files:
                ls.append(os.path.join(self.plugins_dirpath, i))
        return ls
    
    def load_plugins(self) -> None:
        for plugin_path in self.get_plugins_paths():
            plugin = importlib.import_module(".".join([self.dir_name, os.path.basename(plugin_path)]), plugin_path)
            self.plugins.append(plugin.Main)
        self.plugins.sort(key=lambda plugin: plugin.priority)
    
    def init_plugins(self) -> None:
        for plugin in self.plugins:
            plugin.init()
            self.environ.update(plugin.environ)
    
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
