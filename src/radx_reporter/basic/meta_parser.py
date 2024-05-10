import re

import dateutil
import pandas as pd

from .study import Study
from .vocabulary import (
    COLLECTION_METHODS,
    DATA_TYPES,
    FOCUS_POPULATIONS,
    INSTITUTES,
    POPULATION_RANGES,
    PROGRAMS,
    STUDY_DESIGNS,
    STUDY_DOMAINS,
    CollectionMethod,
    DataType,
    FocusPopulation,
    NihInstitute,
    PopulationRange,
    Program,
    StudyDesign,
    StudyDomain,
)
from .hierarchy import (
    FOCUS_POPULATION_HIERARCHY,
    STUDY_DESIGN_HIERARCHY,
    STUDY_DOMAIN_HIERARCHY,
    COLLECTION_METHOD_HIERARCHY,
    DATA_TYPE_HIERARCHY,
)


PROGRAM_KEYWORD = "DCC"
INSTITUTE_KEYWORD = "institutes_supporting_study - CODED"
METHOD_KEYWORDS = ["Data Collection Method", "Data Collection Method Other Specify"]
DESIGN_KEYWORD = "Study Design, Coded"
POPULATION_KEYWORD = "Estimated Participants - Cleaned"
DATATYPES_KEYWORD = "data_general_types - CODED"
DOMAIN_KEYWORDS = [
    "Keywords - Raw",
    "Keywords - Cleaned",
    "Study Domain",
    "Study Domain, Other",
    "Description",
]
PHS_KEYWORD = "phs"
STUDY_START_DATE = "NIH RePORTER Project Start Date"
STUDY_END_DATE = "NIH RePORTER Project End Date"
FOCUS_POPULATION_KEYWORD = "Study Population Focus"


def prepare_string_for_matching(text: str):
    # remove non-alphabetic characters and convert to lowercase
    return re.sub(r"[^a-zA-Z]", "", text).casefold()


def has_match(facet_node, text):
    if not (isinstance(facet_node, NihInstitute) or isinstance(facet_node, Program)):
        for synonym in facet_node.synonyms:
            if prepare_string_for_matching(synonym) in text:
                return True
    return prepare_string_for_matching(facet_node.label) in text


def add_node_and_ancestors(vocabulary_node, node_set):
    while vocabulary_node is not None:
        node_set.add(vocabulary_node)
        vocabulary_node = vocabulary_node.parent


def parse_program(row):
    """
    Parse program keyword (one) from DataFrame row.
    """
    program = prepare_string_for_matching(row[PROGRAM_KEYWORD])
    if pd.isna(program):
        program = Program.UNKNOWN
    for dcc in PROGRAMS:
        if has_match(dcc, program):
            return dcc


def parse_focus_populations(row):
    """
    Parse Study Focus Population keywords (many) from DataFrame row.
    """
    focus_population_text = row[FOCUS_POPULATION_KEYWORD]
    if pd.isna(focus_population_text):
        focus_populations = [FOCUS_POPULATION_HIERARCHY["UNKNOWN OR INVALID"]]
    else:
        focus_population_text = prepare_string_for_matching(focus_population_text)
        focus_populations = [
            focus for focus in FOCUS_POPULATION_HIERARCHY.values() if has_match(focus, focus_population_text)
        ]
        if len(focus_populations) == 0:
            focus_populations.append(FOCUS_POPULATION_HIERARCHY["UNKNOWN OR INVALID"])
    semantic_focus_populations = set()
    for focus in focus_populations:
        add_node_and_ancestors(focus, semantic_focus_populations)
    return semantic_focus_populations


def parse_nih_institutes(row):
    """
    Parse NIH Institutes keywords (many) from DataFrame row.
    """
    nih_institute_text = row[INSTITUTE_KEYWORD]
    if pd.isna(nih_institute_text):
        nih_institutes = [NihInstitute.UNKNOWN]
    else:
        nih_institute_text = prepare_string_for_matching(nih_institute_text)
        nih_institutes = [
            institute
            for institute in INSTITUTES
            if has_match(institute, nih_institute_text)
        ]
        if len(nih_institutes) == 0:
            nih_institutes.append(NihInstitute.UNKNOWN)
    return nih_institutes


def parse_collection_methods(row):
    """
    Parse collection method keywords (many) from DataFrame row.
    """
    collection_method_text = "".join(
        [row[x] for x in METHOD_KEYWORDS if not pd.isna(row[x])]
    )
    collection_method_text = prepare_string_for_matching(collection_method_text)
    collection_methods = [
        method
        for method in COLLECTION_METHOD_HIERARCHY.values()
        if has_match(method, collection_method_text)
    ]
    if len(collection_methods) == 0:
        collection_methods.append(COLLECTION_METHOD_HIERARCHY["UNKNOWN OR INVALID"])
    semantic_collection_methods = set()
    for method in collection_methods:
        add_node_and_ancestors(method, semantic_collection_methods)
    return semantic_collection_methods


