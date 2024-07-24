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

STATUS_KEYWORD = "STUDY STATUS"
PROGRAM_KEYWORD = "STUDY PROGRAM"
INSTITUTE_KEYWORD = "NIH INSTITUTE OR CENTER"
METHOD_KEYWORD = "DATA COLLECTION METHOD"
DESIGN_KEYWORD = "STUDY DESIGN"
POPULATION_KEYWORD = "ESTIMATED PARTICIPANTS"
DATATYPES_KEYWORD = "DATA TYPES"
DOMAIN_KEYWORD = "STUDY TOPICS"
PHS_KEYWORD = "STUDY PHS"
FOCUS_POPULATION_KEYWORD = "STUDY POPULATION FOCUS"
STUDY_STATUS = "STUDY STATUS"


class BasicParser:
    def __init__(self, hierarchy=None):
        self.hierarchy = hierarchy

    def prepare_string_for_matching(self, text: str):
        # remove non-alphabetic characters and convert to lowercase
        return re.sub(r"[^a-zA-Z]", "", text).casefold()

    def has_match(self, facet_node, text):
        if hasattr(facet_node, "synonyms"):
            for synonym in facet_node.synonyms:
                if self.prepare_string_for_matching(synonym) in text:
                    return True
        return self.prepare_string_for_matching(facet_node.label) in text

    def parse_program(self, row):
        """
        Parse program keyword (one) from DataFrame row.
        """
        program = self.prepare_string_for_matching(row[PROGRAM_KEYWORD])
        if pd.isna(program):
            program = None
        for dcc in PROGRAMS:
            if self.has_match(dcc, program):
                return dcc

    def parse_focus_populations(self, row):
        """
        Parse Study Focus Population keywords (many) from DataFrame row.
        """
        focus_population_text = row[FOCUS_POPULATION_KEYWORD]
        if pd.isna(focus_population_text):
            focus_populations = []
        else:
            focus_population_text = self.prepare_string_for_matching(
                focus_population_text
            )
            focus_populations = [
                focus
                for focus in FOCUS_POPULATIONS
                if self.has_match(focus, focus_population_text)
            ]
        return focus_populations

    def parse_nih_institutes(self, row):
        """
        Parse NIH Institutes keywords (many) from DataFrame row.
        """
        nih_institute_text = row[INSTITUTE_KEYWORD]
        if pd.isna(nih_institute_text):
            nih_institutes = []
        else:
            nih_institute_text = self.prepare_string_for_matching(nih_institute_text)
            nih_institutes = [
                institute
                for institute in INSTITUTES
                if self.has_match(institute, nih_institute_text)
            ]
        return nih_institutes

    def parse_collection_methods(self, row):
        """
        Parse collection method keywords (many) from DataFrame row.
        """
        collection_method_text = row[METHOD_KEYWORD]
        if pd.isna(collection_method_text):
            collection_methods = []
        else:
            collection_method_text = self.prepare_string_for_matching(
                collection_method_text
            )
            collection_methods = [
                method
                for method in COLLECTION_METHODS
                if self.has_match(method, collection_method_text)
                if method != CollectionMethod.OTHER
            ]
        return collection_methods

    def parse_study_designs(self, row):
        """
        Parse study design keywords (many) from DataFrame row.
        """
        study_design_text = row[DESIGN_KEYWORD]
        if pd.isna(study_design_text):
            study_designs = []
        else:
            study_design_text = self.prepare_string_for_matching(study_design_text)
            study_designs = [
                design
                for design in STUDY_DESIGNS
                if self.has_match(design, study_design_text)
                if design != StudyDesign.OTHER
            ]
        return study_designs

    def parse_population(self, row):
        """
        Parse data set sample size from DataFrame row and find the appropriate bin.
        """
        population_text = row[POPULATION_KEYWORD]
        if pd.isna(population_text):
            population = None
            population_range = None
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
                population_range = None
        else:
            population = int(population_text)
            population_range = [
                pop_range
                for pop_range in POPULATION_RANGES
                if pop_range.lower_bound <= population_text <= pop_range.upper_bound
            ].pop()
        return population, population_range

    def parse_data_types(self, row):
        """
        Parse data type keywords (multiple) from DataFrame row.
        """
        return []
        # data_type_text = row[DATATYPES_KEYWORD]
        # if pd.isna(data_type_text):
        #     data_types = []
        # else:
        #     data_type_text = self.prepare_string_for_matching(data_type_text)
        #     data_types = [
        #         data_type
        #         for data_type in DATA_TYPES
        #         if self.has_match(data_type, data_type_text)
        #         if data_type != DataType.OTHER
        #     ]
        # return data_types

    def parse_study_domains(self, row):
        """
        Parse study topics from DataFrame row. There can be multiple study topics.
        These are not coded terms in the study metadata dump, so we do our best here
        with case-insenstive string matching to a bank of StudyDomain keywords.
        """
        domain_text = row[DOMAIN_KEYWORD]
        study_domains = []
        if not pd.isna(domain_text):
            domain_text = self.prepare_string_for_matching(domain_text)
            study_domains = [
                topic for topic in STUDY_DOMAINS if self.has_match(topic, domain_text)
            ]
        return study_domains

    def parse_phs(self, row):
        """PHS ID"""
        return row[PHS_KEYWORD]

    def parse_status(self, row):
        return row[STATUS_KEYWORD]

    def parse_metadata_dataframe(self, metadata):
        """
        Each row of the DataFrame contains metadata attributes for the study.
        Process each row and index the study's metadata by its PHS ID.
        """
        studies = {}
        for i, row in metadata.iterrows():
            status = self.parse_status(row)
            if status != "Approved": # only log approved studies
                continue
            program = self.parse_program(row)
            nih_institutes = self.parse_nih_institutes(row)
            collection_methods = self.parse_collection_methods(row)
            study_designs = self.parse_study_designs(row)
            population, population_range = self.parse_population(row)
            data_types = self.parse_data_types(row)
            study_domains = self.parse_study_domains(row)
            focus_populations = self.parse_focus_populations(row)
            phs = self.parse_phs(row)

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
            )
            studies[phs] = study
        return studies
