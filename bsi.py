import tkinter as tk
import tkinter.ttk as ttk
from threading import Thread
import psutil
import wget
import math
import json
import time
import sys
import os

if "config.json" in os.listdir():
	with open("config.json") as config_data_file:
		cfgd = json.load(config_data_file)
else:
	cfgd = 	{
				"timeouts":	{
								"update-time":			0.5,
								"update-cpu-load":		0.5,
								"update-ram":			0.5,
								"update-swap":			0.5,
								"update-average-load":	0.5
							},
				"root":		{
								"attributes":			False
				}
			}
	with open("config.json", "w") as config_data_file:
		json.dump(cfgd, config_data_file)

class timeouts:
	try:
		UpdateTime = cfgd["timeouts"]["update-time"]
		UpdateCPULoad = cfgd["timeouts"]["update-cpu-load"]
		UpdateRAM = cfgd["timeouts"]["update-ram"]
		UpdateSWAP = cfgd["timeouts"]["update-swap"]
		UpdateAverageLoad = cfgd["timeouts"]["update-average-load"]
	except:
		cfgd = 	{
					"timeouts":	{
									"update-time":			0.5,
									"update-cpu-load":		0.5,
									"update-ram":			0.5,
									"update-swap":			0.5,
									"update-average-load":	0.5
								},
					"root":		{
									"attributes":			False
								}
				}
		UpdateTime = cfgd["timeouts"]["update-time"]
		UpdateCPULoad = cfgd["timeouts"]["update-cpu-load"]
		UpdateRAM = cfgd["timeouts"]["update-ram"]
		UpdateSWAP = cfgd["timeouts"]["update-swap"]
		UpdateAverageLoad = cfgd["timeouts"]["update-average-load"]
		with open("config.json", "w") as config_data_file:
			json.dump(cfgd, config_data_file)

class root_operation:
	try:
		attributes = cfgd["root"]["attributes"]
	except:
		cfgd = 	{
					"timeouts":	{
									"update-time":			0.5,
									"update-cpu-load":		0.5,
									"update-ram":			0.5,
									"update-swap":			0.5,
									"update-average-load":	0.5
								},
					"root":		{
									"attributes":			False
								}
				}
		attributes = cfgd["root"]["attributes"]
		with open("config.json", "w") as config_data_file:
			json.dump(cfgd, config_data_file)

class function_operation:
	UpdateTime = True
	UpdateCPULoad = True
	UpdateRAM = True
	UpdateSWAP = True
	UpdateAverageLoadIndicator = True

class proginfo:
	version = "0.1.2-beta"

# Создаём окно
root = tk.Tk()
root.title("БСИ v" + str(proginfo.version))
if "-dev" in sys.argv:
	root.geometry("450x210")
else:
	root.geometry("450x105")
if "icon.ico" in os.listdir():
	root.iconbitmap('icon.ico')
else:
	try:
		wget.download("https://romanin-rf.github.io/basic-system-information/icon.ico")
		root.iconbitmap('icon.ico')
	except:
		LabelErrorInternet = tk.Label(root, text = "🗿", font = 'helvetica 18 bold')
		LabelErrorInternet.place(x = 375, y = 40)
root.resizable(0, 0)
root.attributes("-topmost", root_operation.attributes)

# Обьекты окна
#		Индикаторы
IndicatorCPULoadLabel = tk.Label(root, text = "*", font = 'helvetica 20 bold')
IndicatorRAMLoadLabel = tk.Label(root, text = "*", font = 'helvetica 20 bold')
IndicatorRAMFreeLabel = tk.Label(root, text = "╙", font = 'helvetica 12 bold')
IndicatorSWAPLoadLabel = tk.Label(root, text = "*", font = 'helvetica 20 bold')
IndicatorSWAPFreeLabel = tk.Label(root, text = "╙", font = 'helvetica 12 bold')
IndicatorAverageLoadLabel = tk.Label(root, text = "Loading...", font = 'helvetica 10 bold', bg = "black", fg = "white", width = 10)
#		Счётчики
TextTimeLabel = tk.Label(root, text = "Загрузка", font = 'helvetica 10 bold', bg = "black", fg = "white", width = 10)
TextCPULoadLabel = tk.Label(root, text = "CPU (Нагрузка): Загрузка...", font = 'helvetica 10 bold')
TextRAMLoadLabel = tk.Label(root, text = "RAM (Занято): Загрузка...", font = 'helvetica 10 bold')
TextRAMFreeLabel = tk.Label(root, text = "RAM (Свободно): Загрузка...", font = 'helvetica 10 bold')
TextSWAPLoadLabel = tk.Label(root, text = "Файл Подкачки (Занято): Загрузка...", font = 'helvetica 10 bold')
TextSWAPFreeLabel = tk.Label(root, text = "Файл Подкачки (Свободно): Загрузка...", font = 'helvetica 10 bold')
#		Переключатель для закрепления окна
ButtonSwitchingOptionsAttributes = tk.Label(root, text = "📌", font = 'helvetica 12 bold')
if root_operation.attributes:
	ButtonSwitchingOptionsAttributes["fg"] = "green"
