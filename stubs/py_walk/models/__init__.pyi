import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Union

@dataclass
class Pattern:
    glob: str
    parts: List[Union[re.Pattern[str], None]] = field(init=False)
    negated: bool = False
    is_dir: bool = False

    def __post_init__(self) -> None: ...
    def match(self, path: Path, is_dir: bool) -> List[int]: ...
    def __str__(self) -> str: ...

@dataclass
class Parser:
    patterns: List[Pattern]
    base_dir: Union[Path, None]

    def match(self, path: Union[Path, str]) -> bool: ...
