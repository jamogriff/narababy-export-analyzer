import code
import sys
import time
from .narababy_event_log_parser import NarababyEventLogParser
from .model_factory import ModelFactory
from .dtos.narababy_bottle_feed_row import NarababyBottleFeedRow
from .dtos.narababy_diaper_row import NarababyDiaperRow
from .dtos.narababy_pump_row import NarababyPumpRow
from .db.db import engine, does_database_exist
from .models.base import Base
from .utils.cli_utils import display_success, display_failure, get_elapsed_time

if __name__ == "__main__":
    parser = NarababyEventLogParser()
    file_path = input(f"Enter the file path to the Narababy export CSV: ")
    try:
        parser.check(file_path)
    except (ValueError, FileNotFoundError) as e:
        display_failure(str(e))
        sys.exit(1)

    start = time.perf_counter()
    parse_results = parser.parse()
    end = time.perf_counter()
    capture_percentage = (len(parse_results.data) / parse_results.rows_processed) * 100
    summary = "{0:.0f}% rows captured ({1}/{2}) in {3:.1f} ms".format(capture_percentage, len(parse_results.data), parse_results.rows_processed, get_elapsed_time(start, end))
    display_success(summary)

    if not does_database_exist(engine):
        Base.create_all()
        display_success("Created new database.")
    else:
        display_success("Database exists.")

    model_factory = ModelFactory(parse_results)
    start = time.perf_counter()
    models = model_factory.make()
    end = time.perf_counter()
    total_models = len(models.babies) + len(models.caregivers) + len(models.bottles) + len(models.diapers) + len(models.pumps)
    display_success(f"{total_models} models created via DTOs in {get_elapsed_time(start, end):.1f} ms")


    local_namespace = dict(globals(), **locals())
    code.interact(banner="Lettuce Analyze", local=local_namespace)
