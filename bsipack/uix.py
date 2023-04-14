from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationdrawer import MDNavigationDrawerItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import IRightBodyTouch, ThreeLineAvatarIconListItem, IconLeftWidget, IconRightWidget, TwoLineAvatarIconListItem
# > Typing
from typing import Any
# > Local Imports
try:    from .plugincreator import PluginInfo, PluginUIInfo, PASS_PLUGIN_INFO, PASS_PLUGIN_UI_INFO
except: from plugincreator import PluginInfo, PluginUIInfo, PASS_PLUGIN_INFO, PASS_PLUGIN_UI_INFO

class BSINavigationDrawerItem(MDNavigationDrawerItem):
    def __init__(self, *args, **kwargs):
        kwargs["selected_color"] = kwargs.get("selected_color", "#b83950")
        kwargs["ripple_color"] = kwargs.get("ripple_color", "#ffffff")
        kwargs["text_color"] = kwargs.get("text_color", "#ffffff")
        kwargs["icon_color"] = kwargs.get("icon_color", "#ffffff")
        kwargs["focus_color"] = kwargs.get("focus_color", "#858585")
        
        super().__init__(*args, **kwargs)

class BSILineGridLayout(MDGridLayout):
    def __init__(self, *args, **kwargs):
        kwargs["cols"] = kwargs.get("cols", 3)
        kwargs["rows"] = kwargs.get("rows", 1)
        kwargs["padding"] = kwargs.get("padding", "10dp")
        
        super().__init__(*args, **kwargs)

class BSICenterLabel(MDLabel):
    def __init__(self, **kwargs):
        kwargs["halign"] = kwargs.get("halign", "center")
        
        super().__init__(**kwargs)

class BSIScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.rootbox = MDBoxLayout(
            orientation='vertical',
            padding=("0dp", "70dp", "0dp", "0dp")
        )
        super().add_widget(self.rootbox)
    
    def __repr__(self) -> str: return super().__repr__().replace("<Screen ", f"<{self.__class__.__name__} ")
    def add_widget(self, widget, *args, **kwargs): self.rootbox.add_widget(widget, *args, **kwargs)
    def clear_widgets(self, children=None): self.rootbox.clear_widgets(children)
    def remove_widget(self, widget, *args, **kwargs): self.rootbox.remove_widget(widget, *args, **kwargs)
    def collide_widget(self, widget) -> bool: return self.rootbox.collide_widget(widget)

class BSINavigationDrawerItemPlugin(BSINavigationDrawerItem):
    def __init__(self, *args, **kwargs):
        self.screen_name = kwargs.get("screen_name", "bsi")
        self.bsi_msm = kwargs.get("bsi_msm", None)
        kwargs.pop("screen_name")
        kwargs.pop("bsi_msm")
        super().__init__(*args, **kwargs)
    def on_release(self):
        if self.bsi_msm is not None:
            self.bsi_msm.current = self.screen_name

class BSIRigthSwitch(IRightBodyTouch, MDSwitch):
    """Custom right container."""
    def __init__(self, pl: Any, plugin_info: PluginInfo, *args, **kwargs) -> None:
        kwargs["thumb_color_disabled"] = "grey"
        super().__init__(*args, **kwargs)
        self.plugin_loader = pl
        self.plugin_info = plugin_info
    
    def on_active(self, instance_switch, active_value: bool) -> None:
        super().on_active(instance_switch, active_value)
        try: self.plugin_loader.config.change_settings(self.plugin_info, active_value)
        except: pass

class BSIRigthBoxLayout(IRightBodyTouch, MDBoxLayout):
    def __init__(self, *args, **kwargs) -> None:
        kwargs["adaptive_width"] = True
        super().__init__(*args, **kwargs)

class BSI2LineAvatarIconListItem(TwoLineAvatarIconListItem):
    def __init__(
        self,
        icon: str="language-python",
        first_text_line: str="None",
        second_text_line: str="None",
        *args, **kwargs
    ) -> None:
        kwargs["text"] = first_text_line
        kwargs["secondary_text"] = second_text_line
        
        super().__init__(*args, **kwargs)
        self.iconer = IconLeftWidget(icon=icon)
        
        self.add_widget(self.iconer)

class BSIIconRightWidget(IconRightWidget):
    def __init__(self, plugin_info: PluginInfo, plugin_ui_info: PluginUIInfo, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.plugin_info = plugin_info
        self.plugin_ui_info = plugin_ui_info
        
        self.dialoger = MDDialog(
            title="Info",
            type="confirmation",
            items=[
                BSI2LineAvatarIconListItem("emoticon", "Icon", repr(self.plugin_ui_info.icon_name)),
                BSI2LineAvatarIconListItem("location-exit", "Exists UI", repr(self.plugin_ui_info.init)),
                BSI2LineAvatarIconListItem("rename-box", "Display Name", repr(self.plugin_ui_info.display_name)),
                BSI2LineAvatarIconListItem("fit-to-screen", "Screen Name", repr(self.plugin_ui_info.screen_name)),
                BSI2LineAvatarIconListItem("comment-edit", "Name", repr(self.plugin_info.name)),
                BSI2LineAvatarIconListItem("file-find", "Name ID", repr(self.plugin_info.name_id)),
                BSI2LineAvatarIconListItem("order-bool-descending", "Description", repr(self.plugin_info.desc)),
                BSI2LineAvatarIconListItem("diversify", "Version", repr(self.plugin_info.version)),
                BSI2LineAvatarIconListItem("account", "Author", repr(self.plugin_info.author)),
                BSI2LineAvatarIconListItem("monitor-star", "System", repr(self.plugin_info.system)),
                BSI2LineAvatarIconListItem("chip", "Machine", repr(self.plugin_info.machine))
            ]
        )
    
    def on_release(self):
        super().on_release()
        self.dialoger.open()

class BSIList3LinesSwitchItem(ThreeLineAvatarIconListItem):
    def __init__(
        self,
        icon: str="language-python",
        first_text_line: str="None",
        second_text_line: str="None",
        third_text_line: str="None",
        switch_active: bool=False,
        switch_disabled: bool=False,
        plugin_loader: Any=None,
        plugin_info: PluginInfo=PASS_PLUGIN_INFO,
        plugin_ui_info: PluginUIInfo=PASS_PLUGIN_UI_INFO,
        *args,
        **kwargs
    ) -> None:
        kwargs["text"] = first_text_line
        kwargs["secondary_text"] = second_text_line
        kwargs["tertiary_text"] = third_text_line
        
        super().__init__(*args, **kwargs)
        
        self.iconer = IconLeftWidget(icon=icon)
        self.box_right = BSIRigthBoxLayout(id="rigth_box_container")
        self.switcher = BSIRigthSwitch(
            pl=plugin_loader,
            plugin_info=plugin_info,
            active=switch_active,
            disabled=switch_disabled
        )
        self.infoner = BSIIconRightWidget(plugin_info, plugin_ui_info, icon="information")
        
        self.box_right.add_widget(self.switcher)
        self.box_right.add_widget(self.infoner)
        
        self.add_widget(self.iconer)
        self.add_widget(self.box_right)
