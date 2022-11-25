from kivy.uix.widget import Widget
from dataclasses import dataclass
from typing import Optional, Dict, Any

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
        return PluginInfo("PluginLoader", "0.1.0")
    
    def build_environ(self) -> Dict[str, Any]:
        return {}
    
    def build_ui(self) -> PluginUI:
        return PluginUI("PluginLoader", None, False)
    
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
