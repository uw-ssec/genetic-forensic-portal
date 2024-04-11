from __future__ import annotations

from pathlib import Path

from streamlit.web.bootstrap import run

here = Path(__file__).parent
home_file = here / "app/Home.py"


def up() -> None:
    run(str(home_file), is_hello=False, args=[], flag_options={})
