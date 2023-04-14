from bsipack.plugincreator import Plugin, PluginInfo, PluginUIInfo
from bsipack.pluginloader import PluginLoader
from bsipack.bsi import BSI
from bsipack.uix import *
from kivy.lang import Builder

UI = """\
BSIScreen:
    name: 'example_plugin_screen'
    MDRaisedButton:
        text: "TEST"
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
"""

class ExamplePlugin(Plugin):
    def on_build(self):
        print("* Example Plugin building...")
        return Builder.load_string(UI)

    def on_start(self) -> None:
        print("* Example Plugin is starting...")
    
    def on_stop(self) -> None:
        print("* Example Plugin is stoped...")

def pre_init(pl: PluginLoader, bsi: BSI) -> None:
    print("* Example Plugin - 'pre_init' method called...")

plugin_info = PluginInfo(
    "Example Plugin",
    "bsi.example",
    "An example plugin.",
    "1.0.0",
    "Romanin",
    ["any"], ["any"]
)
plugin_ui_info = PluginUIInfo(True, "hexagon", "example_plugin_screen", "Example Plugin")
plugin_main = ExamplePlugin
