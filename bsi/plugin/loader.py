import os
import sys
import subprocess
import pathlib
import imp
import json
from rich.console import Console
# > KivyMD
from kivymd.uix.list import MDList
from kivymd.uix.scrollview import MDScrollView
# > Typing
from typing import Optional, List, Dict, Any, Tuple, Type
from types import ModuleType
# > Local Imports
try:    from .creator import PluginInfo, Plugin, PluginUIInfo, is_supported_plugin
except: from bsi.plugin.creator import PluginInfo, Plugin, PluginUIInfo, is_supported_plugin
try:    from ..uix import *
except: from bsi.uix import *

# ! Metadata
__name__ = "PluginLoader"
__version__ = "0.4.0"
__version_hash__ = hash(__version__)
__author__ = "Romanin"
__email__ = "semina054@gmail.com"

# ! Initialization
console = Console()

def lsattr(obj: object) -> Dict[str, Any]:
    attrs = {}
    for i in dir(obj): attrs[i] = eval(f"obj.{i}")
    return attrs

def pip(*args) -> None:
    subprocess.check_output([sys.executable, "-m", "pip", *args, "--no-input", "--no-color", "--no-python-version-warning", "--disable-pip-version-check"])

# ! Any Classes
class PluginModuleType(ModuleType):
    plugin_info: PluginInfo
    plugin_ui_info: PluginUIInfo
    plugin_main: Type[Plugin]
    @staticmethod
    def pre_init(pl: Any, bsi: Any) -> None: ...
    def __init__(self, name: str, doc: Optional[str]=..., **kwargs) -> None:
        super().__init__(name, doc)
        self.plugin_info = kwargs.get("plugin_info", None)
        self.plugin_ui_info = kwargs.get("plugin_ui_info", None)
        self.plugin_main = kwargs.get("plugin_main", None)
        if (pre_init_func:=kwargs.get("pre_init", None)) is not None:
            self.pre_init = pre_init_func

# ! PluginLoaderUI
PluginLoaderUI_Info = PluginInfo(
    "Plugin Loader UI",
    "bsi.pluginloader.ui",
    "UI for PluginLoader.",
    __version__,
    "Romanin",
    ["any"], ["any"]
)
PluginLoaderUI_UIInfo = PluginUIInfo(True, "archive-plus", "plugin_loader_ui_screen", "Plugin Loader UI")

class PluginLoaderUI(Plugin):
    def on_build(self):
        self.root_screen = BSIScreen(name="plugin_loader_ui_screen")
        self.plugins_list_scroll = MDScrollView()
        self.plugins_list = MDList()
        
        self.plugins_list_scroll.add_widget(self.plugins_list)
        self.root_screen.add_widget(self.plugins_list_scroll)
        
        # * ...
        self.plugins_list.add_widget(
            BSIList3LinesSwitchItem(
                "archive-plus",
                f"Plugin Loader UI ({__version__})",
                "bsi.pluginloader.ui",
                "Romanin",
                True,
                True,
                None,
                PluginLoaderUI_Info,
                PluginLoaderUI_UIInfo
            )
        )
        
        return self.root_screen
    
    def on_start(self) -> None:
        for i in self.plugin_loader.on_plugins:
            plugin_module: PluginModuleType = i[0]
            self.plugins_list.add_widget(
                BSIList3LinesSwitchItem(
                    plugin_module.plugin_ui_info.icon_name,
                    f"{plugin_module.plugin_info.name} (v{plugin_module.plugin_info.version})",
                    plugin_module.plugin_info.name_id,
                    plugin_module.plugin_info.author,
                    True,
                    False,
                    self.plugin_loader,
                    plugin_module.plugin_info,
                    plugin_module.plugin_ui_info
                )
            )
        
        for i in self.plugin_loader.off_plugins:
            plugin_module: PluginModuleType = i
            self.plugins_list.add_widget(
                BSIList3LinesSwitchItem(
                    plugin_module.plugin_ui_info.icon_name,
                    f"{plugin_module.plugin_info.name} (v{plugin_module.plugin_info.version})",
                    plugin_module.plugin_info.name_id,
                    plugin_module.plugin_info.author,
                    False,
                    False,
                    self.plugin_loader,
                    plugin_module.plugin_info,
                    plugin_module.plugin_ui_info
                )
            )

