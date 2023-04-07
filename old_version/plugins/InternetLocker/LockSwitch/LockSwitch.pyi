from typing import overload, Optional, Literal
from dataclasses import dataclass

# ! Dataclass
@dataclass
class ProccessInfo:
    filename: str
    realpath: str

# ! Functions
def _sp(filename: str) -> Optional[ProccessInfo]: ...

@overload
def search_info(filename: str, wait: Literal[True]) -> ProccessInfo: ...
@overload
def search_info(filename: str, wait: Literal[False]) -> Optional[ProccessInfo]: ...
@overload
def search_info(filename: str) -> Optional[ProccessInfo]: ...

def block_program(process_info: ProccessInfo) -> None: ...
def unblock_program(process_info: ProccessInfo) -> None: ...