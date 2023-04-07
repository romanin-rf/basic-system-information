from dataclasses import dataclass
from typing import Dict, Any, TypeVar

# ? Metadata
__name__ = "PluginCreator"
__version__ = "0.2.4"
__version_hash__ = hash(__version__)
__author__ = "Romanin"
__email__ = "semina054@gmail.com"

# ? Type Constats
T = TypeVar("T")

# ? Dataclasses
@dataclass
class PluginInfo:
    name: str
    version: str
    author: str
    id: str

@dataclass
class PluginUI:
    title: str
    ui: T
    initialising: bool

# ? Other Classes
class HiddenInt(int):
    def __str__(self) -> None: return "..."
    def __repr__(self) -> None: return self.__str__(self)

# ? Environ Class
class Environ:
    def __init__(self, **kwargs) -> None: self.environ: Dict[str, Any] = {**kwargs}
    def synchronisation(self, **kwargs): self.environ.update(**kwargs) ; return self

# ? Constants
STANDART_PLUGIN_INFO = PluginInfo(__name__, __version__, __author__, "pl")

# ? Plugin Class
class Plugin:
    def build_environ(self) -> Dict[str, Any]: return {}
    def build_ui(self) -> PluginUI: return PluginUI("Plugin\nLoader", None, False)
    def build_priority(self) -> int: return 0
    def __init__(self, environ: Environ, plugin_info: PluginInfo=STANDART_PLUGIN_INFO) -> None:
        self.priority: int = self.build_priority()
        self.info: PluginInfo = plugin_info
        self.environ: Environ = environ.synchronisation(**self.build_environ())
        self.ui: PluginUI = self.build_ui()
    def init(self) -> None: pass
    def on_start(self) -> None: pass
    def on_stop(self) -> None: pass
