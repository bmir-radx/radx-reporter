import html
from enum import Enum


def generate_search_url(name: str, facet: str) -> str:
    """
    Returns search URL for the RADx Data Hub based on the provided
    name and facet strings.
    """
    name = html.escape(name)
    facet = html.escape(facet)
    return f"https://radxdatahub.nih.gov/studyExplorer?&facets=%5B%7B%22name%22:%22{name}%22,%22facets%22:%5B%22{facet}%22%5D%7D%5D"


class Program(Enum):
    """
    Enumerations for categorizing studies by the RADx Program (DCC).
    """
    RAD = ("RADx-rad", generate_search_url("dcc", "RADx-rad"))
    UP = ("RADx-UP", generate_search_url("dcc", "RADx-UP"))
    TECH = ("RADx-Tech", generate_search_url("dcc", "RADx Tech"))
    DHT = ("Digital Health Technologies", generate_search_url("dcc", "RADx DHT"))
    MISSING = ("MISSING OR INVALID",)

    def __init__(self, label, url=None):
        self.label = label
        self.url = url


class StudyDesign(Enum):
    """
    Enumerations for categorizing studies by its Study Design(s).
    """
    CASECONTROL = ("Case-Control", generate_search_url("types_array", "Case-Control"))
    LONGITUDINAL = (
        "Prospective Longitudinal Cohort",
        generate_search_url("types_array", "Longitudinal Cohort"),
    )
    FAMILY = (
        "Family/Twins/Trios",
        generate_search_url("types_array", "Family/Twins/Trios"),
    )  # no matches in data hub
    CLINICALTRIAL = (
        "Clinical Trial",
        generate_search_url("types_array", "Interventional/Clinical Trial"),
    )
    CROSSSECTIONAL = (
        "Cross-Sectional",
        generate_search_url("types_array", "Cross-Sectional"),
    )
    INTERVENTIONAL = (
        "Interventional",
        generate_search_url("types_array", "Interventional/Clinical Trial"),
    )  # why is this merged with clinical
    MENDELIAN = (
        "Mendelian",
        generate_search_url("types_array", "Mendelian"),
    )  # no matches in data hub
    XENOGRAFT = (
        "Xenograft",
        generate_search_url("types_array", "Xenograft"),
    )  # no matches in data hub
    METAGENOMICS = (
        "Metagenomics",
        generate_search_url("types_array", "Metagenomics"),
    )  # no matches in data hub
    CLINICALGENETICTESTING = (
        "Clinical Genetic Testing ",
        generate_search_url("types_array", "Clinical Genetic Testing"),
    )  # no matches data hub
    OTHER = ("Other", generate_search_url("types_array", "Other"))
    MISSING = ("MISSING OR INVALID",)

    def __init__(self, label, url=None):
        self.label = label
        self.url = url


class DataType(Enum):
    """
    Enumerations for categorizing studies by the type of data recorded.
    Some of the categories overlap.
    """
    BEHAVIORAL = ("Behavioral",)
    CLINICAL = ("Clinical",)
    COGNITIVE = ("Cognitive",)  # this has a typo in the spreadsheet
    ELECTRONICMEDICALRECORDS = ("Electronic Medical Records",)
    ENVIRONMENTAL = ("Enviornmental (Physical)",)
    FAMILYHISTORY = ("Family History",)
    GENOMIC = ("Genomic",)
    GENOTYPING = ("Genotyping",)
    IMAGING = ("Imaging",)
    IMMULOGICAL = ("Immulogical",)
    INDIVIDUALGENOTYPE = ("Individual Genotype",)
    INDIVIDUALPHENOTYPE = ("Individual Phenotype",)
    INDIVIDUALSEQUENCING = ("Individual Sequencing",)
    METABOLOMIC = ("Metabolomic",)
    PHYSICALACTIVITY = ("Physical Activity",)
    PROTEOMIC = ("Proteomic",)
    PSYCHOLOGICAL = ("Psychological",)
    QUESTIONNAIRE = ("Questionnaires/Surveys",)
    SOCIAL = ("Social",)
    SUPPORTINGDOCUMENTS = ("Supporting Documents",)
    OTHER = ("Other",)
    MISSING = ("MISSING OR INVALID",)

    def __init__(self, label, url=None):
        self.label = label
        self.url = url


