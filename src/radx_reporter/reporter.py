import argparse
import dateutil
import os
import time

import dateutil.parser
import pandas as pd

from .basic import classifier, report_writer
from .basic.meta_parser import MetaParser
from .basic.basic_parser import BasicParser
from .basic.ontology import Ontology


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
        required=False,
        help="Path to save the report output.",
    )
    # parser.add_argument(
    #     "--format",
    #     "-f",
    #     choices=["json", "xlsx"],
    #     default="json",
    #     help="Output format (json or xlsx)",
    # )
    parser.add_argument(
        "--sheet",
        "-s",
        default="Database Export",
        required=False,
        help="Name of the sheet in the input to read.",
    )
    parser.add_argument(
        "--date",
        "-d",
        default=None,
        required=False,
        help="Date until which the report is current.",
    )
    args = parser.parse_args()

    # preprocess the date
    date = args.date
    try:
        date = dateutil.parser(args.date)
    except:
        date = args.date

    labels_tsv = os.path.join(os.path.dirname(__file__), "data/content-ontology", "labels.tsv")
    alt_labels_tsv = os.path.join(
        os.path.dirname(__file__), "data/content-ontology", "altLabels.tsv"
    )
    hierarchy_tsv = os.path.join(
        os.path.dirname(__file__), "data/content-ontology", "hierarchy.tsv"
    )
    aux_terms_tsv = os.path.join(os.path.dirname(__file__), "data/content-ontology", "auxiliaryTerms.tsv")
    ontology = Ontology(
        labels_tsv, aux_terms_tsv, alt_labels_tsv, hierarchy_tsv
    )

    dataframe = pd.read_excel(args.input, sheet_name=args.sheet)


    # without ontology
    Reporter.basic_report(dataframe, date=date)
    
    # with ontology
    # Reporter.semantic_report(dataframe, ontology, date=date)


class Reporter:
    @classmethod
    def basic_report(cls, dataframe, file_name="radx-content-report", date=None):
        if date is None:
            date = time.strftime("%Y-%m-%d")

        meta_parser = BasicParser()
        studies = meta_parser.parse_metadata_dataframe(dataframe)
        study_labels = classifier.label_studies(studies)
        studies_by_classifier = classifier.classify_studies(studies)
        counts = classifier.aggregate_counts(studies_by_classifier)

        report_writer.dump_report_spreadsheet(
            study_labels,
            classifier.aggregate_counts_to_dataframe(studies_by_classifier, len(studies)),
            file_name + ".xlsx",
            dump_auxiliary_terms=True,
            date=date,
        )

    @classmethod
    def semantic_report(cls, dataframe, ontology, file_name="radx-semantic-content-report", date=None):
        if date is None:
            date = time.strftime("%Y-%m-%d")

        meta_parser = MetaParser(ontology)
        studies = meta_parser.parse_metadata_dataframe(dataframe)
        study_labels = classifier.label_studies(studies)
        studies_by_classifier = classifier.classify_studies(studies)
        counts = classifier.aggregate_counts(studies_by_classifier)

        report_writer.dump_report_spreadsheet(
            study_labels,
            classifier.aggregate_counts_to_dataframe(studies_by_classifier, len(studies)),
            file_name + ".xlsx",
            date=date,
        )
