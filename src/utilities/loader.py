import json
from datetime import date

from .constants import PPP_FILE_CLEANED, PPP_FILE_RAW, WB_PPP_API

WB_PPP_DATA_OFFSET = 1
WB_PPP_YEAR_RANGE = 5


def _filterout_pppdata(d_data: list):
    return filter(lambda x: x["value"] is not None, d_data[WB_PPP_DATA_OFFSET])


def _load_from_api(url):
    """Make api request to get PPP data and save to 'ppp.json'"""
    print("GEt file from the internet")


def _load_from_json(file_path):
    return json.load(open(file_path))


def pppdata(file_output=False):
    data = get_pppdata()
    res = {}
    for item in data:
        country = item["country"]["value"]
        if not country in res:
            res[country] = {
                "id": item["country"]["id"],
                "countryiso3code": item["countryiso3code"],
                "ppp": item["value"],
                "date": item["date"],
            }
        else:
            if res[country]["date"] > item["date"]:
                continue
            else:
                res[country]["ppp"] = item["value"]
                res[country]["date"] = item["date"]
    output = {"lastupdated": str(date.today()), "data": res}
    if not file_output:
        return output
    json.dump(output, fp=open(PPP_FILE_CLEANED, "w"), indent=4)


def get_pppdata() -> dict[str, dict]:
    if not PPP_FILE_RAW.exists():
        _load_from_api(WB_PPP_API)
    return _load_from_json(PPP_FILE_CLEANED)["data"]
