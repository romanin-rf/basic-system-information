from dataclasses import dataclass
# > Typing
from typing import List, Literal
# > Local Imports
try:    from .bsi import *
except: from bsi import *

# ! MetaData
__title__: str
__version__: str
__version_hash__: int
__author__: str
__email__: str

# ! Main Objects
@dataclass
class PluginInfo:
    name: str
    name_id: str
    desc: str
    version: str
    author: str
    system: List[Literal["any", "windows", "linux"]]
    machine: List[Literal["any", "amd64", "x86_64"]]

@dataclass
class PluginUIInfo:
    init: bool
    icon_name: str
    screen_name: str
    display_name: str

PASS_PLUGIN_INFO: PluginInfo
PASS_PLUGIN_UI_INFO: PluginUIInfo

class Plugin:
    bsi: BSI
    plugin_loader: ...
    def __init__(self, bsi: BSI, plugin_loader) -> None:    ...
    def on_build(self) -> BSIScreen:                        ...
    def on_start(self) -> None:                             ...
    def on_stop(self) -> None:                              ...

def is_supported_plugin(plugin_info: PluginInfo) -> bool: ...