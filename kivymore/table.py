from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget, WidgetMetaclass
from kivy.uix.label import Label
from typing import Iterable, List, Optional, Any, Union
# * Local Imports
try:
    from . import Units as units
except:
    import Units as units

# ! Constants
By = units.By()

# ! Functions
def _gt(widget: Widget) -> str:
    return widget.text

# ! Main Class
class Table(BoxLayout):
    def __init__(self, сolumns: Iterable[str], **kwargs) -> None:
        super(Table, self).__init__(**kwargs)
        
        self.сolumns: List[str] = [str(i) for i in сolumns]
        self.max_сolumns: int = len(self.сolumns)
        self.rows_list: List[Iterable[Widget]] = []

        self.table_obj: GridLayout = GridLayout(
            cols=self.max_сolumns,
            row_force_default=True,
            row_default_height=kwargs.get("row_height", 30)
        )

        for i in self.сolumns:
            self.table_obj.add_widget(Button(text=i))
        self.add_widget(self.table_obj)
    
    def get_colomn_index(self, сolumn_name: Optional[str]) -> Optional[int]:
        if сolumn_name is not None:
            for idx, i in enumerate(self.сolumns):
                if i == сolumn_name:
                    return idx
    
    def add_row(self, data: Iterable[Widget], **kwargs) -> None:
        data = [i for i in data]
        ignore_errors = kwargs.get("ignore_errors", True)
        if self.max_сolumns == len(data):
            self.rows_list.append(data)
            for i in data:
                self.table_obj.add_widget(i)
        else:
            if not ignore_errors:
                raise ValueError(f"The number of widgets does not match the number of columns ({self.max_сolumns})")
    
    def add_row_text(self, data: Iterable[Any], **kwargs) -> None:
        self.add_row([Label(text=str(i), **kwargs) for i in data][:self.max_сolumns])
    
    def add_row_alternative(self, data: Iterable[Union[Widget, Any]], **kwargs) -> None:
        self.add_row([(i if isinstance(i, WidgetMetaclass) else Label(text=str(i))) for i in data], **kwargs)
    
    def search_row(self, by: units._By=By.COLOMN_NAME_AND_TEXT, **kwargs) -> Optional[List[Widget]]:
        get_text = kwargs.get("on_text", None) or _gt
        if by == By.COLOMN_NAME_AND_TEXT:
            if (colomn_index:=self.get_colomn_index(kwargs.get("colomn_name", None))) is not None:
                if (text:=kwargs.get("text", None)) is not None:
                    text = str(text)
                    for i in self.rows_list:
                        try:
                            if get_text(i[colomn_index]) == text:
                                return i
                        except:
                            pass
    
    def search_row_text(self, by: units._By=By.COLOMN_NAME_AND_TEXT, **kwargs) -> Optional[List[str]]:
        get_text = kwargs.get("on_text", None) or _gt
        kwargs.update({"on_text": get_text})
        self.data = self.search_row(by, **kwargs)
        if self.data is not None:
            try: return [get_text(i) for i in self.data]
            except: pass
    
    def search_rows(self, by: units._By=By.COLOMN_NAME_AND_TEXT, **kwargs) -> List[List[Widget]]:
        get_text = kwargs.get("on_text", None) or _gt
        if by == By.COLOMN_NAME_AND_TEXT:
            if (colomn_index:=self.get_colomn_index(kwargs.get("colomn_name", None))) is not None:
                if (text:=kwargs.get("text", None)) is not None:
                    text, lws = str(text), []
                    for i in self.rows_list:
                        try:
                            if get_text(i[colomn_index]) == text:
                                lws.append(i)
                        except:
                            pass
                    return lws
    
    def search_rows_text(self, by: units._By=By.COLOMN_NAME_AND_TEXT, **kwargs) -> List[List[str]]:
        get_text = kwargs.get("on_text", None) or _gt;kwargs.update({"on_text": get_text})
        self.data = self.search_rows(by, **kwargs)
        if self.data is not None:
            try: return [[get_text(_) for _ in i] for i in self.data]
            except: pass
    
    def delete_row(self, by: units._By=By.COLOMN_NAME_AND_TEXT, **kwargs) -> None:
        data = self.search_row(by, **kwargs)
        if data is not None:
            try:
                self.rows_list.pop(self.rows_list.index(data))
                for i in data:
                    try:
                        self.table_obj.remove_widget(i)
                    except: pass
            except: pass
    
    def delete_rows(self, by: units._By=By.COLOMN_NAME_AND_TEXT, **kwargs) -> None:
        data = self.search_rows(by, **kwargs)
        for widgets in data:
            try:
                self.rows_list.pop(self.rows_list.index(widgets))
                for widget in widgets:
                    try:
                        self.table_obj.remove_widget(widget)
                    except: pass
            except: pass
