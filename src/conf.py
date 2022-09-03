import pathlib
from PySide6.QtCore import QMargins

BASE_DIR = pathlib.Path(__file__).parent.parent

ASSETS_DIR = BASE_DIR.joinpath("assets")

CSS_FILE = ASSETS_DIR / "css/styles.css"

NO_MARGIN = QMargins(0, 0, 0, 0)
