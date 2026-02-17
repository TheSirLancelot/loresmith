"""Import helper for Streamlit multipage apps.

Streamlit can execute pages from `app/pages/` with a working directory / sys.path
that does not include the repository root. This helper ensures the project root is
on `sys.path` so imports like `from app.components...` work consistently.
"""

from __future__ import annotations

import sys
from pathlib import Path


def ensure_project_root_on_path() -> None:
    p = Path(__file__).resolve()
    # app/bootstrap.py -> parents[1] == repo root
    project_root = p.parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))


ensure_project_root_on_path()
