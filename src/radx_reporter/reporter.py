import argparse
import pandas as pd
from .studies import meta_parser
from .studies import classifier
from .studies import report_writer

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
    args = parser.parse_args()

    dataframe = pd.read_excel(args.input, sheet_name="Database Export")
    studies = meta_parser.parse_metadata_file(dataframe)
    study_labels = classifier.label_studies(studies)
    studies_by_classifier = classifier.classify_studies(studies)
    counts = classifier.aggregate_counts(studies_by_classifier)
    report_writer.dump_report(counts, args.output)