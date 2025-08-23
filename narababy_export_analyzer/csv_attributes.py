import csv
from dataclasses import dataclass


@dataclass
class CSVAttributes:
    dialect: csv.Dialect
    has_header: bool
