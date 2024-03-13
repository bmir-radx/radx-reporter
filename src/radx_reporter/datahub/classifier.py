import pandas as pd
import matplotlib.pyplot as plt

from study import Classifier, Study
from typing import Dict, List

def classify_studies(studies: List[Study]):
    """
    Assign studies to its classifier.
    """
    studies_by_classifier = {}
    for classifier in Classifier:
        # check labels for each study and group study by label
        label_to_studies = {label: list() for label in classifier.classifier}
        for study in studies.values():
            for label in study.get_classifiers(classifier):
                label_to_studies[label].append(study)
        studies_by_classifier[classifier] = label_to_studies
    return studies_by_classifier

def count_studies_by_classifier(studies: List[Study], studies_by_classifier: Dict[Classifier, List[Study]]):
    total_count = len(studies)
    counts_by_classifier = {}
    for classifier in Classifier:
        label_counts = [(label, len(grouped_studies), "; ".join([study.phs_id for study in grouped_studies])) for label, grouped_studies in studies_by_classifier[classifier].items()]
        counts = pd.DataFrame({
            classifier.label: [x[0].label for x in label_counts], # these are the labels
            "Count": [x[1] for x in label_counts],
            "Percentage": [100 * x[1] / total_count for x in label_counts],
            "PHS IDs": [x[2] for x in label_counts]
        })
        counts_by_classifier[classifier.label] = counts
    return counts_by_classifier

def label_studies(studies):
    """
    Label studies by their classifiers.
    """
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
        study_labels["Study Designs"].append("; ".join([design.label for design in study.study_designs]),)
        study_labels["Data Types"].append("; ".join([data_type.label for data_type in study.data_types]))
        study_labels["Collection Methods"].append("; ".join([method.label for method in study.collection_methods]))
        study_labels["NIH Institutes"].append("; ".join([institute.label for institute in study.nih_institutes]))
        study_labels["Study Domains"].append("; ".join([topic.label for topic in study.study_domains]))
        study_labels["Population"].append(study.population)
        study_labels["Population Range"].append(study.population_range.label)

    study_labels = pd.DataFrame(study_labels)
    return study_labels

def classified_studies_to_excel(study_labels: Dict[str, List[str]], counts_by_classifier: Dict[Classifier, int], file_name="report.xlxs"):
    with pd.ExcelWriter(file_name) as writer:
        study_labels.to_excel(writer, sheet_name="Labels", index=False)
        for classifier, counts in counts_by_classifier.items():
            counts.to_excel(writer, sheet_name=classifier, index=False)

def plot_bar_chart(studies_by_classifier: Dict[Classifier, List[Study]], file_name="labels.pdf"):
    bar_chart_data = {}
    for classifier in Classifier:
        label_counts = [(label, len(grouped_studies)) for label, grouped_studies in studies_by_classifier[classifier].items()]
        labels = [x[0].label for x in label_counts]
        counts = [x[1] for x in label_counts]
        bar_chart_data[classifier.label] = (labels, counts)

    fig, axs = plt.subplots(1, 7, figsize=(64, 8))
    for i, (title, (labels, counts)) in enumerate(bar_chart_data.items()):
        axs[i].bar(labels, counts)
        axs[i].set_title(title)
        axs[i].set_ylabel("Counts")
        axs[i].set_xticklabels(labels, rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig(file_name)
