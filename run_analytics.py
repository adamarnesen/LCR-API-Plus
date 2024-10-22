import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from analytics.data import *
from analytics.stake_quarterlies import create_quarterly_analytics
from lcr import quarterly_report, unit
from lcr.api import API, CHROME_OPTIONS


def load_profile():
    with open("profile.json") as f:
        profile = json.load(f)
    return profile


def setup_api_from_profile(profile) -> API:
    if profile["chrome_driver_path"]:
        driver = webdriver.Chrome(
            service=Service(profile["chrome_driver_path"]), options=CHROME_OPTIONS
        )
        api = API(
            profile["username"],
            profile["password"],
            profile["unit_number"],
            driver=driver,
        )
    else:
        api = API(profile["username"], profile["password"], profile["unit_number"])
    return api


def download_units_data(profile) -> str:
    """Downloads the units data based on units listed in the `profile`."""
    units = unit.load_units(profile["units"])
    api = setup_api_from_profile(profile)
    reporter = quarterly_report.HistoricalQuarterlyReport(api, units)
    output_file = create_and_get_output_path(f"{profile['unit_name']}.csv")
    reporter.download_historical_quarters_to_csv(units, output_file)
    return output_file


def main():
    profile = load_profile()
    download_units_data(profile)
    start_year = 2022
    create_quarterly_analytics(
        f"analytics\data\{profile['unit_name']}.csv", start_year, profile["unit_name"]
    )


if __name__ == "__main__":
    main()
