from . import PluginCreator as pc
from kivy.uix.button import Button
from kivy.uix.button import Label
from kivy.uix.boxlayout import BoxLayout
from .KivyOnTop import register_topmost, unregister_topmost

class OnTopPlugin(pc.Plugin):
    def build_info(self):
        return pc.PluginInfo("OnTop", "1.0.0", "Romanin", "on.top")
    
    def build_ui(self):
        return pc.PluginUI("", None, False)
    
    def change_button_topmost_status(self, instance: Button, window, title: str) -> None:
        if instance.text == "UT":
            register_topmost(window, title)
            instance.text = "T"
        else:
            unregister_topmost(window, title)
            instance.text = "UT"
    
    def on_start(self) -> None:
        bl = BoxLayout()
        bl.add_widget(
            Button(
                text="UT",
                on_press=lambda instance: self.change_button_topmost_status(
                    instance,
                    self.environ["bsi"].root_window,
                    self.environ["bsi"].title
                )
            )
        )
        bl.add_widget(
            Label(
                text="* Режим поверх окон не отключается!\n[color=ff0000]Для этого требуется перезапуск![/color]",
                font_size=10,
                markup=True
            )
        )
        self.environ["bsi"].w_root.ids["BoxLayoutBSI"].add_widget(bl)

Main = OnTopPlugin()