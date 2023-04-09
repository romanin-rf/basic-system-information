import os
import pathlib
import imp
import json
from rich.console import Console
# > Typing
from typing import Optional, List, Dict, Any, Tuple, Type
# > Local Imports
try:    from .plugincreator import PluginInfo, Plugin
except: from plugincreator import PluginInfo, Plugin
try:    from uix import BSIScreen, BSINavigationDrawerItem
except: from .uix import BSIScreen, BSINavigationDrawerItem

# ! Metadata
__name__ = "PluginCreator"
__version__ = "0.3.0"
__version_hash__ = hash(__version__)
__author__ = "Romanin"
__email__ = "semina054@gmail.com"

# ! Initialization
console = Console()

def lsattr(obj: object) -> Dict[str, Any]:
    attrs = {}
    for i in dir(obj): attrs[i] = eval(f"obj.{i}")
    return attrs

# ! Any Classes
class BSINavigationDrawerItemPlugin(BSINavigationDrawerItem):
    def __init__(self, *args, **kwargs):
        self.screen_name = kwargs.get("screen_name", "bsi")
        self.bsi_msm = kwargs.get("bsi_msm", None)
        kwargs.pop("screen_name")
        kwargs.pop("bsi_msm")
        super().__init__(*args, **kwargs)
    def on_release(self):
        if self.bsi_msm is not None:
            self.bsi_msm.current = self.screen_name

# ! PluginLoaderUI

# ! Plugin Loader
class PluginsConfig:
    @staticmethod
    def dump(config_path: pathlib.Path, data: Dict[str, Dict[str, Any]]) -> None:
        with open(config_path, "w") as config_file:
            json.dump(data, config_file)
    
    @staticmethod
    def load(config_path: pathlib.Path) -> Dict[str, Dict[str, Any]]:
        with open(config_path, "r") as config_file:
            return json.dump(config_file)
    
    def __init__(self, config_path: pathlib.Path) -> None:
        self.__name = config_path
        self.__data = {} # {"ID": {**settings}, ...}
        
        if self.__name.exists():
            try: self.__data = self.load(self.__name)
            except: self.__data = {} ; self.dump(self.__name, self.__data)
    
    @property
    def name(self) -> pathlib.Path: return self.__name
    @property
    def data(self) -> Dict[str, Dict[str, Any]]: return self.__data
    
    def exists_plugin(self, plugin_info: PluginInfo) -> bool: return plugin_info.name_id in self.__data.keys()
    def add_plugin(self, plugin_info: PluginInfo) -> None: ...
    def remove_plugin(self, plugin_info: PluginInfo) -> None: ...
    def change_settings(self, on: Optional[bool]=None) -> None: ...

class PluginLoader:
    def __init__(
        self,
        plugins_dirpath: str,
        config_path: str,
        bsi: Any
    ) -> None:
        self.plugins_dirpath = pathlib.Path(plugins_dirpath)
        self.config_path = pathlib.Path(config_path)
        self.config = PluginsConfig(self.config_path)
        self.bsi = bsi()
        
        if not self.plugins_dirpath.exists():
            self.plugins_dirpath.mkdir()
        
        # * Init Plugins Lists
        self.all_plugins: List[Tuple[PluginInfo, Type[Plugin]]] = []
        self.on_plugins: List[Tuple[PluginInfo, Plugin]] = []
        self.off_plugins: List[Tuple[PluginInfo, Plugin]] = []
    
    def get_plugins_path(self) -> List[Tuple[str, pathlib.Path]]:
        ls = []
        for i in os.listdir(self.plugins_dirpath):
            init_file_path = pathlib.Path(os.path.join(self.plugins_dirpath, i, "__init__.py"))
            if init_file_path.exists():
                ls.append( (i, init_file_path) )
        return ls
    
    def load_plugins(self) -> None:
        for plugin_name, plugin_path in self.get_plugins_path():
            try:
                plugin_data = imp.find_module(plugin_name, [plugin_path, self.plugins_dirpath])
                plugin_module = imp.load_module(plugin_name, *plugin_data)
                plugin_info: PluginInfo = plugin_module.plugin_info
                plugin: Type[Plugin] = plugin_module.plugin_main
                
                self.all_plugins.append( (plugin_info, plugin) )
            except:
                console.print_exception()
    
    def init_plugins(self) -> None:
        for plugin_info, plugin_type in self.all_plugins:
            try:
                plugin = plugin_type(self.bsi, self)
                plugin_ui_info = plugin.on_build_info_ui()
                if plugin_ui_info.init:
                    screen: BSIScreen = plugin.on_build()
                    self.bsi.bsi_msm.add_widget(screen)
                    self.bsi.bsi_nmfi.add_widget(
                        BSINavigationDrawerItemPlugin(
                            icon=plugin_ui_info.icon_name,
                            text=plugin_ui_info.display_name,
                            screen_name=plugin_ui_info.screen_name,
                            bsi_msm=self.bsi.bsi_msm
                        )
                    )
                self.on_plugins.append( (plugin_info, plugin) )
            except:
                console.print_exception()
    
    def start_plugins(self) -> None:
        for plugin_info, plugin in self.on_plugins:
            plugin.on_start()
    
    def stop_plugins(self) -> None:
        for plugin_info, plugin in self.on_plugins:
            plugin.on_stop()
    
    def run(self) -> None:
        self.load_plugins()
        self.bsi.run()