import datetime

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
from vocabulary import CollectionMethod, DataType, NihInstitute, PopulationRange, Program, StudyDesign, StudyDomain

@dataclass(frozen=True)
class DataFile:
    file_name: str
    # data_types: List[str]
    # data_formats: List[str]

@dataclass(frozen=True)
class DataDictionary:
    file_name: str
    # data_types: List[str]
    # data_formats: List[str]

@dataclass(frozen=True)
class Metadata:
    file_name: str

@dataclass(frozen=True)
class Bundle:
    metadata: List[Metadata]
    dictionary: List[DataDictionary]
    data_file: List[DataFile]

@dataclass(frozen=True)
class Institution:
    name: str
    rori_d: Optional[str]
    uei_id: Optional[str]

@dataclass(frozen=True)
class Contributor:
    orcid: str
    name: str
    email: str
    institution: Institution

class Classifier(Enum):
    PROGRAM = ("Program", Program)
    STUDYDESIGN = ("Study Design", StudyDesign)
    DATATYPE = ("Data Type", DataType)
    COLLECTIONMETHOD = ("Collection Method", CollectionMethod)
    NIHINSTITUTE = ("NIH Institute", NihInstitute)
    STUDYDOMAIN = ("Study Domain", StudyDomain)
    POPULATIONRANGE = ("Population Range", PopulationRange)

    def __init__(self, label, classifier):
        self.label = label
        self.classifier = classifier

@dataclass(frozen=True)
class Study:
    bundles: List[Bundle]
    contributors: List[Contributor]
    program: Program
    phs_id: str
    study_designs: List[StudyDesign]
    data_types: List[DataType]
    collection_methods: List[CollectionMethod]
    nih_institutes: List[NihInstitute]
    study_domains: List[StudyDomain]
    population: Optional[int] # population and population_range should be combined in a "study statistics" object
    population_range: PopulationRange
    doi: Optional[str]
    start_date: Optional[datetime.datetime] = None
    end_date: Optional[datetime.datetime] = None

    def get_classifiers(self, classifier: Classifier):
        match classifier:
            case Classifier.PROGRAM:
                return [self.program]
            case Classifier.STUDYDESIGN:
                return self.study_designs
            case Classifier.DATATYPE:
                return self.data_types
            case Classifier.COLLECTIONMETHOD:
                return self.collection_methods
            case Classifier.NIHINSTITUTE:
                return self.nih_institutes
            case Classifier.STUDYDOMAIN:
                return self.study_domains
            case Classifier.POPULATIONRANGE:
                return [self.population_range]
