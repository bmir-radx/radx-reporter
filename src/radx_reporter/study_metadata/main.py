import pandas as pd
from meta_parser import parse_metadata_file
from classifier import classify_studies, aggregate_counts, label_studies
from json_writer import dump_report

if __name__ == "__main__":
    df = pd.read_excel("RADx Study Metadata_Working Version.xlsx", sheet_name="Database Export")
    studies = parse_metadata_file(df)
    study_labels = label_studies(studies)
    studies_by_classifier = classify_studies(studies)
    counts = aggregate_counts(studies_by_classifier)
    dump_report(counts, "report.json")