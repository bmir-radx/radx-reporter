import re

import dateutil
import pandas as pd
import logging

from .study import Study, AdditionalProperty
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
    StudyDesign,
)
from .keywords import Keyword

logger = logging.getLogger(__name__)

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
        program = self.prepare_string_for_matching(row[Keyword.PROGRAM.value])
        if pd.isna(program):
            program = None
        for dcc in PROGRAMS:
            if self.has_match(dcc, program):
                return dcc

    def parse_focus_populations(self, row):
        """
        Parse Study Focus Population keywords (many) from DataFrame row.
        """
        focus_population_text = row[Keyword.FOCUSPOPULATION.value]
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
        nih_institute_text = row[Keyword.INSTITUTE.value]
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
        collection_method_text = row[Keyword.METHOD.value]
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
        study_design_text = row[Keyword.DESIGN.value]
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
        population_text = row[Keyword.COHORTSIZE.value]
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
        data_type_text = row[Keyword.DATATYPES.value]
        if pd.isna(data_type_text):
            data_types = []
        else:
            data_type_text = self.prepare_string_for_matching(data_type_text)
            data_types = [
                data_type
                for data_type in DATA_TYPES
                if self.has_match(data_type, data_type_text)
                if data_type != DataType.OTHER
            ]
        return data_types

    def parse_study_domains(self, row):
        """
        Parse study topics from DataFrame row. There can be multiple study topics.
        These are not coded terms in the study metadata dump, so we do our best here
        with case-insenstive string matching to a bank of StudyDomain keywords.
        """
        domain_text = row[Keyword.DOMAIN.value]
        study_domains = []
        if not pd.isna(domain_text):
            domain_text = self.prepare_string_for_matching(domain_text)
            study_domains = [
                topic for topic in STUDY_DOMAINS if self.has_match(topic, domain_text)
            ]
        return study_domains

    def parse_phs(self, row):
        """PHS ID"""
        return row[Keyword.PHS.value]

    def parse_status(self, row):
        return row[Keyword.STATUS.value]

    def parse_additional_properties(self, row, properties):
        additional_properties = []
        for name in properties:
            additional_properties.append(
                AdditionalProperty(name, row.get(name, None))
            )
        return additional_properties

    def prune_additional_properties(self, dataframe, properties):
        """
        Remove additional properties that do not correspond to column names
        in the dataframe. Also remove additional properties that are redundant
        with the required columns.
        """
        pruned = []
        column_names = set(dataframe.columns.tolist())
        required = {kw.value for kw in Keyword}
        for prop in properties:
            if prop in required:
                continue
            if prop not in column_names:
                logger.warning(f"{prop} does not match a column in the dataframe. Ignoring it.")
                continue
            pruned.append(prop)
        return pruned

    def parse_metadata_dataframe(self, metadata, properties):
        """
        Each row of the DataFrame contains metadata attributes for the study.
        Process each row and index the study's metadata by its PHS ID.
        """
        properties = self.prune_additional_properties(metadata, properties)
        columns_to_parse = [kw.value for kw in Keyword] + properties
        logger.info(f"Parsing dataframe columns: {columns_to_parse}")
        studies = {}
        for _, row in metadata.iterrows():
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
            if properties:
                additional_properties = self.parse_additional_properties(row, properties)
            else:
                additional_properties = []

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
                additional_properties=additional_properties,
                doi=None,
            )
            studies[phs] = study
        return studies
