from bsipack.plugincreator import Plugin, PluginInfo, PluginUIInfo
from bsipack.uix import *
from kivy.lang import Builder

UI = """\
BSIScreen:
    name: 'example_plugin_screen'
    MDRaisedButton:
        text: "TEST"
        pos_hint: {"center_x": .5, "center_y": .5}
"""

class ExamplePlugin(Plugin):
    def on_build_info_ui(self):
        return PluginUIInfo(True, "hexagon", "example_plugin_screen", "Example Plugin")
    
    def on_build(self):
        return Builder.load_string(UI)

    def on_start(self) -> None:
        print("* Example Plugin is starting...")
    
    def on_stop(self) -> None:
        print("* Example Plugin is stoped...")

plugin_info = PluginInfo("Example Plugin", "bsi.example", "0.1.0", "Romanin")
plugin_main = ExamplePlugin

print("* Example Plugin is loaded...")