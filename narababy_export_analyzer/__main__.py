import code
import sys
import time
from bare_cli import BareCLI
from .narababy_event_log_parser import NarababyEventLogParser
from .model_factory import ModelFactory
from .dtos.narababy_bottle_feed_row import NarababyBottleFeedRow
from .dtos.narababy_diaper_row import NarababyDiaperRow
from .dtos.narababy_pump_row import NarababyPumpRow
from .db.db import engine, does_database_exist
from .models.base import Base
from .utils.cli_utils import get_elapsed_time

if __name__ == "__main__":
    io = BareCLI()
    parser = NarababyEventLogParser()
    io.title("Narababy Export Analyzer")
    file_path = io.ask(f"Enter the file path to the Narababy export CSV: ")
    try:
        parser.check(file_path)
    except (ValueError, FileNotFoundError) as e:
        io.error(str(e))
        sys.exit(1)

    start = time.perf_counter()
    parse_results = parser.parse()
    end = time.perf_counter()
    capture_percentage = (len(parse_results.data) / parse_results.rows_processed) * 100
    summary = "{0:.0f}% rows captured ({1}/{2}) in {3:.1f} ms".format(capture_percentage, len(parse_results.data), parse_results.rows_processed, get_elapsed_time(start, end))
    io.success(summary)

    if not does_database_exist(engine):
        Base.create_all()
        io.success("Created new database.")
    else:
        io.success("Database exists.")

    model_factory = ModelFactory(parse_results)
    start = time.perf_counter()
    models = model_factory.make()
    end = time.perf_counter()
    total_models = len(models.babies) + len(models.caregivers) + len(models.bottles) + len(models.diapers) + len(models.pumps)
    io.success(f"{total_models} models created via DTOs in {get_elapsed_time(start, end):.1f} ms")


    local_namespace = dict(globals(), **locals())
    code.interact(banner="Lettuce Analyze", local=local_namespace)
