import code
import sys
from .narababy_event_log_parser import NarababyEventLogParser
from .model_factory import ModelFactory
from .dtos.narababy_bottle_feed_row import NarababyBottleFeedRow
from .dtos.narababy_diaper_row import NarababyDiaperRow
from .dtos.narababy_pump_row import NarababyPumpRow
from .db.db import engine, does_database_exist
from .models.base import Base
from .utils.cli_utils import get_valid_csv_from_user, display_success, display_failure

if __name__ == "__main__":
    try:
        file_path = get_valid_csv_from_user()
    except Exception as e:
        display_failure(str(e))
        sys.exit(1)

    parser = NarababyEventLogParser()
    parse_results = parser.parse(file_path)
    capture_percentage = (len(parse_results.data) / parse_results.rows_processed) * 100
    message = f"{capture_percentage:.0f}% rows captured ({len(parse_results.data)}/{parse_results.rows_processed}) in {parse_results.time_elapsed:.4f} seconds"
    display_success(message)

    if not does_database_exist(engine):
        Base.create_all()
        display_success("Created new database.")
    else:
        display_success("Database exists.")

    model_factory = ModelFactory(parse_results)
    models = model_factory.make()


    local_namespace = dict(globals(), **locals())
    code.interact(banner="Lettuce Analyze", local=local_namespace)
