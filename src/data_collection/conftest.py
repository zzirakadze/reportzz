import glob
import json
import logging
import os
from datetime import datetime

import pytest

test_results: list = []
logger = logging.getLogger(__name__)


def pytest_configure(config) -> None:
    logging.basicConfig(level=logging.INFO)
    if hasattr(config, "workerinput"):
        worker_id = config.workerinput.get("workerid", "master")
        config.worker_output_file = (
            f"test_report_{worker_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
        )
    else:
        config.worker_output_file = (
            f"test_report_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
        )


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call) -> None:
    if call.when == "call":
        test_result = {
            "name": item.nodeid,
            "outcome": "passed" if call.excinfo is None else "failed",
            "duration": call.stop - call.start
            if hasattr(call, "stop") and hasattr(call, "start")
            else None,
            "longrepr": str(call.excinfo) if call.excinfo else None,
            "traceback": call.excinfo.traceback.format() if call.excinfo else None,
            "stdout": call.stdout.str() if call.stdout else None,
            "stderr": call.stderr.str() if call.stderr else None,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "test_file": item.location[0],
            "test_class": item.location[0].split("/")[-1],
            "test_function": item.location[2],
            "test_module": item.location[0].split("/")[-1].split(".")[0],
            "suite_name": item.location[0].split("/")[-1].split(".")[0],
            "test_id": item.location[2],
            "test_description": item.location[2],
            "test_status": "passed" if call.excinfo is None else "failed",
            "test_duration": call.stop - call.start,
            "test_start_time": call.start,
            "test_end_time": call.stop,
        }
        test_results.append(test_result)
        logging.info(f"Test result appended: {test_result}")


@pytest.hookimpl(hookwrapper=True)
def pytest_sessionfinish(session, exitstatus) -> None:
    yield
    report_file = session.config.worker_output_file
    try:
        with open(report_file, "w") as f:
            json.dump(test_results, f, indent=4)
        logging.info(f"Test results written to {report_file}.")
    except Exception as e:
        logging.error(f"Error writing to file: {e}")


def pytest_terminal_summary(terminalreporter, exitstatus, config) -> None:
    if hasattr(config, 'workerinput'):
        return

    logger.info("Starting to aggregate test reports...")

    report_files = glob.glob("test_report_*.json")
    logger.info(f"Found report files: {report_files}")

    aggregated_results = []
    files_to_remove = []

    # Process each report file.
    for file in report_files:
        logger.info(f"Processing file: {file}")
        try:
            with open(file, "r") as f:
                results = json.load(f)
            aggregated_results.extend(results)
            files_to_remove.append(file)
        except Exception as e:
            logger.error(f"Error reading file {file}: {e}")

    if aggregated_results:
        aggregated_file = "aggregated_test_report.json"
        try:
            with open(aggregated_file, "w") as f:
                json.dump(aggregated_results, f, indent=4)
            logger.info(f"Aggregated results written to {aggregated_file}.")
        except Exception as e:
            logger.error(f"Error writing aggregated results: {e}")

        for file in files_to_remove:
            try:
                os.remove(file)
                logger.info(f"Removed file: {file}")
            except Exception as e:
                logger.error(f"Error removing file {file}: {e}")
    else:
        logger.warning("No results found to aggregate.")

