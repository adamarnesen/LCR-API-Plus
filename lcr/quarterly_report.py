from typing import List

import pandas as pd
from lcr.api import API
from lcr.quarter import Quarter
from lcr.unit import Unit


class HistoricalQuarterlyReport:
    def __init__(self, api: API, units):
        self._api = api
        self._units = units

    def __get_report_row(self, lcr: API, unit: Unit, quarter: Quarter):
        qrp = lcr.quarterly_report(unit.number, quarter.quarter, quarter.year)
        reduced_row = {
            "year": quarter.year,
            "quarter.num": quarter.number,
            "quarter": str(quarter),
            "unitId": unit.number,
            "unitName": unit.name,
        }
        for section in qrp["sections"]:
            for row in section["rows"]:
                reduced_row[row["nameResourceId"]] = row["actualValue"]
                reduced_row[f"{row['nameResourceId']}.potential"] = row[
                    "potentialValue"
                ]
        return reduced_row

    def __get_quarterly_report_for_unit(self, unit: Unit, lcr: API):
        quarters = lcr.available_report_quarters(unit)
        unit_report = []
        for q in quarters:
            row = self.__get_report_row(lcr, unit, q)
            unit_report.append(row)
        return unit_report

    def __get_quarterly_report(self, units: List[Unit], lcr: API) -> pd.DataFrame:
        report_table = []
        for unit in units:
            unit_report = self.__get_quarterly_report_for_unit(unit, lcr)
            report_table = report_table + unit_report
        df = pd.DataFrame(report_table)
        return df

    def download_historical_quarters_to_csv(self, stake_units, output_path: str):
        df = self.__get_quarterly_report(stake_units, self._api)
        df.to_csv(output_path, index=False)
        return df
