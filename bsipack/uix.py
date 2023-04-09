from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationdrawer import MDNavigationDrawerItem

class BSINavigationDrawerItem(MDNavigationDrawerItem):
    def __init__(self, *args, **kwargs):
        kwargs["selected_color"] = kwargs.get("selected_color", "#b83950")
        kwargs["ripple_color"] = kwargs.get("ripple_color", "#ffffff")
        
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