# ! Plugin Loader
class PluginsConfig:
    @staticmethod
    def dump(config_path: pathlib.Path, data: Dict[str, Dict[str, Any]]) -> None:
        with open(config_path, "w") as config_file:
            json.dump(data, config_file)
    
    @staticmethod
    def load(config_path: pathlib.Path) -> Dict[str, Dict[str, Any]]:
        with open(config_path) as config_file:
            return json.load(config_file)
    
    def __init__(self, config_path: pathlib.Path) -> None:
        self.__name = config_path
        self.__data = {} # {"ID": {**settings}, ...}
        
        if self.__name.exists():
            try: self.__data = self.load(self.__name)
            except: self.__data = {} ; self.dump(self.__name, self.__data)
        else:
            self.__data = {} ; self.dump(self.__name, self.__data)
    
    @property
    def name(self) -> pathlib.Path: return self.__name
    @property
    def data(self) -> Dict[str, Dict[str, Any]]: return self.__data
    
    def exists_plugin(self, plugin_info: PluginInfo) -> bool:
        return plugin_info.name_id in self.__data.keys()

    def add_plugin(self, plugin_info: PluginInfo) -> None:
        self.__data[plugin_info.name_id] = {
            "name": plugin_info.name,
            "name_id": plugin_info.name_id,
            "version": plugin_info.version,
            "author": plugin_info.author,
            "enabled": True
        }
        self.refresh()

    def remove_plugin(self, plugin_info: PluginInfo) -> None:
        try:
            del self.__data[plugin_info.name_id]
            self.refresh()
        except:
            console.print_exception()

    def change_settings(self, plugin_info: PluginInfo, enabled: Optional[bool]=None) -> None:
        try:
            self.__data[plugin_info.name_id]["enabled"] = self.__data[plugin_info.name_id]["enabled"] if enabled is None else enabled
            self.refresh()
        except:
            console.print_exception()
    
    def get_plugin_settings(self, plugin_info: PluginInfo) -> Optional[Dict[str, Any]]:
        if self.exists_plugin(plugin_info):
            return self.__data[plugin_info.name_id]
    
    def refresh(self) -> None: self.dump(self.__name, self.__data)

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
        self.plm = PluginModuleType(
            "PluginLoaderUI",
            "...",
            plugin_info=PluginLoaderUI_Info,
            plugin_ui_info=PluginLoaderUI_UIInfo,
            plugin_main=PluginLoaderUI
        )
        self.plugin_loader_ui: PluginLoaderUI = ...
        
        if not self.plugins_dirpath.exists():
            self.plugins_dirpath.mkdir()
        
        # * Init Plugins Lists
        self.all_plugins: List[PluginModuleType] = []
        self.on_plugins: List[Tuple[PluginModuleType, Plugin]]  = []
        self.off_plugins: List[PluginModuleType] = []
    
    def get_plugin(self, name_id: str) -> Optional[PluginModuleType]:
        for i in self.all_plugins:
            if i.plugin_info.name_id == name_id:
                return i
    
    def get_plugins_path(self) -> List[Tuple[str, pathlib.Path, Optional[pathlib.Path]]]:
        ls = []
        for i in os.listdir(self.plugins_dirpath):
            init_file_path = pathlib.Path(os.path.join(self.plugins_dirpath, i, "__init__.py"))
            requirements_path_file = pathlib.Path(os.path.join(self.plugins_dirpath, i, "requirements.txt"))
            
            if init_file_path.exists():
                if requirements_path_file.exists():
                    ls.append( (i, init_file_path, requirements_path_file) )
                else:
                    ls.append( (i, init_file_path, None) )
        return ls
    
    def load_plugins(self) -> None:
        plp = self.get_plugins_path()
        
        for plugin_name, plugin_path, requirements_path in plp:
            if requirements_path is not None:
                pip("install", "-r", f"{requirements_path}")
        
        for plugin_name, plugin_path, requirements_path in plp:
            try:
                
                
                plugin_data = imp.find_module(plugin_name, [plugin_path, self.plugins_dirpath])
                plugin_module: PluginModuleType = imp.load_module(plugin_name, *plugin_data)
                
                if is_supported_plugin(plugin_module.plugin_info):
                    if not self.config.exists_plugin(plugin_module.plugin_info):
                        self.config.add_plugin(plugin_module.plugin_info)

                    if (plugin_settings:=self.config.get_plugin_settings(plugin_module.plugin_info)) is not None:
                        if plugin_settings["enabled"]: self.all_plugins.append(plugin_module)
                        else: self.off_plugins.append(plugin_module)
                    else:
                        try: raise RuntimeError(f"Critical error when loading the '{plugin_module.plugin_info.name}' ({plugin_module.plugin_info.name_id}) plugin.")
                        except: console.print_exception()
                else:
                    self.off_plugins.append(plugin_module)
            except: console.print_exception()
    
    def init_plugins(self) -> None:
        if (pre_init_plugin_func:=getattr(self.plm, "pre_init", None)) is not None:
            pre_init_plugin_func(self, self.bsi)
        
        self.plugin_loader_ui = self.plm.plugin_main(self.bsi, self)
        
        if self.plm.plugin_ui_info.init:
            self.bsi.bsi_msm.add_widget(self.plugin_loader_ui.on_build())
            self.bsi.bsi_nmfi.add_widget(
                BSINavigationDrawerItemPlugin(
                    icon =          self.plm.plugin_ui_info.icon_name,
                    text =          self.plm.plugin_ui_info.display_name,
                    screen_name =   self.plm.plugin_ui_info.screen_name,
                    bsi_msm =       self.bsi.bsi_msm
                )
            )
        
        for plugin_module in self.all_plugins:
            try:
                if (pre_init_plugin_func:=getattr(plugin_module, "pre_init", None)) is not None:
                    pre_init_plugin_func(self, self.bsi)

                plugin = plugin_module.plugin_main(self.bsi, self)
                plugin_ui_info = plugin_module.plugin_ui_info
                
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
                self.on_plugins.append( (plugin_module, plugin) )
            except: console.print_exception()
    
    def start_plugins(self) -> None:
        self.plugin_loader_ui.on_start()
        for plugin_module, plugin in self.on_plugins:
            try: plugin.on_start()
            except: console.print_exception()
    
    def stop_plugins(self) -> None:
        self.plugin_loader_ui.on_stop()
        for plugin_module, plugin in self.on_plugins:
            try: plugin.on_stop()
            except: console.print_exception()
    
    def run(self) -> None:
        self.load_plugins()
        self.bsi.run()