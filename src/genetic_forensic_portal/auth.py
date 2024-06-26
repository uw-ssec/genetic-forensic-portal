import logging
import os
import subprocess
import sys
from pathlib import Path
from urllib.request import urlretrieve
from zipfile import ZipFile

HOME_DIR = Path.home()
CACHE_DIR = HOME_DIR / ".cache"
PORTAL_CACHE = CACHE_DIR / "gf-portal"
PORTAL_CACHE.mkdir(parents=True, exist_ok=True)

KEYCLOAK_VERSION = os.environ.get("KEYCLOAK_VERSION", "25.0.0")
KEYCLOAK_URL = os.environ.get(
    "KEYCLOAK_URL",
    f"https://github.com/keycloak/keycloak/releases/download/{KEYCLOAK_VERSION}/keycloak-{KEYCLOAK_VERSION}.zip",
)
KEYCLOAK_ZIP = PORTAL_CACHE / f"keycloak-{KEYCLOAK_VERSION}.zip"
KEYCLOAK_FOLDER = PORTAL_CACHE / f"keycloak-{KEYCLOAK_VERSION}"

here = Path(__file__).parent
REALM_DIRECTORY = here / "config" / "keycloak-realm/"
REALM_DIRECTORY_TEMP = REALM_DIRECTORY / "temp"

KEYCLOAK_PID_FILE = PORTAL_CACHE / "keycloak-pid"

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


def download_and_unzip_keycloak(force: bool = False) -> Path:
    if not KEYCLOAK_FOLDER.exists() or force:
        urlretrieve(KEYCLOAK_URL, KEYCLOAK_ZIP)
        with ZipFile(KEYCLOAK_ZIP, "r") as zip_ref:
            zip_ref.extractall(PORTAL_CACHE)

        if KEYCLOAK_ZIP.exists():
            KEYCLOAK_ZIP.unlink()
    return KEYCLOAK_FOLDER


def start_keycloak(force: bool = False) -> None:
    keycloak_folder = download_and_unzip_keycloak(force)
    if keycloak_folder.exists():
        kc_sh = keycloak_folder / "bin" / "kc.sh"
        kc_sh.chmod(0o755)

        # Import saved realm info and users into keycloak
        logger.info("Importing realm")
        subprocess.run(
            [f"{kc_sh}", "import", "--dir", f"{REALM_DIRECTORY}"],
            stdout=subprocess.DEVNULL,
            check=False,
        )

        logger.info("Realm import completed!")

        # Start keycloak with imported realm
        logger.info("Starting Keycloak with imported realm")
        process = subprocess.Popen(
            [f"{kc_sh}", "start-dev", "--import-realm"], stdout=subprocess.DEVNULL
        )
        logger.info("Keycloak started as process %s", process.pid)

        with KEYCLOAK_PID_FILE.open("w") as f:
            f.write(str(process.pid))


def up() -> None:
    if "DEFAULT_AUTH_ADMIN_PASSWORD" in os.environ:
        os.environ["KEYCLOAK_ADMIN"] = os.environ["DEFAULT_AUTH_ADMIN_USERNAME"]
        os.environ["KEYCLOAK_ADMIN_PASSWORD"] = os.environ[
            "DEFAULT_AUTH_ADMIN_PASSWORD"
        ]
    elif (
        "KEYCLOAK_ADMIN" not in os.environ
        or "KEYCLOAK_ADMIN_PASSWORD" not in os.environ
    ):
        os.environ["KEYCLOAK_ADMIN"] = "admin"
        os.environ["KEYCLOAK_ADMIN_PASSWORD"] = "admin"

    down()
    logger.info("Starting Keycloak")
    start_keycloak()


def down() -> None:
    if KEYCLOAK_PID_FILE.exists():
        logger.info("Stopping Keycloak")
        keycloak_pid_file = KEYCLOAK_PID_FILE.open("r")
        keycloak_pid = keycloak_pid_file.read()
        keycloak_pid_file.close()

        os.system(f"kill -9 {keycloak_pid}")

        KEYCLOAK_PID_FILE.unlink()


def export() -> None:
    if KEYCLOAK_FOLDER.exists():
        logger.info("Exporting Keycloak realm")
        REALM_DIRECTORY_TEMP.mkdir(parents=True, exist_ok=True)
        kc_sh = KEYCLOAK_FOLDER / "bin" / "kc.sh"
        os.system(
            f"{kc_sh} export --realm gf-portal --users same_file --dir {REALM_DIRECTORY_TEMP}"
        )

        logger.info("Export complete!")
        logger.info("Exported files are located in %s", REALM_DIRECTORY_TEMP)
        logger.info(
            "If you'd like to replace the existing configuration, run the following command:"
        )
        logger.info("\tcp -r %s/* %s", REALM_DIRECTORY_TEMP, REALM_DIRECTORY)


if __name__ == "__main__":
    up()
