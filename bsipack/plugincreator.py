import platform
from dataclasses import dataclass

# ! MetaData
__title__ = "PluginCreator"
__version__ = "0.3.6"
__version_hash__ = hash(__version__)
__author__ = "Romanin"
__email__ = "semina054@gmail.com"

# ! Init Classes
@dataclass
class PluginInfo:
    name: str
    name_id: str
    desc: str
    version: str
    author: str
    system: list
    machine: list

@dataclass
class PluginUIInfo:
    init: bool
    icon_name: str
    screen_name: str
    display_name: str

# ! Const
PASS_PLUGIN_INFO = PluginInfo("None", "None", "None", "None", "None", ["any"], ["any"])
PASS_PLUGIN_UI_INFO = PluginUIInfo(False, "language-python", "None", "None")

# ! Plugin Class
class Plugin:
    def __init__(self, bsi, plugin_loader) -> None:
        self.bsi = bsi
        self.plugin_loader = plugin_loader
    def on_build(self): pass
    def on_start(self): pass
    def on_stop(self):  pass

# ! Functions
def is_supported_plugin(plugin_info: PluginInfo) -> bool:
    pun = platform.uname()
    return (
        ("any" in plugin_info.system) and ("any" in plugin_info.machine)
    ) or (
        (pun.system.lower() in plugin_info.system) and (pun.machine.lower() in plugin_info.machine)
    )