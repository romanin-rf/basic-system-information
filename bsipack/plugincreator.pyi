from dataclasses import dataclass
# > Local Imports
try:    from .bsi import *
except: from bsi import *

# ! MetaData
__title__ = "PluginCreator"
__version__ = "0.3.1"
__version_hash__ = hash(__version__)
__author__ = "Romanin"
__email__ = "semina054@gmail.com"

# ! Main Objects
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
    def on_build(self) -> BSIScreen:                        ...
    def on_start(self) -> None:                             ...
    def on_stop(self) -> None:                              ...
