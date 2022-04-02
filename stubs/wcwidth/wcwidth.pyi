from typing import Any

from .table_wide import WIDE_EASTASIAN as WIDE_EASTASIAN
from .table_zero import ZERO_WIDTH as ZERO_WIDTH
from .unicode_versions import list_versions as list_versions

ZERO_WIDTH_CF: Any

def wcwidth(wc: str, unicode_version: str = ...) -> int: ...
def wcswidth(pwcs: str, n: Any | None = ..., unicode_version: str = ...) -> int: ...
