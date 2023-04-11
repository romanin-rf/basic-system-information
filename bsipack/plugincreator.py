from dataclasses import dataclass

# ! MetaData
__title__ = "PluginCreator"
__version__ = "0.3.1"
__version_hash__ = hash(__version__)
__author__ = "Romanin"
__email__ = "semina054@gmail.com"

# ! Init Classes
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

# ! Plugin Class
class Plugin:
    def __init__(self, bsi, plugin_loader) -> None:
        self.bsi = bsi
        self.plugin_loader = plugin_loader
    def on_build(self): pass
    def on_start(self): pass
    def on_stop(self):  pass