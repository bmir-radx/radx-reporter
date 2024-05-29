import json

import pandas as pd

COLUMN_SIZES = {
    "Labels": [10, 10, 15, 15, 18, 15, 15, 12, 19],
    "Program": [10, 7, 12],
    "Study Design": [23, 7, 12],
    "Data Type": [22, 7, 12],
    "Collection Method": [44, 7, 12],
    "NIH Institute": [15, 7, 12],
    "Study Domain": [45, 7, 12],
    "Population Range": [20, 7, 12],
    "Study Focus Population": [55, 7, 12],
}


def autosize_columns(writer, df, sheet_name):
    worksheet = writer.sheets[sheet_name]
    sizes = COLUMN_SIZES[sheet_name]
    for i, size in enumerate(sizes):
        worksheet.set_column(i, i, size)


def apply_hyperlink_format(worksheet, df, hyperlink_format):
    """Make hyperlinks blue and underlined."""
    for col_num, col_name in enumerate(df.columns):
        for row_num, value in enumerate(df[col_name], start=1):
            if isinstance(value, str) and value.startswith("=HYPERLINK"):
                worksheet.write_formula(row_num, col_num, value, hyperlink_format)


def dump_report_spreadsheet(
    study_labels: pd.DataFrame,
    counts_by_classifier: pd.DataFrame,
    file_name: str = "report.xlsx",
    label_limit: int = 10,
):
    """
    Write the Data Hub content report to an Excel spreadsheet.
    """
    with pd.ExcelWriter(file_name, engine="xlsxwriter") as writer:
        workbook = writer.book
        charts_sheet_name = "Charts"
        charts_sheet = workbook.add_worksheet(charts_sheet_name)
        writer.sheets[charts_sheet_name] = charts_sheet
        chart_positions = [
            "A1",
            "I1",
            "A16",
            "I16",
            "A31",
            "I31",
            "A46",
            "I46",
            "A61",
            "I61",
        ]
        chart_positions.reverse()

        # make hyperlinks blue and underlined
        hyperlink_format = workbook.add_format({"font_color": "blue", "underline": 1})

        # write page with labels
        study_labels.to_excel(writer, sheet_name="Labels", index=False)
        autosize_columns(writer, study_labels, "Labels")
        for classifier, counts in counts_by_classifier.items():
            counts.to_excel(writer, sheet_name=classifier, index=False)
            autosize_columns(writer, counts, classifier)
            apply_hyperlink_format(writer.sheets[classifier], counts, hyperlink_format)

            # create a bar chart consisting of the top n labels
            n_labels = min(label_limit, len(counts))

            worksheet = writer.sheets[classifier]
            chart = workbook.add_chart({"type": "bar"})
            chart.add_series(
                {
                    "name": f"Top {classifier} labels",
                    "categories": [classifier, 1, 0, n_labels, 0],
                    "values": [classifier, 1, 1, n_labels, 1],
                    # "categories": top_labels[classifier].tolist(),
                    # "values":     top_labels["Count"].tolist(),
                }
            )
            chart_position = chart_positions.pop()
            charts_sheet.insert_chart(chart_position, chart)


def dump_report(counts, file_name="report.json"):
    """
    Write the Data Hub content report in JSON format.
    """
    with open(file_name, "w") as f:
        f.write(json.dumps(counts, indent=2))
