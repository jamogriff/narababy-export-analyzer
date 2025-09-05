import code
import sys
import time
from bare_cli import BareCLI
from sqlalchemy.orm import Session
from .narababy_event_log_parser import NarababyEventLogParser
from .model_factory import ModelFactory
from .dtos.narababy_bottle_feed_row import NarababyBottleFeedRow
from .dtos.narababy_diaper_row import NarababyDiaperRow
from .dtos.narababy_pump_row import NarababyPumpRow
from .db.db import get_engine, get_session, initialize_database, does_data_exist
from .models.base import Base
from .utils.cli_utils import get_elapsed_time
from .importer import Importer
from .repository.baby_repository import BabyRepository
from .repository.caregiver_repository import CaregiverRepository


if __name__ == "__main__":
    io = BareCLI()
    io.title("Narababy Export Analyzer")

    # Shortcut to data analysis REPL if data already exists
    if does_data_exist():
        choice = io.choice(
            "Data already exists. Do you want to analyze existing data or import another export file?",
            ["Analyze existing data", "Import another export file"],
        )

        if choice[0] == 0:
            io.info("Using existing dataset.")
            baby_repo = BabyRepository(get_session())
            caregiver_repo = CaregiverRepository(get_session())
            babies = baby_repo.find_all()
            choice = io.choice("Whose statistics would you like to view?", [b.name for b in babies])
            selected_baby = babies[choice[0]]
            bottle_stats = baby_repo.find_bottle_statistics(selected_baby)
            diaper_stats = baby_repo.find_diaper_change_statistics(selected_baby)
            io.info("Bottle Stats")
            io.info(f"{bottle_stats.total_bottles} total bottles | {bottle_stats.total_gallons} total gallons of milk drunk | {bottle_stats.average_oz} average fluid ounces per bottle")
            io.info("-" * 10)
            io.info("Diaper Changes")
            io.info(f"{diaper_stats.total_diaper_changes} total diaper changes | {diaper_stats.dirty_diapers} dirty diapers | {diaper_stats.wet_diapers} wet diapers")
            io.info("-" * 10)
            io.info("Caregiver Stats")
            caregiver_feeds = caregiver_repo.find_feeds_by_caregivers(selected_baby)
            for feed in caregiver_feeds:
                io.info(f"{feed.name} fed {selected_baby.name} {feed.total_feeds} times")
            caregiver_diaper_changes = caregiver_repo.find_diaper_changes_by_caregivers(selected_baby)
            for change in caregiver_diaper_changes:
                io.info(f"{change.name} changed {selected_baby.name}'s diapers {change.total_diaper_changes} times")

            io.info("-" * 10)
            io.info(f"Total pumps irrespective of baby")
            caregiver_pumps = caregiver_repo.find_pumps_by_caregivers()
            for pump in caregiver_pumps:
                io.info(f"{pump.name} pumped {pump.total_pumps} times")

            sys.exit(0)
            # local_namespace = dict(globals(), **locals())
            # code.interact(
            #     banner=io.info("REPL environment started"), local=local_namespace
            # )

    parser = NarababyEventLogParser()
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
    summary = "{0:.0f}% rows captured ({1}/{2}) in {3:.1f} ms".format(
        capture_percentage,
        len(parse_results.data),
        parse_results.rows_processed,
        get_elapsed_time(start, end),
    )
    io.success(summary)

    model_factory = ModelFactory(parse_results)
    start = time.perf_counter()
    models = model_factory.make()
    end = time.perf_counter()
    total_models = (
        len(models.babies)
        + len(models.caregivers)
        + len(models.bottles)
        + len(models.diapers)
        + len(models.pumps)
    )
    io.success(
        f"{total_models} models created via DTOs in {get_elapsed_time(start, end):.1f} ms"
    )

    # We have persistable data at this point,
    # so initialize database
    io.info("Initializing database.")
    start = time.perf_counter()
    result = initialize_database()
    Base.metadata.create_all(get_engine())
    end = time.perf_counter()
    io.success(f"Created new database in {get_elapsed_time(start, end):.1f} ms")

    importer = Importer(get_engine())
    start = time.perf_counter()
    importer.import_models(models)
    end = time.perf_counter()
    io.success(
        f"Persisted models to the database in {get_elapsed_time(start, end):.1f} ms"
    )

    start = time.perf_counter()
    errors = importer.validate_inserts(models)
    end = time.perf_counter()
    io.info(f"Validated database insertions in {get_elapsed_time(start, end):.1f} ms")

    if len(errors) == 0:
        io.success("NaraBaby export has successfully been imported.")
    else:
        for error in errors:
            io.error(
                f"{error.expected} models of {error.model} were expected. Actual: {error.actual}"
            )
        # TODO: destroy database
        sys.exit(1)

    # TODO: centralize this
    baby_repo = BabyRepository(get_session())
    caregiver_repo = CaregiverRepository(get_session())
    babies = baby_repo.find_all()
    choice = io.choice("Whose statistics would you like to view?", [b.name for b in babies])
    selected_baby = babies[choice[0]]
    bottle_stats = baby_repo.find_bottle_statistics(selected_baby)
    diaper_stats = baby_repo.find_diaper_change_statistics(selected_baby)
    io.info("Bottle Stats")
    io.info(f"{bottle_stats.total_bottles} total bottles | {bottle_stats.total_gallons} total gallons of milk drunk | {bottle_stats.average_oz} average fluid ounces per bottle")
    io.info("-" * 10)
    io.info("Diaper Changes")
    io.info(f"{diaper_stats.total_diaper_changes} total diaper changes | {diaper_stats.dirty_diapers} dirty diapers | {diaper_stats.wet_diapers} wet diapers")
    io.info("-" * 10)
    io.info("Caregiver Stats")
    caregiver_feeds = caregiver_repo.find_feeds_by_caregivers(selected_baby)
    for feed in caregiver_feeds:
        io.info(f"{feed.name} fed {selected_baby.name} {feed.total_feeds} times")
    caregiver_diaper_changes = caregiver_repo.find_diaper_changes_by_caregivers(selected_baby)
    for change in caregiver_diaper_changes:
        io.info(f"{change.name} changed {selected_baby.name}'s diapers {change.total_diaper_changes} times")

    io.info("-" * 10)
    io.info(f"Total pumps irrespective of baby")
    caregiver_pumps = caregiver_repo.find_pumps_by_caregivers()
    for pump in caregiver_pumps:
        io.info(f"{pump.name} pumped {pump.total_pumps} times")

    sys.exit(0)
    # local_namespace = dict(globals(), **locals())
    # code.interact(
    #     banner=io.info("REPL environment started"), local=local_namespace
    # )

