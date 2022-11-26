import os
import imp
from kivy.uix.widget import Widget
from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Tuple

# ! Info
__title__ = "PluginLoader"
__version__ = "0.1.1"
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

@dataclass
class PluginUI:
    title: str
    ui: Optional[Widget]
    initialising: bool

# ! Classes
class Plugin:
    def build_info(self) -> PluginInfo:
        return PluginInfo(__title__, __version__)
    
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
            plugin = imp.load_module(plugin_name, *plugin_data)
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