def parse_study_designs(row):
    """
    Parse study design keywords (many) from DataFrame row.
    """
    study_design_text = row[DESIGN_KEYWORD]
    if pd.isna(study_design_text):
        study_designs = [STUDY_DESIGN_HIERARCHY["UNKNOWN OR INVALID"]]
    else:
        study_design_text = prepare_string_for_matching(study_design_text)
        study_designs = [
            design for design in STUDY_DESIGN_HIERARCHY.values() if has_match(design, study_design_text)
        ]
        if len(study_designs) == 0:
            study_designs.append(STUDY_DESIGN_HIERARCHY["UNKNOWN OR INVALID"])
    semantic_study_designs = set()
    for design in study_designs:
        add_node_and_ancestors(design, semantic_study_designs)
    return semantic_study_designs


def parse_population(row):
    """
    Parse data set sample size from DataFrame row and find the appropriate bin.
    """
    population_text = row[POPULATION_KEYWORD]
    if pd.isna(population_text):
        population = None
        population_range = PopulationRange.UNKNOWN
    elif isinstance(population_text, str):
        match = re.search(r"\b\d+\b", population_text)
        if match:
            population = int(match.group())
            population_range = [
                pop_range
                for pop_range in POPULATION_RANGES
                if pop_range.lower_bound <= population <= pop_range.upper_bound
            ].pop()
        else:
            population = None
            population_range = PopulationRange.UNKNOWN
    else:
        population = int(population_text)
        population_range = [
            pop_range
            for pop_range in POPULATION_RANGES
            if pop_range.lower_bound <= population_text <= pop_range.upper_bound
        ].pop()
    return population, population_range


def parse_data_types(row):
    """
    Parse data type keywords (multiple) from DataFrame row.
    """
    data_type_text = row[DATATYPES_KEYWORD]
    if pd.isna(data_type_text):
        data_types = [DATA_TYPE_HIERARCHY["UNKNOWN OR INVALID"]]
    else:
        data_type_text = prepare_string_for_matching(data_type_text)
        data_types = [
            data_type for data_type in DATA_TYPE_HIERARCHY.values() if has_match(data_type, data_type_text)
        ]
        if len(data_types) == 0:
            data_types.append(DATA_TYPE_HIERARCHY["UNKNOWN OR INVALID"])
    semantic_data_types = set()
    for data_type in data_types:
        add_node_and_ancestors(data_type, semantic_data_types)
    return semantic_data_types


def parse_study_domains(row):
    """
    Parse study topics from DataFrame row. There can be multiple study topics.
    These are not coded terms in the study metadata dump, so we do our best here
    with case-insenstive string matching to a bank of StudyDomain keywords.
    """
    domain_text = "".join(str(row[x]) for x in DOMAIN_KEYWORDS)
    study_domains = []
    if pd.isna(domain_text):
        study_domains.append(STUDY_DOMAIN_HIERARCHY["UNKNOWN OR INVALID"])
    else:
        domain_text = prepare_string_for_matching(domain_text)
        study_domains = [
            topic for topic in STUDY_DOMAIN_HIERARCHY.values() if has_match(topic, domain_text)
        ]
    semantic_study_domains = set()
    for topic in study_domains:
        add_node_and_ancestors(topic, semantic_study_domains)
    return semantic_study_domains


def parse_dates(row):
    """
    Parse start and end dates for the studies with format:
    date_format = "%Y-%m-%d %H:%M:%S%z"
    """
    start_date = row[STUDY_START_DATE]
    end_date = row[STUDY_END_DATE]
    if pd.isna(start_date):
        start_date = None
    else:
        start_date = dateutil.parser.parse(start_date)
    if pd.isna(end_date):
        end_date = None
    else:
        end_date = dateutil.parser.parse(end_date)
    return start_date, end_date


def parse_phs(row):
    """PHS ID"""
    return row[PHS_KEYWORD]


def parse_metadata_dataframe(metadata):
    """
    Each row of the DataFrame contains metadata attributes for the study.
    Process each row and index the study's metadata by its PHS ID.
    """
    studies = {}
    for i, row in metadata.iterrows():
        program = parse_program(row)
        nih_institutes = parse_nih_institutes(row)
        collection_methods = parse_collection_methods(row)
        study_designs = parse_study_designs(row)
        population, population_range = parse_population(row)
        data_types = parse_data_types(row)
        study_domains = parse_study_domains(row)
        focus_populations = parse_focus_populations(row)
        # start_date, end_date = parse_dates(row)
        phs = parse_phs(row)

        study = Study(
            bundles=None,
            contributors=None,
            program=program,
            phs_id=phs,
            study_designs=study_designs,
            data_types=data_types,
            collection_methods=collection_methods,
            nih_institutes=nih_institutes,
            study_domains=study_domains,
            population=population,
            population_range=population_range,
            focus_populations=focus_populations,
            doi=None,
            # start_date=start_date,
            # end_date=end_date,
        )

        studies[phs] = study
    return studies
