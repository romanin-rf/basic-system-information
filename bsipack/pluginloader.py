import os
import pathlib
import imp
import json
from rich.console import Console
# > Kivy
from kivy.metrics import dp
# > KivyMD
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.list import MDList
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.list import IRightBodyTouch, ThreeLineAvatarIconListItem, IconLeftWidget
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.icon_definitions import md_icons
# > Typing
from typing import Optional, List, Dict, Any, Tuple, Type
from types import ModuleType
# > Local Imports
try:    from .plugincreator import PluginInfo, Plugin, PluginUIInfo
except: from plugincreator import PluginInfo, Plugin, PluginUIInfo
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

class BSIRigthSwitch(IRightBodyTouch, MDSwitch):
    """Custom right container."""
    def __init__(self, pl: Any, plugin_info: PluginInfo, *args, **kwargs) -> None:
        kwargs["thumb_color_disabled"] = "grey"
        super().__init__(*args, **kwargs)
        self.plugin_loader = pl
        self.plugin_info = plugin_info
    
    def on_active(self, instance_switch, active_value: bool) -> None:
        super().on_active(instance_switch, active_value)
        try: self.plugin_loader.config.change_settings(self.plugin_info, active_value)
        except: console.print_exception()

class BSIList3LinesSwitchItem(ThreeLineAvatarIconListItem):
    def __init__(
        self,
        icon: str="language-python",
        first_text_line: str="None",
        second_text_line: str="None",
        third_text_line: str="None",
        switch_active: bool=False,
        switch_disabled: bool=False,
        switch_plugin_loader: Any=None,
        switch_plugin_info: PluginInfo=PluginInfo("None", "None", "None", "None"),
        *args,
        **kwargs
    ) -> None:
        kwargs["text"] = first_text_line
        kwargs["secondary_text"] = second_text_line
        kwargs["tertiary_text"] = third_text_line
        
        super().__init__(*args, **kwargs)
        
        self.iconer = IconLeftWidget(icon=icon)
        self.switcher = BSIRigthSwitch(
            pl=switch_plugin_loader,
            plugin_info=switch_plugin_info,
            active=switch_active,
            disabled=switch_disabled
        )
        
        self.add_widget(self.iconer) ; self.add_widget(self.switcher)

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
                "Plugin Loader UI (v0.3.0)",
                "bsi.pluginloader.ui",
                "Romanin",
                True,
                True
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
                    plugin_module.plugin_info
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
                    plugin_module.plugin_info
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
            plugin_info=PluginInfo("Plugin Loader UI", "bsi.pluginloader.ui", "0.3.0", "Romanin"),
            plugin_ui_info=PluginUIInfo(True, "archive-plus", "plugin_loader_ui_screen", "Plugin Loader UI"),
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
                plugin_module: PluginModuleType = imp.load_module(plugin_name, *plugin_data)
                
                if not self.config.exists_plugin(plugin_module.plugin_info):
                    self.config.add_plugin(plugin_module.plugin_info)
                
                if (plugin_settings:=self.config.get_plugin_settings(plugin_module.plugin_info)) is not None:
                    if plugin_settings["enabled"]:
                        self.all_plugins.append(plugin_module)
                    else:
                        self.off_plugins.append(plugin_module)
                else:
                    try: raise RuntimeError(f"Critical error when loading the '{plugin_module.plugin_info.name}' ({plugin_module.plugin_info.name_id}) plugin.")
                    except: console.print_exception()
                    
                try: console.print(self.plugin_settings)
                except: pass
            except:
                console.print_exception()
    
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
            except:
                console.print_exception()
    
    def start_plugins(self) -> None:
        self.plugin_loader_ui.on_start()
        for plugin_module, plugin in self.on_plugins:
            plugin.on_start()
    
    def stop_plugins(self) -> None:
        self.plugin_loader_ui.on_stop()
        for plugin_module, plugin in self.on_plugins:
            plugin.on_stop()
    
    def run(self) -> None:
        self.load_plugins()
        self.bsi.run()