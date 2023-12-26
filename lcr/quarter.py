class Quarter:
    def __init__(self, year, quarter):
        self._year = year
        self._quarter = quarter

    def __init__(self, encoded_quarter: str):
        y, q = encoded_quarter.split("-")
        self._year = int(y)
        self._quarter = int(q)

    @property
    def year(self):
        return self._year

    @year.setter
    def name(self, value):
        if not isinstance(value, int):
            raise ValueError("Year must be an integer.")
        self._name = value

    @property
    def quarter(self):
        return self._quarter

    @quarter.setter
    def number(self, value):
        if not isinstance(value, int):
            raise ValueError("Quarter must be an integer")
        self._quarter = value

    def __str__(self):
        return f"{self._year}-Q{self._quarter}"