else:
	ButtonSwitchingOptionsAttributes["fg"] = "red"

# Загрузка обьектов
TextTimeLabel.place(x = 365, y = 0)
ButtonSwitchingOptionsAttributes.place(x = 340, y = -5)
TextCPULoadLabel.place(x = 15, y = 0)
TextRAMLoadLabel.place(x = 15, y = 20)
TextRAMFreeLabel.place(x = 15, y = 40)
TextSWAPLoadLabel.place(x = 15, y = 60)
TextSWAPFreeLabel.place(x = 15, y = 80)
IndicatorCPULoadLabel.place(x = 0, y = 0)
IndicatorRAMLoadLabel.place(x = 0, y = 20)
IndicatorRAMFreeLabel.place(x = 0, y = 40)
IndicatorSWAPLoadLabel.place(x = 0, y = 60)
IndicatorSWAPFreeLabel.place(x = 0, y = 80)
IndicatorAverageLoadLabel.place(x = 365, y = 20)

# Функция округления float
def rounding_float(var: float):
	var_str = str(var)
	value_after_point = var_str[(var_str.find(".") + 1):]
	var_float_remains = float(str("0." + value_after_point))
	if var_float_remains >= 0.5:
		varout = math.ceil(var)
	else:
		varout = math.floor(var)
	return varout

# Функции обновления
def UpdateTimeLabel():
	while function_operation.UpdateTime:
		try:
			TextTimeLabel["text"] = str(time.strftime("%H:%M:%S", time.localtime()))
		except:
			TextTimeLabel["text"] = "Ошибка"
		time.sleep(timeouts.UpdateTime)

def UpdateCPULoadLabel():
	while function_operation.UpdateCPULoad:
		try:
			percent_load = psutil.cpu_percent()
			if percent_load < 50:
				IndicatorCPULoadLabel["fg"] = "green"
			elif percent_load < 70:
				IndicatorCPULoadLabel["fg"] = "#c9cc02"
			elif percent_load < 90:
				IndicatorCPULoadLabel["fg"] = "orange"
			elif percent_load >= 90:
				IndicatorCPULoadLabel["fg"] = "red"
			TextCPULoadLabel["text"] = "CPU (Нагрузка): " + str(percent_load) + " %"
		except:
			TextCPULoadLabel["text"] = "CPU (Нагрузка): Ошибка..."
		time.sleep(timeouts.UpdateCPULoad)

def UpdateRAMLoadLabel():
	while function_operation.UpdateRAM:
		try:
			total_mem_mb = (psutil.virtual_memory().total / 1024) / 1024
			used_mem_mb = (psutil.virtual_memory().used / 1024) / 1024
			used_mem_present = psutil.virtual_memory().percent
			if type(total_mem_mb) == float:
				total_mem_mb = rounding_float(total_mem_mb)
			if type(used_mem_mb) == float:
				used_mem_mb = rounding_float(used_mem_mb)
			if used_mem_present < 50:
				IndicatorRAMLoadLabel["fg"] = "green"
			elif used_mem_present < 70:
				IndicatorRAMLoadLabel["fg"] = "#c9cc02"
			elif used_mem_present < 90:
				IndicatorRAMLoadLabel["fg"] = "orange"
			elif used_mem_present >= 90:
				IndicatorRAMLoadLabel["fg"] = "red"
			TextRAMLoadLabel["text"] = "RAM (Занято): {0} МБ/{1} МБ ({2} %)".format(used_mem_mb, total_mem_mb, used_mem_present)
		except:
			TextRAMLoadLabel["text"] = "RAM (Занято): Ошибка..."
		time.sleep(timeouts.UpdateCPULoad)

def UpdateRAMFreeLabel():
	while function_operation.UpdateRAM:
		try:
			total_mem_mb = (psutil.virtual_memory().total / 1024) / 1024
			free_mem_mb = (psutil.virtual_memory().free / 1024) / 1024
			free_mem_present = float(str(100 - psutil.virtual_memory().percent)[:4])
			if type(total_mem_mb) == float:
				total_mem_mb = rounding_float(total_mem_mb)
			if type(free_mem_mb) == float:
				free_mem_mb = rounding_float(free_mem_mb)
			TextRAMFreeLabel["text"] = "RAM (Свободно): {0} МБ/{1} МБ ({2} %)".format(free_mem_mb, total_mem_mb, free_mem_present)
		except:
			TextRAMFreeLabel["text"] = "RAM (Свободно): Ошибка..."
		time.sleep(timeouts.UpdateCPULoad)

