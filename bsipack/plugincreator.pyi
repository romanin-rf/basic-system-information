from dataclasses import dataclass
# > Local Imports
try:    from .bsi import *
except: from bsi import *

@dataclass
class PluginInfo:
    name: str
    name_id: str
    version: str
    author: str

@dataclass
class PluginUIInfo:
    init: bool
    icon_name: str
    screen_name: str
    display_name: str

class Plugin:
    bsi: BSI
    plugin_loader: ...
    def __init__(self, bsi: BSI, plugin_loader) -> None:    ...
    def on_build_info_ui(self) -> PluginUIInfo:             ...
    def on_build(self) -> BSIScreen:                        ...
    def on_start(self) -> None:                             ...
    def on_stop(self) -> None:                              ...

