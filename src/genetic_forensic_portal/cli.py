from __future__ import annotations

from pathlib import Path

from streamlit.web.bootstrap import run

from genetic_forensic_portal import auth

here = Path(__file__).parent
home_file = here / "app/Home.py"


def up() -> None:
    if not auth.KEYCLOAK_PID_FILE.exists():
        auth.start_keycloak()
    run(str(home_file), is_hello=False, args=[], flag_options={})
