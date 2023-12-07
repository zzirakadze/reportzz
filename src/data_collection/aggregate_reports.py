import glob
import json
import logging
import os

logger = logging.getLogger(__name__)


def aggregate_reports():
    report_files = glob.glob("test_report_*.json")
    aggregated_results = []

    for file in report_files:
        with open(file, "r") as f:
            results = json.load(f)
            aggregated_results.extend(results)
        os.remove(file)

    if aggregated_results:
        with open("aggregated_test_report.json", "w") as f:
            json.dump(aggregated_results, f, indent=4)
        logger.info(f"Aggregated results written to aggregated_test_report.json.")
    else:
        logger.warning("No results found to aggregate.")


if __name__ == "__main__":
    aggregate_reports()
