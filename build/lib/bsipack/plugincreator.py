from dataclasses import dataclass

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