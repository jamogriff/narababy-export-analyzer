import code
from .narababy_event_log_parser import NarababyEventLogParser
from .model_factory import ModelFactory
from .dtos.narababy_bottle_feed_row import NarababyBottleFeedRow
from .dtos.narababy_diaper_row import NarababyDiaperRow
from .dtos.narababy_pump_row import NarababyPumpRow
from .db.engine import engine

if __name__ == "__main__":
    p = NarababyEventLogParser()
    file_path = "csv_fun/data/export_raw.csv"
    data = p.parse(file_path)
    factory = ModelFactory(data)

    local_namespace = dict(globals(), **locals())
    code.interact(banner="Lettuce Analyze", local=local_namespace)
