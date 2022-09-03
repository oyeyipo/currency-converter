import json
from datetime import date

from .constants import PPP_FILE_CLEANED, PPP_FILE_RAW, WB_PPP_API, COUNTRIES_METADATA

WB_PPP_DATA_OFFSET = 1
WB_PPP_YEAR_RANGE = 5


def _filterout_pppdata(d_data: list):
    return filter(lambda x: x["value"] is not None, d_data[WB_PPP_DATA_OFFSET])


def _load_from_api(url):
    """Make api request to get PPP data and save to 'ppp.json'"""
    print("GEt file from the internet")


def _load_from_json(file_path):
    return _filterout_pppdata(json.load(open(file_path)))


def pppdata(file_output=False):
    data = _get_pppdata_uncleaned()
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

    res = _add_countries_metadata(res)
    output = {"lastupdated": str(date.today()), "data": res}
    if not file_output:
        return output
    json.dump(output, fp=open(PPP_FILE_CLEANED, "w"), indent=4)


def _get_pppdata_uncleaned():
    if not PPP_FILE_RAW.exists():
        _load_from_api(WB_PPP_API)
    return _load_from_json(PPP_FILE_RAW)


def _add_countries_metadata(data: dict) -> dict:
    countries_md = json.load(open(COUNTRIES_METADATA, encoding="utf-8"))
    for country in data:
        iso_code = data[country]["countryiso3code"]

        for item in countries_md:
            if item["isoAlpha3"] != iso_code:
                continue
            data[country]["currency"] = item["currency"]
            data[country]["flag"] = item["flag"]

    return {key: data[key] for key in data if "currency" in data[key]}


def get_pppdata() -> dict[str, dict]:
    pppdata(True)
    return json.load(open(PPP_FILE_CLEANED))["data"]
