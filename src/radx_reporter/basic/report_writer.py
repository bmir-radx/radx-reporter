import json

import pandas as pd


def dump_report_spreadsheet(
    study_labels: pd.DataFrame,
    counts_by_classifier: pd.DataFrame,
    file_name: str = "report.xlsx",
):
    """
    Write the Data Hub content report to an Excel spreadsheet.
    """
    with pd.ExcelWriter(file_name) as writer:
        study_labels.to_excel(writer, sheet_name="Labels", index=False)
        for classifier, counts in counts_by_classifier.items():
            counts.to_excel(writer, sheet_name=classifier, index=False)


def dump_report(counts, file_name="report.json"):
    """
    Write the Data Hub content report in JSON format.
    """
    with open(file_name, "w") as f:
        f.write(json.dumps(counts, indent=2))
