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
    RAD = ("radxrad", generate_search_url("dcc", "RADx-rad"))
    UP = ("radxup", generate_search_url("dcc", "RADx-UP"))
    TECH = ("radxtech", generate_search_url("dcc", "RADx Tech"))
    DHT = ("radxdht", generate_search_url("dcc", "RADx DHT"))
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
        "prospective longitudinal cohort",
        generate_search_url("types_array", "Longitudinal Cohort"),
    )
    FAMILY = (
        "familytwinstrios",
        generate_search_url("types_array", "Family/Twins/Trios"),
    )  # no matches in data hub
    CLINICALTRIAL = (
        "clinical trial",
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
    behavioral = ("behavioral",)
    CLINICAL = ("clinical",)
    COGNITIVE = ("cognitive",)  # this has a typo in the spreadsheet
    ELECTRONICMEDICALRECORDS = ("electronic medical records",)
    ENVIRONMENTAL = ("enviornmental physical",)
    FAMILYHISTORY = ("family history",)
    GENOMIC = ("genomic",)
    GENOTYPING = ("genotyping",)
    IMAGING = ("imaging",)
    IMMULOGICAL = ("immulogical",)
    INDIVIDUALGENOTYPE = ("individual genotype",)
    INDIVIDUALPHENOTYPE = ("individual phenotype",)
    INDIVIDUALSEQUENCING = ("individual sequencing",)
    METABOLOMIC = ("metabolomic",)
    PHYSICALACTIVITY = ("physical activity",)
    PROTEOMIC = ("proteomic",)
    PSYCHOLOGICAL = ("psychological",)
    QUESTIONNAIRE = ("questionnairessurveys",)
    SOCIAL = ("social",)
    SUPPORTINGDOCUMENTS = ("supporting documents",)
    OTHER = ("other",)
    MISSING = ("MISSING OR INVALID",)

    def __init__(self, label, url=None):
        self.label = label
        self.url = url


class CollectionMethod(Enum):
    """
    Enumerations for categorizing studies by its data collection method.
    """
    QUESTIONNAIRE = (
        "questionnairesurvey",
        generate_search_url("source_array", "Survey"),
    )  # to be removed
    INTERVIEW = (
        "interview or focus group",
        generate_search_url("source_array", "Interview or Focus Group"),
    )
    WEARABLE = ("wearable", generate_search_url("source_array", "Wearable"))
    SMARTPHONE = ("smartphone", generate_search_url("source_array", "Smartphone"))
    TESTINGDEVICE = (
        "covid testing device",
        generate_search_url("source_array", "COVID Testing Device"),
    )
    WASTEWATER = (
        "wastewater sampling",
        generate_search_url("source_array", "Wastewater Sampling"),
    )
    CONTACTTRACING = (
        "contact tracing",
        generate_search_url("source_array", "Contact Tracing"),
    )
    OTHER = ("other", generate_search_url("source_array", "Other"))
    MISSING = "MISSING OR INVALID"

    def __init__(self, label, url=None):
        self.label = label
        self.url = url


class NihInstitute(Enum):
    """
    Enumerations for categorizing studies by its supporting NIH Institute.
    """
    NCATS = ("ncats", generate_search_url("institutes_supporting_study_array", "NCATS"))
    NCCIH = ("nccih", generate_search_url("institutes_supporting_study_array", "NCCIH"))
    NCI = ("nci", generate_search_url("institutes_supporting_study_array", "NCI"))
    NDA = ("nda", generate_search_url("institutes_supporting_study_array", "NDA"))
    NEI = ("nei", generate_search_url("institutes_supporting_study_array", "NEI"))
    NHGRI = ("nhgri", generate_search_url("institutes_supporting_study_array", "NHGRI"))
    NHLBI = ("nhlbi", generate_search_url("institutes_supporting_study_array", "NHLBI"))
    NIA = ("nia", generate_search_url("institutes_supporting_study_array", "NIA"))
    NIAAA = ("niaaa", generate_search_url("institutes_supporting_study_array", "NIAAA"))
    NIAID = ("niaid", generate_search_url("institutes_supporting_study_array", "NIAID"))
    NIAMS = ("niams", generate_search_url("institutes_supporting_study_array", "NIAMS"))
    NIBIB = ("nibib", generate_search_url("institutes_supporting_study_array", "NIBIB"))
    NICHD = ("nichd", generate_search_url("institutes_supporting_study_array", "NICHD"))
    NIDA = ("nida", generate_search_url("institutes_supporting_study_array", "NIDA"))
    NIDCD = ("nidcd", generate_search_url("institutes_supporting_study_array", "NIDCD"))
    NIDCR = ("nidcr", generate_search_url("institutes_supporting_study_array", "NIDCR"))
    NIDDK = ("niddk", generate_search_url("institutes_supporting_study_array", "NIDDK"))
    NIEHS = ("niehs", generate_search_url("institutes_supporting_study_array", "NIEHS"))
    NIGMS = ("nigms", generate_search_url("institutes_supporting_study_array", "NIGMS"))
    NIHOD = (
        "nih od",
        generate_search_url("institutes_supporting_study_array", "NIH OD"),
    )
    NIMH = ("nimh", generate_search_url("institutes_supporting_study_array", "NIMH"))
    NIMHD = ("nimhd", generate_search_url("institutes_supporting_study_array", "NIMHD"))
    NINDS = ("ninds", generate_search_url("institutes_supporting_study_array", "NINDS"))
    NINR = ("ninr", generate_search_url("institutes_supporting_study_array", "NINR"))
    NLM = ("nlm", generate_search_url("institutes_supporting_study_array", "NLM"))
    NIH = (
        "nih",
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
        "testing rateuptake",
        generate_search_url("topics_array", "Testing Rate/Uptake"),
    )
    PERCEPTIONS = (
        "pandemic perceptions and decisionmaking",
        generate_search_url("topics_array", "Pandemic Perceptions and Decision-Making"),
    )
    ANTIGEN = (
        "antigen testing",
        generate_search_url("topics_array", "Antigen Testing"),
    )
    SCHOOL = (
        "covid in school settings",
        generate_search_url("topics_array", "COVID in School Settings"),
    )
    DIAGNOSTIC = (
        "diagnostic testing",
        generate_search_url("topic_array", "Diagnostic Testing"),
    )
    BEHAVIORS = (
        "health behaviors",
        generate_search_url("topic_array", "Health Behaviors"),
    )
    COMORBIDITIES = (
        "comorbidities",
        generate_search_url("topics_array", "Comorbidities"),
    )
    POC = (
        "pointofcare poc testing",
        generate_search_url("topics_array", "Point-of-Care (POC) Testing"),
    )
    VOC = (
        "novel biosensing and voc",
        generate_search_url("topics_array", "Novel Biosensing and VOC"),
    )
    SCREENING = (
        "screening testing",
        generate_search_url("topics_array", "Screening Testing"),
    )
    HOTSPOTS = ("COVID Hotspots", generate_search_url("topics_array", "COVID Hotspots"))
    DESERTS = (
        "covid testing deserts",
        generate_search_url("topics_array", "COVID Testing Deserts"),
    )
    DISEASESURVEILLANCE = (
        "disease surveillance",
        generate_search_url("topics_array", "Disease Surveillance"),
    )
    MULTIMODALSURVEILLANCE = (
        "multimodal surveillance",
        generate_search_url("topics_array", "Multimodal Surveillance"),
    )
    CHEMOSENSORY = (
        "chemosensory testing",
        generate_search_url("topics_array", "Chemosensory Testing"),
    )
    SEROPREVALENCE = (
        "seroprevalence",
        generate_search_url("topics_array", "Seroprevalence"),
    )
    MISC = (
        "multisystem inflammatory syndrome in children (mis-c)",
        generate_search_url(
            "topics_array", "Multisystem Inflammatory Syndrome in Children (MIS-C)"
        ),
    )
    MIS = (
        "multisystem inflammatory syndrome mis",
        generate_search_url("topics_array", "Multisystem Inflammatory Syndrome (MIS)"),
    )
    WASTEWATER = (
        "wastewater surveillance",
        generate_search_url("topics_array", "Wastewater Surveillance"),
    )
    IMMUNERESPONSES = (
        "immune responses",
        generate_search_url("topics_array", "Immune Responses"),
    )
    MENTALHEALTH = (
        "mental health",
        generate_search_url("topics_array", "Mental Health"),
    )
    SUBSTANCEUSE = (
        "substance use",
        generate_search_url("topics_array", "Substance Use"),
    )
    VIROLOGICALTESTING = (
        "virological testing",
        generate_search_url("topics_array", "Virological Testing"),
    )
    RAPIDTESTING = (
        "rapid diagnostic testing",
        generate_search_url("topics_array", "Rapid Diagnostic Test (RDT)"),
    )
    PCRTESTING = (
        "laboratory pcr testing",
        generate_search_url("topics_array", "Molecular (PCR/Nucleic Acid) Testing"),
    )
    ANTIBODYTESTING = (
        "serological antibody testing",
        generate_search_url("topics_array", "Serological (Antibody) Testing"),
    )
    MOBILETESTING = (
        "mobile unit testing",
        generate_search_url("topics_array", "Mobile Unit Testing"),
    )
    ATHOMETESTING = (
        "athome testing",
        generate_search_url("topics_array", "Self-Testing (At-Home or OTC)"),
    )
    VACCINATIONRATE = (
        "vaccination rate/ptake",
        generate_search_url("topics_array", "Vaccination Rate/Uptake"),
    )
    VARIANTS = ("Variants", generate_search_url("topics_array", "Variants"))
    SOCIALDETERMINANTS = (
        "social determinants of health",
        generate_search_url("topics_array", "Social Determinants of Health"),
    )
    COMMUNITYOUTREACH = (
        "community outreach programs",
        generate_search_url("topics_array", "Community Outreach Programs"),
    )
    MEDICALDEVICEDEVELOPMENT = (
        "medical device development",
        generate_search_url("topics_array", "Medical Device/Tool Development"),
    )
    BIOSENSORTECHNOLOGY = (
        "biosensor technology",
        generate_search_url("topics_array", "Biosensor Technology"),
    )
    AIML = (
        "artifical intelligence and machine learning",
        generate_search_url(
            "topics_array", "Artificial Intelligence and Machine Learning"
        ),
    )
    NGS = (
        "next generation sequencing ngs",
        generate_search_url("topics_array", "Next Generation Sequencing (NGS)"),
    )
    DIGITALHEALTH = (
        "digital health applications",
        generate_search_url("topics_array", "Digital Health Applications"),
    )
    INFLUENZA = ("influenza", generate_search_url("topics_array", "Influenza"))
    # no entries in data hub
    CHILDREN = (
        "children",
        generate_search_url("topics_array", "Children"),
    )  # study population focus
    MINORITIES = (
        "minorities",
        generate_search_url("topics_array", "Minorities"),
    )  # study population focus
    AFRICANAMERICANPOPULATION = (
        "african american population",
        generate_search_url("topics_array", "African American Population"),
    )  # study population focus
    TRIBALPOPULATION = (
        "tribal population",
        generate_search_url("topics_array", "Tribal Population"),
    )  # study population focus
    HISPANICPOPULATION = (
        "hispanic and latino population",
        generate_search_url("topics_array", "Hispanic and Latino Population"),
    )  # study population focus
    PREGNANCY = (
        "pregnancy",
        generate_search_url("topics_array", "Pregnancy"),
    )  # study population focus
    LONGCOVID = ("long covid", generate_search_url("topics_array", "Long COVID"))
    AGING = ("aging", generate_search_url("topics_array", "Aging"))
    CANCER = ("cancer", generate_search_url("topics_array", "Cancer"))
    NUTRITION = ("nutrition", generate_search_url("topics_array", "Nutrition"))
    DIABETES = ("diabetes", generate_search_url("topics_array", "Diabetes"))
    OBESITY = ("obesity", generate_search_url("topics_array", "Obesity"))
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


class FocusPopulation(Enum):
    RACIALMINORITIES = (
        "racial and ethnic minorities",
        generate_search_url("study_focus_population", "Racial and Ethnic Minorities"),
    )
    IMMIGRANTS = (
        "immigrants",
        generate_search_url("study_focus_population", "Immigrants"),
    )
    AFRICANAMERICAN = (
        "african american",
        generate_search_url("study_focus_population", "African American"),
    )
    HISPANICLATINO = (
        "hispanic and latino",
        generate_search_url("study_focus_population", "Hispanic and Latino"),
    )
    HAWAIINPACIFICISLANDER = (
        "native hawaiian or other pacific islander",
        generate_search_url("study_focus_population", "Native Hawaiian or other Pacific Islander"),
    )
    ASIAN = (
        "asian",
        generate_search_url("study_focus_population", "Asian"),
    )
    CHILDREN = (
        "children",
        generate_search_url("study_focus_population", "Children"),
    )
    SCHOOLCOMMUNITY = (
        "school community members",
        generate_search_url("study_focus_population", "School Community Members"),
    )
    ESSENTIALWORKERS = (
        "essential workers",
        generate_search_url("study_focus_population", "Essential Workers"),
    )
    PREGNANTWOMEN = (
        "pregnant or nursing women",
        generate_search_url("study_focus_population", "Pregnant (or Nursing) Women"),
    )
    IDDISABILITIES = (
        "intellectual and developmental disabilities",
        generate_search_url("study_focus_population", "Intellectual and Developmental Disabilities"),
    )
    HOMELESS = (
        "homelessunhoused",
        generate_search_url("study_focus_population", "Homeless/Unhoused"),
    )
    INCARCERATED = (
        "incarcerated/institutionalized or criminal legal system involvement",
        generate_search_url("study_focus_population", "Incarcerated/Institutionalized (or Criminal Legal System Involvement)"),
    )
    HIVAIDS = (
        "people living with hiv/aids",
        generate_search_url("study_focus_population", "People Living with HIV/AIDs"),
    )
    DIALYSISPATIENTS = (
        "dialysis patients",
        generate_search_url("study_focus_population", "Dialysis Patients"),
    )
    SEXGENDERMINROTIES = (
        "sexual and gender minorities",
        generate_search_url("study_focus_population", "Sexual and Gender Minorities"),
    )
    RURAL = (
        "rural communities",
        generate_search_url("study_focus_population", "Rural Communities"),
    )
    UNDERSERVED = (
        "underservedvulnerable population",
        generate_search_url("study_focus_population", "Underserved/Vulnerable Population"),
    )
    LOWERSOCIOECONOMIC = (
        "lower socioeconomic status ses population",
        generate_search_url("study_focus_population", "Lower Socioeconomic Status (SES) Population"),
    )
    ELDERLY = (
        "older adults or elderly",
        generate_search_url("study_focus_population", "Older Adults or Elderly"),
    )
    ADULTS = (
        "adults",
        generate_search_url("study_focus_population", "Adults"),
    )
    MISSING = ("MISSING OR INVALID",)

    def __init__(self, label, url=None):
        self.label = label
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
    FOCUSPOPULATION = ("Study Focus Population", FocusPopulation)

    def __init__(self, label, classifier):
        self.label = label
        self.classifier = classifier


INSTITUTES = list(NihInstitute)
STUDY_DESIGNS = list(StudyDesign)
POPULATION_RANGES = list(PopulationRange)
DATA_TYPES = list(DataType)
STUDY_DOMAINS = list(StudyDomain)
COLLECTION_METHODS = list(CollectionMethod)
FOCUS_POPULATIONS = list(FocusPopulation)
PROGRAMS = {program.label: program for program in list(Program)}
