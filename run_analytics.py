import json
from analytics.data import *
from analytics.stake_quarterlies import create_quarterly_analytics
from lcr import unit, quarterly_report
from lcr.api import API


def load_profile():
    with open("profile.json") as f:
        profile = json.load(f)
    return profile


def download_units_data(profile):
    units = unit.load_units(profile["units"])
    api = API(profile["username"], profile["password"], profile["unit_number"])
    reporter = quarterly_report.HistoricalQuarterlyReport(api, units)
    reporter.download_historical_quarters_to_csv(
        units, create_and_get_output_path(f"{profile['unit_name']}.csv")
    )


def main():
    profile = load_profile()
    download_units_data(profile)
    start_year = 2022
    create_quarterly_analytics(f"analytics\data\{profile['unit_name']}.csv", start_year)


if __name__ == "__main__":
    main()
