from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.navigationdrawer import MDNavigationDrawerMenu, MDNavigationDrawer, MDNavigationDrawerItem
from kivy.properties import ColorProperty, StringProperty, NumericProperty

class BSINavigationDrawerClickableItem(MDNavigationDrawerItem):
    selected_color = ColorProperty("#b83950")
    ripple_color = ColorProperty("#ffffff")

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
