import json

import pandas as pd

COLUMN_SIZES = {
    "Info": [10, 10, 25, 10],
    "Labels": [10, 10, 15, 15, 18, 15, 15, 25, 20, 20],
    "Program": [10, 7, 10, 12],
    "Study Design": [23, 7, 10, 12],
    "Data Type": [22, 7, 10, 12],
    "Collection Method": [44, 7, 10, 12],
    "NIH Institute": [15, 7, 10, 12],
    "Study Domain": [45, 7, 10, 12],
    "Population Range": [20, 7, 10, 12],
    "Study Focus Population": [55, 7, 10, 12],
}

INFO_TEXT = [
    ("B2", "This workbook collects statistics on studies stored in the RADx Data Hub and provides information on the number of studies corresponding to labels on the studies."),
    ("B5", "Workbook objectives:"),
    ("C6", "Provide an overview of the metadata labels applied to each study to inform users as the content that is available on the Data Hub."),
    ("C7", "Provide statistics on the studies that belong to each label."),
    ("B9", "Information provided by each sheet:"),
    ("C10", "Charts"),
    ("D10", "This sheet graphically summarizes statistics of study count per label for the most popular labels."),
    ("C11", "Labels"),
    ("D11", "This sheet shows lists each study by PHS ID and all of the metadata labels that have been applied to it."),
    ("C12", "Program"),
    ("D12", "This sheet lists each RADx program and reports the number of studies belonging to each RADx program."),
    ("C13", "Study Design"),
    ("D13", "This sheet lists different study designs that characterize RADx studies and reports the number of studies that feature each study design."),
    ("C14", "Data Type"),
    ("D14", "This sheet lists different data types that characterize RADx studies and reports the number of studies that report data of that type."),
    ("C15", "Collection Method"),
    ("D15", "This sheet lists different collection methods used to generate the study data and reports the number of studies that use each collection method."),
    ("C16", "NIH Institute"),
    ("D16", "This sheet lists the different NIH institutes that supported RADx studies and reports the number of studies that were supported by each institute."),
    ("C17", "Study Domain"),
    ("D17", "This sheet lists the different study domains that characterize studies in the RADx Data Hub and reports the number of studies that belong to each study domain."),
    ("C18", "Population Range"),
    ("D18", "This sheet lists several population (sample size) ranges to characterize the size of each study and reports the number of studies whose size falls into each range."),
    ("C19", "Study Focus Population"),
    ("D19", "This sheet lists the demographic groups targeted by RADx studies and reports the number of studies that focus on each population group."),
    # ("B20", "Column descriptions:"),
    # ("C21", "Count"),
    # ("D21", "This column gives the number of studies labeled by each term."),
    # ("C22", "Coded Term"),
    # ("D22", "This column in each of the 8 sheets denotes whether a term is an original term drawn for labels on studies in the Data Hub (TRUE) or if it is a term introduced by semantic relationships described by the RADx Study Analysis Vocabulary."),
    # ("C23", "PHS IDs"),
    # ("D23", "This column gives the PHS IDs for studies labeled by each term."),
    # ("C24", "Program"),
    # ("D24", "The Program column in the Program sheet contains each Data Collection Center responsible for providing data to the RADx Data Hub."),
    # ("C25", "Study Design"),
    # ("D25", "The Study Design column in the Study Design sheet contains each Study Design term as provided by the RADx Study Analysis Vocabulary"),
    # ("C26", "Data Type"),
    # ("D26", "The Data Type column in the Data Type sheet contains each Data Type term as provided by the RADx Study Analysis Vocabulary."),
    # ("C27", "Collection Method"),
    # ("D27", "The Collection Method column in the Collection Method sheet contains each Collection Method term as provided by the RADx Study Analysis Vocabulary."),
    # ("C28", "NIH Institute"),
    # ("D28", "The NIH Institute column in the NIH Institute sheet contains each NIH Institute used to label studies in the RADx Data Hub."),
    # ("C29", "Study Domain"),
    # ("D29", "The Study Domain column in the Study Domain sheet contains each Study Domain term as provided by the RADx Study Analysis Vocabulary."),
    # ("C30", "Population Range"),
    # ("D30", "The Population Range column in the Population Range sheet contains each Population Range used to label studies in the RADx Data Hub."),
    # ("C31", "Study Focus Population"),
    # ("D31", "The Study Focus Population column in the Study Focus Population sheet contains each Study Focus Population term as provided by the RADx Study Analysis Vocabulary."),
]


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
    dump_auxiliary_terms: bool = False,
    date = None,
):
    """
    Write the Data Hub content report to an Excel spreadsheet.
    """
    with pd.ExcelWriter(file_name, engine="xlsxwriter") as writer:
        workbook = writer.book
        # informational sheet
        info_sheet_name = "Info"
        worksheet_info = workbook.add_worksheet(info_sheet_name)
        writer.sheets[info_sheet_name] = worksheet_info
        for location, text in INFO_TEXT:
            worksheet_info.write(location, text)
        # write date. this cannot be automated as long as reports are generated manually
        worksheet_info.write("B3", f"Current as of {date}")
        autosize_columns(writer, study_labels, "Info")

        # sheet with all of the graphs
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
        percent_format = workbook.add_format({"num_format": "0.00%"})

        # write page with labels
        study_labels.to_excel(writer, sheet_name="Labels", index=False)
        autosize_columns(writer, study_labels, "Labels")
        for classifier, counts in counts_by_classifier.items():
            if dump_auxiliary_terms:
                counts = counts[counts["Coded Term"] == True]
                counts = counts.drop(columns = ["Coded Term"])
            # insert tabular data in reverse sorted order by counts
            counts.to_excel(writer, sheet_name=classifier, index=False)
            count_sheet = writer.sheets[classifier]
            # convert float to percentage in percentage column
            for row_num, value in enumerate(counts["Percentage"], start=1):
                count_sheet.write_number(row_num, 2, value, percent_format)
            autosize_columns(writer, counts, classifier)
            apply_hyperlink_format(writer.sheets[classifier], counts, hyperlink_format)

            # insert a hidden sheet with the top n labels in sorted order
            # this is required because xlsxwriter bar charts plot from
            # bottom to top for whatever reason with no way to reverse a 
            # plotting range, so the vertical ordering won't match the tabular data
            hidden_sheet_name = "hidden" + classifier
            # remove auxiliary terms from plotting
            if not dump_auxiliary_terms:
                coded_counts = counts[counts["Coded Term"] == True]
            else:
                coded_counts = counts

            # create a bar chart consisting of the top n labels
            n_labels = min(label_limit, len(coded_counts))

            ranked_counts = coded_counts.nlargest(n_labels, columns=["Count"])
            ranked_counts = ranked_counts.iloc[::-1]
            ranked_counts.to_excel(writer, sheet_name=hidden_sheet_name, index=False)
            hidden_sheet = writer.sheets[hidden_sheet_name]
            hidden_sheet.hide()

            chart = workbook.add_chart({"type": "bar"})
            if classifier == "Program":
                chart_title = "Program"
            else:
                chart_title = f"Top {classifier} Labels"
            chart.add_series(
                {
                    "name": chart_title,
                    "categories": [hidden_sheet_name, 1, 0, n_labels, 0],
                    "values": [hidden_sheet_name, 1, 1, n_labels, 1],
                }
            )
            chart.set_x_axis({"name": "Study Counts"})
            chart.set_legend({"none": True})
            chart_position = chart_positions.pop()
            charts_sheet.insert_chart(chart_position, chart)


def dump_report(counts, file_name="report.json"):
    """
    Write the Data Hub content report in JSON format.
    """
    with open(file_name, "w") as f:
        f.write(json.dumps(counts, indent=2))
