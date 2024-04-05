import pandas as pd

def dump_report(study_labels, counts_by_classifier, file_name="report.xlsx"):
    with pd.ExcelWriter("report.xlsx") as writer:
        study_labels.to_excel(writer, sheet_name="Labels", index=False)
        for classifier, counts in counts_by_classifier.items():
            counts.to_excel(writer, sheet_name=classifier, index=False)