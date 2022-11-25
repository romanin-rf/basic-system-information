from . import PluginCreator as pc
from kivy.lang.builder import Builder

ui = Builder.load_string(
"""\
Label:
    text: 'ExamplePlugin (v1.0.0) from Romanin'
"""
)

class ExamplePlugin(pc.Plugin):
    def build_info(self) -> pc.PluginInfo:
        return pc.PluginInfo("ExamplePlugin", "1.0.0")
    
    def build_ui(self):
        return pc.PluginUI("Example\nPlugin", ui, True)
    
    def on_start(self) -> None:
        print("- ExamplePlugin is stated")

Main = ExamplePlugin()