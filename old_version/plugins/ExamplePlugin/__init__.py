from . import PluginCreator as pc
from kivy.lang.builder import Builder

ui = Builder.load_string(
"""\
Label:
    text: 'ExamplePlugin (v1.0.0) from Romanin'
"""
)

class ExamplePlugin(pc.Plugin):
    def build_ui(self):
        return pc.PluginUI("Example\nPlugin", ui, True)
    
    def on_start(self) -> None:
        print("- ExamplePlugin is starting...")
    
    def on_stop(self) -> None:
        print("- ExamplePlugin is stoping...")

plugin_info = pc.PluginInfo("ExamplePlugin", "1.0.0", "Romanin", "example")
plugin_main = ExamplePlugin