class CollectionMethod(Enum):
    """
    Enumerations for categorizing studies by its data collection method.
    """
    QUESTIONNAIRE = (
        "Questionnaire/Survey",
        generate_search_url("source_array", "Survey"),
    )  # to be removed
    INTERVIEW = (
        "Interview or Focus Group",
        generate_search_url("source_array", "Interview or Focus Group"),
    )
    WEARABLE = ("Wearable", generate_search_url("source_array", "Wearable"))
    SMARTPHONE = ("Smartphone", generate_search_url("source_array", "Smartphone"))
    TESTINGDEVICE = (
        "COVID Testing Device",
        generate_search_url("source_array", "COVID Testing Device"),
    )
    WASTEWATER = (
        "Wastewater Sampling",
        generate_search_url("source_array", "Wastewater Sampling"),
    )
    CONTACTTRACING = (
        "Contact Tracing",
        generate_search_url("source_array", "Contact Tracing"),
    )
    OTHER = ("Other", generate_search_url("source_array", "Other"))
    MISSING = "MISSING OR INVALID"

    def __init__(self, label, url=None):
        self.label = label
        self.url = url


class NihInstitute(Enum):
    """
    Enumerations for categorizing studies by its supporting NIH Institute.
    """
    NCATS = ("NCATS", generate_search_url("institutes_supporting_study_array", "NCATS"))
    NCCIH = ("NCCIH", generate_search_url("institutes_supporting_study_array", "NCCIH"))
    NCI = ("NCI", generate_search_url("institutes_supporting_study_array", "NCI"))
    NDA = ("NDA", generate_search_url("institutes_supporting_study_array", "NDA"))
    NEI = ("NEI", generate_search_url("institutes_supporting_study_array", "NEI"))
    NHGRI = ("NHGRI", generate_search_url("institutes_supporting_study_array", "NHGRI"))
    NHLBI = ("NHLBI", generate_search_url("institutes_supporting_study_array", "NHLBI"))
    NIA = ("NIA", generate_search_url("institutes_supporting_study_array", "NIA"))
    NIAAA = ("NIAAA", generate_search_url("institutes_supporting_study_array", "NIAAA"))
    NIAID = ("NIAID", generate_search_url("institutes_supporting_study_array", "NIAID"))
    NIAMS = ("NIAMS", generate_search_url("institutes_supporting_study_array", "NIAMS"))
    NIBIB = ("NIBIB", generate_search_url("institutes_supporting_study_array", "NIBIB"))
    NICHD = ("NICHD", generate_search_url("institutes_supporting_study_array", "NICHD"))
    NIDA = ("NIDA", generate_search_url("institutes_supporting_study_array", "NIDA"))
    NIDCD = ("NIDCD", generate_search_url("institutes_supporting_study_array", "NIDCD"))
    NIDCR = ("NIDCR", generate_search_url("institutes_supporting_study_array", "NIDCR"))
    NIDDK = ("NIDDK", generate_search_url("institutes_supporting_study_array", "NIDDK"))
    NIEHS = ("NIEHS", generate_search_url("institutes_supporting_study_array", "NIEHS"))
    NIGMS = ("NIGMS", generate_search_url("institutes_supporting_study_array", "NIGMS"))
    NIHOD = (
        "NIH OD",
        generate_search_url("institutes_supporting_study_array", "NIH OD"),
    )
    NIMH = ("NIMH", generate_search_url("institutes_supporting_study_array", "NIMH"))
    NIMHD = ("NIMHD", generate_search_url("institutes_supporting_study_array", "NIMHD"))
    NINDS = ("NINDS", generate_search_url("institutes_supporting_study_array", "NINDS"))
    NINR = ("NINR", generate_search_url("institutes_supporting_study_array", "NINR"))
    NLM = ("NLM", generate_search_url("institutes_supporting_study_array", "NLM"))
    NIH = (
        "NIH",
        generate_search_url("institutes_supporting_study_array", "NIH"),
    )  # added this because phs003366 only has this as an entry
    MISSING = ("MISSING OR INVALID",)

    def __init__(self, label, url=None):
        self.label = label
        self.url = url