def UpdateSWAPLoadLabel():
	while function_operation.UpdateSWAP:
		try:
			total_mem_mb = (psutil.swap_memory().total / 1024) / 1024
			used_mem_mb = (psutil.swap_memory().used / 1024) / 1024
			used_mem_present = psutil.swap_memory().percent
			if type(total_mem_mb) == float:
				total_mem_mb = rounding_float(total_mem_mb)
			if type(used_mem_mb) == float:
				used_mem_mb = rounding_float(used_mem_mb)
			if used_mem_present < 50:
				IndicatorSWAPLoadLabel["fg"] = "green"
			elif used_mem_present < 70:
				IndicatorSWAPLoadLabel["fg"] = "#c9cc02"
			elif used_mem_present < 90:
				IndicatorSWAPLoadLabel["fg"] = "orange"
			elif used_mem_present >= 90:
				IndicatorSWAPLoadLabel["fg"] = "red"
			TextSWAPLoadLabel["text"] = "Файл Подкачки (Занято): {0} МБ/{1} МБ ({2} %)".format(used_mem_mb, total_mem_mb, used_mem_present)
		except:
			TextSWAPLoadLabel["text"] = "Файл Подкачки (Занято): Ошибка..."
		time.sleep(timeouts.UpdateSWAP)

def UpdateSWAPFreeLabel():
	while function_operation.UpdateSWAP:
		try:
			total_mem_mb = (psutil.swap_memory().total / 1024) / 1024
			free_mem_mb = (psutil.swap_memory().free / 1024) / 1024
			free_mem_present = float(str(100 - psutil.swap_memory().percent)[:4])
			if type(total_mem_mb) == float:
				total_mem_mb = rounding_float(total_mem_mb)
			if type(free_mem_mb) == float:
				free_mem_mb = rounding_float(free_mem_mb)
			TextSWAPFreeLabel["text"] = "Файл Подкачки (Свободно): {0} МБ/{1} МБ ({2} %)".format(free_mem_mb, total_mem_mb, free_mem_present)
		except:
			TextSWAPFreeLabel["text"] = "Файл Подкачки (Свободно): Ошибка..."
		time.sleep(timeouts.UpdateSWAP)

def SwitchingOptionsAttributes(event):
	global root_operation
	if root_operation.attributes:
		root_operation.attributes = False
		cfgd["root"]["attributes"] = False
		root.attributes("-topmost", root_operation.attributes)
		ButtonSwitchingOptionsAttributes["fg"] = "red"
	else:
		root_operation.attributes = True
		cfgd["root"]["attributes"] = True
		root.attributes("-topmost", root_operation.attributes)
		ButtonSwitchingOptionsAttributes["fg"] = "green"
	with open("config.json", "w") as config_data_file:
		json.dump(cfgd, config_data_file)

def AverageLoadIndicator():
	while function_operation.UpdateAverageLoadIndicator:
		try:
			ColorIndicatorList = [IndicatorCPULoadLabel["fg"], IndicatorRAMLoadLabel["fg"], IndicatorSWAPLoadLabel["fg"]]
			wag = 0
			AverageLoadPoints = 0
			while wag != len(ColorIndicatorList):
				ColorIndicatorFG = str(ColorIndicatorList[wag])
				if ColorIndicatorFG == "green":
					AverageLoadPoints += 1
				elif ColorIndicatorFG == "#c9cc02":
					AverageLoadPoints += 2
				elif ColorIndicatorFG == "orange":
					AverageLoadPoints += 3
				elif ColorIndicatorFG == "red":
					AverageLoadPoints += 4
				wag += 1
			ColorAverageLoadIndicator = ""
			TextAverageLoadIndicator = ""
			if AverageLoadPoints <= 3:
				ColorAverageLoadIndicator = "green"
				TextAverageLoadIndicator = "Очень низкая"
			elif AverageLoadPoints <= 6:
				ColorAverageLoadIndicator = "#c9cc02"
				TextAverageLoadIndicator = "Низкая"
			elif AverageLoadPoints <= 9:
				ColorAverageLoadIndicator = "orange"
				TextAverageLoadIndicator = "Средняя"
			else:
				ColorAverageLoadIndicator = "red"
				TextAverageLoadIndicator = "Высокая"
			IndicatorAverageLoadLabel["fg"] = ColorAverageLoadIndicator
			IndicatorAverageLoadLabel["text"] = TextAverageLoadIndicator
		except:
			IndicatorAverageLoadLabel["fg"] = "white"
			IndicatorAverageLoadLabel["text"] = "Ошибка"
		time.sleep(timeouts.UpdateAverageLoad)

# Привязка объектов
ButtonSwitchingOptionsAttributes.bind('<Button-1>', SwitchingOptionsAttributes)

# Запуск в фоне
Thread(target = UpdateTimeLabel, args = (), daemon = True).start()
Thread(target = UpdateCPULoadLabel, args = (), daemon = True).start()
Thread(target = UpdateRAMLoadLabel, args = (), daemon = True).start()
Thread(target = UpdateRAMFreeLabel, args = (), daemon = True).start()
Thread(target = UpdateSWAPLoadLabel, args = (), daemon = True).start()
Thread(target = UpdateSWAPFreeLabel, args = (), daemon = True).start()
Thread(target = AverageLoadIndicator, args = (), daemon = True).start()

# Конец
root.mainloop()
function_operation.UpdateTime = False
function_operation.UpdateCPULoad = False
function_operation.UpdateRAM = False
function_operation.UpdateSWAP = False
function_operation.UpdateAverageLoadIndicator = False