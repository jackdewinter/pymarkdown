import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Union

from .models import Parser, Pattern

def get_parser_from_list(
    pattern_list: List[str], base_dir: Union[Path, str, None] = None
) -> Parser: ...
