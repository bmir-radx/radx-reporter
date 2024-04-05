import dateutil
import pandas as pd
from study import Study
from vocabulary import (
    Program, StudyDesign, StudyDomain, DataType, CollectionMethod, NihInstitute, PopulationRange,
    INSTITUTES, STUDY_DESIGNS, POPULATION_RANGES, DATA_TYPES, STUDY_DOMAINS, COLLECTION_METHODS
)

def parse_program(row):
    program = row["contribution"]
    if pd.isna(program):
        program = Program.MISSING
    else:
        program = Program(program)
    return program

def parse_nih_institutes(row):
    nih_institute_text = row["institutes_supporting_study - CODED"]
    if pd.isna(nih_institute_text):
        nih_institutes = [NihInstitute.MISSING]
    else:
        nih_institutes = [institute for institute in INSTITUTES if institute.label in nih_institute_text]
        if len(nih_institutes) == 0:
            nih_institutes.append(NihInstitute.MISSING)
    return nih_institutes

def parse_collection_methods(row):
    collection_method_text = row["source - CODED"]
    if pd.isna(collection_method_text):
        collection_methods = [CollectionMethod.MISSING]
    else:
        collection_methods = [method for method in COLLECTION_METHODS if method.label in collection_method_text]
        if len(collection_methods) == 0:
            collection_methods.append(CollectionMethod.MISSING)
    return collection_methods

def parse_study_designs(row):
    study_design_text = row["types - CODED"]
    if pd.isna(study_design_text):
        study_designs = [StudyDesign.MISSING]
    else:
        study_designs = [design for design in STUDY_DESIGNS if design.label in study_design_text]
        if len(study_designs) == 0:
            study_designs.append(StudyDesign.MISSING)
    return study_designs
    
def parse_population(row):
    population_text = row["estimated_participants"]
    if pd.isna(population_text):
        population = None
        population_range = PopulationRange.MISSING
    elif isinstance(population_text, str):
        match = re.search(r"\b\d+\b", population_text)
        if match:
            population = int(match.group())
            population_range = [pop_range for pop_range in POPULATION_RANGES if pop_range.lower_bound <= population <= pop_range.upper_bound].pop()
        else:
            population = None
            population_range = PopulationRange.MISSING
    else:
        population = int(population_text)
        population_range = [pop_range for pop_range in POPULATION_RANGES if pop_range.lower_bound <= population_text <= pop_range.upper_bound].pop()
    return population, population_range

def parse_data_types(row):
    # these are coded?
    data_type_text = row["data_general_types.1"]
    if pd.isna(data_type_text):
        data_types = [DataType.MISSING]
    else:
        data_types = [data_type for data_type in DATA_TYPES if data_type.label in data_type_text]
        if len(data_types) == 0:
            data_types.append(DataType.MISSING)
    return data_types

def parse_study_domains(row):
    subject_text = row["subject"]
    description_text = row["description"]
    if pd.isna(subject_text):
        subject_text = ""
    if pd.isna(description_text):
        description_text = ""
    study_topic_text = subject_text.lower() + description_text.lower()
    study_domains = [topic for topic in STUDY_DOMAINS if topic.label.lower() in study_topic_text]
    if len(study_domains) == 0:
        study_domains.append(StudyDomain.MISSING)
    return study_domains

def parse_dates(row):
    start_date = row["studystartdate"]
    end_date = row["studyenddate"]
    date_format = "%Y-%m-%d %H:%M:%S%z"
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
    return row["phs"]

def parse_metadata_file(metadata):
    
    studies = {}
    for i, row in metadata.iterrows():
        program = parse_program(row)
        nih_institutes = parse_nih_institutes(row)
        collection_methods = parse_collection_methods(row)
        study_designs = parse_study_designs(row)
        population, population_range = parse_population(row)
        data_types = parse_data_types(row)
        study_domains = parse_study_domains(row)
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
            doi=None,
            start_date=start_date,
            end_date=end_date,
        )
    
        studies[phs] = study