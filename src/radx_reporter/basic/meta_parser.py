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


PROGRAM_KEYWORD = "contribution"
INSTITUTE_KEYWORD = "institutes_supporting_study - CODED"
METHOD_KEYWORD = "source - CODED"
DESIGN_KEYWORD = "types - CODED"
POPULATION_KEYWORD = "estimated_participants"
DATATYPES_KEYWORD = "data_general_types.1"
SUBJECT_KEYWORD = "subject"
DESCRIPTION_KEYWORD = "description"
PHS_KEYWORD = "phs"
STUDY_START_DATE = "studystartdate"
STUDY_END_DATE = "studyenddate"
FOCUS_POPULATION_KEYWORD = "Study Population Focus"


def parse_program(row):
    """
    Parse program keyword (one) from DataFrame row.
    """
    program = row[PROGRAM_KEYWORD]
    if pd.isna(program):
        program = Program.MISSING
    else:
        program = PROGRAMS[program]
    return program


def parse_focus_populations(row):
    """
    Parse Study Focus Population keywords (many) from DataFrame row.
    """
    focus_population_text = row[FOCUS_POPULATION_KEYWORD]
    if pd.isna(focus_population_text):
        focus_populations = [FocusPopulation.MISSING]
    else:
        focus_populations = [
            focus
            for focus in FOCUS_POPULATIONS
            if focus.label in focus_population_text
        ]
        if len(focus_populations) == 0:
            focus_populations.append(FocusPopulation.MISSING)
    return focus_populations


def parse_nih_institutes(row):
    """
    Parse NIH Institutes keywords (many) from DataFrame row.
    """
    nih_institute_text = row[INSTITUTE_KEYWORD]
    if pd.isna(nih_institute_text):
        nih_institutes = [NihInstitute.MISSING]
    else:
        nih_institutes = [
            institute
            for institute in INSTITUTES
            if institute.label in nih_institute_text
        ]
        if len(nih_institutes) == 0:
            nih_institutes.append(NihInstitute.MISSING)
    return nih_institutes


def parse_collection_methods(row):
    """
    Parse collection method keywords (many) from DataFrame row.
    """
    collection_method_text = row[METHOD_KEYWORD]
    if pd.isna(collection_method_text):
        collection_methods = [CollectionMethod.MISSING]
    else:
        collection_methods = [
            method
            for method in COLLECTION_METHODS
            if method.label in collection_method_text
        ]
        if len(collection_methods) == 0:
            collection_methods.append(CollectionMethod.MISSING)
    return collection_methods


def parse_study_designs(row):
    """
    Parse study design keywords (many) from DataFrame row.
    """
    study_design_text = row[DESIGN_KEYWORD]
    if pd.isna(study_design_text):
        study_designs = [StudyDesign.MISSING]
    else:
        study_designs = [
            design for design in STUDY_DESIGNS if design.label in study_design_text
        ]
        if len(study_designs) == 0:
            study_designs.append(StudyDesign.MISSING)
    return study_designs


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
        data_types = [DataType.MISSING]
    else:
        data_types = [
            data_type for data_type in DATA_TYPES if data_type.label in data_type_text
        ]
        if len(data_types) == 0:
            data_types.append(DataType.MISSING)
    return data_types


def parse_study_domains(row):
    """
    Parse study topics from DataFrame row. There can be multiple study topics.
    These are not coded terms in the study metadata dump, so we do our best here
    with case-insenstive string matching to a bank of StudyDomain keywords.
    """
    subject_text = row[SUBJECT_KEYWORD]
    description_text = row[DESCRIPTION_KEYWORD]
    if pd.isna(subject_text):
        subject_text = ""
    if pd.isna(description_text):
        description_text = ""
    study_topic_text = subject_text.lower() + description_text.lower()
    study_domains = [
        topic for topic in STUDY_DOMAINS if topic.label.lower() in study_topic_text
    ]
    if len(study_domains) == 0:
        study_domains.append(StudyDomain.MISSING)
    return study_domains


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
        start_date, end_date = parse_dates(row)
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
            start_date=start_date,
            end_date=end_date,
        )

        studies[phs] = study
    return studies
