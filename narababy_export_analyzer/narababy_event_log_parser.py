import csv
import time
from typing import cast
from .dtos.narababy_event_row import NarababyEventRow
from .parse_results import ParseResults
from .csv_attributes import CSVAttributes


class NarababyEventLogParser:

    def parse(self, csv_file_path: str) -> ParseResults:
        start = time.perf_counter()
        # TODO check that it is a CSV
        csv_attributes = self._get_csv_attributes(csv_file_path)

        with open(csv_file_path, "r") as f:
            reader = csv.reader(f, csv_attributes.dialect)

            if csv_attributes.has_header:
                header = next(reader)
                print(f"Header: {header}")

            row_count = 0
            data: list[NarababyEventRow] = []
            for row in reader:
                row_count += 1
                if row[0] in NarababyEventRow.registry.keys():
                    row_class = NarababyEventRow.registry[row[0]]
                    row_instance = row_class()
                    row_instance.hydrate_from_row(row)
                    data.append(row_instance)

            capture_percentage = (len(data) / row_count) * 100

            print("----------------")
            end = time.perf_counter()
            time_elapsed = end - start
            print(
                f"{capture_percentage:.0f}% rows captured ({len(data)}/{row_count}) in {time_elapsed:.4f} seconds"
            )
            print("----------------")

            return ParseResults(data, row_count, time_elapsed)

    def _get_csv_attributes(self, csv_file_path: str) -> CSVAttributes:
        csv_sniffer = csv.Sniffer()
        with open(csv_file_path, "r") as f:
            sample = f.read(1024)

        # MyPy incorrectly thinks the result of sniff()
        # is the Dialect class and not an instance of Dialect
        return CSVAttributes(
            cast(csv.Dialect, csv_sniffer.sniff(sample)), csv_sniffer.has_header(sample)
        )
