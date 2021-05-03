import os
import sys
import wget
import json
import time
from threading import Thread
# Дополнительные библеотеки
import lmgs_libs.ColorMindustry as cmind
import lmgs_libs.pydustry as pydustry

# Графическая библеотека
import rich
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich.layout import Layout

# Конфигурации
class _proginfo:
	name = "LMGS"
	version = "0.3-beta"
	versionint = 0.3
	company = "RCR"
	author = "Roman Slabicky"

class _cfg:
	class _net:
		url_gl = "https://raw.githubusercontent.com/Anuken/Mindustry/master/servers_v6.json"
		gldata = None

	class _timeout:
		GetStatus = 1
		GetStatusHandler = 5

		SpeedUpdateTable = 5
		UpTableGL = 30

	class _works:
		UpTableGL = True
		Starting = True
		TimeoutErrorTableAddHandler = True

	sort_id = 6

class _tmp:
	cycle = 0
	table = None
	tabled = []

class _func:
	def UpdateTableGL(csl):
		while _cfg._works.UpTableGL:
			_func.clear()
			csl.print(_tmp.table, justify = "center")
			time.sleep(_cfg._timeout.SpeedUpdateTable)

	def TimeoutErrorTableAddHandler(address_list, cycle_id):
		if len(address_list) == 1:
			MindServer = pydustry.Server(str(address_list[0]))
		else:
			MindServer = pydustry.Server(str(address_list[0]), int(address_list[1]))
		try:
			StatusServer = MindServer.get_status(_cfg._timeout.GetStatusHandler)
			if (_tmp.table != None) and (cycle_id == _tmp.cycle):
				_tmp.table.add_row(str(time.strftime("%H:%M:%S", time.localtime())), str(address_list[0]) if (len(address_list) == 1) else str(address_list[0]) + ":" + str(address_list[1]), ((StatusServer["name"].replace("[]", "[/]")).replace("   ", "")).replace("||", ""), str(StatusServer["version"]), cmind.del_color_in_str(StatusServer["map"]), str(StatusServer["wave"]), str(StatusServer["players"]))
		except:
			_tmp.table.add_row("[white on red]" + str(time.strftime("%H:%M:%S", time.localtime())), "[white on red]" + (str(address_list[0]) if (len(address_list) == 1) else str(address_list[0]) + ":" + str(address_list[1])), "[white on red]ERROR", "[white on red]ERROR", "[white on red]ERROR", "[white on red]ERROR", "[white on red]ERROR")

	def set_title(titles: str):
		if sys.platform == "win32":
			os.system(f"title {titles}")
		elif sys.platform == "linux":
			pass

	def clear():
		if sys.platform == "win32":
			os.system("cls")
		elif sys.platform == "linux":
			os.system("clear")

# Логика
console = Console()
_func.set_title(f"{_proginfo.name} v{_proginfo.version} ({_proginfo.versionint})")

# Загрузка
with Progress() as LoadingCBIMS:
	TaskLoadingCBIMS = LoadingCBIMS.add_task("[cyan]Loading...", total = 4)

	filename_gl = wget.download(_cfg._net.url_gl)
	LoadingCBIMS.update(TaskLoadingCBIMS, advance = 1)
	console.clear()
	LoadingCBIMS.update(TaskLoadingCBIMS, advance = 1)

	with open(filename_gl) as glfile:
		_cfg._net.gldata = json.load(glfile)
	LoadingCBIMS.update(TaskLoadingCBIMS, advance = 1)

	os.remove(filename_gl)
	LoadingCBIMS.update(TaskLoadingCBIMS, advance = 1)

# Работа программы
Thread(target = _func.UpdateTableGL, args = (console,), daemon = True).start()

while _cfg._works.Starting:
	_tmp.table = Table(title = f"[yellow]{_proginfo.name}[/] [cyan]v{_proginfo.version}[/] ([red]{_proginfo.versionint}[/]) from [green]{_proginfo.company}[/] @ [pink]{_proginfo.author}[/]")

	_tmp.table.add_column("Time Parsing", justify = "center")
	_tmp.table.add_column("Host", justify = "center")
	_tmp.table.add_column("Name", justify = "center")
	_tmp.table.add_column("Core Verison", justify = "center", style = "green")
	_tmp.table.add_column("Map", justify = "center")
	_tmp.table.add_column("Wave", justify = "center", style = "cyan")
	_tmp.table.add_column("Players", justify = "center", style = "yellow")

	wag_category = 0
	while wag_category != len(_cfg._net.gldata):
		wag_server = 0
		while wag_server != len(_cfg._net.gldata[wag_category]["address"]):
			ServerAddress = _cfg._net.gldata[wag_category]["address"][wag_server].split(":")
			if len(ServerAddress) == 1:
				MindServer = pydustry.Server(str(ServerAddress[0]))
			else:
				MindServer = pydustry.Server(str(ServerAddress[0]), int(ServerAddress[1]))
			try:
				StatusServer = MindServer.get_status(timeout = _cfg._timeout.GetStatus)
				_tmp.table.add_row(str(time.strftime("%H:%M:%S", time.localtime())), str(address_list[0]) if (len(address_list) == 1) else str(address_list[0])+ ":" + str(address_list[1]), StatusServer["name"].replace("[]", "[/]").replace("   ", "").replace("||", ""), str(StatusServer["version"]), cmind.del_color_in_str(StatusServer["map"]), str(StatusServer["wave"]), str(StatusServer["players"]))
			except:
				Thread(target = _func.TimeoutErrorTableAddHandler, args = (ServerAddress, _tmp.cycle), daemon = True).start()
			wag_server += 1
		wag_category += 1
	time.sleep(_cfg._timeout.UpTableGL)
	_tmp.cycle += 1