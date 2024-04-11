from __future__ import annotations

import subprocess
from pathlib import Path

here = Path(__file__).parent
home_file = here / "app/Home.py"


def up() -> None:
    subprocess.run(["python", "-m", "streamlit", "run", str(home_file)], check=False)