class StudyDomain(Enum):
    """
    Enumerations for categorizing studies by its Study Domain(s).
    This is also called the study topic.
    """
    TESTINGRATE = (
        "Testing Rate/Uptake",
        generate_search_url("topics_array", "Testing Rate/Uptake"),
    )
    PERCEPTIONS = (
        "Pandemic Perceptions and Decision-Making",
        generate_search_url("topics_array", "Pandemic Perceptions and Decision-Making"),
    )
    ANTIGEN = (
        "Antigen Testing",
        generate_search_url("topics_array", "Antigen Testing"),
    )
    SCHOOL = (
        "COVID in School Settings",
        generate_search_url("topics_array", "COVID in School Settings"),
    )
    DIAGNOSTIC = (
        "Diagnostic Testing",
        generate_search_url("topic_array", "Diagnostic Testing"),
    )
    BEHAVIORS = (
        "Health Behaviors",
        generate_search_url("topic_array", "Health Behaviors"),
    )
    COMORBIDITIES = (
        "Comorbidities",
        generate_search_url("topics_array", "Comorbidities"),
    )
    POC = (
        "Point-of-Care (POC) Testing",
        generate_search_url("topics_array", "Point-of-Care (POC) Testing"),
    )
    VOC = (
        "Novel Biosensing and VOC",
        generate_search_url("topics_array", "Novel Biosensing and VOC"),
    )
    SCREENING = (
        "Screening Testing",
        generate_search_url("topics_array", "Screening Testing"),
    )
    HOTSPOTS = ("COVID Hotspots", generate_search_url("topics_array", "COVID Hotspots"))
    DESERTS = (
        "COVID Testing Deserts",
        generate_search_url("topics_array", "COVID Testing Deserts"),
    )
    DISEASESURVEILLANCE = (
        "Disease Surveillance",
        generate_search_url("topics_array", "Disease Surveillance"),
    )
    MULTIMODALSURVEILLANCE = (
        "Multimodal Surveillance",
        generate_search_url("topics_array", "Multimodal Surveillance"),
    )
    CHEMOSENSORY = (
        "Chemosensory Testing",
        generate_search_url("topics_array", "Chemosensory Testing"),
    )
    SEROPREVALENCE = (
        "Seroprevalence",
        generate_search_url("topics_array", "Seroprevalence"),
    )
    MISC = (
        "Multisystem Inflammatory Syndrome in Children (MIS-C)",
        generate_search_url(
            "topics_array", "Multisystem Inflammatory Syndrome in Children (MIS-C)"
        ),
    )
    MIS = (
        "Multisystem Inflammatory Syndrome (MIS)",
        generate_search_url("topics_array", "Multisystem Inflammatory Syndrome (MIS)"),
    )
    WASTEWATER = (
        "Wastewater Surveillance",
        generate_search_url("topics_array", "Wastewater Surveillance"),
    )
    IMMUNERESPONSES = (
        "Immune Responses",
        generate_search_url("topics_array", "Immune Responses"),
    )
    MENTALHEALTH = (
        "Mental Health",
        generate_search_url("topics_array", "Mental Health"),
    )
    SUBSTANCEUSE = (
        "Substance Use",
        generate_search_url("topics_array", "Substance Use"),
    )
    VIROLOGICALTESTING = (
        "Virological Testing",
        generate_search_url("topics_array", "Virological Testing"),
    )
    RAPIDTESTING = (
        "Rapid Diagnostic Testing",
        generate_search_url("topics_array", "Rapid Diagnostic Test (RDT)"),
    )
    PCRTESTING = (
        "Laboratory (PCR) Testing",
        generate_search_url("topics_array", "Molecular (PCR/Nucleic Acid) Testing"),
    )
    ANTIBODYTESTING = (
        "Serological (Antibody) Testing",
        generate_search_url("topics_array", "Serological (Antibody) Testing"),
    )
    MOBILETESTING = (
        "Mobile Unit Testing",
        generate_search_url("topics_array", "Mobile Unit Testing"),
    )
    ATHOMETESTING = (
        "At-Home Testing",
        generate_search_url("topics_array", "Self-Testing (At-Home or OTC)"),
    )
    VACCINATIONRATE = (
        "Vaccination Rate/Uptake",
        generate_search_url("topics_array", "Vaccination Rate/Uptake"),
    )
    VARIANTS = ("Variants", generate_search_url("topics_array", "Variants"))
    SOCIALDETERMINANTS = (
        "Social Determinants of Health",
        generate_search_url("topics_array", "Social Determinants of Health"),
    )
    COMMUNITYOUTREACH = (
        "Community Outreach Programs",
        generate_search_url("topics_array", "Community Outreach Programs"),
    )
    MEDICALDEVICEDEVELOPMENT = (
        "Medical Device Development",
        generate_search_url("topics_array", "Medical Device/Tool Development"),
    )
    BIOSENSORTECHNOLOGY = (
        "Biosensor Technology",
        generate_search_url("topics_array", "Biosensor Technology"),
    )
    AIML = (
        "Artifical Intelligence and Machine Learning",
        generate_search_url(
            "topics_array", "Artificial Intelligence and Machine Learning"
        ),
    )
    NGS = (
        "Next Generation Sequencing (NGS)",
        generate_search_url("topics_array", "Next Generation Sequencing (NGS)"),
    )
    DIGITALHEALTH = (
        "Digital Health Applications",
        generate_search_url("topics_array", "Digital Health Applications"),
    )
    INFLUENZA = ("Influenza", generate_search_url("topics_array", "Influenza"))
    # no entries in data hub
    CHILDREN = (
        "Children",
        generate_search_url("topics_array", "Children"),
    )  # study population focus
    MINORITIES = (
        "Minorities",
        generate_search_url("topics_array", "Minorities"),
    )  # study population focus
    AFRICANAMERICANPOPULATION = (
        "African American Population",
        generate_search_url("topics_array", "African American Population"),
    )  # study population focus
    TRIBALPOPULATION = (
        "Tribal Population",
        generate_search_url("topics_array", "Tribal Population"),
    )  # study population focus
    HISPANICPOPULATION = (
        "Hispanic and Latino Population",
        generate_search_url("topics_array", "Hispanic and Latino Population"),
    )  # study population focus
    PREGNANCY = (
        "Pregnancy",
        generate_search_url("topics_array", "Pregnancy"),
    )  # study population focus
    LONGCOVID = ("Long COVID", generate_search_url("topics_array", "Long COVID"))
    AGING = ("Aging", generate_search_url("topics_array", "Aging"))
    CANCER = ("Cancer", generate_search_url("topics_array", "Cancer"))
    NUTRITION = ("Nutrition", generate_search_url("topics_array", "Nutrition"))
    DIABETES = ("Diabetes", generate_search_url("topics_array", "Diabetes"))
    OBESITY = ("Obesity", generate_search_url("topics_array", "Obesity"))
    MISSING = ("MISSING OR INVALID",)

    def __init__(self, label, url=None):
        self.label = label
        self.url = url


