from kivymd.uix.navigationdrawer import MDNavigationDrawerMenu
from bsipack.plugincreator import Plugin, PluginInfo, PluginUIInfo
from bsipack.pluginloader import PluginLoader
from bsipack.bsi import BSI

class RussianTranslatePlugin(Plugin): pass

def pre_init(pl: PluginLoader, bsi: BSI) -> None:
    # * Перевод навигационного меню
    navigate_menu: MDNavigationDrawerMenu = bsi.bsi_root.ids["main_navigate_menu_driwer"].children[0]
    navigate_menu.children[-2].text = "Разделы"
    navigate_menu.children[-3].text = "БСИ"
    try: navigate_menu.children[-4].text = "Плагины"
    except: pass
    
    # * Перевод основного меню
    bsi.bsi_ms.children[0].children[-1].children[-1].text = "ЦП (Нагрузка)"
    bsi.bsi_ms.children[0].children[-2].children[-1].text = "ОЗУ (Занято)"
    bsi.bsi_ms.children[0].children[-3].children[-1].text = "ОЗУ (Всего)"
    bsi.bsi_ms.children[0].children[-4].children[-1].text = "Файл Подкачки (Занято)"
    bsi.bsi_ms.children[0].children[-5].children[-1].text = "Файл Подкачки (Всего)"

plugin_info = PluginInfo(
    "Русский Перевод",
    "bsi.translate.russian",
    "Русский перевод для BSI.",
    "0.3.5",
    "Romanin"
)
plugin_ui_info = PluginUIInfo(False, "sign-language", "", "Russian Translate Plugin")
plugin_main = RussianTranslatePlugin
