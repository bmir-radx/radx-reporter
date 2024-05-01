import argparse

import pandas as pd

from .basic import classifier, meta_parser, report_writer


def study_metadata_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Path to the metadata file to process.",
    )
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        help="Path to save the report output.",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["json", "xlsx"],
        default="json",
        help="Output format (json or xlsx)",
    )
    parser.add_argument(
        "--sheet",
        "-s",
        default="Database Export",
        required=False,
        help="Name of the sheet in the input to read."
    )
    args = parser.parse_args()

    dataframe = pd.read_excel(args.input, sheet_name=args.sheet, skiprows=1)
    studies = meta_parser.parse_metadata_dataframe(dataframe)
    study_labels = classifier.label_studies(studies)
    studies_by_classifier = classifier.classify_studies(studies)
    counts = classifier.aggregate_counts(studies_by_classifier)

    if args.format == "json":
        report_writer.dump_report(counts, args.output)
    elif args.format == "xlsx":
        report_writer.dump_report_spreadsheet(
            study_labels,
            classifier.aggregate_counts_to_dataframe(studies_by_classifier),
            args.output,
        )
