from enum import Enum

class Program(Enum):
    RAD = "RADx-rad"
    UP = "RADx-UP"
    TECH = "RADx-Tech"
    DHT = "Digital Health Technologies"
    MISSING = "MISSING OR INVALID"

    def __init__(self, label):
        self.label = label

class StudyDesign(Enum):
    CASECONTROL = "Case-Control"
    CASESET = "Case Set" # remove
    LONGITUDINAL = "Prospective Longitudinal Cohort"
    FAMILY = "Family/Twins/Trios"
    CLINICALTRIAL = "Clinical Trial"
    TUMOR = "Tumor vs. Matched-Normal" # should be part of case control
    CROSSSECTIONAL = "Cross-Sectional"
    COLLECTION = "Collection" # remove
    CONTROLSET = "Control Set" # should be part of case-control
    METHODS = "Methods" # remove
    INTERVENTIONAL = "Interventional"
    MENDELIAN = "Mendelian"
    XENOGRAFT = "Xenograft"
    METAGENOMICS = "Clinical Genetic Testing "
    CLINICALGENETICTESTING = "Clinical Genetic Testing "
    OTHER = "Other" # remove
    MISSING = "MISSING OR INVALID"

    def __init__(self, label):
        self.label = label

class DataType(Enum):
    """I think some of these overlap"""
    BEHAVIORAL = "Behavioral"
    CLINICAL = "Clinical"
    COGNITIVE = "Coginitive" # this has a typo in the spreadsheet
    ELECTRONICMEDICALRECORDS = "Electronic Medical Records"
    ENVIRONMENTAL = "Enviornmental (Physical)"
    FAMILYHISTORY = "Family History"
    GENOMIC = "Genomic"
    GENOTYPING = "Genotyping"
    IMAGING = "Imaging"
    IMMULOGICAL = "Immulogical"
    INDIVIDUALGENOTYPE = "Individual Genotype"
    INDIVIDUALPHENOTYPE = "Individual Phenotype"
    INDIVIDUALSEQUENCING = "Individual Sequencing"
    METABOLOMIC = "Metabolomic"
    METAGENOMIC = "Metagenomic"
    PHYSICALACTIVITY = "Physical Activity"
    PROTEOMIC = "Proteomic"
    PSYCHOLOGICAL = "Psychological"
    QUESTIONNAIRE = "Questionnaires/Surveys"
    SOCIAL = "Social"
    SUPPORTINGDOCUMENTS = "Supporting Documents"
    OTHER = "Other"
    MISSING = "MISSING OR INVALID"

    def __init__(self, label):
        self.label = label

class CollectionMethod(Enum):
    QUESTIONNAIRE = "Questionnaire/Survey" # to be removed
    WEARABLE = "Wearable"
    SMARTPHONE = "Smartphone"
    TESTINGDEVICE = "COVID Testing Device"
    WASTEWATER = "Wastewater Sampling"
    OTHER = "Other"
    MISSING = "MISSING OR INVALID"

    def __init__(self, label):
        self.label = label

class NihInstitute(Enum):
    NCATS = "NCATS"
    NCCIH = "NCCIH"
    NCI   = "NCI"
    NDA   = "NDA"
    NEI   = "NEI"
    NHGRI = "NHGRI"
    NHLBI = "NHLBI"
    NIA   = "NIA"
    NIAAA = "NIAAA"
    NIAID = "NIAID"
    NIAMS = "NIAMS"
    NIBIB = "NIBIB"
    NICHD = "NICHD"
    NIDA  = "NIDA"
    NIDCD = "NIDCD"
    NIDCR = "NIDCR"
    NIDDK = "NIDDK"
    NIEHS = "NIEHS"
    NIGMS = "NIGMS"
    NIHOD = "NIH OD"
    NIMH  = "NIMH"
    NIMHD = "NIMHD"
    NINDS = "NINDS"
    NINR  = "NINR"
    NLM   = "NLM"
    NIH   = "NIH" # added this because phs003366 only has this as an entry
    MISSING = "MISSING OR INVALID"

    def __init__(self, label):
        self.label = label

class StudyDomain(Enum):
    LONGCOVID = "Long COVID"
    MISC = "Multisystem Inflammatory Syndrome in Children (MIS-C)"
    MIS = "Multisystem Inflammatory Syndrome (MIS)"
    WASTEWATER = "Wastewater Surveillance"
    AGING = "Aging"
    CANCER = "Cancer" 
    CHILDREN = "Children" # study population focus
    CLINICALTRIALS = "Clinical Trials" # remove
    IMMUNERESPONSES = "Immune Responses"
    MENTALHEALTH = "Mental Health"
    MINORITIES = "Minorities" # study population focus
    AFRICANAMERICANPOPULATION = "African American Population" # study population focus
    TRIBALPOPULATION = "Tribal Population" # study population focus
    HISPANICPOPULATION = "Hispanic and Latino Population" # study population focus
    NUTRITION = "Nutrition"
    PREGNANCY = "Pregnancy" # study population focus
    SUBSTANCEUSE = "Substance Use"
    VIROLOGICALTESTING = "Virological Testing"
    RAPIDTESTING = "Rapid Diagnostic Testing"
    PCRTESTING = "Laboratory (PCR) Testing"
    ANTIBODYTESTING = "Serological (Antibody) Testing"
    MOBILETESTING = "Mobile Unit Testing"
    ATHOMETESTING = "At-Home Testing"
    TREATMENTS = "Treatments" # remove
    VACCINATIONRATE = "Vaccination Rate/Uptake"
    VARIANTS = "Variants"
    SOCIALDETERMINANTS = "Social Determinants of Health"
    DIABETES = "Diabetes"
    OBESITY = "Obesity"
    COMMUNITYOUTREACH = "Community Outreach Programs"
    MEDICALDEVICEDEVELOPMENT = "Medical Device Development"
    BIOSENSORTECHNOLOGY = "Biosensor Technology"
    AIML = "Artifical Intelligence and Machine Learning"
    NGS = "Next Generation Sequencing (NGS)"
    DIGITALHEALTH = "Digital Health Applications"
    INFLUENZA = "Influenza"
    MISSING = "MISSING OR INVALID"

    def __init__(self, label):
        self.label = label

class PopulationRange(Enum):
    SMALLEST = ("<250", 0, 249)
    SMALLER = ("250-500", 250, 499) # 250-499
    SMALL = ("500-1,000", 500, 999) # 500-999
    LARGE = ("1,000-2,000", 1000, 1999) # 1000-1999
    LARGER = ("2,000-5,000", 2000, 4999)
    LARGEST = (">5,000", 5000, float("inf"))
    MISSING = ("MISSING OR INVALID", float("inf"), float("-inf"))

    def __init__(self, label, lower_bound, upper_bound):
        self.label = label
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
