import os
import csv
import time
from typing import cast
from .dtos.narababy_event_row import NarababyEventRow
from .dtos.parse_results import ParseResults


class NarababyEventLogParser:
    csv_export_file: None | str
    csv_dialect: None | csv.Dialect

    def check(self, csv_file_path: str) -> None:
        """Validate a CSV file to ensure parsing only occurs on valid export files.

        Method must be called prior to parse(), since this sets
        the csv_export and csv_dialect attributes that the parse() method
        utilizes.

        Raises:
            FileNotFoundError: If file does not exist.
            ValueError: If CSV file does not match reference Narababy export. 
        """

        self._assert_is_file(csv_file_path)
        self._assert_file_is_csv(csv_file_path)

        csv_sniffer = csv.Sniffer()
        # Check that CSV file has a header
        with open(csv_file_path, "r") as f:
            sample = f.read(1024)

        has_header = csv_sniffer.has_header(sample)
        if not has_header:
            raise ValueError("Narababy export CSV must have a header row.")

        # MyPy incorrectly thinks the result of sniff()
        # is the Dialect class and not an instance of Dialect
        csv_dialect = cast(csv.Dialect, csv_sniffer.sniff(sample))

        with open(csv_file_path, "r") as f:
            reader = csv.reader(f, csv_dialect)
            header = next(reader)

        # The first 20 values of Narababy's reference
        # CSV header that input CSV should be measured against
        reference_header = [
            'Type', 'Profile Name', 'Start Date/time', 'Start Date/time (Epoch)',
            'Created By Caregiver', 'Last Updated By Caregiver', 'Note', 'Time Zone',
            '[Bottle Feed] Type', '[Bottle Feed] Breast Milk Volume',
            '[Bottle Feed] Breast Milk Volume Unit', '[Bottle Feed] Formula Name',
            '[Bottle Feed] Formula Volume', '[Bottle Feed] Formula Volume Unit',
            '[Bottle Feed] Volume', '[Bottle Feed] Volume Unit', '[Diaper] Type',
            '[Diaper] Detail', '[Diaper] Dirty Color', '[Diaper] Dirty Texture'
        ]

        if header[:20] != reference_header:
            raise ValueError("Provided CSV's header does not match reference Narababy export CSV.")

        # At this point we are dealing with a valid CSV export
        # Set attributes to enable calling parse
        self.csv_dialect = csv_dialect
        self.csv_export_file = csv_file_path

    def parse(self) -> ParseResults:
        """Extract export CSV data into DTOs. Must be called after calling check method."""

        with open(self.csv_export_file, "r") as f:
            reader = csv.reader(f, self.csv_dialect)

            # Consume header row so we are only processing data
            header = next(reader)

            row_count = 0
            data: list[NarababyEventRow] = []
            for row in reader:
                # If there's an event type in the first column
                # then count as processed
                if row[0]:
                    row_count += 1
                    # If that event type is in the Row registry
                    # create a DTO and add it to the dataset 
                    if row[0] in NarababyEventRow.registry.keys():
                        row_class = NarababyEventRow.registry[row[0]]
                        row_instance = row_class()
                        row_instance.hydrate_from_row(row)
                        data.append(row_instance)

            return ParseResults(data, row_count)

    def _assert_is_file(self, file_path: str) -> None:
        """Assert the file is on the filesystem.

        Raises:
            FileNotFoundError: If file does not exist.
        """

        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

    def _assert_file_is_csv(self, file_path: str) -> None:
        """Assert the file is a CSV.

        Raises:
            ValueError: If file does not end in .csv.
        """

        if os.path.splitext(file_path)[1].lower() != ".csv":
            raise ValueError("Narababy export file must be a .csv file")


