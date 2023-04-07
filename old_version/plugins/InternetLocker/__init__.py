import os
import json
import keyboard
from threading import Thread
from typing import Dict, List, Any, Union, TypeVar, Callable
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from .kivymore.table import Table, By
from . import PluginCreator as pc
from . import LockSwitch as lsw

# ! Constants
LOCAL_PATH = os.path.dirname(__file__)
CONFIG_LOCKER_PATH = os.path.join(LOCAL_PATH, "locker_config.json")
FUNC_TYPE = Callable[[], None]

# ! Type Alias Constants
T = TypeVar("T")

# ! Config Worker
class LockerConfig:
    def load_json(self, fp: str) -> List[Dict[str, Any]]:
        try: return json.load(open(fp))
        except:
            json.dump([], open(fp,"w"))
            return json.load(open(fp))
    
    def dump_json(self, fp: str, data: List[Dict[str, Any]]) -> None:
        json.dump(data, open(fp,"w"))
    
    def __init__(self, fp: str) -> None:
        self.name: str = fp
    
    @property
    def cfg(self) -> List[Dict[str, Any]]:
        return self.load_json(self.name)
    
    @cfg.setter
    def cfg(self, value: List[Dict[str, Any]]):
        self.dump_json(self.name, value)
    
    def fget(self, filename: str, default: T) -> Union[Dict[str, Any], T]:
        for i in self.cfg:
            if i["filename"] == filename:
                return i
        return default
    
    def iget(self, filename: str, default: T) -> Union[int, T]:
        for idx, i in enumerate(self.cfg):
            if i["filename"] == filename:
                return idx
        return default
    
    def update(self, filename: str, data: Dict[str, Any]) -> None:
        if (idx:=self.iget(filename, None)) is not None:
            cfg = self.cfg
            cfg[idx] = data
            self.cfg = cfg
    
    def add(self, data: Dict[str, Any]) -> bool:
        try:
            if self.fget(data["filename"], None) is None:
                if (data["filename"] != "") and (data["key"] != ""):
                    cfg = self.cfg
                    cfg.append(data)
                    self.cfg = cfg
                    return True
        except: pass
        return False
    
    def delete(self, filename: str) -> bool:
        if (idx:=self.iget(filename, None)) is not None:
            cfg = self.cfg
            del cfg[idx]
            self.cfg = cfg

# ! Plugin Class
class InternetLocker(pc.Plugin):
    def build_ui(self):
        self.main = FloatLayout()
        self.scrollview_table = ScrollView(do_scroll_x=False, do_scroll_y=True, bar_width=10)
        self.table = Table(["Filename", "Key", "Lock", "Deleting"])
        self.adder = GridLayout(
            rows=1,
            row_force_default=True,
            row_default_height=30,
            pos=(0, -525)
        )
        
        self.input_filename = TextInput()
        self.input_key = TextInput()
        self.button_add = Button(text="Add")
        
        self.adder.add_widget(self.input_filename)
        self.adder.add_widget(self.input_key)
        self.adder.add_widget(self.button_add)
        self.scrollview_table.add_widget(self.table)
        self.main.add_widget(self.scrollview_table)
        self.main.add_widget(self.adder)
        return pc.PluginUI("Internet\nLocker", self.main, True)
    
    def __init__(self, *args, **kwargs) -> None:
        super(InternetLocker, self).__init__(*args, **kwargs)
        self.locker_config: LockerConfig = LockerConfig(CONFIG_LOCKER_PATH)
        self.locker_key_handler: Dict[str, FUNC_TYPE] = {}
        self.key_check_running = False
    
    def delete_proccess_in_table(self, data: Dict[str, Any]) -> None:
        self.table.delete_row(By.COLOMN_NAME_AND_TEXT, colomn_name="Filename", text=data["filename"])
    
    def delete_proccess_in_hotkey(self, data: Dict[str, Any]) -> None:
        try: del self.locker_key_handler[data["filename"]]
        except: pass
    
    def delete_proccess_in_cfg(self, data: Dict[str, Any]) -> None:
        self.locker_config.delete(data["filename"])
    
    def delete_general(self, data: Dict[str, Any]) -> None:
        if (cdata:=self.locker_config.fget(data["filename"], None)) is not None:
            if not cdata["lock"]:
                self.delete_proccess_in_table(cdata)
                self.delete_proccess_in_hotkey(cdata)
                self.delete_proccess_in_cfg(cdata)
    
    def change_lock_state(self, data: Dict[str, Any], progress_info: lsw.ProccessInfo) -> None:
        if (ndata:=self.locker_config.fget(data["filename"], None)) is not None:
            if ndata["lock"]:
                lsw.unblock_program(progress_info)
                ndata["lock"] = False
            else:
                lsw.block_program(progress_info)
                ndata["lock"] = True
            self.locker_config.update(data["filename"], ndata)
            self.table.search_row(By.COLOMN_NAME_AND_TEXT, colomn_name="Filename", text=ndata["filename"])[2].text = str(ndata["lock"])
    
    def add_proccess_in_cfg(self, data: Dict[str, Any]) -> None:
        self.locker_config.add(data)
    
    def add_proccess_in_hotkey(self, data: Dict[str, Any]) -> None:
        if self.locker_key_handler.get(data["filename"], None) is None:
            proccess_info = lsw.search_info(data["filename"])
            func = lambda *args, **kwargs: self.change_lock_state(data, proccess_info)
            self.locker_key_handler[data["filename"]] = keyboard.add_hotkey(data["key"], func)
    
    def add_proccess_in_table(self, data: Dict[str, Any]) -> None:
        if self.table.search_row(By.COLOMN_NAME_AND_TEXT, colomn_name="Filename", text=data["filename"]) is None:
            func = lambda instance: self.delete_general(data)
            self.table.add_row([*[Label(text=str(i)) for i in data.values()], Button(text="Delete", on_press=func)])
    
    def add_general(self, data: Dict[str, Any]) -> None:
        self.add_proccess_in_cfg(data)
        self.add_proccess_in_table(data)
        Thread(target=self.add_proccess_in_hotkey, args=(data,)).start()
    
    def get_data_from_adder(self) -> Dict[str, Any]:
        return {"filename": self.input_filename.text, "key": self.input_key.text, "lock": False}
    
    def button_adder(self):
        return lambda instance: self.add_general(self.get_data_from_adder())
    
    def init(self) -> None:
        self.button_add.bind(on_press=self.button_adder())
        for i in self.locker_config.cfg:
            self.add_general(i)

# ? {"filename": "", "key": "1", "lock": False}
# ! Initialization
plugin_info = pc.PluginInfo("InternetLocker", "1.0.0", "Romanin", "internet.locker")
plugin_main = InternetLocker
