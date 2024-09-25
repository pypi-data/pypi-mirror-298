# init file for SMART_MRS package

# module import declaration
from . import applied
from . import artifacts
from . import IO
from . import support

# Wildcard (*) import declaration
__all__ = ["applied", "artifacts", "IO", "support"]

# variable declaration
VERSION = "1.0"
LAST_UPDATED = "2024_08_20"
AUTHORS = "Bugler et al."
