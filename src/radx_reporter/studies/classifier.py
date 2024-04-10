from dataclasses import asdict, dataclass
from typing import Dict, List

import pandas as pd

from .study import Study
from .vocabulary import Classifier


def label_studies(studies: Dict[str, Study]):
    study_labels = {
        "phs": [],
        "Program": [],
        "Study Designs": [],
        "Data Types": [],
        "Collection Methods": [],
        "NIH Institutes": [],
        "Study Domains": [],
        "Population": [],
        "Population Range": [],
    }

    for key, study in studies.items():
        study_labels["Program"].append(study.program.label)
        study_labels["phs"].append(study.phs_id)
        study_labels["Study Designs"].append(
            "; ".join([design.label for design in study.study_designs]),
        )
        study_labels["Data Types"].append(
            "; ".join([data_type.label for data_type in study.data_types])
        )
        study_labels["Collection Methods"].append(
            "; ".join([method.label for method in study.collection_methods])
        )
        study_labels["NIH Institutes"].append(
            "; ".join([institute.label for institute in study.nih_institutes])
        )
        study_labels["Study Domains"].append(
            "; ".join([topic.label for topic in study.study_domains])
        )
        study_labels["Population"].append(study.population)
        study_labels["Population Range"].append(study.population_range.label)

    study_labels = pd.DataFrame(study_labels)
    return study_labels


def classify_studies(studies: List[Study]):
    studies_by_classifier = {}
    for classifier in Classifier:
        # check labels for each study and group study by label
        label_to_studies = {label: list() for label in classifier.classifier}
        for study in studies.values():
            for label in study.get_classifiers(classifier):
                label_to_studies[label].append(study)
        studies_by_classifier[classifier] = label_to_studies
    return studies_by_classifier


def aggregate_counts_to_dataframe(studies: List[Study]):
    total_count = len(studies)
    counts_by_classifier = {}
    for classifier in Classifier:
        label_counts = [
            (
                label,
                len(grouped_studies),
                "; ".join([study.phs_id for study in grouped_studies]),
            )
            for label, grouped_studies in studies[classifier].items()
        ]
        counts = pd.DataFrame(
            {
                classifier.label: [
                    x[0].label for x in label_counts
                ],  # these are the labels
                "Count": [x[1] for x in label_counts],
                "Percentage": [100 * x[1] / total_count for x in label_counts],
                "PHS IDs": [x[2] for x in label_counts],
            }
        )
        counts_by_classifier[classifier.label] = counts
    return counts_by_classifier


@dataclass
class Count:
    label: str
    url: str
    count: int
    studies: List[str]


def aggregate_counts(studies_by_classifier):
    aggregate_counts = {}
    for classifier in Classifier:
        counts = []
        for label, studies in studies_by_classifier[classifier].items():
            count = Count(
                label.label,
                label.url,
                len(studies),
                [study.phs_id for study in studies],
            )
            counts.append(asdict(count))
        aggregate_counts[classifier.label] = counts
    return aggregate_counts