class PopulationRange(Enum):
    """
    Enumerations for categorizing studies by its population size.
    The RADx Data Hub search filter has several bins for population
    size that are followed here.
    """
    SMALLEST = (
        "1-250",
        1,
        250,
        generate_search_url("estimated_participant_range", "1 - 250"),
    )
    SMALLER = (
        "251-500",
        251,
        500,
        generate_search_url("estimated_participant_range", "251 - 500"),
    )
    SMALL = (
        "501-1,000",
        501,
        1000,
        generate_search_url("estimated_participant_range", "501 - 1000"),
    )
    LARGE = (
        "1,001-2,000",
        1001,
        2000,
        generate_search_url("estimated_participant_range", "1001 - 2000"),
    )
    LARGER = (
        "2,001-5,000",
        2001,
        5000,
        generate_search_url("estimated_participant_range", "2001 - 5000"),
    )
    LARGEST = (
        ">5,000",
        5001,
        float("inf"),
        generate_search_url("estimated_participant_range", "> 5000"),
    )
    ZERO = (
        "No Participant",
        0,
        0,
        generate_search_url("estimated_participant_range", "No Participant"),
    )
    UNKNOWN = (
        "MISSING OR INVALID",
        float("inf"),
        float("-inf"),
        generate_search_url("estimated_participant_range", "Unknown"),
    )

    def __init__(self, label, lower_bound, upper_bound, url=None):
        self.label = label
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.url = url


class Classifier(Enum):
    """
    Enumerations to facilate grouping by one of the following categories.
    """
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


INSTITUTES = list(NihInstitute)
STUDY_DESIGNS = list(StudyDesign)
POPULATION_RANGES = list(PopulationRange)
DATA_TYPES = list(DataType)
STUDY_DOMAINS = list(StudyDomain)
COLLECTION_METHODS = list(CollectionMethod)
PROGRAMS = {program.label: program for program in list(Program)}
