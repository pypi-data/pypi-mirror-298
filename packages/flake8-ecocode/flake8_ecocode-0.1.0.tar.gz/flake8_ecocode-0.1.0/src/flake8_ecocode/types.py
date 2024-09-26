# Flake8 error type: (line number, column, warning message, caller type)
from typing import Tuple

FlakeError = Tuple[int, int, str, type]
