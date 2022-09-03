from conf import ASSETS_DIR

PPP_FILE_RAW = ASSETS_DIR / "ppp.json"
PPP_FILE_CLEANED = ASSETS_DIR / "clean.json"
WB_PPP_API = "https://api.worldbank.org/v2/en/country/all/indicator/PA.NUS.PPP?format=json&per_page=20000&source=2&date=${year - 5}:${year}"
