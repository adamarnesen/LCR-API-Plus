import json
from typing import Dict, List


class Unit:
    def __init__(self, unit_name, unit_number):
        self._name = unit_name
        self._number = unit_number

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Unit name must be a string")
        self._name = value

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        if not isinstance(value, int):
            raise ValueError("Unit number must be an integer")
        self._number = value

    def to_dict(self):
        return {"name": self._name, "number": self._number}

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["number"])

    def __str__(self):
        return f"Unit(Name: {self._name}, Number: {self._number})"


def load_units(units_json_file: str):
    with open(units_json_file) as f:
        json_units = json.load(f)
    units = []
    for json_unit in json_units:
        units.append(Unit(json_unit["name"], json_unit["number"]))
    return units
