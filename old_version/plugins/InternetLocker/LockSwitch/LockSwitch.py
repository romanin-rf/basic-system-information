import os
import psutil
from dataclasses import dataclass

"""
netsh advfirewall firewall add rule name="Notepad" dir=out action=block program="C:\\Windows\\notepad.exe"
netsh advfirewall firewall add rule name="Notepad" dir=in action=block program="C:\\Windows\\notepad.exe"
netsh advfirewall firewall delete rule name="Notepad"
"""

# ! Dataclass
@dataclass
class ProccessInfo:
    filename: str
    realpath: str

# ! Functions
def _sp(filename: str):
    for i in psutil.pids():
        try:
            p = psutil.Process(i)
            if os.path.basename(p.exe()) == filename:
                return ProccessInfo(os.path.basename(p.exe()), p.exe())
        except:
            pass

def search_info(filename: str, wait: bool=False):
    if wait:
        while True:
            if (pid:=_sp(filename)) is not None:
                return pid
    else:
        return _sp(filename)

def block_program(process_info: ProccessInfo):
    try:
        os.system(f"netsh advfirewall firewall add rule name=\"{process_info.filename}_Blocking\" dir=out action=block program=\"{process_info.realpath}\"")
        os.system(f"netsh advfirewall firewall add rule name=\"{process_info.filename}_Blocking\" dir=in action=block program=\"{process_info.realpath}\"")
    except:
        pass

def unblock_program(process_info: ProccessInfo):
    try:
        os.system(f"netsh advfirewall firewall delete rule name=\"{process_info.filename}_Blocking\"")
    except:
        pass
